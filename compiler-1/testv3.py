from schemev3 import SCMRead, make_fixnum, SCMTrue, SCMFalse, \
    make_character
import unittest
import io

class TestFixnumObject(unittest.TestCase):
    def test_SCMRead(self):

        s = "123455"
        s0 = "      123414"
        f = io.StringIO(s)
        f0 = io.StringIO(s0)
        self.assertEqual(SCMRead(f), make_fixnum(int(s)))
        self.assertEqual(SCMRead(f0), make_fixnum(int(s0)))

class TestBoolean(unittest.TestCase):
    def test_SCMBool(self):
        t = "#t"
        f = "#f"
        t1 = "       #t   "
        f2 = "     #f "
        self.assertEqual(SCMRead(io.StringIO(t)), SCMTrue)
        self.assertEqual(SCMRead(io.StringIO(f)), SCMFalse)
        self.assertEqual(SCMRead(io.StringIO(t1)), SCMTrue)
        self.assertEqual(SCMRead(io.StringIO(f2)), SCMFalse)

class TestCharacter(unittest.TestCase):
    def test_character(self):
        c0 = "#\\a"
        c1 = "  #\\b"
        s = "  #\\space"
        n = "  #\\newline "
        g = "  #\\g  "
        self.assertEqual(SCMRead(io.StringIO(c0)),
                         make_character("a"))
        self.assertEqual(SCMRead(io.StringIO(c1)),
                         make_character("b"))
        self.assertEqual(SCMRead(io.StringIO(s)),
                         make_character(" "))
        self.assertEqual(SCMRead(io.StringIO(n)),
                         make_character("\n"))
        self.assertEqual(SCMRead(io.StringIO(g)),
                         make_character("g"))


if __name__ == "__main__":
    unittest.main()
