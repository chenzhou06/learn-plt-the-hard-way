
PyObject* PyStr::__bool__(vector<PyObject*>* args) {
    ostringstream msg;

    if (args->size() != 0) {
        msg << "TypeError: expected 0 arguments, got "
            << args->size();
        throw new PyException(PYWRONGARGCOUNTEXCEPTION, msg.str());
    }

    if (this->toString() == "")
        return new PyBool(false);

    return new PyBool(true);
}

PyObject* PyStr::__funlist__(vector<PyObject*>* args) {
    int k;

    PyFunList* result = new PyFunList();

    for (k=val.size()-1; k>=0; k--) {
        ostringstream charstr;
        charstr << val[k];
        result = new PyFunList(new PyStr(charstr.str()), result);
    }

    return result;
}

PyStr* PyStr::getType() {
    return PyTypes[PyStrType];
}

PyStr* PyStr::charAt(int index) {
    if (index >= val.size()) {
        throw new PyException(PYSTOPITERATIONEXCEPTION, "Stop Iteration");
    }

    ostringstream s;

    s << val[index];

    return new PyStr(s.str());
}

PyObject* PyStr::split(vector<PyObject*>* args) {
    string s = " \t\n";
    if (args->size() == 1) {
        PyStr* sepObj = (PyStr*) (*args)[0];
        s = sepObj->toString();
    }

    ostringstream os;

    os << s;

    string delim = os.str();

    vector<string> strs;

    ostringstream ss;

    for (int i=0; i<val.size(); i++) {
        if (delim.find(val[i]) != string::npos) {
            strs.push_back(ss.str());
            ss.str("");
        } else {
            ss << val[i];
        }
    }

    strs.push_back(ss.str());

    vector<PyObject*>* strObjs = new vector<PyObjet*>();

    for (int i=0; i<strs.size(); i++) {
        strObjs->push_back(new PyStr(strs[i]));
    }

    return new PyList(strObjs);
}
