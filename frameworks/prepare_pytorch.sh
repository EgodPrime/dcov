git clone --recursive https://github.com/pytorch/pytorch
pushd pytorch
git checkout v2.1.0
git submodule sync
git submodule update --init --recursive
popd