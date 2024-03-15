from . import dcov
import time

if __name__ == '__main__':
    dcov.init_bitmap()
    
    bitmap_size = dcov.dcov_info.get_bitmap_size()
    
    s = time.time_ns()
    for i in range(100):
        dcov.get_bb_cnt_python()
    e = time.time_ns()
    print(f"running get_bb_cnt_python for 100 times with bitmap size {bitmap_size} costs on average {(e-s)/1e8} ms.")
    
    s = time.time_ns()
    for i in range(100):
        dcov.get_bb_cnt_c()
    e = time.time_ns()
    print(f"running get_bb_cnt_c for 100 times with bitmap size {bitmap_size} costs on average {(e-s)/1e8} ms.")
    