
#ifndef PYBOOL_H
#define PYBOOL_H

#include "PyType.h"
#include "PyCallable.h"
#include <string>
using namespace std;

class PyBool : public PyObject {
public:
    PyBool();
    PyBool(bool val);
    PyBool(const PyBool& orig);
    virtual ~PyBool();

    PyType* getType();
    string toString();
    bool getVal();

protected:
    bool val;
    virtual PyObject* __float__(vector<PyObject*>* args);
    virtual PyObject* __int__(vector<PyObject*>* args);
    virtual PyObject* __bool__(vector<PyObject*>* args);
    virtual PyObject* __eq__(vector<PyObject*>* args);
};

#endif
