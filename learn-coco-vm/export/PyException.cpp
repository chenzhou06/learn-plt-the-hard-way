
#include "PyList.h"
#include "PyBool.h"
#include <unordered_map>
#include <sstream>

using namespace std;

struct names {

    static unordered_map<int, string> create_map() {
        unordered_map<int, string> m;
        m[PYEXCEPTION] = "Exception";
        m[PYEMPTYSTACKEXCEPTION] = "EmptyStackException";
        m[PYPARSEEXCEPTION] = "ParseException";
        m[PYILLEGALOPERATIONEXCEPTION] = "IllegalOperationException";
        m[PYWRONGARGCOUNTEXCEPTION] = "WrongArgCountExeption";
        m[PYSTOPITERATIONEXCEPTION] = "StopIterationException";
        m[PYMATCHEXCEPTION] = "MatchException";

        return m;
    }
};

static unordered_map<int, string> excnames = names::create_map();

PyException::PyException(int exception, PyObject* v):
    PyObject(), exceptionType(exception), val(v)
{
    dict["__excmatch__"] =
        (PyObject* (PyObject::*)(vector<PyObject*>*))
        (&PyException::__excmatch__);
}

PyException::PyException(int exception, string msg):
    PyObject(), exceptionType(exception), val(new PyStr(msg))
{
    dict["__excmatch__"] =
        (PyObject* (PyObject::*)(vector<PyObject*>*))
        (&PyException::__excmatch__);
}

PyException::~PyException() {
    try {
        delete val;
    } catch (...) {}
}

int PyException::getExceptionType() {
    return exceptionType;
}

string PyException::toString() {
    return val->toString();
}

PyType* PyException::getType() {
    return PyTypes[PyExceptionTypeId];
}

void PyException::printTraceBack() {
    for (int k=0; k<traceback.size(); k++) {
        cerr << "=========> At PC="
             << (traceback[k]->getPC()-1)
             << " in this function."
             << endl;
        cerr << traceback[k]->getCode().prettyString("", true);
    }
}

void PyException::tracebackAppend(PyFrame* frame) {
    traceback.push_back(frame);
}

PyObject* PyException::getTraceBack() {
    return new PyList((vector<PyObject*>*)&traceback);
}

PyObject* PyException::__excmatch__(vector<PyObject*>* args) {
    ostringstream msg;

    if (args->size() != 1) {
        msg << "TypeError: excepted 1 arguments, got "
            << args->size();
        throw new PyException(PYWRONGARGCOUNTEXCEPTION, msg.str());
    }

    PyObject* arg = (*args)[0];

    if (this->getType() == arg)
        return new PyBool(true);

    if (this->getType() != arg->getType()) {
        msg << "TypeError: Exception match type mismatch. Excepted Exception Object got "
            << arg->toString();
        throw new PyException(PYILLEGALOPERATIONEXCEPTION, msg.str());
    } // The official version of this code has not this pair of parenthesis.

    PyException* other = (PyException*) arg;

    return new PyBool(this->getExceptionType() == other->getExceptionType());
}
