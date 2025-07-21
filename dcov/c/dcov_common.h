#ifndef _DCOV_COMMON_H_
#define _DCOV_COMMON_H_
#include <stdint.h>
static const uint32_t bitmap_size = 1<<20;
static const uint32_t bytemap_size = bitmap_size>>3;
static int shm_key_py=4399;
static int shm_key_c=4400;
static int shm_key_java=4401;
static int shmid_py,shmid_c,shmid_java;
static uint8_t* m_data_py, *m_data_c, *m_data_java;
#endif
