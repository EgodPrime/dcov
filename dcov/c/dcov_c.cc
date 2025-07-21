#include <sanitizer/coverage_interface.h>
#include <functional>
#include <sys/shm.h>
#include <string.h>
#include "dcov_c.h"
#include <iostream>


static bool __init__shm__ = [](){
    char* DCOV_KEY_C = getenv("DCOV_KEY_C");
    if (DCOV_KEY_C != nullptr) {
        shm_key_c = atoi(DCOV_KEY_C);
    }
    // std::cout<<"DCOV Loaded with DCOV_KEY_C="<<shm_key_c<<std::endl;
    shmid_c = shmget(shm_key_c, bytemap_size, IPC_CREAT | 0666);
    m_data_c = (unsigned char*) shmat(shmid_c, NULL, 0);
    return true;
}();

void _on_hit(uint8_t* m_data, uint32_t edge_idx){
    // printf("hit %d\n", edge_idx);
    uint32_t idx = edge_idx/8;
    uint32_t bit = edge_idx%8;
    uint8_t new_byte = 1<<bit;
    m_data[idx] |= new_byte;
}

extern "C" void __sanitizer_cov_trace_pc_guard_init(
    uint32_t *start,
    uint32_t *stop) 
{
    static uint32_t ET_c = 0;
    if (start == stop || *start) return;
    for (uint32_t *x = start; x < stop; x++){
      *x = ++ET_c;
    }
}

extern "C" void __sanitizer_cov_trace_pc_guard(uint32_t *edge_idx) {
    if (!*edge_idx) return; 
    _on_hit(m_data_c, *edge_idx);
    *edge_idx=0;
}