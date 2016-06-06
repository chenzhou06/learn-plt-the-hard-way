from schemev12 import SCMRead, make_fixnum, SCMTrue, SCMFalse, \
    make_character, make_string, SCMTheEmptyList, SCMCons, \
    make_symbol, is_if, if_predicate, if_alternative, if_consequent, \
    add_proc, is_null_proc, is_boolean_proc, is_integer_proc, \
    is_symbol_proc, is_char_proc, is_string_proc, is_pair_proc
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
        self.assertIs(SCMRead(io.StringIO(empty3)), SCMTheEmptyList)


class TestPair(unittest.TestCase):
    def test_pair(self):
        p1 = "(0 . 1)"
        p2 = "(0 1)"
        p3 = "(0 . (1 . ()))"
        p4 = "(0 . (1 . 2))"
        p1_e = SCMCons(make_fixnum(0), make_fixnum(1))
        p2_e = SCMCons(make_fixnum(0),
                       SCMCons(make_fixnum(1), SCMTheEmptyList))
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
        s3 = "scheme?"
        s3_e = make_symbol(s3)
        s4 = "scheme-p"
        s4_e = make_symbol(s4)
        self.assertEqual(SCMRead(io.StringIO(s1)), s1_e)
        self.assertEqual(SCMRead(io.StringIO(s3)), s3_e)
        self.assertEqual(SCMRead(io.StringIO(s4)), s4_e)


class TestIf(unittest.TestCase):
    def setUp(self):
        self.ifexp = SCMRead(io.StringIO("(if #t 0 1)"))
        self.ifexp2 = SCMRead(io.StringIO("(if #t 0)"))

    def test_if(self):
        self.assertTrue(is_if(self.ifexp))

    def test_if_predicate(self):
        self.assertIs(if_predicate(self.ifexp),
                      SCMTrue)

    def test_if_consequent(self):
        self.assertEqual(if_consequent(self.ifexp),
                         make_fixnum(0))

    def test_if_alternative(self):
        self.assertEqual(if_alternative(self.ifexp),
                         make_fixnum(1))
        self.assertIs(if_alternative(self.ifexp2), SCMFalse)


class TestProc(unittest.TestCase):
    def setUp(self):
        self.opints = SCMRead(io.StringIO("(1 2)"))
        self.opnull = SCMRead(io.StringIO("(())"))
        self.optrue = SCMRead(io.StringIO("(#t)"))
        self.opfalse = SCMRead(io.StringIO("(#f)"))
        self.opint = SCMRead(io.StringIO("(1)"))
        self.opsymbol = SCMRead(io.StringIO("(a b c)"))
        self.opchar = SCMRead(io.StringIO("(#\\a)"))
        self.opstring = SCMRead(io.StringIO("""("abs")"""))
        self.oppair = SCMRead(io.StringIO("((1 2))"))

    def test_add_proc(self):
        self.assertEqual(add_proc(self.opints), make_fixnum(3))

    def test_is_null_proc(self):
        self.assertTrue(is_null_proc(self.opnull))
        self.assertFalse(is_null_proc(self.opints))

    def test_is_boolean_proc(self):
        self.assertTrue(is_boolean_proc(self.optrue))
        self.assertTrue(is_boolean_proc(self.opfalse))
        self.assertFalse(is_boolean_proc(self.opints))

    def test_is_symbol_proc(self):
        self.assertTrue(is_symbol_proc(self.opsymbol))
        self.assertFalse(is_symbol_proc(self.opints))

    def test_is_integer_proc(self):
        self.assertTrue(is_integer_proc(self.opint))
        self.assertTrue(is_integer_proc(self.opints))
        self.assertFalse(is_integer_proc(self.optrue))

    def test_is_char_proc(self):
        self.assertTrue(is_char_proc(self.opchar))
        self.assertFalse(is_char_proc(self.opints))

    def test_is_string_proc(self):
        self.assertTrue(is_string_proc(self.opstring))
        self.assertFalse(is_string_proc(self.opchar))

    def test_is_pair_proc(self):
        self.assertTrue(is_pair_proc(self.oppair))
        self.assertFalse(is_pair_proc(self.opnull))




if __name__ == "__main__":
    unittest.main()
