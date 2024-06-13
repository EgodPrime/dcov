#define PY_SSIZE_T_CLEAN    // programmers love obscure statements
#include <Python.h>
#include <algorithm>
#include "pyptr.h"
#include "dcov.h"
#include "dcov_trace.h"
#include "MurmurHash3.h"

#ifndef PYPY_VERSION
    #include "opcode.h"
#endif

unsigned int hash_line(const char* filename, unsigned int lineno){
    unsigned int hash;
    char str[256] {'\0'};
    strcat(str, filename);
    char bb_idx_str[16] = {0};
    sprintf(bb_idx_str, "%d",lineno);
    strcat(str, bb_idx_str);
    MurmurHash3_x86_32(str, strlen(str), 0, &hash);
    return hash % bitmap_size;
}

/**
 * Tracks code coverage.
 */
class Probe {
    PyPtr<> _sci;
    PyPtr<> _filename;
    PyPtr<> _lineno_or_branch;
    unsigned int line_idx;
    bool _signalled;
    bool _removed;
    int _d_miss_count;
    int _u_miss_count;
    int _no_signal_count;
    int _d_miss_threshold;
    std::byte* _code;

public:
    Probe(PyObject* sci, PyObject* filename, PyObject* lineno_or_branch, PyObject* d_miss_threshold):
        _sci(PyPtr<>::borrowed(sci)), _filename(PyPtr<>::borrowed(filename)),
        _lineno_or_branch(PyPtr<>::borrowed(lineno_or_branch)),
        _signalled(false), _removed(false),
        _d_miss_count(-1), _u_miss_count(0), _no_signal_count(0),
        _d_miss_threshold(PyLong_AsLong(d_miss_threshold)), _code(nullptr) {
            const char* filename_c = PyUnicode_AsUTF8(filename);
            unsigned int lineno = PyLong_AsLong(lineno_or_branch);
            line_idx = hash_line(filename_c, lineno);
                    }


    static PyObject*
    newCapsule(Probe* p) {
        return PyCapsule_New(p, NULL,
                             [](PyObject* cap) {
                                 delete (Probe*)PyCapsule_GetPointer(cap, NULL);
                             });
    }


    PyObject* signal() {
        // _d_miss_threshold == -1 means de-instrument (disable) this block,
        //      but don't de-instrument Python;
        // _d_miss_threshold == -2 means don't de-instrument either
        if (!_signalled || (_code == nullptr && _d_miss_threshold < -1)) {
            _signalled = true;
            on_bb_hit_python(line_idx);
        }
        Py_RETURN_NONE;
    }


    PyObject* no_signal() {
        ++_no_signal_count;
        Py_RETURN_NONE;
    }


    PyObject* mark_removed() {
        _removed = true;
        Py_RETURN_NONE;
    }

    PyObject* was_removed() {
        if (_removed) {
            Py_RETURN_TRUE;
        }
        Py_RETURN_FALSE;
    }

    PyObject* get_stats() {
        PyPtr<> d_miss_count = PyLong_FromLong(std::max(_d_miss_count, 0));
        PyPtr<> u_miss_count = PyLong_FromLong(_u_miss_count);
        PyPtr<> total_count = PyLong_FromLong(1 + _d_miss_count + _u_miss_count + _no_signal_count);
        return PyTuple_Pack(5, (PyObject*)_filename, (PyObject*)_lineno_or_branch,
                            (PyObject*)d_miss_count, (PyObject*)u_miss_count,
                            (PyObject*)total_count);
    }

    PyObject* set_immediate(PyObject* code_bytes, PyObject* offset) {
#ifdef PYPY_VERSION
        PyErr_SetString(PyExc_Exception, "Error: set_immediate does not work with PyPy");
        return NULL;
#endif

        _code = reinterpret_cast<std::byte*>(PyBytes_AsString(code_bytes));
        if (_code == nullptr) {
            return NULL;
        }
        _code += PyLong_AsLong(offset);

        Py_RETURN_NONE;
    }
};


PyObject*
probe_new(PyObject* self, PyObject* const* args, Py_ssize_t nargs) {
    if (nargs < 4) {
        PyErr_SetString(PyExc_Exception, "Missing argument(s)");
        return NULL;
    }

    return Probe::newCapsule(new Probe(args[0], args[1], args[2], args[3]));
}


PyObject*
probe_set_immediate(PyObject* self, PyObject* const* args, Py_ssize_t nargs) {
    if (nargs < 3) {
        PyErr_SetString(PyExc_Exception, "Missing argument(s)");
        return NULL;
    }

    return static_cast<Probe*>(PyCapsule_GetPointer(args[0], NULL))->set_immediate(args[1], args[2]);
}

#define METHOD_WRAPPER(method) \
    static PyObject*\
    probe_##method(PyObject* self, PyObject* const* args, Py_ssize_t nargs) {\
        if (nargs < 1) {\
            PyErr_SetString(PyExc_Exception, "Missing argument");\
            return NULL;\
        }\
    \
        return static_cast<Probe*>(PyCapsule_GetPointer(args[0], NULL))->method();\
    }

METHOD_WRAPPER(signal);
METHOD_WRAPPER(no_signal);
METHOD_WRAPPER(mark_removed);
METHOD_WRAPPER(was_removed);
METHOD_WRAPPER(get_stats);


static PyMethodDef methods[] = {
    {"new", (PyCFunction)probe_new, METH_FASTCALL, "creates a new probe"},
    {"set_immediate", (PyCFunction)probe_set_immediate, METH_FASTCALL, "sets up for immediate removal"},
    {"signal", (PyCFunction)probe_signal, METH_FASTCALL, "signals this probe's line or branch was reached"},
    {"no_signal", (PyCFunction)probe_no_signal, METH_FASTCALL, "like signal, but called only after this probe is removed"},
    {"mark_removed", (PyCFunction)probe_mark_removed, METH_FASTCALL, "marks a probe removed (de-instrumented)"},
    {"was_removed", (PyCFunction)probe_was_removed, METH_FASTCALL, "returns whether probe was removed"},
    {"get_stats", (PyCFunction)probe_get_stats, METH_FASTCALL, "returns probe stats"},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef probe_module = {
    PyModuleDef_HEAD_INIT,
    "probe",
    NULL, // no documentation
    -1,
    methods,
    NULL,
    NULL,
    NULL,
    NULL
};


PyMODINIT_FUNC
PyInit_probe() {
    PyObject* m = PyModule_Create(&probe_module);
    if (m == nullptr) {
        return nullptr;
    }

    return m;
}

