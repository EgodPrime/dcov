import builtins

from dcov.python.dcov_loader import DcovMetaPathFinder, LoaderWrapper
from dcov.python.dcov_monitor import register_by_cov_type
from dcov.python.dcov_py import (
    clear_bitmap_c,
    clear_bitmap_java,
    clear_bitmap_py,
    clear_bitmap_x,
    close_bitmap_c,
    close_bitmap_java,
    close_bitmap_py,
    close_bitmap_x,
    copy_bitmap,
    count_aflpp_bytes,
    count_bits_c,
    count_bits_java,
    count_bits_py,
    count_bits_x,
    get_bitmap_size,
    merge_bitmap,
    on_hit_py,
    on_hit_py_edge,
    open_bitmap_c,
    open_bitmap_java,
    open_bitmap_py,
    open_bitmap_x,
)

setattr(builtins, "on_hit_py", on_hit_py)
setattr(builtins, "on_hit_py_edge", on_hit_py_edge)

__all__ = [
    "LoaderWrapper",
    "DcovMetaPathFinder",
    "register_by_cov_type",
    "get_bitmap_size",
    "open_bitmap_py",
    "open_bitmap_c",
    "open_bitmap_java",
    "clear_bitmap_py",
    "clear_bitmap_c",
    "clear_bitmap_java",
    "close_bitmap_py",
    "close_bitmap_c",
    "close_bitmap_java",
    "count_bits_py",
    "count_bits_c",
    "count_bits_java",
    "open_bitmap_x",
    "clear_bitmap_x",
    "close_bitmap_x",
    "count_bits_x",
    "copy_bitmap",
    "merge_bitmap",
    "count_aflpp_bytes",
]
