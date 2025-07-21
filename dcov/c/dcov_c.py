import sys

from qiling import Qiling
from qiling.const import QL_INTERCEPT, QL_VERBOSE

import dcov

BITMAP_SIZE = dcov.get_bitmap_size()


def hook_block(ql, address, size):
    # print(">>> Tracing basic block at 0x%x, block size = 0x%x" % (address, size))
    p1 = address & 0xFFFF00000000
    p2 = address & 0x0000FFFF0000
    p3 = address & 0x00000000FFFF
    idx = (p1 * 17 ^ p2 * 20 ^ p3 * 23) % BITMAP_SIZE
    dcov.on_hit_py(idx)


def run_c(cmd: list[str]):
    bin = Qiling(cmd, r"/", verbose=QL_VERBOSE.OFF)

    def null_rseq_impl(ql: Qiling, abi: int, length: int, flags: int, sig: int):
        return 0

    bin.os.set_syscall("rseq", null_rseq_impl, QL_INTERCEPT.CALL)
    bin.os.set_syscall("lgetxattr", null_rseq_impl, QL_INTERCEPT.CALL)
    bin.os.set_syscall("getxattr", null_rseq_impl, QL_INTERCEPT.CALL)

    bin.hook_block(hook_block)
    bin.run()


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("Usage: dcov_c cmd [cmd ...]")
        sys.exit(1)
    run_c(args)
