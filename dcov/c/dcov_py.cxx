#include <sanitizer/coverage_interface.h>
#include <functional>
#include <sys/shm.h>
#include <string.h>
#include <Python.h>
#include "dcov_py.h"
#include <iostream>

static bool __init__shm__ = [](){
    char* DCOV_KEY_PYTHON = std::getenv("DCOV_KEY_PYTHON");
    if (DCOV_KEY_PYTHON != nullptr) {
        shm_key_py = std::atoi(DCOV_KEY_PYTHON);
    }
    //std::cout<<"DCOV Loaded with DCOV_KEY_PYTHON="<<shm_key_py<<std::endl;
    shmid_py = shmget(shm_key_py, bytemap_size, IPC_CREAT | 0666);
    m_data_py = (unsigned char*) shmat(shmid_py, NULL, 0);
    return true;
}();

void set_bit(uint8_t* m_data, uint32_t edge_idx){
    uint32_t idx = edge_idx/8;
    uint32_t bit = edge_idx%8;
    uint8_t new_byte = 1<<bit;
    m_data[idx] |= new_byte;
}

uint32_t _count_bits(unsigned char* m_data){
    unsigned int count = 0;
    #pragma omp parallel for reduction(+:count)
    for (size_t i = 0; i < bytemap_size; i++) {
        unsigned char c = m_data[i];
        c = ( c & 0x55 ) + ( (c >> 1)  & 0x55 ) ;
        c = ( c & 0x33 ) + ( (c >> 2)  & 0x33 ) ;
        c = ( c & 0x0f ) + ( (c >> 4)  & 0x0f ) ;
        count += c;
    }
    return count;
}

uint32_t hash_edge(uint32_t a, uint32_t b){
    std::hash<uint32_t> hasher;
    uint32_t h1 = hasher(a);
    uint32_t h2 = hasher(b);
    uint32_t r = h1 ^ (h2 + 0x9e3779b9 + (h1 << 6) + (h1 >> 2));
    r = r % bitmap_size;
    return r;
}

static PyObject * get_bitmap_size(PyObject *self, PyObject *args){
    return PyLong_FromLong(bitmap_size);
}

static PyObject * open_bitmap_py(PyObject *self, PyObject *args){
    shmid_py = shmget(shm_key_py, bytemap_size, IPC_CREAT | 0666);
    m_data_py = (unsigned char*) shmat(shmid_py, NULL, 0);
    return Py_None;
}

static PyObject * open_bitmap_c(PyObject *self, PyObject *args){
    shmid_c = shmget(shm_key_c, bytemap_size, IPC_CREAT | 0666);
    m_data_c = (unsigned char*) shmat(shmid_c, NULL, 0);
    return Py_None;
}

static PyObject * open_bitmap_java(PyObject *self, PyObject *args){
    shmid_java = shmget(shm_key_java, bytemap_size, IPC_CREAT | 0666);
    m_data_java = (unsigned char*) shmat(shmid_java, NULL, 0); 
    return Py_None;
}

static PyObject * clear_bitmap_py(PyObject *self, PyObject *args){
    shmid_py = shmget(shm_key_py, bytemap_size, IPC_CREAT | 0666);
    m_data_py = (unsigned char*) shmat(shmid_py, NULL, 0);
    memset(m_data_py, 0, bytemap_size);
    return Py_None;
}

static PyObject * clear_bitmap_c(PyObject *self, PyObject *args){
    shmid_c = shmget(shm_key_c, bytemap_size, IPC_CREAT | 0666);
    m_data_c = (unsigned char*) shmat(shmid_c, NULL, 0);
    memset(m_data_c, 0, bytemap_size);
    return Py_None;
}

static PyObject * clear_bitmap_java(PyObject *self, PyObject *args){
    shmid_java = shmget(shm_key_java, bytemap_size, IPC_CREAT | 0666);
    m_data_java = (unsigned char*) shmat(shmid_java, NULL, 0);
    memset(m_data_java, 0, bytemap_size);
    return Py_None;
}

static PyObject * close_bitmap_py(PyObject *self, PyObject *args){
    shmid_py = shmget(shm_key_py, bytemap_size, IPC_CREAT | 0666);
    m_data_py = (unsigned char*) shmat(shmid_py, NULL, 0);
    shmdt(m_data_py);
    shmctl(shmid_py, IPC_RMID, NULL);
    return Py_None;
}

static PyObject * close_bitmap_c(PyObject *self, PyObject *args){
    shmid_c = shmget(shm_key_c, bytemap_size, IPC_CREAT | 0666);
    m_data_c = (unsigned char*) shmat(shmid_c, NULL, 0);
    shmdt(m_data_c);
    shmctl(shmid_c, IPC_RMID, NULL);
    return Py_None;
}

