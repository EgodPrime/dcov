import sys
import time
sys.path.append('../../..')
from dcov import dcov

repeat = 100

if __name__ == '__main__':
    f = open('results.txt', 'a+')
    
    dcov.init_bitmap()
    dcov.randomize_bitmap()
    
    bitmap_size = dcov.dcov_info.get_bitmap_size()>>3
    if bitmap_size > 1<<20:
        bitmap_size = bitmap_size>>20
        unit = 'MB'
    elif bitmap_size > 1<<10:
        bitmap_size = bitmap_size>>10
        unit = 'KB'
    else:
        unit = 'Byte'
    
    dt = 0
    for i in range(repeat):
        # dcov.randomize_bitmap_python()
        t0 = time.time_ns()
        dcov.get_bb_cnt_python()
        dt += time.time_ns() - t0
    dt= dt/1e6/repeat
    print(f"running get_bb_cnt_python for {repeat} times with {bitmap_size} {unit} bitmap costs on average {dt} ms.")
    f.write(f",{dt}")
    
    dt = 0
    for i in range(repeat):
        # dcov.randomize_bitmap_c()
        t0 = time.time_ns()
        dcov.get_bb_cnt_c()
        dt += time.time_ns() - t0
    dt= dt/1e6/repeat
    print(f"running get_bb_cnt_c for {repeat} times with {bitmap_size} {unit} bitmap costs on average {dt} ms.")
    f.write(f",{dt}")
    
    dt = 0
    for i in range(repeat):
        # dcov.randomize_bitmap_c()
        t0 = time.time_ns()
        dcov.get_bb_cnts()
        dt += time.time_ns() - t0
    dt= dt/1e6/repeat
    print(f"running get_bb_cnts for {repeat} times with {bitmap_size} {unit} bitmap costs on average {dt} ms.")
    f.write(f",{dt}\n")
    