#include "PyStack.h"
#include "PyScanner.h"
#include "PyParser.h"
#include "PyCode.h"
#include "PyObject.h"           // Oh, maybe I shall start here.
#include "PyInt.h"
#include "PyType.h"
#include "PyFunction.h"
#include "PyBuiltInPrint.h"
#include "PyBuiltInFPrint.h"
#include "PyBuiltInTPrint.h"
#include "PyException.h"        // Include once.
#include "PyExceptionType.h"
#include "PyBuiltInInput.h"
#include "PyStr.h"
#include "PyFloat.h"
#include "PyBool.h"
#include "PyRange.h"
#include "PyRangeType.h"
#include "PyRangeIterator.h"
#include "PyBuiltInIter.h"
#include "PyBuiltInLen.h"
#include "PyBuiltInConcat.h"
#include "PyFrame.h"
#include "PyException.h"        // Yes, include twice.
#include <iostream>
#include <fstream>
#include <unordered_map>
#include <csignal>
#include <stdlib.h>

using namespace std;

vector<PyFrame*> callStack;

void pushFrame(PyFrame* frame) {
  callStack.push_back(frame);
  if (callStack.size() == 1000) {
    throw new PyException(PYILLEGALOPERATIONEXCEPTION, "Call Stack Overflow.");
  }
}

void popFrame() {
  callStack.pop_back();
}

void sigHandler(int signum) {
  cerr <<"\n\n";
  cerr << "**********************************************************" << endl;
  cerr << "      An Uncaught Exception Occurred" << endl;
  cerr << "**********************************************************" << endl;
  cerr << "Signal: ";
  switch (signum) {
  case SIGABRT:
    cerr << "Program Execution Aborted" << endl;
    break;
  case SIGFPE:
    cerr << "Arithmetic or Overflow Error" << endl;
    break;
  case SIGILL:
    cerr << "Illegal Instruction in Virtual Machine" << endl;
    break;
  case SIGINT:
    cerr << "Execution Interrupted" << endl;
    break;
  case SIGSEGV:
    cerr << "Illegal Memory Access" << endl;
    break;
  case SIGTERM:
    cerr << "Termination Requested" << endl;
    break;
  }

  cerr << "----------------------------------------------------------" << endl;
  cerr << "                  The Exception's Traceback" << endl;

  // Go through the stack to print error information.
  for (int k=callStack.size()-1; k>=0; k--) {
    cerr << "==========> At PC="
	 << (callStack[k]->getPC()-1)
	 << " in this function."
	 << endl;
    cerr << callStack[k]->getCode().prettyString("",true);
    exit(0);
  }
}

unordered_map<PyTypeId, PyType*, std::hash<int> > PyTypes;
bool verbose = false;

unordered_map<PyTypeId, PyType*, std::hash<int> > initTypes() {

    unordered_map<PyTypeId, PyType*, std::hash<int> > types;

    PyType* typeType = new PyType("type", PyTypeType);
    types[PyTypeType] = typeType;

    PyType* noneType = new PyType("NoneType", PyNoneType);
    types[PyNoneType] = noneType;

    PyType* boolType = new PyType("bool", PyBoolType);
    types[PyBoolType] = boolType;

    PyType* intType = new PyType("int", PyIntType);
    types[PyIntType] = intType;

    PyType* floatType = new PyType("float", PyFloatType);
    types[PyFloatType] = floatType;

    PyType* strType = new PyType("str", PyStrType);
    types[PyStrType] = strType;

    PyType* functionType = new PyType("function", PyFunctionType);
    types[PyFunctionType] = functionType;

    PyType* builtinType = new PyType("builtin_function_or_method", PyBuiltInType);
    types[PyBuiltInType] = builtinType;

    PyType* rangeType = new PyRangeType("range", PyRangeTypeId);
    types[PyRangeTypeId] = rangeType;

    PyType* exceptionType = new PyExceptionType("Exception", PyExceptionTypeId);
    types[PyExceptionTypeId] = exceptionType;

    PyType* rangeIteratorType = new PyType("range_iterator", PyRangeIteratorType);
    types[PyRangeIteratorType] = rangeIteratorType;

    PyType* listType = new PyType("list", PyListType);
    types[PyListType] = listType;

    PyType* funListType = new PyType("funlist", PyFunListType);
    types[PyFunListType] = funListType;

    PyType* tupleType = new PyType("tuple", PyTupleType);
    types[PyTupleType] = tupleType;

    PyType* listIteratorType = new PyType("list_iterator", PyListIteratorType);
    types[PyListIteratorType] = listIteratorType;

    PyType* listIteratorType = new PyType("funlist_iterator", PyFunListIteratorType);
    types[PyFunListIteratorType] = listIteratorType;

    PyType* tupleIteratorType = new PyType("tuple_iterator", PyTupleIteratorType);
    types[PyTupleIteratorType] = tupleIteratorType;

    PyType* strIteratorType = new PyType("str_iterator", PyStrIteratorType);
    types[PyStrIteratorType] = strIteratorType;

    PyType* codeType = new PyType("code", PyCodeType);
    types[PyCodeType] = codeType;

    PyType* cellType = new PyType("cell", PyCellType);
    types[PyCellType] = cellType;

    return types;
}

