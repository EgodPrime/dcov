rm -f results.txt
echo "dlf,analyzer,ET(ms),AT(ms),TT(ms)" > results.txt
conda run -n tf2.11.0      python exp.py --libname tensorflow --mode base
conda run -n tf2.11.0      python exp.py --libname tensorflow --mode coverage.py
conda run -n tf2.11.0      python exp.py --libname tensorflow --mode slipcover
conda run -n tf2.11.0      python exp.py --libname tensorflow --mode dcov-python
conda run -n tf2.11.0-ins  python exp.py --libname tensorflow --mode dcov-c
conda run -n tf2.11.0-ins  python exp.py --libname tensorflow --mode dcov
conda run -n pt2.1.0       python exp.py --libname torch      --mode base
conda run -n pt2.1.0       python exp.py --libname torch      --mode coverage.py
conda run -n pt2.1.0       python exp.py --libname torch      --mode slipcover
conda run -n pt2.1.0       python exp.py --libname torch      --mode dcov-python
conda run -n pt2.1.0-ins   python exp.py --libname torch      --mode dcov-c
conda run -n pt2.1.0-ins   python exp.py --libname torch      --mode dcov
conda run -n pp2.6.1       python exp.py --libname paddle     --mode base
conda run -n pp2.6.1       python exp.py --libname paddle     --mode coverage.py
conda run -n pp2.6.1       python exp.py --libname paddle     --mode slipcover
conda run -n pp2.6.1       python exp.py --libname paddle     --mode dcov-python
conda run -n pp2.6.1-ins   python exp.py --libname paddle     --mode dcov-c
conda run -n pp2.6.1-ins   python exp.py --libname paddle     --mode dcov