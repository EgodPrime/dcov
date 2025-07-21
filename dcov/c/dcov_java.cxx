#include <sanitizer/coverage_interface.h>
#include <functional>
#include <sys/shm.h>
#include <string.h>
#include "dcov_common.h"
#include <iostream>

static bool __init__shm__ = [](){
    char* DCOV_KEY_JAVA = std::getenv("DCOV_KEY_JAVA");
    if (DCOV_KEY_JAVA != nullptr) {
        shm_key_java = std::atoi(DCOV_KEY_JAVA);
    }
    std::cout<<"DCOV Loaded with DCOV_KEY_JAVA="<<shm_key_java<<std::endl;
    shmid_java = shmget(shm_key_java, bytemap_size, IPC_CREAT | 0666);
    m_data_java = (unsigned char*) shmat(shmid_java, NULL, 0);
    return true;
}();

extern "C"  void set_bit(int index){
    uint32_t x = (uint32_t) index;
    uint32_t idx = x/8;
    uint32_t bit = x%8;
    uint8_t new_byte = 1<<bit;
    m_data_java[idx] |= new_byte;
}