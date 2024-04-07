## Before All
Remeber to build and install dcov before anything!!!

We divided the build-from-source process into `prepare_xx.sh` and `compile_xx.sh` for each deep learning framework (DLF).

The `prepare_xx.sh` creates a conda environment, downloads the source code and applies the patch for instrumentation.

The `compile_xx.sh` build DLF from source with instrumentation and install the generated .whl into the conda environment.

## TensorFlow

### download source code
```bash
bash prepare_tensorflow.sh
```

### create python env
```bash
conda create -n tf2.11.0-ins python=3.9
conda activate tf2.11.0-ins
conda install bazel==5.4.1
pip install numpy wheel packaging requests opt_einsum
pip install keras_preprocessing --no-deps
conda deactivate
```

### build
```bash
# in one terminal
../dcov_ins_server
# in another terminal
conda activate tf2.11.0-ins
# For the choices that appear in configure, type enter for all of them.
bash compile_tensorflow.sh
conda deactivate
```

## PyTorch

### download source code
```bash
bash prepare_pytorch.sh
```

### create python env
```bash
conda create -n pt2.2.0-ins python=3.9
conda activate pt2.2.0-ins
conda install cmake ninja pyyaml
conda install intel::mkl-static intel::mkl-include
pushd pytorch
pip install -r requirements.txt
popd
conda deactivate
```

### build
```bash
# in one terminal
../dcov_ins_server
# in another terminal
conda activate pt2.2.0-ins
bash compile_pytorch.sh
conda deactivate
```

## PaddlePaddle

### download source code
```bash
bash prepare_paddle.sh
```

### create python env
```bash
conda create -n pp2.6.0-ins python=3.9
conda activate pp2.6.0-ins
apt install -y swig wget patchelf unrar
pip install numpy protobuf ninja cmake
conda deactivate
```

### build
```bash
# in one terminal
../dcov_ins_server
# in another terminal
conda activate pp2.6.0-ins
bash compile_paddle.sh
conda deactivate
```