make clean
make
make install
cd ..
python -m dcov.test_get_bb_cnt
cd dcov
