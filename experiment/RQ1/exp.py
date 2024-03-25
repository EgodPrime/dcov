from os.path import join, abspath
import time
import os
import argparse
import sys
sys.path.append('../../..')
from dcov import dcov

data_dir_prefix = abspath('../benchmark')

def conduct_exp(libname:str, predo, report_and_save):
    data_dir = join(data_dir_prefix, libname)
    f = predo(libname)
    exec(f"import {libname}")
    print("Testing......")
    time_start = time.time_ns()
    for idx in range(100):
        file_path = os.path.join(data_dir, f"experiment_{idx}.py")
        
        code = open(file_path, 'r', encoding='utf-8').read()
        exec(code)
        
        print(f"Executing: {file_path}, ", end="")
        try:
            for _ in range(100):
                exec(code)
        except:
            print("something wrong!")
            continue
        
        time_used = (time.time_ns() - time_start)/1000000
        report_and_save(idx, time_used, f)
    f.close()

def predo_base(libname:str):
    f = open(f'{libname}_base.txt', 'w')
    f.write(f"iteration,time_used(ms)\n")
    return f

def predo_dcov(libname:str):
    f = open(f'{libname}_dcov.txt', 'w')
    f.write(f"iteration,time_used(ms),python_coverage,c_coverage\n")
    dcov.init_bitmap()
    return f
    
def report_and_save_base(idx, time_used, f):
    print(f"current is {time_used} ms")
    record = f"{idx+1},{time_used}\n"
    f.write(record)
    
def report_and_save_dcov(idx, time_used, f):
    pc,cc = dcov.get_bb_cnts()
    print(f"current time is {time_used} ms, Python coverage is {pc}, C coverage is {cc}")
    record = f"{idx+1},{time_used},{pc},{cc}\n"
    f.write(record)

def conduct_base(libname:str):
    conduct_exp(libname, predo_base, report_and_save_base)
    
def conduct_dcov(libname: str):
    conduct_exp(libname, predo_dcov, report_and_save_dcov)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--libname', type=str, required=True, choices=['tensorflow','torch','paddle'])
    parser.add_argument('--mode', type=str, required=True, choices=['base', 'dcov'])
    
    args = parser.parse_args()
    libname = args.libname
    mode = args.mode
    
    if mode == 'base':
        conduct_base(libname)
    elif mode == 'dcov':
        conduct_dcov(libname)