FROM ubuntu:20.04

WORKDIR /root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential wget libgmp-dev
    
ENV DEBIAN_FRONTEND=dialog

# conda环境安装
RUN wget -c https://repo.anaconda.com/miniconda/Miniconda3-py39_24.1.2-0-Linux-x86_64.sh && \
    chmod a+x /root/Miniconda3-py39_24.1.2-0-Linux-x86_64.sh && \
    /roor/Miniconda3-py39_24.1.2-0-Linux-x86_64.sh -b -p /root/miniconda3 && \
    rm /root/Miniconda3-py39_24.1.2-0-Linux-x86_64.sh && \
    chmod a+x /root/miniconda3/etc/profile.d/conda.sh  &&\
    ln -s /root/miniconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /root/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