static PyObject * close_bitmap_java(PyObject *self, PyObject *args){
    shmid_java = shmget(shm_key_java, bytemap_size, IPC_CREAT | 0666);
    m_data_java = (unsigned char*) shmat(shmid_java, NULL, 0);
    shmdt(m_data_java);
    shmctl(shmid_java, IPC_RMID, NULL);
    return Py_None;
}

static PyObject * count_bits_py(PyObject *self, PyObject *args){
    uint32_t res = _count_bits(m_data_py);
    return PyLong_FromLong(res);
}

static PyObject * count_bits_c(PyObject *self, PyObject *args){
    uint32_t res = _count_bits(m_data_c);
    return PyLong_FromLong(res);
}

static PyObject * count_bits_java(PyObject *self, PyObject *args){
    uint32_t res = _count_bits(m_data_java);
    return PyLong_FromLong(res);
}

static PyObject * on_hit_py_edge(PyObject *self, PyObject *args){
    uint32_t edge_idx;
    if (PyArg_ParseTuple(args, "i", &edge_idx)){
        set_bit(m_data_py, hash_edge(previous_edge_idx, edge_idx));
        previous_edge_idx = edge_idx;
        return Py_None;
    }else{
        return NULL;
    }
}

static PyObject * on_hit_py(PyObject *self, PyObject *args){
    uint32_t edge_idx;
    if (PyArg_ParseTuple(args, "i", &edge_idx)){
        set_bit(m_data_py, edge_idx);
        return Py_None;
    }else{
        return NULL;
    }
}

static PyObject * set_bit_c(PyObject *self, PyObject *args){
    uint32_t loc;
    if (PyArg_ParseTuple(args, "i", &loc)){
        set_bit(m_data_c, loc);
        return Py_None;
    }else{
        return NULL;
    }
}

static PyObject * set_bit_c_edge(PyObject *self, PyObject *args){
    uint32_t loc;
    if (PyArg_ParseTuple(args, "i", &loc)){
        set_bit(m_data_c, hash_edge(prev_loc_c, loc));
        return Py_None;
    }else{
        return NULL;
    }
}

static PyObject* open_bitmap_x(PyObject *self, PyObject *args){
    int key; // key for shared memory
    if (PyArg_ParseTuple(args, "i", &key)){
        shmid_py = shmget(key, bytemap_size, IPC_CREAT | 0666);
        return Py_None;
    }
    return NULL;
}

static PyObject* clear_bitmap_x(PyObject *self, PyObject *args){
    int key; // key for shared memory
    if (PyArg_ParseTuple(args, "i", &key)){
        int shmid = shmget(key, bytemap_size, IPC_CREAT | 0666);
        uint8_t* data = (uint8_t*)shmat(shmid, NULL, 0);
        memset(data, 0, bytemap_size);
        shmdt(data);
        return Py_None;
    }
    return NULL;
}

static PyObject* close_bitmap_x(PyObject *self, PyObject *args){
    int key; // key for shared memory
    if (PyArg_ParseTuple(args, "i", &key)){
        int shmid = shmget(key, bytemap_size, IPC_CREAT | 0666);
        shmctl(shmid, IPC_RMID, 0);
        return Py_None;
    }
    return NULL;
}

static PyObject* count_bits_x(PyObject *self, PyObject *args){
    int key; // key for shared memory
    if (PyArg_ParseTuple(args, "i", &key)){
        int shmid = shmget(key, bytemap_size, IPC_CREAT | 0666);
        uint8_t* data = (unsigned char*)shmat(shmid, NULL, 0);
        uint32_t res = _count_bits(data);
        shmdt(data);
        return PyLong_FromLong(res);
    }
    return NULL;
}

static PyObject * copy_bitmap(PyObject *self, PyObject *args){
    int ori, dst;
    if (PyArg_ParseTuple(args, "ii", &ori, &dst)){
        int shmid_ori = shmget(ori, bytemap_size, 0666);
        uint8_t* data_ori = (unsigned char*)shmat(shmid_ori, NULL, 0);
        int shmid_dst = shmget(dst, bytemap_size, 0666);
        uint8_t* data_dst = (unsigned char*)shmat(shmid_dst, NULL, 0);
        memcpy(data_dst, data_ori, bytemap_size);
        shmdt(data_ori);
        shmdt(data_dst);
        return Py_None;
    }
    return NULL;
}

