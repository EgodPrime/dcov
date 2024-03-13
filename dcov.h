#ifndef _DCOV_H_
#define _DCOV_H_
const int shm_key_python = 4399;
const int shm_key_c = 4400;
const unsigned int bitmap_size = 1<<28;
const unsigned int bytemap_size = bitmap_size/8;
static int shmid_python, shmid_c;
static unsigned char* m_data_python, *m_data_c;
#endif
