from enum import Enum
import io

# Model

class ObjectType(Enum):
    FIXNUM = 1


class _ObjectFixnum:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class SCMObject:
    def __init__(self, type, data):
        "type: ObjectType. data: _ObjectFixnum"
        self.type = type
        self.data = _ObjectFixnum(data)

    def __eq__(self, other):
        return self.data.value == other.data.value

    def __repr__(self):
        return "<Type: {}, Value: {}>".format(self.type, self.data)

def make_fixnum(value):
    return SCMObject(ObjectType.FIXNUM, value)

def is_fixnum(obj):
    return obj.type == ObjectType.FIXNUM

# Read
def eat_whitespace(fhandle):
    char = None
    while True:
        char = fhandle.read(1)
        if char.isspace():
            continue
        elif char == ";":
            in_comment = True
            while True:
                char2 = fhandle.read(1)
                if char2 == "\n":
                    break
            continue
        else:
            break
    return char

def read_digit(fhandle, leading):
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

def is_delimiter(c):
    # EOF not handled.
    return c.isspace() or c == "(" or c == ")" or c == "\"" or c == ";" or c == ""

# This may not necessary.
def peek(iostream):
    return

def SCMRead(fhandle):
    "Return an object from a file handle."
    sign = 1
    num = 0
    in_comment = False
    digits = []

    char = eat_whitespace(fhandle)
    if char.isdigit():
        value = read_digit(fhandle, char)
        return make_fixnum(value)
    elif char == "-":
        char2 = fhandle.read(1)
        if char2.isdigit():
            value = read_digit(fhandle, char2)
            return make_fixnum(value)
        else:
            raise Exception("Unexpected character '{}'".format(char2))
    else:
        raise Exception("Unexpected character '{}'".format(char))

# Evaluate
# Placeholder
def SCMEval(exp):
    return exp

# Print
def SCMWrite(obj):
    if (obj.type == ObjectType.FIXNUM):
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
