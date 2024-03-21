## Installation(Ubuntu 20.04)

I strongly recommend you to do this in an independent docker container!
And for convenience, I've defaulted to doing the following installation steps in a Docker container.

### Step I. Install GCC 9.4.0 from source

#### 1) download gcc source code
```bash
apt install wget -y

cd /root

wget -c https://github.com/gcc-mirror/gcc/archive/refs/tags/releases/gcc-9.4.0.tar.gz

# try this if you are in China
# https://mirrors.tuna.tsinghua.edu.cn/gnu/gcc/gcc-9.4.0/gcc-9.4.0.tar.gz

tar -zxf gcc-9.4.0.tar.gz
```

#### 2) let gcc download prerequets itself
```bash
cd /root/gcc-9.4.0
./contrib/download_prerequisites
```

#### 3) comiple
```bash
cd /root
# outside gcc source dir
mkdir gcc_build & cd gcc_build
../gcc-9.4.0/configure --prefix=/root/gcc_install --enable-languages=c,c++ --disable-multilib
make
make install
```

#### 4) delete the default gcc if you alread installed another one
```bash
rm /usr/bin/gcc
rm /usr/local/bin/gcc
```

#### 5) link your own gcc
```bash
cd /usr/bin
ln -s /root/gcc_install/bin/gcc gcc
```

#### 6) check if everything is right

```bash
root@59be348e802d:~# gcc -v
Using built-in specs.
COLLECT_GCC=gcc
COLLECT_LTO_WRAPPER=/root/gcc_install/bin/../libexec/gcc/x86_64-pc-linux-gnu/9.4.0/lto-wrapper
Target: x86_64-pc-linux-gnu
Configured with: ../gcc-9.4.0/configure --prefix=/root/gcc_install --enable-languages=c,c++ --disable-multilib
Thread model: posix
gcc version 9.4.0 (GCC)
```
If everything works correctly, you should see the similar information.

### Step II. Compile dcov from source

Dcov contains 3 main shared libraries:

libdcov_ins.so: a gcc plugin that inserts basic block hooks into target (For C/C++).


libdcov_trace.so: contains implementations for the hooks inserted by libdcov_ins.so and slipcover.py.


libdcov_info.so: used to get the statistics of basic blocks, which is further integrated into python APIs.

#### 1) install a python 3.9 environment

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

#### 2) download dcov and compile
```bash
git clone https://

cd dcov

make

make install
```

*If you have different python environment, you should edit the Makefile to make some adjustment.*