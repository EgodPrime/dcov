import time
import ctypes
import signal
import sys

_LIB = ctypes.CDLL('libundercov_info.so')
init_bitmap = _LIB.init_bitmap
close_bitmap = _LIB.close_bitmap
get_bb_cnt = _LIB.get_bb_cnt
save_bitmap = _LIB.save_bitmap


class CoverageC:

    @staticmethod
    def init():
        init_bitmap()

    @staticmethod
    def close():
        close_bitmap()

    @staticmethod
    def get():
        return get_bb_cnt()

    @staticmethod
    def save_bitmap():
        return save_bitmap()