from enum import Enum

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
def peek(infile):
    char = infile.peek(1)
    return char

def SCMRead(fhandle):
    "Return an object from infile."
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

        if char.isdigit() or (char == "-" and char.peek(1).isdigit()):
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
            raise Exception("bad input. Unexpected '{}'".format(char))

    value = int("".join(digits))
    return make_fixnum(value)


import unittest

class TestFixnumObject(unittest.TestCase):
    def test_SCMRead(self):
        import io
        s = "123455"
        s0 = "      123414"
        f = io.StringIO(s)
        f0 = io.StringIO(s0)
        self.assertEqual(SCMRead(f), make_fixnum(int(s)))
        self.assertEqual(SCMRead(f0), make_fixnum(int(s0)))

if __name__ == "__main__":
    unittest.main()
