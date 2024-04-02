mkdir -p dlf_whls_ins
pushd tensorflow
./configure
bazel build --config=opt --config=dcov //tensorflow/tools/pip_package:build_pip_package
/bazel-bin/tensorflow/tools/pip_package/build_pip_package ../dlf_whls_ins/
pip install ../dlf_whls_ins/tensorflow-2.11.1-cp39-cp39-linux_x86_64.whl
popd