# DCOV: Lightweight Code Coverage Analyzer For Deep Learning Framwork Fuzzing

Dcov contains 3 main shared libraries and 1 executable program:

libdcov_ins.so: a gcc plugin that inserts basic block-level probes into PUT (For C/C++).

libdcov_trace.so: contains implementations of coverage collecting for the probes inserted by libdcov_ins.so and slipcover.py.

libdcov_info.so: used to get the statistics of basic blocks, which is further integrated into python APIs.

dcov_ins_server: offers atomic and increasing basic block id to libdcov_ins.so

## Installation(Ubuntu 20.04)

I strongly recommend you to do this in an independent docker container!
And for convenience, I've defaulted to doing the following installation steps in a Docker container.

### Step I. Build GCC 9.4.0 from source

```bash
bash download_gcc.sh
bash build_gcc.sh
# add sudo if you are not the root user or not in docker container
bash bind_gcc.sh
```

### Step II. Install miniconda

You can use any python environment because all we need is just the header files.
In this place I would like to use miniconda.

```bash
cd /root
wget -c https://repo.anaconda.com/miniconda/Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
bash Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
# inputs follwing key
# enter
# q
# yes
# enter
# yes
rm Miniconda3-py39_23.1.0-1-Linux-x86_64.sh
```

After the installation of miniconda finished, you need to restart the terminal before you continue.
```
conda create -n py39 python=3.9
```

### Step III. Compile dcov from source & Installation
```bash
apt install libgmp-dev
cd dcov
make
# add sudo if you are not the root user or not in docker container
make install
```

*If you have different python environment, you should edit the Makefile to make some adjustment.*

## How To Build Deep Learning Frameworks With DCOV
See [here](frameworks/README.MD).

## How To Replay All The Evaluations In Our Paper
See [here](experiment/REAMDE.MD).