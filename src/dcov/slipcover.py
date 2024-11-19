from __future__ import annotations

import dis
import sys
import threading
import types
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Set
from dcov import bytecode as bc
from dcov import probe

VERSION = "0.3.2"

# FIXME provide __all__

# Counter.total() is new in 3.10
if sys.version_info[0:2] < (3, 10):

    def counter_total(self: Counter) -> int:
        return sum([self[n] for n in self])

    setattr(Counter, "total", counter_total)


class PathSimplifier:
    def __init__(self):
        self.cwd = Path.cwd()

    def simplify(self, path: str) -> str:
        f = Path(path)
        try:
            return str(f.relative_to(self.cwd))
        except ValueError:
            return path


class Slipcover:
    def __init__(
        self,
        collect_stats: bool = False,
        immediate: bool = False,
        d_miss_threshold: int = 50,
        branch: bool = False,
        skip_covered: bool = False,
        disassemble: bool = False,
    ):
        self.collect_stats = collect_stats
        self.immediate = immediate
        self.d_miss_threshold = d_miss_threshold
        self.branch = branch
        self.skip_covered = skip_covered
        self.disassemble = disassemble

        # mutex protecting this state
        self.lock = threading.RLock()

        # maps to guide CodeType replacements
        self.replace_map: Dict[types.CodeType, types.CodeType] = dict()
        self.instrumented: Dict[str, set] = defaultdict(set)

        # notes which code lines have been instrumented
        self.code_lines: Dict[str, set] = defaultdict(set)
        self.code_branches: Dict[str, set] = defaultdict(set)

        # provides an index (line_or_branch -> offset) for each code object
        self.code2index: Dict[types.CodeType, list] = dict()

        # notes which lines and branches have been seen.
        self.all_seen: Dict[str, set] = defaultdict(set)

        # notes lines/branches seen since last de-instrumentation
        self._get_newly_seen()

        self.modules = []
        self.all_probes = []

    def _get_newly_seen(self):
        """Returns the current set of ``new'' lines, leaving a new container in place."""

        # We trust that assigning to self.newly_seen is atomic, as it is triggered
        # by a STORE_NAME or similar opcode and Python synchronizes those.  We rely on
        # C extensions' atomicity for updates within self.newly_seen.  The lock here
        # is just to protect callers of this method (so that the exchange is atomic).

        with self.lock:
            newly_seen = self.newly_seen if hasattr(self, "newly_seen") else None
            self.newly_seen: Dict[str, set] = defaultdict(set)

        return newly_seen

    def instrument(
        self, co: types.CodeType, parent: types.CodeType = 0
    ) -> types.CodeType:
        """Instruments a code object for coverage detection.

        If invoked on a function, instruments its code.
        """
        if isinstance(co, types.FunctionType):
            co.__code__ = self.instrument(co.__code__)
            return co.__code__

        assert isinstance(co, types.CodeType)
        # print(f"instrumenting {co.co_name}")

        ed = bc.Editor(co)

        # handle functions-within-functions
        for i, c in enumerate(co.co_consts):
            if isinstance(c, types.CodeType):
                ed.set_const(i, self.instrument(c, co))

        # 这里是把C里的signal函数加入Python常量列表，这样就可以调用函数了
        ed.add_const(probe.no_signal)  # used during de-instrumentation
        probe_signal_index = ed.add_const(probe.signal)

        """from opcode.py
        jrel_op('JUMP_FORWARD', 110)    # Number of bytes to skip
        jabs_op('JUMP_IF_FALSE_OR_POP', 111) # Target byte offset from beginning of code
        jabs_op('JUMP_IF_TRUE_OR_POP', 112)  # ""
        jabs_op('JUMP_ABSOLUTE', 113)        # ""
        jabs_op('POP_JUMP_IF_FALSE', 114)    # ""
        jabs_op('POP_JUMP_IF_TRUE', 115)     # ""
        """
        block_offsets = []
        bytecode = co.co_code
        offset = 0
        while offset < len(bytecode):
            b = bytecode[offset]
            if b < 110 or b > 115:
                offset += 2
                continue
            if b == 110:
                block_offsets.append(
                    offset + bytecode[offset + 1] + 2
                )  # +2是因为从下一对字节码开始跳
            elif b == 111 or b == 112:
                pass  # 没遇到过，暂不处理
            elif b == 113:
                block_offsets.append(bytecode[offset + 1])
            elif b == 114 or b == 115:  # 参数指向远分支，下一对字节码是近分支
                block_offsets.append(offset + 2)
                block_offsets.append(bytecode[offset + 1])

            offset += 2

        off_list = list(dis.findlinestarts(co))

        for off_item in off_list:
            offset, lineno = off_item
            if offset not in block_offsets:
                off_list.remove(off_item)

        branch_set = set()
        insert_labels = []
        probes = []

        delta = 0
        for off_item in off_list:
            if len(off_item) == 2:  # from findlinestarts
                offset, lineno = off_item
                if lineno == 0:
                    continue  # Python 3.11.0b4 generates a 0th line

                # Can't insert between an EXTENDED_ARG and the final opcode
                if offset >= 2 and co.co_code[offset - 2] == bc.op_EXTENDED_ARG:
                    while (
                        offset < len(co.co_code)
                        and co.co_code[offset - 2] == bc.op_EXTENDED_ARG
                    ):
                        offset += 2  # TODO will we overtake the next offset from findlinestarts?

                insert_labels.append(lineno)

                tr = probe.new(self, co.co_filename, lineno, self.d_miss_threshold)
                probes.append(tr)
                tr_index = ed.add_const(tr)

                delta += ed.insert_function_call(
                    offset + delta, probe_signal_index, (tr_index,)
                )

            else:  # from find_const_assignments
                begin_off, end_off, branch_index = off_item
                branch = co.co_consts[branch_index]

                branch_set.add(branch)
                insert_labels.append(branch)

                tr = probe.new(self, co.co_filename, branch, self.d_miss_threshold)
                probes.append(tr)
                ed.set_const(branch_index, tr)

                delta += ed.insert_function_call(
                    begin_off + delta,
                    probe_signal_index,
                    (branch_index,),
                    repl_length=end_off - begin_off,
                )

        ed.add_const("__slipcover__")  # mark instrumented
        new_code = ed.finish()

        if self.disassemble:
            dis.dis(new_code)

        if self.collect_stats:
            self.all_probes.extend(probes)

        if self.immediate:
            for tr, off in zip(probes, ed.get_inserts()):
                probe.set_immediate(tr, new_code.co_code, off)
        else:
            index = list(zip(ed.get_inserts(), insert_labels))

        with self.lock:
            # Python 3.11.0b4 generates a 0th line
            self.code_lines[co.co_filename].update(
                line[1] for line in dis.findlinestarts(co) if line[1] != 0
            )
            self.code_branches[co.co_filename].update(branch_set)

            if not parent:
                self.instrumented[co.co_filename].add(new_code)

            if not self.immediate:
                self.code2index[new_code] = index

        return new_code

    def deinstrument(self, co, lines: set) -> types.CodeType:
        """De-instruments a code object previously instrumented for coverage detection.

        If invoked on a function, de-instruments its code.
        """

        assert not self.immediate

        if isinstance(co, types.FunctionType):
            co.__code__ = self.deinstrument(co.__code__, lines)
            return co.__code__

        assert isinstance(co, types.CodeType)
        # print(f"de-instrumenting {co.co_name}")

        ed = bc.Editor(co)

        co_consts = co.co_consts
        for i, c in enumerate(co_consts):
            if isinstance(c, types.CodeType):
                nc = self.deinstrument(c, lines)
                if nc is not c:
                    ed.set_const(i, nc)

        index = self.code2index[co]

        for offset, lineno in index:
            func = ed.get_inserted_function(offset)
            if lineno in lines and func:
                func_index, func_arg_index, *_ = func
                if co_consts[func_index] == probe.signal:
                    probe.mark_removed(co_consts[func_arg_index])

                    if self.collect_stats:
                        # If collecting stats, rather than disabling the probe, we switch to
                        # calling the 'probe.no_signal' function on it (which we conveniently added
                        # to the consts before probe.signal, during instrumentation), so that
                        # we have the total execution count needed for the reports.
                        ed.replace_inserted_function(offset, func_index - 1)
                    else:
                        ed.disable_inserted_function(offset)

        new_code = ed.finish()
        if new_code is co:
            return co

        # no offsets changed, so the old code's index is still usable
        self.code2index[new_code] = index

        with self.lock:
            self.replace_map[co] = new_code

            if co in self.instrumented[co.co_filename]:
                self.instrumented[co.co_filename].remove(co)
                self.instrumented[co.co_filename].add(new_code)

        return new_code

    def get_coverage(self):
        """Returns coverage information collected."""

        with self.lock:
            # FIXME calling _get_newly_seen will prevent de-instrumentation if still running!
            newly_seen = self._get_newly_seen()

            for file, lines in newly_seen.items():
                self.all_seen[file].update(lines)

            simp = PathSimplifier()

            if self.collect_stats:
                d_misses = defaultdict(Counter)
                u_misses = defaultdict(Counter)
                totals = defaultdict(Counter)
                for p in self.all_probes:
                    (
                        filename,
                        lineno,
                        d_miss_count,
                        u_miss_count,
                        total_count,
                    ) = probe.get_stats(p)
                    if d_miss_count:
                        d_misses[filename].update({lineno: d_miss_count})
                    if u_miss_count:
                        u_misses[filename].update({lineno: u_miss_count})
                    totals[filename].update({lineno: total_count})

            files = dict()
            for f, f_code_lines in self.code_lines.items():
                if f in self.all_seen:
                    branches_seen = {
                        x for x in self.all_seen[f] if isinstance(x, tuple)
                    }
                    lines_seen = self.all_seen[f] - branches_seen
                else:
                    lines_seen = branches_seen = set()

                f_files = {
                    "executed_lines": sorted(lines_seen),
                    "missing_lines": sorted(f_code_lines - lines_seen),
                }

                summary = f_files["summary"] = {
                    "covered_lines": len(f_files["executed_lines"]),
                    "missing_lines": len(f_files["missing_lines"]),
                }

                nom = summary["covered_lines"]
                den = nom + summary["missing_lines"]

                if self.branch:
                    f_files["executed_branches"] = sorted(branches_seen)
                    f_files["missing_branches"] = sorted(
                        self.code_branches[f] - branches_seen
                    )
                    summary["covered_branches"] = len(f_files["executed_branches"])
                    summary["missing_branches"] = len(f_files["missing_branches"])

                    nom += summary["covered_branches"]
                    den += summary["covered_branches"] + summary["missing_branches"]

                # the check for den == 0 is just defensive programming... there's always at least 1 line
                summary["percent_covered"] = 100.0 if den == 0 else 100 * nom / den

                if self.collect_stats:
                    # Once a line reports in, it's available for deinstrumentation.
                    # Each time it reports in after that, we consider it a miss (like a cache miss).
                    # We differentiate between (de-instrument) "D misses", where a line
                    # reports in after it _could_ have been de-instrumented and (use) "U misses"
                    # and where a line reports in after it _has_ been de-instrumented, but
                    # didn't use the code object where it's deinstrumented.
                    f_files["stats"] = {
                        "d_misses_pct": round(
                            d_misses[f].total() / totals[f].total() * 100, 1
                        ),
                        "u_misses_pct": round(
                            u_misses[f].total() / totals[f].total() * 100, 1
                        ),
                        "top_d_misses": [
                            f"{it[0]}:{it[1]}" for it in d_misses[f].most_common(5)
                        ],
                        "top_u_misses": [
                            f"{it[0]}:{it[1]}" for it in u_misses[f].most_common(5)
                        ],
                        "top_lines": [
                            f"{it[0]}:{it[1]}" for it in totals[f].most_common(5)
                        ],
                    }

                files[simp.simplify(f)] = f_files

            summary = {
                "covered_lines": sum(
                    files[fn]["summary"]["covered_lines"] for fn in files
                ),
                "missing_lines": sum(
                    files[fn]["summary"]["missing_lines"] for fn in files
                ),
            }

            nom = summary["covered_lines"]
            den = nom + summary["missing_lines"]

            if self.branch:
                summary["covered_branches"] = sum(
                    files[fn]["summary"]["covered_branches"] for fn in files
                )
                summary["missing_branches"] = sum(
                    files[fn]["summary"]["missing_branches"] for fn in files
                )

                nom += summary["covered_branches"]
                den += summary["covered_branches"] + summary["missing_branches"]

            summary["percent_covered"] = 100.0 if den == 0 else 100 * nom / den

            import datetime

            return {
                "meta": {
                    "software": "slipcover",
                    "version": VERSION,
                    "timestamp": datetime.datetime.now().isoformat(),
                    "branch_coverage": self.branch,
                },
                "files": files,
                "summary": summary,
            }

    @staticmethod
    def find_functions(items, visited: set):
        import inspect

        def is_patchable_function(func):
            # PyPy has no "builtin functions" like CPython. instead, it uses
            # regular functions, with a special type of code object.
            # the second condition is always True on CPython
            return inspect.isfunction(func) and type(func.__code__) is types.CodeType

        def find_funcs(root):
            if is_patchable_function(root):
                if root not in visited:
                    visited.add(root)
                    yield root

            # Prefer isinstance(x,type) over isclass(x) because many many
            # things, such as str(), are classes
            elif isinstance(root, type):
                if root not in visited:
                    visited.add(root)

                    # Don't use inspect.getmembers(root) since that invokes getattr(),
                    # which causes any descriptors to be invoked, which results in either
                    # additional (unintended) coverage and/or errors because __get__ is
                    # invoked in an unexpected way.
                    obj_names = dir(root)
                    for obj_key in obj_names:
                        mro = (root,) + root.__mro__
                        for base in mro:
                            if (
                                base == root or base not in visited
                            ) and obj_key in base.__dict__:
                                yield from find_funcs(base.__dict__[obj_key])
                                break

            elif (
                isinstance(root, classmethod) or isinstance(root, staticmethod)
            ) and is_patchable_function(root.__func__):
                if root.__func__ not in visited:
                    visited.add(root.__func__)
                    yield root.__func__

        # FIXME this may yield "dictionary changed size during iteration"
        return [f for it in items for f in find_funcs(it)]

    def register_module(self, m):
        self.modules.append(m)

    def deinstrument_seen(self) -> None:
        with self.lock:
            newly_seen = self._get_newly_seen()

            for file, new_set in newly_seen.items():
                for co in self.instrumented[file]:
                    self.deinstrument(co, new_set)

                self.all_seen[file].update(new_set)

            # Replace references to code
            if self.replace_map:
                visited = set()

                # XXX the set of function objects could be pre-computed at register_module;
                # also, the same could be done for functions objects in globals()
                for m in self.modules:
                    for f in Slipcover.find_functions(m.__dict__.values(), visited):
                        if f.__code__ in self.replace_map:
                            f.__code__ = self.replace_map[f.__code__]

                globals_seen = []
                for frame in sys._current_frames().values():
                    while frame:
                        if not frame.f_globals in globals_seen:
                            globals_seen.append(frame.f_globals)
                            for f in Slipcover.find_functions(
                                frame.f_globals.values(), visited
                            ):
                                if f.__code__ in self.replace_map:
                                    f.__code__ = self.replace_map[f.__code__]

                        for f in Slipcover.find_functions(
                            frame.f_locals.values(), visited
                        ):
                            if f.__code__ in self.replace_map:
                                f.__code__ = self.replace_map[f.__code__]

                        frame = frame.f_back

                # all references should have been replaced now... right?
                self.replace_map.clear()
