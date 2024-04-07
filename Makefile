GCC_DIR=./gcc_install
CC=${GCC_DIR}/bin/gcc
CXX=${GCC_DIR}/bin/g++
GCC_PLUGIN_HEADERS=${GCC_DIR}/lib/gcc/x86_64-pc-linux-gnu/9.4.0/plugin/include
CXX_FLAGS_COMMON=-std=c++17 -O3 -fPIC -shared
PYTHON_ENV_DIR=$(shell dirname $(shell dirname $(shell which python)))
PYTHON_VERSION=$(shell ls ${PYTHON_ENV_DIR}/include -l | grep python3 | awk '{print $$NF}') 
PYTHON_INCLUDE_DIR=${PYTHON_ENV_DIR}/include/${PYTHON_VERSION}

BITMAP_SIZE=28
ifeq ($(BITMAP_SIZE), 16)
  CXX_FLAGS_COMMON+= -DBITMAP_SIZE_16
else ifeq ($(BITMAP_SIZE), 20)
  CXX_FLAGS_COMMON+= -DBITMAP_SIZE_20
else ifeq ($(BITMAP_SIZE), 24)
  CXX_FLAGS_COMMON+= -DBITMAP_SIZE_24
endif

ifeq ($(NO_PARALLEL), 1)
  CXX_FLAGS_COMMON+= -DNO_PARALLEL
endif

ifeq ($(NORMAL_BIT_COUNT), 1)
  CXX_FLAGS_COMMON+= -DNORMAL_BIT_COUNT
endif

all: dcov_ins dcov_ins_server dcov_trace dcov_info probe
	
.PHONY: check
check:
	@echo "PYTHON_INCLUDE_DIR: ${PYTHON_INCLUDE_DIR}" 

.PHONY: dcov_info
dcov_info:
	${CXX} ${CXX_FLAGS_COMMON} -lrt -pthread -fopenmp  dcov_info.cxx -o libdcov_info.so

.PHONY: dcov_trace
dcov_trace:
	${CXX} ${CXX_FLAGS_COMMON} -lrt dcov_info.cxx dcov_trace.cxx -o libdcov_trace.so

.PHONY: dcov_ins
dcov_ins:
	${CXX} ${CXX_FLAGS_COMMON} -fno-rtti -Wno-literal-suffix -I${GCC_PLUGIN_HEADERS} MurmurHash3.cxx dcov_ins.cxx -o libdcov_ins.so

.PHONY: dcov_ins_server
dcov_ins_server:
	${CXX} -std=c++17 -O3 -lrt dcov_ins_server.cxx -o dcov_ins_server

.PHONY: probe
probe:
	${CXX} ${CXX_FLAGS_COMMON} -pthread -fopenmp -I./ -I${PYTHON_INCLUDE_DIR} dcov_trace.cxx MurmurHash3.cxx probe.cxx -o probe.so

.PHONY: install
install:
	cp libdcov*.so /usr/lib

.PHONY: clean
clean:
	rm -f libdcov*.so probe.so dcov_ins_server

.PHONY: uninstall
uninstall:
	rm /usr/lib/libdcov*.so
