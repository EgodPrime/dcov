#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>
#include <stdio.h>
#include "dcov.h"
#include "dcov_trace.h"

// 一种C语言特有的小把戏，可以使得下面这个函数在库文件被加载时自动运行
static bool __init__shm__ = [](){
    shmid_python = shmget(shm_key_python, bytemap_size, IPC_CREAT | 0666);
    m_data_python = (unsigned char*) shmat(shmid_python, NULL, 0);
    shmid_c = shmget(shm_key_c, bytemap_size, IPC_CREAT | 0666);
    m_data_c = (unsigned char*) shmat(shmid_c, NULL, 0);
    return true;
}();

void _on_bb_hit(unsigned char* m_data, int bb_idx){
    unsigned char data;
    unsigned int idx = bb_idx/8;
    unsigned char bit = bb_idx%8;
    unsigned char new_byte = 1<<bit;
    do
    {
        data = __atomic_load_1(m_data+idx, __ATOMIC_SEQ_CST);
        new_byte = data | new_byte;
    }
    while (!__atomic_compare_exchange_1(m_data+idx, &data, new_byte, false, __ATOMIC_SEQ_CST, __ATOMIC_SEQ_CST));
}

extern "C" void on_bb_hit_python(unsigned int bb_idx){
    _on_bb_hit(m_data_python, bb_idx);
}

extern "C" void on_bb_hit_c(unsigned int bb_idx){
    _on_bb_hit(m_data_c, bb_idx);
}