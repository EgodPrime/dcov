#ifndef _DCOV_H_
#define _DCOV_H_
static const int shm_key_python = 4399;
static const int shm_key_c = 4400;
static const unsigned int bitmap_size = 1<<28;
static const unsigned int bytemap_size = bitmap_size/8;
static int shmid_python, shmid_c;
static unsigned char* m_data_python, *m_data_c;
#endif
