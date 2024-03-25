pushd ./FreeFuzz/src
conda run -n tf2.11.0-ins python FreeFuzz.py --conf expr_tf.conf
conda run -n tf2.11.0-ins python FreeFuzz.py --conf expr_tf_fb.conf
conda run -n pt2.1.0-ins python FreeFuzz.py --conf expr_pt.conf
conda run -n pt2.1.0-ins python FreeFuzz.py --conf expr_pt_fb.conf
popd