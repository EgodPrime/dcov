#ifndef _DCOV_PY_H_
#define _DCOV_PY_H_
#include <stdint.h>
#include <Python.h>
#include "dcov_common.h"
static uint32_t previous_edge_idx = -1;
static uint32_t prev_loc_c = -1;
static PyObject * get_bitmap_size(PyObject *self, PyObject *args);
static PyObject * open_bitmap_py(PyObject *self, PyObject *args);
static PyObject * open_bitmap_c(PyObject *self, PyObject *args);
static PyObject * open_bitmap_java(PyObject *self, PyObject *args);
static PyObject * clear_bitmap_py(PyObject *self, PyObject *args);
static PyObject * clear_bitmap_c(PyObject *self, PyObject *args);
static PyObject * clear_bitmap_java(PyObject *self, PyObject *args);
static PyObject * close_bitmap_py(PyObject *self, PyObject *args);
static PyObject * close_bitmap_c(PyObject *self, PyObject *args);
static PyObject * close_bitmap_java(PyObject *self, PyObject *args);
static PyObject * count_bits_py(PyObject *self, PyObject *args);
static PyObject * count_bits_c(PyObject *self, PyObject *args);
static PyObject * count_bits_java(PyObject *self, PyObject *args);
static PyObject * on_hit_py(PyObject *self, PyObject *args);
static PyObject * on_hit_py_edge(PyObject *self, PyObject *args);
// more flexible versions of the functions that take a key_name and key
static PyObject * open_bitmap_x(PyObject *self, PyObject *args);
static PyObject * clear_bitmap_x(PyObject *self, PyObject *args);
static PyObject * close_bitmap_x(PyObject *self, PyObject *args);
static PyObject * count_bits_x(PyObject *self, PyObject *args);
static PyObject * copy_bitmap(PyObject *self, PyObject *args);
static PyObject * merge_bitmap(PyObject *self, PyObject *args);
static PyObject * count_aflpp_bytes(PyObject *self, PyObject *args);
#endif
