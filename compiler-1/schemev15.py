#!/usr/bin/env python3
from enum import Enum
import sys


# Model
class ObjectType(Enum):
    "Types"
    FIXNUM = 1
    BOOLEAN = 2
    CHARACTER = 3
    STRING = 4
    THE_EMPTY_LIST = 5
    PAIR = 6
    SYMBOL = 7
    PRIMITIVE_PROC = 8
    COMPOUND_PROC = 9


class _ObjectValue:
    "Private object for store value."   # TODO: redundant
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class SCMObject:
    "Base class for scheme types."
    def __init__(self, type_, data):
        "type: ObjectType. data: _ObjectValue"
        self.type = type_
        self.data = _ObjectValue(data)

    def __eq__(self, other):
        return self.data.value == other.data.value

    def __repr__(self):
        return "<Type: {}, Value: {}>".format(self.type, self.data)

# FIXME: Re-factoring to user better var name.
# Global
SCMTheEmptyList = SCMObject(ObjectType.THE_EMPTY_LIST, None)
SCMTrue = SCMObject(ObjectType.BOOLEAN, True)
SCMFalse = SCMObject(ObjectType.BOOLEAN, False)
SCMSymbolTable = SCMTheEmptyList  # TODO: default dict
SCMTheEmptyEnvironment = SCMTheEmptyList


def is_the_empty_list(obj):
    "Empty list predicate."
    return obj is SCMTheEmptyList


def is_boolean(obj):
    "Boolean predicates."
    return obj.type == ObjectType.BOOLEAN


def is_false(obj):
    "False is False."
    return obj is SCMFalse


def is_true(obj):
    "True is true."
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


def make_compound_proc(parameters, body, env):
    "Make a compound procedure."

    obj = SCMObject(ObjectType.COMPOUND_PROC,
                    dict(parameters=parameters, body=body, env=env))
    return obj



def is_primitive_proc(obj):
    return obj.type == ObjectType.PRIMITIVE_PROC


# Primitive Procedures
#
# Arithmetic operations
def add_proc(arguments):
    """Add numbers from arguments."""
    result = 0
    while not is_the_empty_list(arguments):
        result += SCMCar(arguments).data.value
        arguments = SCMCdr(arguments)
    return make_fixnum(result)


def sub_proc(arguments):
    """Subtraction."""
    # TODO: reduce after implement scheme pair as list.
    result = SCMCar(arguments).data.value
    arguments = SCMCdr(arguments)
    while not is_the_empty_list(arguments):
        result -= SCMCar(arguments).data.value
        arguments = SCMCdr(arguments)
    return make_fixnum(result)


def mul_proc(arguments):
    """Multiplication."""
    result = 1
    while not is_the_empty_list(arguments):
        result *= SCMCar(arguments).data.value
        arguments = SCMCdr(arguments)
    return make_fixnum(result)


