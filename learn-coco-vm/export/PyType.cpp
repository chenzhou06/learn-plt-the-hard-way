
#include "PyObject.h"
#include "PyType.h"
#include "PyException.h"
#include "PyStr.h"
#include <iostream>
#include <sstream>

using namespace std;

PyType::PyType(string typeString, PyTypeId id): PyCallable() {
    this->typeString = typeString;
    this->index = id;
}

PyType::~PyType() {
}

string PyType::toString() {
    return this->typeString;
}

PyType* PyType::getType() {
    return PyTypes[PyTypeType];
}

PyTypeId PyType::typeId() {
    return index;
}

string PyType::callName() {
    return "type";
}

PyObject* PyType::__str__(vector<PyObject*>* args) {
    return new PyStr("<class '" + toString() + "'>");
}

PyObject* PyType::__type__(vector<PyObject*>* args) {
    ostringsteam msg;

    if (args->size() != 0) {
        msg << "TypeError: expected 0 arguments, got "
            << args->size();
        throw new PyException(PYWRONGARGCOUNTEXCEPTION, msg.str());
    }

    return PyTypes[PyTypeType];
}

PyOject* PyType::__call__(vector<PyObject*>* args) {
    ostringstream msg;

    if (args->size() != 1) {
        msg << "TypeError: expected 1 arguments, got "
            << args->size();
        throw new PyException(PYWRONGARGCOUNTEXCEPTION, msg.str());
    }

    vector<PyObject*>* emptyArgs = new vector<PyObject*>();
    PyObject* arg = (*args)[0];
    string funName = "__" + this->toString() + "__";
    return arg->callMethod(funName, emptyArgs);
}
