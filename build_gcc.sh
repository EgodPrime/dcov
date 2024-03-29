DCOV_DIR=$(pwd)
pushd gcc-9.4.0
./contrib/download_prerequisites
popd
rm -rf gcc_build
mkdir gcc_build
pushd gcc_build
${DCOV_DIR}/gcc-9.4.0/configure --prefix=${DCOV_DIR}/gcc_install --enable-languages=c,c++ --disable-multilib
make
make install
popd