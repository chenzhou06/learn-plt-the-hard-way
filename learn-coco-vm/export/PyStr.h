
#ifndef PYSTR_H
#define PYSTR_H

class PyObject;                 // TODO: ?

#include "PyCallable.h"
#include <string>
using namespace std;

class PyStr : public PyObject {
public:
    PyStr(string s);
    PyStr(const PyStr& orig);
    virtual ~PyStr();
    PyType* getType();
    string toString();
    PyStr* charAt(int index);

protected:
    string val;

    PyObject* __add__(vector<PyObject*>* args);
    PyObject* __str__(vector<PyObject*>* args);
    PyObject* __float__(vector<PyObject*>* args);
    PyObject* __int__(vector<PyObject*>* args);
    PyObject* __bool__(vector<PyObject*>* args);
    PyObject* __funlist__(vector<PyObject*>* args); // TODO: ?
    PyObject* __eq__(vector<PyObject*>* args);
    PyObject* split(vector<PyObject*>* args);
};

#endif
