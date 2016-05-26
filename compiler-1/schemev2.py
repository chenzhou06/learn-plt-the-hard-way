from enum import Enum
import io

# Model
class ObjectType(Enum):
    FIXNUM = 1
    BOOLEAN = 2

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

SCMTrue = SCMObject(ObjectType.BOOLEAN, True)
SCMFalse = SCMObject(ObjectType.BOOLEAN, False)

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

def SCMRead(fhandle):
    "Return an object from a file handle."
    last_char = ""

    # Remove whitespace and comment
    char = eat_whitespace(fhandle)

    # Boolean
    if char == "#":
        return read_bool(fhandle)
    # Digit
    elif char.isdigit():
        value = read_digit(fhandle, char)
        return make_fixnum(value)
    elif char == "-":
        return make_fixnum(fhandle, fhandle.read(1))
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
    import sys, io
    while True:
        s = input("> ")
        s = io.StringIO(s)
        SCMWrite(SCMEval(SCMRead(s)))


if __name__ == "__main__":
    main()
