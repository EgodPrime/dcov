rm -f results.txt
echo "dlf,analyzer,ET(ms),AT(ms),TT(ms)" > results.txt
conda run -n tf2.11.0      python exp.py --libname tensorflow --mode base
conda run -n pt2.1.0       python exp.py --libname torch      --mode base
conda run -n pp2.6.1       python exp.py --libname paddle     --mode base

conda run -n tf2.11.0      python exp.py --libname tensorflow --mode coverage.py
conda run -n pt2.1.0       python exp.py --libname torch      --mode coverage.py
conda run -n pp2.6.1       python exp.py --libname paddle     --mode coverage.py

conda run -n tf2.11.0      python exp.py --libname tensorflow --mode slipcover
conda run -n pt2.1.0       python exp.py --libname torch      --mode slipcover
conda run -n pp2.6.1       python exp.py --libname paddle     --mode slipcover

conda run -n tf2.11.0      python exp.py --libname tensorflow --mode dcov-python
conda run -n pt2.1.0       python exp.py --libname torch      --mode dcov-python
conda run -n pp2.6.1       python exp.py --libname paddle     --mode dcov-python

conda run -n tf2.11.0-ins  python exp.py --libname tensorflow --mode dcov-c
conda run -n pt2.1.0-ins   python exp.py --libname torch      --mode dcov-c
conda run -n pp2.6.1-ins   python exp.py --libname paddle     --mode dcov-c

conda run -n tf2.11.0-ins  python exp.py --libname tensorflow --mode dcov
conda run -n pt2.1.0-ins   python exp.py --libname torch      --mode dcov
conda run -n pp2.6.1-ins   python exp.py --libname paddle     --mode dcov

conda run -n tf2.11.0-gcov python exp.py --libname tensorflow --mode gcov
start_time=$(date +%s%N)  
lcov -c --no-external --include /home/dcov/dlf_compile_workspace/tensorflow-gcov/tensorflow --rc lcov_branch_coverage=1 --directory ./bazel-out/k8-opt/bin/tensorflow/ --base-directory ~/dlf_compile_workspace/tensorflow-gcov/ -o all.info
end_time=$(date +%s%N)  
X=$(( (end_time - start_time) / 1000000 ))  
# 读取result_gcov.txt的最后一行
last_line=$(tail -n 1 results.txt)
# 使用IFS（内部字段分隔符）按逗号分割最后一行，并存入数组
IFS=',' read -r -a array <<< "$last_line"
# 计算新的倒数第一个数据（X加上倒数第三个数据）
new_last=$(echo "${array[-3]} + $X" | bc)
# 替换倒数第二个和倒数第一个数据
array[-2]=$X
array[-1]=$new_last
# 将数组重新组合为一个由逗号分隔的字符串
new_line=$(IFS=,; echo "${array[*]}")
# 使用sed替换文件中的最后一行
sed -i '$ d' results.txt # 先删除最后一行
echo "$new_line" >> results.txt # 然后添加新的最后一行