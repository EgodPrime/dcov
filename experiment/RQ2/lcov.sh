start_time=$(date +%s%N)  
lcov -c --no-external --include /home/dcov/dlf_compile_workspace/tensorflow-gcov/tensorflow --rc lcov_branch_coverage=1 --directory ./bazel-out/k8-opt/bin/tensorflow/ --base-directory ~/dlf_compile_workspace/tensorflow-gcov/ -o all.info
end_time=$(date +%s%N)  

# 计算执行时间（毫秒）  
execution_time=$(( (end_time - start_time) / 1000 ))  

# 输出执行时间  
echo "Command executed in $execution_time us."