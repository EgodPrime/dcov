conda run -n tf2.11.0      python exp.py --libname tensorflow --mode base
sleep 2
conda run -n tf2.11.0-ins  python exp.py --libname tensorflow --mode dcov
sleep 2
conda run -n pt2.1.0       python exp.py --libname torch --mode base
sleep 2
conda run -n pt2.1.0-ins   python exp.py --libname torch --mode dcov
sleep 2
conda run -n pp2.6.1       python exp.py --libname paddle --mode base
sleep 2
conda run -n pp2.6.1-ins   python exp.py --libname paddle --mode dcov
python plot_together.py