#ifndef _DCOV_H_
#define _DCOV_H_
static const int shm_key_python = 4399;
static const int shm_key_c = 4400;

#if defined(BITMAP_SIZE_16)
static const unsigned int bitmap_size = 1<<16;
#elif defined(BITMAP_SIZE_20)
static const unsigned int bitmap_size = 1<<20;
#elif defined(BITMAP_SIZE_24)
static const unsigned int bitmap_size = 1<<24;
#else
static const unsigned int bitmap_size = 1<<28;
#endif

static const unsigned int bytemap_size = bitmap_size/8;
static int shmid_python, shmid_c;
static unsigned char* m_data_python, *m_data_c;
#endif
