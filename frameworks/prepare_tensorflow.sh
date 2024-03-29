conda create -n tf2.11.0-ins python=3.9
conda activate tf2.11.0-ins
pip install numpy wheel packaging requests opt_einsum
pip install keras_preprocessing --no-deps
git clone https://github.com/tensorflow/tensorflow.git
pushd tensorflow
git checkout r2.11
patch -p0 < ../tensorflow.patch
popd