static PyObject * merge_bitmap(PyObject *self, PyObject *args){
    /* 
    将ori中的1合并到dst中，达到以下效果：
    dst[i] = ori[i] | dst[i]
    */
    int ori, dst;
    if (PyArg_ParseTuple(args, "ii", &ori, &dst)){
        int shmid_ori = shmget(ori, bytemap_size, 0666);
        uint8_t* data_ori = (unsigned char*)shmat(shmid_ori, NULL, 0);
        int shmid_dst = shmget(dst, bytemap_size, 0666);
        uint8_t* data_dst = (unsigned char*)shmat(shmid_dst, NULL, 0);

        #pragma omp parallel for
        for (size_t i = 0; i < bytemap_size; i++) {
            data_dst[i] |= data_ori[i];
        }

        shmdt(data_ori);
        shmdt(data_dst);
        return Py_None;
    }
    return NULL;
}

static PyObject* count_aflpp_bytes(PyObject* self, PyObject* args) {
    uint32_t afl_bytemap_size;
    int aflpp_bytemap_key;
    
    if (!PyArg_ParseTuple(args, "ii", &afl_bytemap_size, &aflpp_bytemap_key)) {
        return NULL;
    }

    
    int shmid_aflpp = shmget(aflpp_bytemap_key, afl_bytemap_size, 0666);
    uint8_t* data_aflpp = (unsigned char*)shmat(shmid_aflpp, NULL, 0);

    uint32_t  ret = 0;

    #pragma omp parallel for
    for (size_t i = 0; i < afl_bytemap_size; i++) {
      if(data_aflpp[i]){
        ret++;
      }
    }
    shmdt(data_aflpp);
    return PyLong_FromLong(ret);
}

static PyMethodDef DcovInfoMethods[] = {
    {"get_bitmap_size",  get_bitmap_size, METH_VARARGS,
     "Get the size of the bitmap"},
    {"open_bitmap_py",  open_bitmap_py, METH_VARARGS,
     "Open the bitmap for python"},
    {"open_bitmap_c",  open_bitmap_c, METH_VARARGS,
     "Open the bitmap for c"},
    {"open_bitmap_java",  open_bitmap_java, METH_VARARGS,
     "Open the bitmap for java"},
    {"clear_bitmap_py",  clear_bitmap_py, METH_VARARGS,
     "Clear the bitmap for python"},
    {"clear_bitmap_c",  clear_bitmap_c, METH_VARARGS,
     "Clear the bitmap for c"},
    {"clear_bitmap_java",  clear_bitmap_java, METH_VARARGS,
     "Clear the bitmap for java"},
    {"close_bitmap_py",  close_bitmap_py, METH_VARARGS,
     "Close the bitmap for python"},
    {"close_bitmap_c",  close_bitmap_c, METH_VARARGS,
     "Close the bitmap for c"},
    {"close_bitmap_java",  close_bitmap_java, METH_VARARGS,
        "Close the bitmap for java"},
    {"count_bits_py",  count_bits_py, METH_VARARGS,
        "Get the number of bit 1 in Python's bitmap"},
    {"count_bits_c",  count_bits_c, METH_VARARGS,
        "Get the number of bit 1 in C's bitmap"},
    {"count_bits_java",  count_bits_java, METH_VARARGS,
        "Get the number of bit 1 in Java's bitmap"},
    {"on_hit_py",  on_hit_py, METH_VARARGS,
        "on_hit_py(hit_id: int)"},
    {"on_hit_py_edge",  on_hit_py_edge, METH_VARARGS,
        "on_hit_py_edge(edge_id: int)"},
    {"open_bitmap_x",  open_bitmap_x, METH_VARARGS,
        "Open the bitmap of specified key"},
    {"clear_bitmap_x",  clear_bitmap_x, METH_VARARGS,
        "Clear the bitmap of specified key"},
    {"close_bitmap_x",  close_bitmap_x, METH_VARARGS,
        "Close the bitmap of specified key"},
    {"count_bits_x",  count_bits_x, METH_VARARGS,
        "Get the number of bit 1 in the bitmap of specified key"},
    {"copy_bitmap", copy_bitmap, METH_VARARGS,
        "Copy the bitmap from ori to dst"},
    {"merge_bitmap", merge_bitmap, METH_VARARGS,
        "Merge the bitmap from ori to dst"},
    {"count_aflpp_bytes", count_aflpp_bytes, METH_VARARGS,
        "Get the number of bytes in the bitmap of specified key"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

static struct PyModuleDef dcov_py = {
    PyModuleDef_HEAD_INIT,
    "dcov_py",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    DcovInfoMethods
};

PyMODINIT_FUNC
PyInit_dcov_py(void)
{
    return PyModule_Create(&dcov_py);
}
