CC = clang
CXX = clang++
CXXFLAGS = -std=c++17 -g
GCC_PLUGIN_HEADERS=/usr/lib/gcc/x86_64-linux-gnu/11/plugin/include
LLVM_HEADERS=/usr/lib/llvm-15/include

all: libdcov_llvm_pass.so libdcov_c.so libdcov_java.so dcov-cc count_bits clear_bitmap


dcov_c.o: dcov_c.cc
	$(CXX) $(CXXFLAGS) -c $<

libdcov_c.so: dcov_c.o
	$(CXX) $(CXXFLAGS) -shared -fPIC $< $(LDFLAGS) -o $@

# libdcov_c.a: dcov_c.o
# 	ar rcs $@ $<

libdcov_llvm_pass.so: dcov_llvm_pass.so.cxx
	$(CXX) $(CXXFLAGS) -shared -fPIC $< -I${LLVM_HEADERS} $(LDFLAGS) -o $@

libdcov_java.so: dcov_java.cxx dcov_java.h dcov_common.h
	$(CXX) $(CXXFLAGS) -shared -fPIC $< $(LDFLAGS) -o $@

# libdcov_gimple.so: dcov_gimple.cxx MurmurHash3.cxx dcov_common.h
# 	$(CXX) $(CXXFLAGS) -shared -fPIC -fno-rtti -Wno-array-bounds -I${GCC_PLUGIN_HEADERS} $< $(LDFLAGS) -o $@

dcov-cc: dcov-cc.cxx
	$(CXX) $(CXXFLAGS) -o $@ $<
# ln -sf dcov-cc dcov-gcc
# ln -sf dcov-cc dcov-g++
	ln -sf dcov-cc dcov-clang
	ln -sf dcov-cc dcov-clang++

# dcov-ld: dcov-ld.cxx
# 	$(CXX) $(CXXFLAGS) -o $@ $<

count_bits: count_bits.cxx
	$(CXX) $(CXXFLAGS) -o $@ $<

clear_bitmap: clear_bitmap.cxx
	$(CXX) $(CXXFLAGS) -o $@ $<
                                                                                                                                                                                                                                                                                            
.PHONY: install
install: all
	cp -t /usr/lib/ libdcov_llvm_pass.so libdcov_java.so libdcov_c.so 
	cp -t /usr/bin/ dcov-clang dcov-clang++ count_bits clear_bitmap

.PHONY: uninstall
uninstall:
	rm -f /usr/lib/dcov_c.o  /usr/lib/libdcov_c.so /usr/lib/libdcov_c.a /usr/lib/libdcov_java.so /usr/lib/libdcov_gimple.so /usr/lib/libdcov_llvm_pass.so
	rm -f /usr/bin/dcov-clang /usr/bin/dcov-clang++ /usr/bin/dcov-ld /usr/bin/dcov-gcc /usr/bin/dcov-g++ /usr/bin/count_bits /usr/bin/clear_bitmap

.PHONY: clean
clean:
	rm -f dcov_c.o libdcov_c.so libdcov_c.a libdcov_java.so dcov-cc dcov-clang dcov-clang++  dcov-ld libdcov_gimple.so libdcov_llvm_pass.so count_bits clear_bitmap

