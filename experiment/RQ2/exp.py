from os.path import join, abspath, dirname
import time
import os
import argparse
import sys
cur_dir = dirname(abspath(__file__))
dcov_par = dirname(dirname(dirname(cur_dir)))
sys.path.append(dcov_par)
from dcov import dcov

repeat = 100
data_dir_prefix = join(dirname(cur_dir),'benchmark')

def get_dlf_src_path():
    import site
    import os
    dlf_prefix = site.getsitepackages()[-1]
    dlf_libs = ["tensorflow", "torch", "paddle"]
    for entry in os.listdir(dlf_prefix):
        if entry in dlf_libs:
            res= os.path.join(dlf_prefix, entry)
            print(f"DL framework package source is {res}")
            return res
    return None
        
def predo_base():
    pass

cov = None
def predo_coverage_py():
    import coverage
    global cov
    cov = coverage.Coverage(data_file='coverage.py.coverage',
                            source_pkgs=[libname],
                            include=['*.py'],
                            branch=False,)

sci = None   
def predo_slipcover():
    global sci
    import slipcover as sc
    file_matcher = sc.FileMatcher()
    lib_pkg_source = get_dlf_src_path()
    file_matcher.addSource(lib_pkg_source)
    sci = sc.Slipcover(
        immediate=True,
        d_miss_threshold=50,
        branch=True,
        skip_covered=True,
        disassemble=False,
    )
    from slipcover.importer import SlipcoverMetaPathFinder
    sys.meta_path.insert(
        0,
        SlipcoverMetaPathFinder(
            sci,file_matcher, False
        ),
    )
    
def predo_dcov_python():
    from dcov import dcov
    dcov.init_bitmap_python()
    
def predo_dcov_C():
    from dcov import dcov
    dcov.init_bitmap_c()
    
def predo_dcov():
    from dcov import dcov
    dcov.init_bitmap()
    
def execution_base(code):
    exec(code)
    
def execution_coverage_py(code):
    global cov
    cov.start()
    exec(code)
    cov.stop()

def analysis_base():
    pass

def analysis_coverage_py():
    global cov
    cov.get_data()
    
def analysis_slipcover():
    global sci
    sci.get_coverage()
    
def analysis_dcov_python():
    dcov.get_bb_cnt_python()
    
def analysis_dcov_C():
    dcov.get_bb_cnt_c()

def analysis_dcov():
    dcov.get_bb_cnts()

def conduct_exp(libname:str, mode, predo, execution, analysis):
    predo()
    exec(f"import {libname}")
    data_dir = join(data_dir_prefix, libname)
    time_ET = 0
    time_AT = 0
    for idx in range(100):
        file_path = os.path.join(data_dir, f"experiment_{idx}.py")
        code = open(file_path, 'r', encoding='utf-8').read()
        print(f"Executing: {file_path}...")
        try:
            for _ in range(repeat):
                t0 = time.time_ns()
                execution(code)
                time_ET += time.time_ns() - t0
                t0 = time.time_ns()
                analysis()
                time_AT += time.time_ns() - t0
        except:
            print("something wrong!")
            continue
    time_TT = time_ET + time_AT
    time_ET /= 1000000
    time_AT /= 1000000
    time_TT /= 1000000
    with open("results.txt", 'a+') as f:
        f.write(f"{libname},{mode},{time_ET},{time_AT},{time_TT}\n")

def conduct_base(libname:str, mode):
    conduct_exp(libname, mode, predo_base, execution_base, analysis_base)

def conduct_coverage_py(libname:str, mode):
    conduct_exp(libname, mode, predo_coverage_py, execution_coverage_py, analysis_coverage_py)

def conduct_slipcover(libname:str, mode):
    conduct_exp(libname, mode, predo_slipcover, execution_base, analysis_slipcover)

def conduct_dcov_python(libname:str, mode):
    conduct_exp(libname, mode, predo_dcov_python, execution_base, analysis_dcov_python)
        
def conduct_dcov_c(libname:str, mode):
    conduct_exp(libname, mode, predo_dcov_C, execution_base, analysis_dcov_C)
        
def conduct_dcov(libname:str, mode):
    conduct_exp(libname, mode, predo_dcov, execution_base, analysis_dcov)
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--libname', type=str, required=True, choices=['tensorflow','torch','paddle'])
    parser.add_argument('--mode', type=str, required=True, choices=['base', 'coverage.py', 'slipcover', 'dcov-python', 'dcov-c', 'dcov', 'gcov'])
    args = parser.parse_args()
    libname = args.libname
    mode = args.mode
    
    if libname=='tensorflow':
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        
    if mode == 'base' or mode=='gcov':
        conduct_base(libname, mode)
    elif mode == 'coverage.py':
        conduct_coverage_py(libname, mode)
    elif mode == 'slipcover':
        conduct_slipcover(libname, mode)
    elif mode == 'dcov-python':
        conduct_dcov_python(libname, mode)
    elif mode == 'dcov-c':
        conduct_dcov_c(libname, mode)
    elif mode == 'dcov':
        conduct_dcov(libname, mode)