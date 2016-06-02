from enum import Enum


# Model
class ObjectType(Enum):
    FIXNUM = 1
    BOOLEAN = 2
    CHARACTER = 3
    STRING = 4
    THE_EMPTY_LIST = 5


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


SCMTheEmptyList = SCMObject(ObjectType.THE_EMPTY_LIST, None)
SCMTrue = SCMObject(ObjectType.BOOLEAN, True)
SCMFalse = SCMObject(ObjectType.BOOLEAN, False)


def is_empty_list(obj):
    return obj == SCMTheEmptyList


def is_boolean(obj):
    return obj.type == ObjectType.BOOLEAN


def is_false(obj):
    return obj.data.value == False


def is_true(obj):
    return obj.data.value == True


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


# Read
def is_delimiter(c):
    return c.isspace() or c == "(" or c == ")" or c == "\"" or c == ";" or c == ""


def eat_whitespace(fhandle):
    char = None
    while True:
        char = fhandle.read(1)
        if char.isspace():
            continue
        elif char == ";":
            while True:
                char2 = fhandle.read(1)
                if char2 == "\n":
                    break
            continue
        else:
            break
    return char


def read_digit(fhandle, leading):
    "Read digits, return corresponding integer."
    digits = [leading]
    while True:
        char = fhandle.read(1)
        if char.isdigit():
            digits.append(char)
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
    if not is_delimiter(fhandle.read(1)):
        raise Exception("Character not followed by delimiter")
    else:
        pass


def read_character(fhandle, leading):
    if leading == "\\":
        char = fhandle.read(1)
        char2 = None
        if char == "":
            raise Exception("Incomplete character literal")
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
        raise Exception("Unknown boolean or character literal")


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


def read_empty_list(fhandle):
    char = eat_whitespace(fhandle)
    if char == ")":
        return SCMTheEmptyList
    else:
        raise Exception("Unexcepted character {}. Expecting ')'".format(char))


def SCMRead(fhandle):
    "Return an object from a file handle."
    char = eat_whitespace(fhandle)

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
    elif char == "-":
        char2 = fhandle.read(1)
        if char2.isdigit():
            value = read_digit(fhandle, char2)
            return make_fixnum(-1*value)
        else:
            raise Exception("Unexpected character '{}'".format(char2))
    # String
    elif char == "\"":
        return make_string(read_string(fhandle))
    # Empty list
    elif char == "(":
        return read_empty_list(fhandle)
    else:
        raise Exception("Unexpected character '{}'".format(char))


# Evaluate
# Placeholder
def SCMEval(exp):
    return exp


# Print
def SCMWrite(obj):
    if obj.type == ObjectType.FIXNUM:
        print(obj.data.value)
    elif obj.type == ObjectType.BOOLEAN:
        print(obj.data.value)
    else:
        raise Exception("Cannot write unkown type")


# REPL
def main():
    print("Welcome to Bootstrap Scheme.", "Use ctrl-c to exit.")
    import io
    while True:
        s = input("> ")
        s = io.StringIO(s)
        SCMWrite(SCMEval(SCMRead(s)))


if __name__ == "__main__":
    main()
