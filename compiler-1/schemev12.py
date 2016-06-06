from enum import Enum


# Model
class ObjectType(Enum):
    FIXNUM = 1
    BOOLEAN = 2
    CHARACTER = 3
    STRING = 4
    THE_EMPTY_LIST = 5
    PAIR = 6
    SYMBOL = 7
    PRIMITIVE_PROC = 8


class _ObjectValue:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class SCMObject:
    def __init__(self, type, data):
        "type: ObjectType. data: _ObjectValue"
        self.type = type
        self.data = _ObjectValue(data)

    def __eq__(self, other):
        return self.data.value == other.data.value

    def __repr__(self):
        return "<Type: {}, Value: {}>".format(self.type, self.data)


# Global
SCMTheEmptyList = SCMObject(ObjectType.THE_EMPTY_LIST, None)
SCMTrue = SCMObject(ObjectType.BOOLEAN, True)
SCMFalse = SCMObject(ObjectType.BOOLEAN, False)
SCMSymbolTable = SCMTheEmptyList  # TODO: default dict
SCMTheEmptyEnvironment = SCMTheEmptyList


def is_the_empty_list(obj):
    return obj is SCMTheEmptyList


def is_boolean(obj):
    return obj.type == ObjectType.BOOLEAN


def is_false(obj):
    return obj is SCMFalse


def is_true(obj):
    return obj is SCMTrue


def SCMCons(car, cdr):
    return SCMObject(ObjectType.PAIR, (car, cdr))


def is_symbol(obj):
    return obj.type == ObjectType.SYMBOL


def make_fixnum(value):
    return SCMObject(ObjectType.FIXNUM, value)


def is_fixnum(obj):
    return obj.type == ObjectType.FIXNUM


def make_character(value):
    return SCMObject(ObjectType.CHARACTER, value)


def is_character(obj):
    return obj.type == ObjectType.CHARACTER


def make_string(value):
    return SCMObject(ObjectType.STRING, value)


def is_string(obj):
    return obj.type == ObjectType.STRING


def is_pair(obj):
    return obj.type == ObjectType.PAIR


def SCMCar(obj):
    car, _ = obj.data.value
    return car


def SCMSetCar(obj, car):
    _, cdr = obj.data.value
    obj.data.value = (car, cdr)
    return


def SCMCdr(obj):
    _, cdr = obj.data.value
    return cdr


def make_primitive_proc(fn):
    return SCMObject(ObjectType.PRIMITIVE_PROC, fn)


def make_symbol(value):
    global SCMSymbolTable
    element = SCMSymbolTable
    while not is_the_empty_list(element):
        if SCMCar(element).data.value == value:
            return SCMCar(element)
        else:
            element = SCMCdr(element)

    obj = SCMObject(ObjectType.SYMBOL, value)
    SCMSymbolTable = SCMCons(obj, SCMSymbolTable)
    return obj


def is_primitive_proc(obj):
    return obj.type == ObjectType.PRIMITIVE_PROC


# Primitive Procedures
def add_proc(arguments):
    result = 0
    while not is_the_empty_list(arguments):
        result += SCMCar(arguments).data.value
        arguments = SCMCdr(arguments)
    return make_fixnum(result)


def is_null_proc(arguments):
    return is_the_empty_list(SCMCar(arguments)) is True


def is_boolean_proc(arguments):
    return is_boolean(SCMCar(arguments)) is True


def is_symbol_proc(arguments):
    return is_symbol(SCMCar(arguments)) is True


def is_integer_proc(arguments):
    return is_fixnum(SCMCar(arguments)) is True


def is_char_proc(arguments):
    return is_character(SCMCar(arguments)) is True


def is_string_proc(arguments):
    return is_string(SCMCar(arguments)) is True


def is_pair_proc(arguments):
    return is_pair(SCMCar(arguments)) is True


# Inits
SCMQuoteSymbol = make_symbol("quote")
SCMDefineSymbol = make_symbol("define")
SCMSetSymbol = make_symbol("set!")
SCMOkSymbol = make_symbol("ok")
SCMIfSymbol = make_symbol("if")


def SCMSetCdr(obj, cdr):
    car, _ = obj.data.value
    obj.data.value = (car, cdr)
    return


