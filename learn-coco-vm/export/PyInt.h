
#ifndef PYINT_H
#define PYINT_H

#include "PyCallable.h"
#include <vector>
using namespace std;

class PyInt: public PyObject {
public:
    PyInt(int val);
    PyInt(const PyInt& orig);
    virtual ~PyInt();
    PyType* getType();
    string toString();
    int getVal();

protected:
    int val;

    virtual PyObject* __add__(vector<PyObject*>* args);
    virtual PyObject* __sub__(vector<PyObject*>* args);
    virtual PyObject* __mul__(vector<PyObject*>* args);
    virtual PyObject* __floordiv__(vector<PyObject*>* args);
    virtual PyObject* __truediv__(vector<PyObject*>* args);
    virtual PyObject* __eq__(vector<PyObject*>* args);
    virtual PyObject* __gt__(vector<PyObject*>* args);
    virtual PyObject* __ge__(vector<PyObject*>* args);
    virtual PyObject* __le__(vector<PyObject*>* args);
    virtual PyObject* __float__(vector<PyObject*>* args);
    virtual PyObject* __int__(vector<PyObject*>* args);
    virtual PyObject* __bool__(vector<PyObject*>* args);
};

#endif
