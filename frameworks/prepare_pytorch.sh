conda create -n pt2.1.0-ins python=3.9
conda activate pt2.1.0-ins
git clone --recursive https://github.com/pytorch/pytorch
pushd pytorch
git checkout v2.1.0
git submodule sync
git submodule update --init --recursive
pip install -r requirements.txt
conda install cmake ninja pyyaml
conda install intel::mkl-static intel::mkl-include