def enclosing_environment(env):
    return SCMCdr(env)


def first_frame(env):
    return SCMCar(env)


def make_frame(variables, values):
    return SCMCons(variables, values)


def frame_variables(frame):
    return SCMCar(frame)


def frame_values(frame):
    return SCMCdr(frame)


def add_binding_to_frame(var, val, frame):
    SCMSetCar(frame, SCMCons(var, SCMCar(frame)))
    SCMSetCdr(frame, SCMCons(val, SCMCdr(frame)))


def extend_environment(variables, vals, base_env):
    return SCMCons(make_frame(variables, vals), base_env)


def lookup_variable_value(var, env):
    while not is_the_empty_list(env):
        frame = first_frame(env)
        variables = frame_variables(frame)
        values = frame_values(frame)
        while not is_the_empty_list(variables):
            if var == SCMCar(variables):
                return SCMCar(values)
            else:
                variables = SCMCdr(variables)
                values = SCMCdr(values)
        env = enclosing_environment(env)
    raise Exception("Unbound variable '{}'".format(var))


def set_variable_value(var, val, env):
    while not is_the_empty_list(env):
        frame = first_frame(env)
        variables = frame_variables(frame)
        values = frame_values(frame)
        while not is_the_empty_list(variables):
            if var == SCMCar(variables):
                SCMSetCar(values, val)
                return
            else:
                variables = SCMCdr(variables)
                values = SCMCdr(values)
        env = enclosing_environment(env)
    raise Exception("Unbound variable '{}'".format(var))


def define_variable(var, val, env):
    frame = first_frame(env)
    variables = frame_variables(frame)
    values = frame_values(frame)
    while not is_the_empty_list(variables):
        if var == SCMCar(variables):
            SCMSetCar(values, val)
            return
        else:
            variables = SCMCdr(variables)
            values = SCMCdr(values)
    add_binding_to_frame(var, val, frame)


def setup_environment():
    return extend_environment(SCMTheEmptyList,
                              SCMTheEmptyList,
                              SCMTheEmptyEnvironment)

SCMTheGlobalEnvironment = setup_environment()
# inits
define_variable(make_symbol("+"),
                make_primitive_proc(add_proc),
                SCMTheGlobalEnvironment)


# Read
def is_delimiter(c):
    return c.isspace() or c == "(" or c == ")" or \
        c == "\"" or c == ";" or c == ""


def is_initial(c):
    return c.isalpha() or c == "*" or c == "/" or \
        c == "<" or c == "=" or c == "?" or c == "!"


def peek(fhandle):
    pos = fhandle.tell()
    char = fhandle.read(1)
    fhandle.seek(pos)
    return char


def eat_whitespace(fhandle):
    while True:
        pos = fhandle.tell()
        char = fhandle.read(1)
        if char == "":
            break
        elif char.isspace():
            continue
        elif char == ";":
            while True:
                pos = fhandle.tell()
                char = fhandle.read(1)
                if char == "" or char == "\n":
                    break
        else:
            break
    return char, pos


def read_digit(fhandle, leading):
    "Read digits, return corresponding integer."
    digits = [leading]
    while True:
        c = peek(fhandle)
        if c.isdigit():
            digits.append(fhandle.read(1))
            continue
        elif is_delimiter(c):
            return int("".join(digits))
        else:
            raise Exception("Number not followed by delimiter")


def read_bool(fhandle):
    "Return a boolean or just the character."
    char = fhandle.read(1)
    if char == "t":
        return SCMTrue
    elif char == "f":
        return SCMFalse
    else:
        return char


def eat_expected_string(fhandle, expect):
    e = [fhandle.read(1) for _ in expect]
    real = "".join(e)
    if real == expect:
        return True
    else:
        raise Exception("Unexpected characters '{}'".format(real))


def peek_expected_delimiter(fhandle):
    if not is_delimiter(peek(fhandle)):
        raise Exception("Character not followed by delimiter.")
    else:
        return


