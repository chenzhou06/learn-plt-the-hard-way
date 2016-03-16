
#ifndef PYTYPE_H
#define PYTYPE_H

#include "PyCallable.h"
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

enum PyTypeId {
    PyTypeType,
    PyNoneType,
    PyBoolType,
    PyIntType,
    PyFloatType,
    PyStrType,
    PyFunctionType,
    PyBuiltInType,              // TODO: What's this?
    PyRangeTypeId,
    PyRangeIteratorType,
    PyListType,
    PyListIteratorType,
    PyFunListType,              // TODO:Why another list?
    PyFunListIteratorType,
    PyStrIteratorType,
    PyCodeType,
    PyTupleType,
    PyTupleIteratorType,
    PyCellType,
    PyExceptionTypeId
};

class pyType: public PyCallable {
public:
    PyType(string typeString, PyTypeId id);
    virtual ~PyType();
    string toString();
    PyType* getType();
    PyTypeId typeId();
    string callName();

protected:
    string typeString;
    PyTypeId index;

    virtual PyObject* __call__(vector<PyObject*>* args);
    virtual PyObject* __str__(vector<PyObject*>* args);
    virtual PyObject* __type__(vector<PyObject*>* args);
};

extern unordered_map<PyTypeId, PyType*, std::hash<int>> PyTypes;

#endif
