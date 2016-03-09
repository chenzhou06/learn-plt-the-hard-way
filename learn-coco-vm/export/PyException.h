
#ifndef PYEXCEPTION_H_
#define PYEXCEPTION_H_

#include "PyObject.h"
class PyFrame;
#include <string>
using namespace std;

class PyException : public PyObject {
public:
    PyException(int exceptType, PyObject* val);
    PyException(int exceptType, string message);
    virtual ~PyException();
    int getExceptionType();
    void tracebackAppend(PyFrame* frame);
    string toString();
    PyType* getType();
    PyObject* getTraceBack();
    void printTraceBack();

protected:
    int exceptionType;
    PyObject* val;
    vector<PyFrame*> traceback;
    virtual PyObject* __excmatch__(vector<PyObject*>* args);
};

const int PYEXCEPTION = 1;
const int PYEMPTYSTACKEXCEPTION = 2;
const int PYPARSEEXCEPTION = 3;
const int PYILLEGALOPERATIONEXCEPTION = 4;
const int PYWRONGARGCOUNTEXCEPTION = 5;
const int PYSTOPITERATIONEXCEPTION = 6;
const int PYMATCHEXCEPTION = 7;

#endif
