
git clone https://github.com/tensorflow/tensorflow.git
pushd tensorflow
git checkout v2.11.0
patch -p1 < ../tensorflow.patch
popd