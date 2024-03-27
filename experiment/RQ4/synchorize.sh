rm -rf FreeFuzz/src/*-output
scp -r FreeFuzz/src dcov@192.168.114.2:~/dcov/experiment/RQ4/FreeFuzz/
scp -r FreeFuzz/src dcov@192.168.114.3:~/dcov/experiment/RQ4/FreeFuzz/
scp -r FreeFuzz/src dcov@192.168.114.4:~/dcov/experiment/RQ4/FreeFuzz/
scp ../../dcov.py dcov@192.168.114.2:~/dcov/
scp ../../dcov.py dcov@192.168.114.3:~/dcov/
scp ../../dcov.py dcov@192.168.114.4:~/dcov/