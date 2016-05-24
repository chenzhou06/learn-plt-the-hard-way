from enum import Enum
import io

# Model
class ObjectType(Enum):
    FIXNUM = 1
    BOOLEAN = 2
    CHARACTER = 3

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

def make_character(value):
    return SCMObject(ObjectType.CHARACTER, value)

def is_character(obj):
    return obj.type == ObjectType.CHARACTER


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
    digits = []
    last_char = ""
    have_return = False

    in_bool_or_char = False
    in_bool = False
    in_char = False
    in_comment = False
    in_digits, expect_digit = False, False

    for char in fhandle.read():
        # Update iterator buffer
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

        # Boolean or character
        if not in_bool_or_char and char == "#":
            in_bool_or_char = True
            continue
        elif in_bool_or_char and char == "t":
            in_bool_or_char = False
            in_char = False
            return SCMTrue
        elif in_bool_or_char and char == "f":
            in_bool_or_char = False
            in_char = False
            return SCMFalse
        elif in_bool_or_char and char == "\\":
            # Read character
            in_char = True
            in_bool = False
            continue

        # Character
        if in_char and char == "s":
            pace = "".join([next(fhandle.read()) for _ in range(0,4)])
            if pace == "pace":
                in_char = False
                return make_character(" ")
            else:
                raise Exception("Unexpected characters {}".format(pace))
        elif in_char and char == "n":
            ewline = "".join([next(fhandle.read()) for _ in range(0,6)])
            if ewline == "ewline":
                in_char = False
                return make_character("\n")
            else:
                raise Exception("Unexpected characters {}".format(ewline))
        elif in_char:
            in_char = False
            return make_character(char)

        # Digit
        if not in_digits and char.isdigit():
            if last_char == "-":
                sign = -1
            in_digits = True
            digits.append(char)
            continue
        elif in_digits and char.isdigit():
            digits.append(char)
            continue
        elif in_digits and not char.isdigit():
            in_digits = False
            return make_fixnum(sign*int("".join(digits)))

    if in_digits:
        in_digits = False
        return make_fixnum(sign*int("".join(digits)))
    else:
        raise Exception("Read illegal state")

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
