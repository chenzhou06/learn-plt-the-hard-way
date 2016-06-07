from schemev12 import SCMRead, SCMEval, make_fixnum, SCMTrue, SCMFalse, \
    make_character, make_string
from schemev12 import SCMTheEmptyList, SCMTheGlobalEnvironment, SCMCons, \
    make_symbol, make_primitive_proc, define_variable, is_if, \
    if_predicate, if_alternative, if_consequent
from schemev12 import is_null_proc, is_boolean_proc, is_integer_proc, \
    is_symbol_proc, is_char_proc, is_string_proc, is_pair_proc, \
    is_procedure_proc
from schemev12 import char_to_integer_proc, integer_to_char_proc, \
    number_to_string_proc, string_to_number_proc, symbol_to_string_proc, \
    string_to_symbol_proc
from schemev12 import add_proc, sub_proc, mul_proc, quotient_proc, remainder_proc
import unittest
import io

define_variable(make_symbol("+"),
                make_primitive_proc(add_proc),
                SCMTheGlobalEnvironment)


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


class TestTypePredicate(unittest.TestCase):
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
        self.procedure = SCMEval(SCMRead(io.StringIO("(+)")), SCMTheGlobalEnvironment)

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

    def test_is_procedure_proc(self):
        # self.assertTrue(is_procedure_proc(self.procedure))
        # self.assertFalse(is_procedure_proc(self.oppair))
        pass


class TestTypeConversion(unittest.TestCase):
    def setUp(self):
        self.char = SCMRead(io.StringIO("(#\\a)"))
        self.integer = SCMRead(io.StringIO("(97)"))
        self.number = SCMRead(io.StringIO("(12345)"))
        self.string = SCMRead(io.StringIO("(\"12345\")"))
        self.symbol = SCMRead(io.StringIO("(abc)"))
        self.sybstr = SCMRead(io.StringIO("""("abc")"""))

    def test_char_and_integer(self):
        self.assertEqual(char_to_integer_proc(self.char),
                         make_fixnum(97))
        self.assertEqual(integer_to_char_proc(self.integer),
                         make_character("a"))

    def test_number_and_proc(self):
        self.assertEqual(number_to_string_proc(self.number),
                         make_string("12345"))
        self.assertEqual(string_to_number_proc(self.string),
                         make_fixnum(12345))

    def test_symbol_and_string(self):
        self.assertEqual(symbol_to_string_proc(self.symbol),
                         make_string("abc"))
        self.assertEqual(string_to_symbol_proc(self.sybstr),
                         make_symbol("abc"))


class TestArithmetic(unittest.TestCase):
    """Test for primitive arithmetic procedures."""

    def setUp(self):
        self.opints = SCMRead(io.StringIO("(1 2)"))
        self.opints2 = SCMRead(io.StringIO("(9 2)"))

    def test_add_proc(self):
        self.assertEqual(add_proc(self.opints), make_fixnum(3))

    def test_sub_proc(self):
        self.assertEqual(sub_proc(self.opints), make_fixnum(-1))

    def test_mul_proc(self):
        self.assertEqual(mul_proc(self.opints), make_fixnum(2))

    def test_quotient_proc(self):
        self.assertEqual(quotient_proc(self.opints2), make_fixnum(4))
        self.assertEqual(quotient_proc(self.opints), make_fixnum(0))

    def test_remainder_proc(self):
        self.assertEqual(remainder_proc(self.opints), make_fixnum(1))
        self.assertEqual(remainder_proc(self.opints2), make_fixnum(1))


if __name__ == "__main__":
    unittest.main()
