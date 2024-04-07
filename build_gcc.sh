DCOV_DIR=$(pwd)
pushd gcc-9.4.0
./contrib/download_prerequisites
popd
rm -rf gcc_build
mkdir gcc_build
pushd gcc_build
${DCOV_DIR}/gcc-9.4.0/configure --prefix=${DCOV_DIR}/gcc_install --enable-languages=c,c++ --disable-multilib
make -j$(nproc)
make install
popd
pushd /usr/bin
mv gcc gcc.backup
mv g++ g++.backup
ln -s ${DCOV_DIR}/gcc_install/bin/gcc gcc
ln -s ${DCOV_DIR}/gcc_install/bin/g++ g++
popd
gcc -v
