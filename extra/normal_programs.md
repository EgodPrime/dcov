## libtiff
link: https://github.com/libsdl-org/libtiff

### build and instrumentation

### test cases generation

### coverage curve

## live555
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