import ctypes
import sys
import os

dcov_info = ctypes.CDLL('libdcov_info.so')
sci = None
file_matcher = None

def get_dlf_src_path():
    import site
    import subprocess
    import os

    dlf_prefix = site.getsitepackages()[-1]
    dlf_libs = ["tensorflow", "torch", "paddle", "oneflow"]
    for entry in os.listdir(dlf_prefix):
        for lib in dlf_libs:
            if lib == entry:
                return os.path.join(dlf_prefix, entry)
    return None

def insert_slipcover():
    from slipcover import Slipcover
    from importer import FileMatcher, SlipcoverMetaPathFinder
    # file_matcher用于限定覆盖率的统计对象，比如只收集PyTorch的源码覆盖信息
    file_matcher = FileMatcher()
    lib_pkg_source = get_dlf_src_path()
    file_matcher.addSource(lib_pkg_source)
    sci = Slipcover(
        collect_stats=False,
        immediate=True,
        d_miss_threshold=50,
        branch=False,
        skip_covered=True,
        disassemble=False
    )
    # 在meta_path中添加一个模块加载器，这个加载器在加载模块时会进行字节码插桩
    sys.meta_path.insert(
        0,
        SlipcoverMetaPathFinder(
            sci, file_matcher, False
        ),
    )

def init_bitmap_python():
    insert_slipcover()
    dcov_info.init_bitmap_python()

init_bitmap_c=dcov_info.init_bitmap_c

def init_bitmap():
    insert_slipcover()
    dcov_info.init_bitmap()

close_bitmap_python=dcov_info.close_bitmap_python
close_bitmap_c=dcov_info.close_bitmap_c
close_bitmap=dcov_info.close_bitmap
get_bb_cnt_python=dcov_info.get_bb_cnt_python
get_bb_cnt_c=dcov_info.get_bb_cnt_c

def get_bb_cnts():
    return get_bb_cnt_python(), get_bb_cnt_c()

save_bitmap=dcov_info.save_bitmap