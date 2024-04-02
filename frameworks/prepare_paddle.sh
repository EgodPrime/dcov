git clone https://github.com/PaddlePaddle/Paddle.git
pushd Paddle
git checkout v2.6.1
patch < ../Paddle_patch.diff
popd