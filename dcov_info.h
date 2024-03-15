#ifndef _DCOV_INFO_H_
#define _DCOV_INFO_H_

#include "dcov_info.h"

/* dcov_info.cxx
begin
*/
extern "C" int get_bitmap_size();
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
