> To better demonstrate the generalisability of DCOV, we have the experiments bellow.

## 1. libtiff
link: https://github.com/libsdl-org/libtiff

### build and instrumentation

```
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
# Clone live555 repository
git clone https://github.com/rgaufman/live555.git
# Move to the folder
cd live555
# Checkout the buggy version of Live555
git checkout ceeb4f4
# Apply a patch. See the detailed explanation for the patch below
patch -p1 < $DCOV_DIR/extra/live555.patch
# Generate Makefile
./genMakefiles linux
# Compile the source
make
```

### test cases generation

We generate test cases for live555 by AFLNet's turtorial: https://github.com/aflnet/aflnet/tree/master

We run AFLNet for 4 hours and obtain 843 test cases

### test case replay [log](./run_live555.log)

### coverage curve

<img src="https://anonymous.4open.science/r/dcov-4710/extra/coverage_live555.png" alt="Curve">

## 3. numpy
link: 

### build and instrumentation

### test cases generation

### test case replay [log](./run_numpy.log)

### coverage curve