def read_character(fhandle, leading):
    if leading == "\\":
        char = fhandle.read(1)
        char2 = None
        if char == "":
            raise Exception("Incomplete character literal.")
        elif char == "s":
            char2 = fhandle.read(1)
            if char2 == "p":
                eat_expected_string(fhandle, "ace")
                peek_expected_delimiter(fhandle)
                return make_character(" ")
        elif char == "n":
            char2 = fhandle.read(1)
            if char2 == "e":
                eat_expected_string(fhandle, "wline")
                peek_expected_delimiter(fhandle)
                return make_character("\n")
        elif char2 and is_delimiter(char2):
            return make_character(char)
        else:
            peek_expected_delimiter(fhandle)
            return make_character(char)
    else:
        raise Exception("Unknown boolean or character literal.")


def read_string(fhandle):
    s = ""
    while True:
        char = fhandle.read(1)
        if char != "\"":
            if char == "\\":
                char_escaped = fhandle.read(1)
                if char_escaped == "n":
                    char = "\n"
            elif char == "":    # EOF
                raise Exception("non-terminated string literal")
            else:
                s += char
        else:
            break
    return s


def read_pair(fhandle):
    char, pos = eat_whitespace(fhandle)
    if char == ")":
        return SCMTheEmptyList
    fhandle.seek(pos)           # Ungetc: reset file pointer
    car_obj = SCMRead(fhandle)
    char, pos = eat_whitespace(fhandle)
    if char == ".":
        c = peek(fhandle)
        if not is_delimiter(c):
            raise Exception("dot not followed by delimiter")

        cdr_obj = SCMRead(fhandle)
        char, _ = eat_whitespace(fhandle)
        if char != ")":
            raise Exception("where was the trailing right paren?")
        return SCMCons(car_obj, cdr_obj)
    else:
        fhandle.seek(pos)       # Reset file pointer
        cdr_obj = read_pair(fhandle)
        return SCMCons(car_obj, cdr_obj)


def SCMRead(fhandle):
    "Return an object from a file handle."
    buffer = ""
    char, _ = eat_whitespace(fhandle)

    if char == "#":
        candidate = read_bool(fhandle)
        if isinstance(candidate, str):
            # Character
            return read_character(fhandle, candidate)
        else:
            # Boolean
            return candidate
    # Digit
    elif char.isdigit():
        value = read_digit(fhandle, char)
        return make_fixnum(value)
    elif char == "-" and peek(fhandle).isdigit():
        char2 = fhandle.read(1)
        value = read_digit(fhandle, char2)
        return make_fixnum(-1*value)
    # Symbol
    elif is_initial(char) or ((char == "+" or char == "-") and
                              is_delimiter(peek(fhandle))):
        while (is_initial(char) or char.isdigit() or
               char == "+" or char == "-"):
            buffer += char
            pos = fhandle.tell()
            char = fhandle.read(1)

        if is_delimiter(char):
            fhandle.seek(pos)
            return make_symbol(buffer)
        else:
            e = "Symbol not followed by delimiter. Found '{}'.".format(char)
            raise Exception(e)
    # String
    elif char == "\"":
        return make_string(read_string(fhandle))
    # Empty list
    elif char == "(":
        return read_pair(fhandle)
    # Quoted expression
    elif char == "\'":
        return SCMCons(SCMQuoteSymbol,
                       SCMCons(SCMRead(fhandle), SCMTheEmptyList))
    else:
        raise Exception("Unexpected character '{}'".format(char))


# Evaluate
def is_self_evaluating(exp):
    return (is_boolean(exp) or
            is_fixnum(exp) or
            is_character(exp) or
            is_string(exp))


def is_variable(exp):
    return is_symbol(exp)


def is_tagged_list(exp, tag):
    if is_pair(exp):
        the_car = SCMCar(exp)
        return is_symbol(the_car) and the_car == tag
    else:
        return False


def is_quoted(exp):
    return is_tagged_list(exp, SCMQuoteSymbol)


def text_of_quotation(exp):
    return SCMCar(SCMCdr(exp))


def is_assignment(exp):
    return is_tagged_list(exp, SCMSetSymbol)


def assignment_variable(exp):
    return SCMCar(SCMCdr(exp))


def assignment_value(exp):
    return SCMCar(SCMCdr(SCMCdr(exp)))


def is_definition(exp):
    return is_tagged_list(exp, SCMDefineSymbol)


def definition_variable(exp):
    return SCMCar(SCMCdr(exp))


def definition_value(exp):
    return SCMCar(SCMCdr(SCMCdr(exp)))


