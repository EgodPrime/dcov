rm -f results.txt
echo "BITMAP_SIZE,NO_PARALLEL,NORAM_BIT_COUNT,get_bb_cnt_python(ms),get_bb_cnt_c(ms),get_bb_cnts(ms)" > results.txt

bitmap_size=("16" "20" "24" "28")  
no_parallel=("1" "0")  
normal_bit_count=("1" "0") 

for size in "${bitmap_size[@]}"; do  
    for par in "${no_parallel[@]}"; do  
        for bc in "${normal_bit_count[@]}"; do
            echo "BITMAP_SIZE=$size NO_PARALLEL=$par NORMAL_BIT_COUNT=$bc"   
            bash build.sh BITMAP_SIZE=$size NO_PARALLEL=$par NORMAL_BIT_COUNT=$bc  
            echo -n "${size},${par},${bc}" >> results.txt  
            conda run -n tf2.11.0 python exp.py  
        done  
    done  
done

# 如果中途执行失败了，一定要回到dcov目录下按照默认配置重新编译
# 执行顺利时最后一个任务就是默认配置