#ifndef _DCOV_TRACE_H_
#define _DCOV_TRACE_H_
#include "dcov.h"
/* dcov_trace.cxx
begin
*/
extern "C" void on_bb_hit_python(unsigned int bb_idx);
extern "C" void on_bb_hit_c(unsigned int bb_idx);
/* dcov_trace.cxx
end
*/
#endif
