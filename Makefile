GCC_PLUGIN_DIR=/root/gcc_9.4.0_install
CC=${GCC_PLUGIN_DIR}/bin/gcc
CXX=${GCC_PLUGIN_DIR}/bin/g++
GCC_PLUGIN_HEADERS=${GCC_PLUGIN_DIR}/lib/gcc/x86_64-pc-linux-gnu/9.4.0/plugin/include
CXX_FLAGS_COMMON=-std=c++17 -O3 -fPIC -shared

all: dcov_ins dcov_trace dcov_info probe

.PHONY: dcov_info
dcov_info:
	${CXX} ${CXX_FLAGS_COMMON} -lrt -pthread -fopenmp  dcov_info.cxx -o libdcov_info.so

.PHONY: dcov_trace
dcov_trace:
	${CXX} ${CXX_FLAGS_COMMON} -lrt dcov_trace.cxx -o libdcov_trace.so

.PHONY: dcov_ins
dcov_ins:
	${CXX} ${CXX_FLAGS_COMMON} -fno-rtti -Wno-literal-suffix -I${GCC_PLUGIN_HEADERS} MurmurHash3.cxx dcov_ins.cxx -o libdcov_ins.so

.PHONY: probe
probe:
	${CXX} ${CXX_FLAGS_COMMON} -pthread -fopenmp -I./ -I/root/miniconda3/envs/tf2.11.0-ins/include/python3.9 dcov_info.cxx dcov_trace.cxx MurmurHash3.cxx probe.cxx -o probe.so

.PHONY: install
install:
	cp libdcov*.so /usr/lib

.PHONY: clean
clean:
	rm -f libdcov*.so probe.so

.PHONY: uninstall
uninstall:
	rm /usr/lib/libdcov*.so