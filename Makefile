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

all: dcov_ins_server libdcov_info.so libdcov_trace.so libdcov_ins.so probe
	
.PHONY: check
check:
	@echo "PYTHON_INCLUDE_DIR: ${PYTHON_INCLUDE_DIR}" 

.PHONY: libdcov_info.so
libdcov_info.so: src/dcov_info.cxx
	${CXX} ${CXX_FLAGS_COMMON} -lrt -pthread -fopenmp  src/dcov_info.cxx -o dcov/libdcov_info.so

.PHONY: libdcov_trace.so
libdcov_trace.so: src/dcov_info.cxx src/dcov_trace.cxx
	${CXX} ${CXX_FLAGS_COMMON} -lrt src/dcov_info.cxx src/dcov_trace.cxx -o dcov/libdcov_trace.so

.PHONY: libdcov_ins.so
libdcov_ins.so: src/MurmurHash3.cxx src/dcov_ins.cxx
	${CXX} ${CXX_FLAGS_COMMON} -fno-rtti -Wno-literal-suffix -I${GCC_PLUGIN_HEADERS} src/MurmurHash3.cxx src/dcov_ins.cxx -o dcov/libdcov_ins.so

.PHONY: dcov_ins_server
dcov_ins_server: src/dcov_ins_server.cxx
	${CXX} -std=c++17 -O3 -lrt src/dcov_ins_server.cxx -o dcov/dcov_ins_server

.PHONY: probe
probe: src/dcov_trace.cxx src/MurmurHash3.cxx src/probe.cxx
	${CXX} ${CXX_FLAGS_COMMON} -pthread -fopenmp -I./ -I${PYTHON_INCLUDE_DIR} src/dcov_trace.cxx src/MurmurHash3.cxx src/probe.cxx -o dcov/probe.so

.PHONY: install
install:
	cp -f dcov/libdcov*.so /usr/lib/

.PHONY: clean
clean:
	rm -f dcov/libdcov*.so dcov/probe.so dcov/dcov_ins_server

.PHONY: uninstall
uninstall:
	rm /usr/lib/libdcov*.so
