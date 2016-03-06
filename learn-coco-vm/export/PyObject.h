
#ifndef PYOBJECT_H_
#define PYOBJECT_H_

#include <string>
#include <unordered_map>
#include <vector>
#include <iostream>

using namespace std;

class PyType;

class PyObject {
public:
    PyObject();
    virtual ~PyObject();
    virtual PyType* getType();
    virtual string toString();
    void decRef();
    void incRef();
    int getRefCount() const;    // TODO: Explain these three `ref` functions.

    PyObject* callMethod(string name, vector<PyObject*>* args);

protected:
    unordered_map<string,
                  PyObject* (PyObject::*)(vector<PyObject*>*)>
    dict;                       // TODO: Explain this.

    int refCount;

    virtual PyObject* __str__(vector<PyObject*>* args);
    virtual PyObject* __type__(vector<PyObject*>* args);
};

ostream& operator << (ostream& os, PyObject& t); // TODO: Explain this.

extern bool verbose;            // TODO: Explain `extern`.

#endif
