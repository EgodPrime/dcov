is_docker() {  
    if [ -f /.dockerenv ]; then  
        return 0  
    else  
        return 1  
    fi  
}  

conda create -n pp2.6.1-ins python=3.9
conda activate pp2.6.1-ins
if is_docker; then  
    # 在Docker容器中直接执行命令  
    apt install -y swig wget patchelf unrar
else  
    # 在虚拟机或其他环境中使用sudo执行命令  
    sudo apt install -y swig wget patchelf unrar
fi
pip install numpy protobuf ninja cmake
git clone https://github.com/PaddlePaddle/Paddle.git
pushd Paddle
git checkout v2.6.1
patch -p0 < ../Paddle_patch.diff
popd