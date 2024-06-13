> To better demonstrate the generalisability of DCOV, we have the experiments bellow.

## 1. libtiff
link: https://github.com/libsdl-org/libtiff

### build and instrumentation

```bash
DCOV_DIR=<path to dcov>
git clone https://github.com/libsdl-org/libtiff
cd libtiff
CC=gcc CXX=g++ CFLAGS="-fplugin=libdcov_ins.so -lrt -ldcov_trace" CXXFLAGS="-fplugin=libdcov_ins.so -lrt -ldcov_trace" LDFLAGS="-lrt -ldcov_trace" ./configure
make
```

### test cases generation

We generate test cases for libtiff by AFL's demo test sets:https://lcamtuf.coredump.cx/afl/demo/

We run AFL for 5 hours and obtain 7171 test cases

### test case replay [log](./run_libtiff.log)

### coverage curve

<img src="https://anonymous.4open.science/r/dcov-4710/extra/coverage_libtiff.png" alt="Curve">

## 2. live555
link: https://github.com/rgaufman/live555.git

### build and instrumentation

```bash
DCOV_DIR=<path to dcov>
git clone https://github.com/rgaufman/live555.git
cd live555
# Checkout the buggy version of Live555(This step is made by AFLNet, we just follow it)
git checkout ceeb4f4
patch -p1 < $DCOV_DIR/extra/live555.patch
./genMakefiles linux
make
```

### test cases generation

We generate test cases for live555 by AFLNet's turtorial: https://github.com/aflnet/aflnet/tree/master

We run AFLNet for 4 hours and obtain 843 test cases

### test case replay [log](./run_live555.log)

### coverage curve

<img src="https://anonymous.4open.science/r/dcov-4710/extra/coverage_live555.png" alt="Curve">

## 3. numpy
link: https://github.com/numpy/numpy

### build and instrumentation

```bash
pip install numpy
```

### test cases generation

Numpy offers official test suites at https://numpy.org/doc/stable/reference/testing.html.

We run its official test suites and collect coverage by dcov with:

```python
import numpy
import dcov
import threading
import time

f = open('run_numpy.log', 'w', buffering=1)
f.write("time_used(ms), py_cov, coverage_time_used(ms)\n")

def loop_py_cov(event):
    t0 = time.time()
    while not event.is_set():
        t1 = time.time_ns()
        py_cov = dcov.get_bb_cnt_python()
        dt = (time.time_ns() - t1)/1000000
        t_now = (time.time() - t0)*1000
        f.write(f"{t_now}, {py_cov}, {dt}\n")
        time.sleep(0.01)

if __name__ == '__main__':
    dcov.init_bitmap_python(dlf_name='numpy', dlf_mode=False)
    stop = threading.Event()
    th = threading.Thread(target=loop_py_cov, args=(stop,))
    th.start()
    numpy.test(label='slow')
    stop.set()
```

### test case replay [log](./run_numpy.log)

### coverage curve

<img src="https://anonymous.4open.science/r/dcov-4710/extra/coverage_numpy.png" alt="Curve">