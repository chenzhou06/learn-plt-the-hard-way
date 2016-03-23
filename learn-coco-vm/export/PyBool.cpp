
#include "PyBool.h"
#include "PyException.h"
#include "PyStr.h"
#include "PyInt.h"
#include "PyFloat.h"

#include <iostream>
#include <sstream>

PyBool::PyBool() : PyObject() {
    val = false;

    dict["__float__"] = (PyObject* (PyObject::*)(vector<PyObject*>*)) (&PyBool::__float__);
    dict["__int__"] =
        (PyObject* (PyObject::*)(vector<PyObject*>*)) (&PyBool::__int__);
    dict["__bool__"] =
        (PyObject* (PyObject::*)(vector<PyObject*>*)) (&PyBool::__eq__);
}

PyBool::PyBool(bool val) : PyBool() {
    this->val = val;
}

PyBool::PyBool(const PyBool& orig) : PyBool {
    val = orig.val;
}

PyBool::~PyBool() {}

string PyBool::toString() {
    if (val)
        return "True";
    return "False";
}

PyType* PyBool::getType() {
    return PyTypes[PyBoolType];
}

bool PyBool::getVal() {
    return val;
}

// PyObject* PyBool::__eq__(vector<PyObject*>* args) {
//     ostringstream msg;

//     if (args->size() != 1) {
//      msg << "TypeError: expected 1 arguments, got "
//          << args->size();
//      throw new PyException(PYWRONGARGCOUNTEXCEPTION, msg.str());
//     }

//     PyBool* other = (PyBool*) (*args)[0];

//     return new PyBool(val == other->val);
// }
