
#include "PyObject.h"
#include "PyException.h"
#include "PyStr.h"
#include <iostream>
#include "PyType.h"
#include <sstream>

using namespace std;

ostream& operator << (ostream &os, PyObject &t) {
    return os << t.toString();
}

PyObject* PyObject::callMethod(string name, vector<PyObject*>* args) {

    PyObject* (PyObject::*mbr)(vector<PyObject*>*);

    if (dict.find(name) == dict.ednd()) {
        throw new PyException(PYILLEGALOPERATIONEXCEPTION,
                              "TypeError: '" +
                              getType()->toString() +
                              "' object has no attribute '" +
                              name +
                              "'");
    }

    mbr = dict[name];

    return (this->*mbf)(args);
}

PyObject* PyObject::__str__(vector<PyObject*>* args) {
    ostringstream msg;

    if (args->size() != 0) {
        msg << "TypeError: expected 0 arguments, got "
            << args->size();
        throw new PyException(PYWRONGARGCOUNTEXCEPTION, msg.str());
    }

    return new PyStr(toString());
}

PyObject* PyObject::__type__(vector<PyObject*>* args) {
    ostringstream msg;

    if (args->size() != 0) {
        msg << "TypeError: expected 0 arguments, got "
            << args->size();
        throw new PyException(PYWRONGARGCOUNTEXCEPTION, msg.str());
    }

    return (PyObject*)this->getType();
}

PyType* PyObject::getType() {
    return NULL;
}

string PyObject::toString() {
    return "PyObject()";
}

void PyObject::incRef() {
    refCount++;
}

void PyObject::decRef() {
    refCount--;
}

int PyObject::getRefCount() const {
    return refCount;
}