def quotient_proc(arguments):
    """Quotient."""
    num1 = SCMCar(arguments).data.value
    num2 = SCMCar(SCMCdr(arguments)).data.value
    return make_fixnum(num1 // num2)


def remainder_proc(arguments):
    """Remainder."""
    num1 = SCMCar(arguments).data.value
    num2 = SCMCar(SCMCdr(arguments)).data.value
    return make_fixnum(num1 % num2)



# Primitive comparison
# FIXME: Should return scheme boolean objects.
def is_number_equal_proc(arguments):
    """Compare two numbers, if equal returns true."""
    value = SCMCar(arguments).data.value
    while not is_the_empty_list(SCMCdr(arguments)):
        if value != SCMCar(SCMCdr(arguments)).data.value:
            return False
        arguments = SCMCdr(arguments)
    return True


def is_less_then_proc(arguments):
    """If arguments is decreasing then returns true."""
    previous = SCMCar(arguments).data.value
    next_ = None
    while not is_the_empty_list(SCMCdr(arguments)):
        next_ = SCMCar(SCMCdr(arguments)).data.value
        arguments = SCMCdr(arguments)
        if previous < next_:
            previous = next_
        else:
            return False
    return True


def is_greater_then_proc(arguments):
    """If arguments is increasing then returns false."""
    previous = SCMCar(arguments).data.value
    next_ = None
    while not is_the_empty_list(SCMCdr(arguments)):
        next_ = SCMCar(SCMCdr(arguments)).data.value
        arguments = SCMCdr(arguments)
        if previous > next_:
            previous = next_
        else:
            return False
    return True


# Type predicates
def is_null_proc(arguments):
    """Null predicate."""
    return is_the_empty_list(SCMCar(arguments)) is True


def is_boolean_proc(arguments):
    """Boolean predicate."""
    return is_boolean(SCMCar(arguments)) is True


def is_symbol_proc(arguments):
    """Symbol predicate."""
    return is_symbol(SCMCar(arguments)) is True


def is_integer_proc(arguments):
    """Integer predicate."""
    return is_fixnum(SCMCar(arguments)) is True


def is_char_proc(arguments):
    """Character predicate."""
    return is_character(SCMCar(arguments)) is True


def is_string_proc(arguments):
    """String predicate."""
    return is_string(SCMCar(arguments)) is True


def is_pair_proc(arguments):
    """Pair predicate."""
    return is_pair(SCMCar(arguments)) is True


def is_compound_proc(obj):
    "Compound procedure predicate."
    return obj.type == ObjectType.COMPOUND_PROC


def is_procedure_proc(arguments):        # TODO: Untested
    """Procedure predicate."""
    obj = SCMCar(arguments)
    return SCMTrue if is_primitive_proc(obj) or is_compound_proc(obj) else \
        SCMFalse


# List procedures
def cons_proc(arguments):
    """Cons procedure."""
    return SCMCons(SCMCar(arguments),
                   SCMCar(SCMCdr(arguments)))


def car_proc(arguments):
    """Car procedure."""
    return SCMCar(SCMCar(arguments))


def cdr_proc(arguments):
    """Cdr procedure."""
    return SCMCdr(SCMCar(arguments))


def set_car_proc(arguments):
    """Set car procedure."""
    SCMSetCar(SCMCar(arguments), SCMCar(SCMCdr(arguments)))
    return SCMOkSymbol

def set_cdr_proc(arguments):
    """Set cdr procedure."""
    SCMSetCdr(SCMCar(arguments), SCMCar(SCMCdr(arguments)))
    return SCMOkSymbol


def list_proc(arguments):
    """List procedure."""
    return arguments


# Comparison
def is_eq_proc(arguments):
    obj1 = SCMCar(arguments)
    obj2 = SCMCar(SCMCdr(arguments))
    if obj1.type != obj2.type:
        return SCMFalse
    else:
        return SCMTrue if obj1.data.value == \
            obj2.data.value else SCMFalse


# Type conversions, TODO: add test
def char_to_integer_proc(arguments):
    """Convert character to integer."""
    return make_fixnum(ord(SCMCar(arguments).data.value))


def integer_to_char_proc(arguments):
    """Convert integer to character."""
    return make_character(chr(SCMCar(arguments).data.value))


def number_to_string_proc(arguments):
    """Convert number to string."""
    return make_string(str(SCMCar(arguments).data.value))


def string_to_number_proc(arguments):
    """Convert string to number."""
    return make_fixnum(int(SCMCar(arguments).data.value))


def symbol_to_string_proc(arguments):
    """Convert symbol to string."""
    return make_string(SCMCar(arguments).data.value)


def string_to_symbol_proc(arguments):
    """Convert string to symbol."""
    return make_symbol(SCMCar(arguments).data.value)


# Singleton
SCMQuoteSymbol = make_symbol("quote")
SCMDefineSymbol = make_symbol("define")
SCMSetSymbol = make_symbol("set!")
SCMOkSymbol = make_symbol("ok")
SCMIfSymbol = make_symbol("if")
SCMLambdaSymbol = make_symbol("lambda")
SCMBeginSymbol = make_symbol("begin")
SCMCondSymbol = make_symbol("cond")
SCMElseSymbol = make_symbol("else")


def make_lambda(parameters, body):
    "Make a lambda pair."
    return SCMCons(SCMLambdaSymbol, SCMCons(parameters, body))


def is_lambda(exp):
    "Starts by lambda symbol."
    return is_tagged_list(exp, SCMLambdaSymbol)


def lambda_parameters(exp):
    "Parameters of lambda."
    return SCMCar(SCMCdr(exp))


def lambda_body(exp):
    "Body of lambda."
    return SCMCdr(SCMCdr(exp))


def make_begin(exp):
    "Make a begin expression."
    return SCMCons(SCMBeginSymbol, exp)


def is_begin(exp):
    "Begin expression predicate."
    return is_tagged_list(exp, SCMBeginSymbol)


def begin_actions(exp):
    """Extract begin actions.

    ```
    (begin exp1 exp2 exp3)
    => (exp1 exp2 exp3)
    ```
    """
    return SCMCdr(exp)


def is_last_exp(seq):
    "Is the last expression."
    return is_the_empty_list(SCMCdr(seq))


def first_exp(seq):
    "First expression"
    return SCMCar(seq)


def rest_exp(seq):
    "Rest expression."
    return SCMCdr(seq)


def is_cond(exp):
    "Cond predicate."
    return is_tagged_list(exp, SCMCondSymbol)


def cond_clauses(exp):
    "Extract clause."
    return SCMCdr(exp)


def cond_predicate(clause):
    "Extract predicate from a condition clause."
    return SCMCar(clause)


def cond_actions(clause):
    "Extract actions from a condition clause."
    return SCMCdr(clause)


def is_cond_else_clause(clause):
    "Else clause predicate."
    return cond_predicate(clause) is SCMElseSymbol


def sequence_to_exp(seq):
    "Sequence to expressions."
    if is_the_empty_list(seq):
        return seq
    elif is_last_exp(seq):
        return first_exp(seq)
    else:
        return make_begin(seq)


def expand_clauses(clauses):
    "Expand clauses."
    if is_the_empty_list(clauses):
        return SCMFalse
    else:
        first = SCMCar(clauses)
        rest = SCMCdr(clauses)
        if is_cond_else_clause(first):
            if is_the_empty_list(rest):
                return sequence_to_exp(cond_actions(first))
            else:
                raise Exception("else clause is not last cond->if")
        else:
            return make_if(cond_predicate(first),
                           sequence_to_exp(cond_actions(first)),
                           expand_clauses(rest))


def cond_to_if(exp):
    "Condition to if expression."
    return expand_clauses(cond_clauses(exp))


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


def definition_variable(exp):
    """Definition variable."""
    if is_symbol(SCMCar(SCMCdr(exp))):
        return SCMCar(SCMCdr(exp))
    else:
        return SCMCar(SCMCar(SCMCdr(exp)))


def definition_value(exp):
    "Definition value."
    if is_symbol(SCMCar(SCMCdr(exp))):
        return SCMCar(SCMCdr(SCMCdr(exp)))
    else:
        return make_lambda(SCMCdr(SCMCar(SCMCdr(exp))),
                           SCMCdr(SCMCdr(exp)))


def make_if(predicate, consequent, alternative):
    """Make a if expression from tree expressions.

    ```
    predicate consequent alternative
    => (if predicate consequent alternative)
    ```
    """
    return SCMCons(SCMIfSymbol,
                   SCMCons(predicate,
                           SCMCons(consequent,
                                   SCMCons(alternative, SCMTheEmptyList))))


def setup_environment():
    return extend_environment(SCMTheEmptyList,
                              SCMTheEmptyList,
                              SCMTheEmptyEnvironment)

SCMTheGlobalEnvironment = setup_environment()
# inits
def add_procedure(scheme_name, py_name):
    define_variable(make_symbol(scheme_name),
                    make_primitive_proc(py_name),
                    SCMTheGlobalEnvironment)
    return

add_procedure("null?", is_null_proc)
add_procedure("boolean?", is_boolean_proc)
add_procedure("symbol?", is_symbol_proc)
add_procedure("integer?", is_integer_proc)
add_procedure("char?", is_char_proc)
add_procedure("string?", is_string_proc)
add_procedure("pair?", is_pair_proc)
add_procedure("procedure?", is_procedure_proc)

add_procedure("char->integer", char_to_integer_proc)
add_procedure("integer->char", integer_to_char_proc)
add_procedure("number->string", number_to_string_proc)
add_procedure("string->number", string_to_number_proc)
add_procedure("symbol->string", symbol_to_string_proc)
add_procedure("string->symbol", string_to_symbol_proc)

add_procedure("+", add_proc)
add_procedure("-", sub_proc)
add_procedure("*", mul_proc)
add_procedure("quotient", quotient_proc)
add_procedure("remainder", remainder_proc)
add_procedure("=", is_number_equal_proc)
add_procedure("<", is_less_then_proc)
add_procedure(">", is_greater_then_proc)

add_procedure("cons", cons_proc)
add_procedure("car", car_proc)
add_procedure("cdr", cdr_proc)
add_procedure("set-car!", set_car_proc)
add_procedure("set-cdr!", set_cdr_proc)
add_procedure("list", list_proc)

add_procedure("eq?", is_eq_proc)


# Read
def is_delimiter(c):
    return c.isspace() or c == "(" or c == ")" or \
        c == "\"" or c == ";" or c == ""


def is_initial(c):
    return (c.isalpha() or c == "*" or c == "/" or c == ">" or
            c == "<" or c == "=" or c == "?" or c == "!")


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
        char = peek(fhandle)
        if char.isdigit():
            digits.append(fhandle.read(1))
            continue
        elif is_delimiter(char):
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
        raise Exception("Unknown boolean or character literal, '{}'.".format(leading))


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
    elif is_lambda(exp):
        return make_compound_proc(lambda_parameters(exp),
                                  lambda_body(exp),
                                  env)
    elif is_begin(exp):
        exp = begin_actions(exp)
        while not is_last_exp(exp):
            SCMEval(first_exp(exp), env)
            exp = rest_exp(exp)
        exp = first_exp(exp)
        return SCMEval(exp, env)
    elif is_cond(exp):
        exp = cond_to_if(exp)
        return SCMEval(exp, env)
    elif is_application(exp):
        procedure = SCMEval(operator(exp), env)
        arguments = list_of_values(operands(exp), env)
        if is_primitive_proc(procedure):
            return procedure.data.value(arguments)
        elif is_compound_proc(procedure):
            env = extend_environment(
                procedure.data.value.get("parameters"),
                arguments,
                procedure.data.value.get("env"))
            exp = make_begin(procedure.data.value.get("body"))
            return SCMEval(exp, env)
        else:
            raise Exception("Unknown procedure type.")
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
    elif obj.type == ObjectType.PRIMITIVE_PROC or obj.type == ObjectType.COMPOUND_PROC:
        print("<#<procedure>")
    else:
        raise Exception("Cannot write unkown type")


# REPL
def repl():
    "Repl"
    print("Welcome to Bootstrap Scheme.", "Use ctrl-c to exit.")
    import io
    while True:
        s = input("> ")
        s = io.StringIO(s)
        SCMWrite(SCMEval(SCMRead(s), SCMTheGlobalEnvironment))
        print()


if __name__ == "__main__":
    repl()
