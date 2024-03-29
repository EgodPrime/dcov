## Before All
Remeber to build and install dcov before anything!!!

We divided the build-from-source process into `prepare_xx.sh` and `compile_xx.sh` for each deep learning framework (DLF).

The `prepare_xx.sh` creates a conda environment, downloads the source code and applies the patch for instrumentation.

The `compile_xx.sh` build DLF from source with instrumentation and install the generated .whl into the conda environment.

## TensorFlow
```bash
# in one terminal
../dcov_ins_server
# in another terminal
bash prepare_tensorflow.sh
bash compile_tensorflow.sh
```

## PyTorch
```bash
# in one terminal
../dcov_ins_server
# in another terminal
bash prepare_pytorch.sh
bash compile_pytorch.sh
```

## PaddlePaddle
```bash
# in one terminal
../dcov_ins_server
# in another terminal
bash prepare_paddle.sh
bash compile_paddle.sh
```