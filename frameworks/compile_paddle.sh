mkdir -p dlf_whls_ins
pushd Paddle
rm -rf build
mkdir -p build
pushd build
python_prefix=$(dirname $(dirname $(which python)))
cmake .. -GNinja -DPY_VERSION=3.9 -DPYTHON_EXECUTABLE:FILEPATH=$python_prefix/bin/python -DPYTHON_INCLUDE_DIR:PATH=python_prefix/include/python3.9 -DPYTHON_LIBRARY:FILEPATH=python_prefix/lib/libpython3.9.so -DWITH_GPU=OFF
ninja -j$(nproc)
popd
cp build/python/dist/paddlepaddle-2.6.1-cp39-cp39-linux_x86_64.whl ../dlf_whls_ins/
pip install ../dlf_whls_ins/paddlepaddle-2.6.1-cp39-cp39-linux_x86_64.whl
popd
