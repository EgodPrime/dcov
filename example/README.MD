## Python

```bash
# 原版
python example_numpy.py
# 自动插桩
dcov-python example_numpy.py
```

## Java
```bash
# 原版
java -cp ./gson-2.12.1.jar example_gson.java
# 自动插桩
java -javaagent:/usr/lib/dcov_agent.jar -cp ./gson-2.12.1.jar example_gson.java
```

## C++
```bash
# 原版
clang++ example_cpp.cpp -o example_cpp
count_bits 2144 # expect 0
./example_cpp
count_bits 2144 # expect 0
# 自动插桩
dcov-clang++ example_cpp.cpp -o example_cpp 
count_bits 2144 # expect 0
DCOV_KEY_C=2144 ./example_cpp
count_bits 2144 # expect 3
```