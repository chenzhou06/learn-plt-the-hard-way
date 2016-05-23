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

def is_delimiter(c):
    # EOF not handled.
    return c.isspace() or c == "(" or c == ")" or c == "\"" or c == ";";

# This may not necessary.
def peek(iostream):
    return

def SCMRead(fhandle):
    "Return an object from a file handle."
    sign = 1
    num = 0
    in_comment = False
    digits = []

    for char in fhandle.read():
        # Remove white space and comment.
        if char.isspace():
            continue
        elif not in_comment and char == ";":
            in_comment = True
            continue
        elif in_comment and char != "\n":
            continue
        elif in_comment and char == "\n":
            in_comment = False
            continue

        if char.isdigit() or (char == "-" and peek(fhandle).isdigit()):
            if char == "-":
                sign = -1
            elif char.isdigit():
                digits.append(char)
            elif is_delimiter(char):
                f.write(char)
                break
            else:
                raise Exception("Number not followed by delimiter")
        else:
            raise Exception("Bad input. Unexpected '{}'".format(char))
    value = int("".join(digits))
    return make_fixnum(value)

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
