#ifndef _DCOV_H_
#define _DCOV_H_
const int shm_key_python = 4399;
const int shm_key_c = 4400;
const unsigned int bitmap_size = 1<<28;
const unsigned int bytemap_size = bitmap_size/8;
static int shmid_python, shmid_c;
static unsigned char* m_data_python, *m_data_c;

/* dcov_trace.cxx
begin
*/
extern "C" void on_bb_hit_python(unsigned int bb_idx);
extern "C" void on_bb_hit_c(unsigned int bb_idx);
/* dcov_trace.cxx
end
*/

/* dcov_info.cxx
begin
*/
// open and map the python bitmap
extern "C" void open_bitmap_python();
// open and map the c bitmap
extern "C" void open_bitmap_c();
// open and map the bitmaps of both python and c
extern "C" void open_bitmap();
// init the python bitmap to all zeros(based on `open_bitmap_python`)
extern "C" void init_bitmap_python();
// init the c bitmap to all zeros(based on `open_bitmap_c`)
extern "C" void init_bitmap_c();
// init the bitmaps of both python and c to all zeros
extern "C" void init_bitmap();
// close the python bitmap
extern "C" void close_bitmap_python();
// close the c bitmap
extern "C" void close_bitmap_c();
// close the bitmaps of both python and c
extern "C" void close_bitmap();
// get the count of no-zero bits in the python bitmap
extern "C" unsigned int get_bb_cnt_python();
// get the count of no-zero bits in the c bitmap
extern "C" unsigned int get_bb_cnt_c();
// save the bitmaps into files
extern "C" void save_bitmap();
/* dcov_info.cxx
end
*/
#endif
