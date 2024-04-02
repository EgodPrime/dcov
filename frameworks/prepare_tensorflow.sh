
git clone https://github.com/tensorflow/tensorflow.git
pushd tensorflow
git checkout r2.11
patch < ../tensorflow.patch
popd