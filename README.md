
# Coverage for Python+C+Java Programs


## Requirements

You need `make`, `clang` to build the C code in dcov, and `miniconda` to create a virtual python environment.

Here below is the steps to install the requirements:

```bash
# suppose you are the root user in docker container
apt-get install build-essential
apt-get install clang # must be newer than 14
```

## Installation

```bash
# Python
CXX=clang++ pip install . 
# C/C++
make install -C dcov/c
# Java
make -C dcov/java
make install -C dcov/java
```
## Uninstallation

```bash
make uninstall -C dcov/c
make uninstall -C dcov/java
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

# Java覆盖率临时使用例子

> 需要安装jdk和maven

```bash
# 设置java agent路径变量
export JAVA_AGENT_PATH="/root/.m2/repository/com/kb310/dcov/1.0-SNAPSHOT/dcov-1.0-SNAPSHOT-jar-with-dependencies.jar"
# 生成java测试用put
cd tests/java
mvn package
# 以docker容器环境为例的执行路径如下（dcov位于/root/下）
DCOV_JAVA_PREFIX=com/kb310/exampleput \
java -javaagent:$JAVA_AGENT_PATH  -jar /root/dcov/tests/java/target/exampleput-1.0-SNAPSHOT.jar

# 通用用法
DCOV_JAVA_PREFIX=<被测程序包名> \
java -javaagent:<DcovAgent jar包路径> <options>
```

# C静态插桩
```bash
# 将CC和CXX分别设置为dcov-clang和dcov-clang++
# 例子1：
./configure && make
CC=dcov-clang CXX=dcov-clang++ ./configure && make
# 例子2：
cmake .. && make
CC=dcov-clang CXX=dcov-clang++ cmake .. && make
```