def is_if(exp):
    return is_tagged_list(exp, SCMIfSymbol)


def if_predicate(exp):
    return SCMCar(SCMCdr(exp))


def if_consequent(exp):
    return SCMCar(SCMCdr(SCMCdr(exp)))


def if_alternative(exp):
    if is_the_empty_list(SCMCdr(SCMCdr(SCMCdr(exp)))):
        return SCMFalse
    else:
        return SCMCar(SCMCdr(SCMCdr(SCMCdr(exp))))


def is_application(exp):
    return is_pair(exp)


def operator(exp):
    return SCMCar(exp)


def operands(exp):
    return SCMCdr(exp)


def is_no_operands(ops):
    return is_the_empty_list(ops)


def first_operand(ops):
    return SCMCar(ops)


def rest_operands(ops):
    return SCMCdr(ops)


def eval_assignment(exp, env):
    set_variable_value(assignment_variable(exp),
                       SCMEval(assignment_value(exp), env),
                       env)
    return SCMOkSymbol


def eval_definition(exp, env):
    define_variable(definition_variable(exp),
                    SCMEval(definition_value(exp), env),
                    env)
    return SCMOkSymbol


def SCMEval(exp, env):
    if is_self_evaluating(exp):
        return exp
    elif is_variable(exp):
        return lookup_variable_value(exp, env)
    elif is_quoted(exp):
        return text_of_quotation(exp)
    elif is_assignment(exp):
        return eval_assignment(exp, env)
    elif is_definition(exp):
        return eval_definition(exp, env)
    elif is_if(exp):
        exp = if_consequent(exp) if is_true(SCMEval(if_predicate(exp), env)) \
              else if_alternative(exp)
        return SCMEval(exp, env)     # TODO: Tailcall
    elif is_application(exp):
        procedure = SCMEval(operator(exp), env)
        arguments = list_of_values(operands(exp), env)
        return procedure.data.value(arguments)
    else:
        raise Exception("Cannot eval unknown expression type")


def list_of_values(exps, env):
    "Eval operands for application."
    if is_no_operands(exps):
        return SCMTheEmptyList
    else:
        return SCMCons(SCMEval(first_operand(exps), env),
                       list_of_values(rest_operands(exps), env))


def write_pair(obj):
    car = SCMCar(obj)
    cdr = SCMCdr(obj)

    SCMWrite(car)
    if cdr.type == ObjectType.PAIR:
        print(" ", end="")
        write_pair(cdr)
    elif cdr.type == ObjectType.THE_EMPTY_LIST:
        return
    else:
        print(" . ", end="")
        SCMWrite(cdr)
        return


# Print
def SCMWrite(obj):
    if obj.type == ObjectType.FIXNUM:
        print(obj.data.value, end="")
    elif obj.type == ObjectType.BOOLEAN:
        print(obj.data.value, end="")
    elif obj.type == ObjectType.THE_EMPTY_LIST:
        print("()", end="")
    elif obj.type == ObjectType.CHARACTER:
        c = obj.data.value
        fmt = "#\\{}"
        if c == "\n":
            print(fmt.format("newline"), end="")
        elif c == " ":
            print(fmt.format("space"), end="")
        else:
            print(fmt.format(c), end="")
    elif obj.type == ObjectType.STRING:
        s = obj.data.value
        fmt = "\"{}\""
        s = s.replace("\n", "\\n")
        s = s.replace("\\", "\\\\")
        s = s.replace("\"", "\\\"")
        print(fmt.format(s), end="")
    elif obj.type == ObjectType.PAIR:
        print("(", end="")
        write_pair(obj)
        print(")", end="")
    elif obj.type == ObjectType.SYMBOL:
        s = obj.data.value
        print(s, end="")
    elif obj.type == ObjectType.PRIMITIVE_PROC:
        print("<#<procedure>")
    else:
        raise Exception("Cannot write unkown type")


# REPL
def main():
    print("Welcome to Bootstrap Scheme.", "Use ctrl-c to exit.")
    import io
    while True:
        s = input("> ")
        s = io.StringIO(s)
        SCMWrite(SCMEval(SCMRead(s), SCMTheGlobalEnvironment))
        print()


if __name__ == "__main__":
    main()
