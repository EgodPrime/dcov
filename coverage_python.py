import ctypes
import os
import sys

from . import slipcover as sc

# slipcover的动态库，实现了桩代码的功能。我方的修改为：行覆盖信息直接记录在共享内存中。
probe = ctypes.CDLL(os.path.join(os.path.dirname(__file__), "slipcover", "probe.so"))

def get_dlf_src_path():
    import site
    import subprocess
    import os

    dlf_prefix = site.getsitepackages()[-1]
    command = f'ls {dlf_prefix} | grep -E "(tensorflow|torch|paddle|oneflow)"'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').split('\n')[0].strip()
    path = os.path.join(dlf_prefix, output)
    return path

class CoveragePython:
    sci = None
    file_matcher = None

    @staticmethod
    def init(lib=None):
        CoveragePython.insert_slipcover(lib)
        # 初始化共享内存（不初始化直接运行也可以，这里手动初始化是为了清空数据）
        probe.init_bitmap()

    @staticmethod
    def awake(lib: str):
        CoveragePython.insert_slipcover(lib)

    @staticmethod
    def insert_slipcover():
        # file_matcher用于限定覆盖率的统计对象，比如只收集PyTorch的源码覆盖信息
        CoveragePython.file_matcher = sc.FileMatcher()
        lib_pkg_source = get_dlf_src_path()
        CoveragePython.file_matcher.addSource(lib_pkg_source)
        CoveragePython.sci = sc.Slipcover(
            collect_stats=False,
            immediate=True,
            d_miss_threshold=50,
            branch=False,
            skip_covered=True,
            disassemble=False,
        )
        from .importer import SlipcoverMetaPathFinder

        # 在meta_path中添加一个模块加载器，这个加载器在加载模块时会进行字节码插桩
        sys.meta_path.insert(
            0,
            SlipcoverMetaPathFinder(
                CoveragePython.sci, CoveragePython.file_matcher, False
            ),
        )

    @staticmethod
    # @time_it
    def get():
        # 直接从共享内存获取覆盖信息，跳过slipcover的python代码
        return probe.get_bb_cnt_python()

    @staticmethod
    def close():
        probe.close_bitmap_python()

    @staticmethod
    def save_bitmap():
        probe.save_bitmap()
