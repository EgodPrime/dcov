import ctypes
import sys
from os.path import abspath, join, dirname

dcov_info = ctypes.CDLL('libdcov_info.so')
sci = None
file_matcher = None


def get_dlf_src_path(package_name=None):
    import site
    import os
    
    python_env_dir = site.getsitepackages()[-1]
    if package_name is None:
        print("package name is not specified, use the site-package dir")
        return python_env_dir
    package_dir = os.path.join(python_env_dir, package_name)
    if not os.path.exists(package_dir):
        raise FileNotFoundError(f"{package_dir} is not a correct path")

    print(f"Package being instrumented is {package_dir}")
    return package_dir


def insert_slipcover(**kwargs):
    from dcov.slipcover import Slipcover
    from dcov.importer import FileMatcher, SlipcoverMetaPathFinder
    global file_matcher
    global sci
    file_matcher = FileMatcher()
    lib_pkg_source = get_dlf_src_path(**kwargs)
    file_matcher.addSource(lib_pkg_source)
    sci = Slipcover(
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


def init_bitmap_python(**kwargs):
    insert_slipcover(**kwargs)
    dcov_info.init_bitmap_python()


init_bitmap_c = dcov_info.init_bitmap_c


def init_bitmap(**kwargs):
    insert_slipcover(**kwargs)
    dcov_info.init_bitmap()


open_bitmap = dcov_info.open_bitmap
clear_bitmap_python = dcov_info.clear_bitmap_python
clear_bitmap_c = dcov_info.clear_bitmap_c
clear_bitmap = dcov_info.clear_bitmap
randomize_bitmap_python = dcov_info.randomize_bitmap_python
randomize_bitmap_c = dcov_info.randomize_bitmap_c
randomize_bitmap = dcov_info.randomize_bitmap
close_bitmap_python = dcov_info.close_bitmap_python
close_bitmap_c = dcov_info.close_bitmap_c
close_bitmap = dcov_info.close_bitmap
get_bb_cnt_python = dcov_info.get_bb_cnt_python
get_bb_cnt_c = dcov_info.get_bb_cnt_c


def get_bb_cnts():
    return get_bb_cnt_python(), get_bb_cnt_c()
