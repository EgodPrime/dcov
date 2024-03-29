DCOV_DIR=$(pwd)
pushd /usr/bin
mv gcc gcc.backup
mv g++ g++.backup
ln -s ${DCOV_DIR}/gcc_install/bin/gcc gcc
ln -s ${DCOV_DIR}/gcc_install/bin/g++ g++
popd
gcc -v