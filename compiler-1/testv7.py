from schemev7 import SCMRead, make_fixnum, SCMTrue, SCMFalse, \
    make_character, make_string, SCMTheEmptyList, SCMCons, \
    make_symbol
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
        self.assertEqual(SCMRead(io.StringIO("-1234")),
                         make_fixnum(int("-1234")))


class TestBoolean(unittest.TestCase):
    def test_SCMBool(self):
        t = "#t"
        f = "#f"
        t1 = "       #t   "
        f2 = "     #f "
        self.assertIs(SCMRead(io.StringIO(t)), SCMTrue)
        self.assertIs(SCMRead(io.StringIO(f)), SCMFalse)
        self.assertIs(SCMRead(io.StringIO(t1)), SCMTrue)
        self.assertIs(SCMRead(io.StringIO(f2)), SCMFalse)


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


class TestString(unittest.TestCase):
    def test_string(self):
        s0 = "\"asdf\""
        s1 = "\"asdf\"asdf\""
        s2 = "\"asdf\n\""
        s3 = """\"asdf
\""""
        self.assertEqual(SCMRead(io.StringIO(s0)),
                         make_string("asdf"))
        self.assertEqual(SCMRead(io.StringIO(s1)),
                         make_string("asdf"))
        self.assertEqual(SCMRead(io.StringIO(s2)),
                         make_string("asdf\n"))
        self.assertEqual(SCMRead(io.StringIO(s3)),
                         make_string("asdf\n"))


class TestTheEmptyList(unittest.TestCase):
    def test_emptylist(self):
        empty1 = """()"""
        empty2 = """       ( )  """
        empty3 = """
(
;; comment
)
"""
        self.assertIs(SCMRead(io.StringIO(empty1)),
                      SCMTheEmptyList)
        self.assertIs(SCMRead(io.StringIO(empty2)),
                      SCMTheEmptyList)
        self.assertIs(SCMRead(io.StringIO(empty3)),
                      SCMTheEmptyList)


class TestPair(unittest.TestCase):
    def test_pair(self):
        p1 = "(0 . 1)"
        p2 = "(0 1)"
        p3 = "(0 . (1 . ()))"
        p4 = "(0 . (1 . 2))"
        p1_e = SCMCons(make_fixnum(0), make_fixnum(1))
        p2_e = SCMCons(make_fixnum(0), SCMCons(make_fixnum(1), SCMTheEmptyList))
        p3_e = p2_e
        p4_e = SCMCons(make_fixnum(0), SCMCons(make_fixnum(1), make_fixnum(2)))
        self.assertEqual(SCMRead(io.StringIO(p1)),
                         p1_e)
        self.assertEqual(SCMRead(io.StringIO(p2)),
                         p2_e)
        self.assertEqual(SCMRead(io.StringIO(p3)),
                         p3_e)
        self.assertEqual(SCMRead(io.StringIO(p4)),
                         p4_e)


class TestSymbol(unittest.TestCase):
    def test_symbol(self):
        s1 = "asdf"
        s1_e = make_symbol(s1)
        s2 = "+vra"
        s2_e = make_symbol(s2)
        s3 = "scheme?"
        s3_e = make_symbol(s3)
        s4 = "scheme-p"
        s4_e = make_symbol(s4)
        self.assertEqual(SCMRead(io.StringIO(s1)), s1_e)
        self.assertEqual(SCMRead(io.StringIO(s2)), s2_e)
        self.assertEqual(SCMRead(io.StringIO(s3)), s3_e)
        self.assertEqual(SCMRead(io.StringIO(s4)), s4_e)


if __name__ == "__main__":
    unittest.main()