int main(int argc, char* argv[]) {
    char* filename;

    signal(SIGABRT, sigHandler);
    signal(SIGFPE, sigHandler);
    signal(SIGILL, sigHandler);
    signal(SIGINT, sigHandler);
    signal(SIGSEGV, sigHandler);
    signal(SIGTERM, sigHandler);

if (argc != 2 && argc !=3) {
   cerr << "Invoke as : coco [-v] filename" << endl; // Expect 2-3 arguments.
   return 0;
}

PyTypes = initTypes();                 // Trigger type initializer.

if (argc == 2)
   filename = argv[1];
else {
    filename = argv[2];          // The last argument is the filename.
    verbose = true;              // Verbose switch on.
}

try {
    PyParser* parser = new PyParser(filename);

    vector<PyCode*>* code = parser->parse();

    string indent = "";           // TODO: Why?

    for (int i = 0; i < code->size(); i++) {
	cerr << (*code)[i]->prettyString(indent, false) << endl;
	cerr << endl;
    }

    unordered_map<string, PyObject*> globals; // Global environment is a hashmap.

    globals["print"] = new PyBuiltInPrint();
    globals["fprint"] = new PyBuiltInFPrint();
    globals["tprint"] = new PyBuiltInTPrint();
    globals["input"] = new PyBuiltInInput();
    globals["iter"] = PyTypes[PyIterType];
    globals["float"] =  PyTypes[PyFloatType];
    globals["int"] =  PyTypes[PyIntType];
    globals["str"] =  PyTypes[PyStrType];
    globals["funlist"] = PyTypes[PyFunListType];
    globals["list"] = PyTypes[PyListType];
    globals["type"] = PyTypes[PyTypeType];
    globals["bool"] = PyTypes[BoolType];
    globals["range"] = PyTypes[PyRangeTypeId];
    globals["Exception"] = PyTypes[PyExceptionTypeId];
    globals["len"] = new PyBuiltInLen();
    globals["concat"] = new PyBuiltInConcat();

    bool foundMain = false;

    for (int i = 0; i < code->size(); i++) {
	if ((*code)[i]->getName() == "main")
	    foundMain = true;

	globals[(*code)[i]->getName()] = new PyFunction(*((*code)[i]),
							globals,NULL);

	if (!foundMain) {
	    cerr << "Error: No main() function found. A main() is required in CoCo VM programs."
		 << endl;
	    return 0;
	}

	vector<PyObject*>* args = new vector<PyObject*>();
	PyObject* result = globals["main"]->callMethod("__call__", args);
    } catch (PyException* ex) {
	cerr << "\n\n";
	cerr << "*********************************************************" << endl;
	cerr << "            An Uncaught Exception Occurred" << endl;
	cerr << "*********************************************************" << endl;
	cerr << ex->toString() << endl;
	cerr << "---------------------------------------------------------" << endl;
	cerr << "              The Exception's Traceback" << endl;
	cerr << "---------------------------------------------------------" << endl;
	ex->printTraceBack();
	cerr << "*********************************************************" << endl;
	cerr << "            An Uncaught Exception Occurred (See Above) " << endl;
	cerr << "*********************************************************" << endl;
	cerr << ex->toString() << endl;
	cerr << "*********************************************************" << endl;
    }

    return 0;
 }
