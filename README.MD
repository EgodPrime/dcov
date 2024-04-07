# DCOV: Lightweight Code Coverage Analyzer For Deep Learning Framework Testing

Dcov contains 3 main shared libraries and 1 executable program:

libdcov_ins.so: a gcc plugin that inserts basic block-level probes into PUT (For C/C++).

libdcov_trace.so: contains implementations of coverage collecting for the probes inserted by libdcov_ins.so and slipcover.py.

libdcov_info.so: used to get the statistics of basic blocks, which is further integrated into python APIs.

dcov_ins_server: offers atomic and increasing basic block id to libdcov_ins.so

## Installation(Based on docker)

### Step I. Build docker image and create a container

```bash
docker build -t dcov:latest -f Dockerfile .
docker run -itd --name dcov -v ${PWD}:/root dcov:latest
docker exec -it dcov bash
```

### Step II. Build GCC 9.4.0 from source

We use gcc 9.4.0 to compile dcov and DL frameworks

```bash
# download and extract
wget -c https://mirrors.tuna.tsinghua.edu.cn/gnu/gcc/gcc-9.4.0/gcc-9.4.0.tar.gz
tar -zxf gcc-9.4.0.tar.gz
# build and install
bash build_gcc.sh
```

### Step III. Compile dcov from source & Installation

```bash
conda create -n py39 python=3.9
conda actiavte py39
pushd dcov
make
# add sudo if you are not the root user or not in docker container
make install
popd
```

## Compatibility
We tested the following deep learning frameworks on their releases of the last two years (2022/4-2024/4). 

|DLF|Version|Builder|Compatible|
|---|---|---|---|
|TensorFlow|v2.8.0-v2.9.0|bazel|X|
|TensorFlow|v2.10.0|bazel|√|
|TensorFlow|v2.11.0|bazel|√|
|TensorFlow|v2.12.0-v2.16.0|bazel|X|
|PyTorch|v2.0.0|cmake+make|X|
|PyTorch|v2.1.0|cmake+make|√|
|PyTorch|v2.2.0|cmake+make|√|
|PaddlePaddle|v2.1.0|cmake+make|√|
|PaddlePaddle|v2.2.0|cmake+make|X|
|PaddlePaddle|v2.3.0|cmake+make|X|
|PaddlePaddle|v2.4.0|cmake+ninja|√|
|PaddlePaddle|v2.5.0|cmake+ninja|√|
|PaddlePaddle|v2.6.0|cmake+ninja|√|

## How To Build Deep Learning Frameworks With DCOV
See [here](frameworks/README.MD).

## How To Replay All The Evaluations In Our Paper
See [here](experiment/REAMDE.MD).