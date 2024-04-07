FROM ubuntu:20.04
WORKDIR /root
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential wget libgmp-dev
CMD ["/bin/bash"]
