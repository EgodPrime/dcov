mkdir -p dlf_whls_ins
pushd pytorch
export CMAKE_PREFIX_PATH=$(dirname $(dirname $(which python)))
export CMAKE_C_FLAGS="-fplugin=libdcov_ins.so -lrt -ldcov_trace"
export CMAKE_CXX_FLAGS="-fplugin=libdcov_ins.so -lrt -ldcov_trace"
export CMAKE_LINKER_FLAGS="-lrt -ldcov_trace"
export USE_CUDA=0 USE_ROCM=0 MAX_JOBS=$(nproc)
python setup.py bdist_wheel
cp dist/torch-2.2.0a0+git8ac9b20-cp39-cp39-linux_x86_64.whl ../dlf_whls_ins/
pip install ../dlf_whls_ins/torch-2.2.0a0+git8ac9b20-cp39-cp39-linux_x86_64.whl
popd
