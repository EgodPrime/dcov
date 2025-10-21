
# Coverage for Python+C+Java Programs

This repository is the implementation of our paper "Lightweight Code Coverage Analysis for Deep Learning Library Fuzzing" which is accepted by [IEEE DSC 2025's workshop (VAAL)](https://dsc.pcl.ac.cn/2025/AcceptedPapers.html). 

This is the pure Python version.

## Requirements

- rust: https://rust-lang.org/tools/install/

## Installation

```bash
# Python
pip install . 
```

## Python Usage

```python
import dcov
dcov.open_dcov_py()

with dcov.LoaderWrapper() as loader:
    loader.add_source("some source dir")
    import ... # the target library
    while True: # suppose there is a fuzzing loop
        py_cov_0 = dcov.count_bits_py()
        # do some fuzzing jobs
        py_cov_increase = dcov.count_bits_py() - py_cov_0
        if py_cov_increase > 0:
            # do some feedback job
    dcov.clear_bitmap_py()        

dcov.close_bitmap_py()
```