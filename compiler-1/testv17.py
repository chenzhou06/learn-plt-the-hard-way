"""Tests for schemev12.py."""
import unittest
import io
from schemev17 import *

class TestFixnumObject(unittest.TestCase):
    """Tests for fixnum."""
    def test_scmread(self):
        "SCMRead"
        num1 = io.StringIO("123455")
        num2 = io.StringIO("      123414")
        self.assertEqual(SCMRead(num1), make_fixnum(123455))
        self.assertEqual(SCMRead(num2), make_fixnum(123414))
        self.assertEqual(SCMRead(io.StringIO("-1234")),
                         make_fixnum(int("-1234")))


class TestBoolean(unittest.TestCase):
    "Tests for boolean."
    def test_scmbool(self):
        "SCMBool"
        true1 = "#t"
        false1 = "#f"
        true2 = "       #t   "
        false2 = "     #f "
        self.assertIs(SCMRead(io.StringIO(true1)), SCMTrue)
        self.assertIs(SCMRead(io.StringIO(false1)), SCMFalse)
        self.assertIs(SCMRead(io.StringIO(true2)), SCMTrue)
        self.assertIs(SCMRead(io.StringIO(false2)), SCMFalse)


class TestCharacter(unittest.TestCase):
    "Tests for character."
    def test_character(self):
        "SCMRead for character."
        char1 = "#\\a"
        char2 = "  #\\b"
        char3 = "  #\\space"
        char4 = "  #\\newline "
        char5 = "  #\\g  "
        self.assertEqual(SCMRead(io.StringIO(char1)),
                         make_character("a"))
        self.assertEqual(SCMRead(io.StringIO(char2)),
                         make_character("b"))
        self.assertEqual(SCMRead(io.StringIO(char3)),
                         make_character(" "))
        self.assertEqual(SCMRead(io.StringIO(char4)),
                         make_character("\n"))
        self.assertEqual(SCMRead(io.StringIO(char5)),
                         make_character("g"))


class TestString(unittest.TestCase):
    "Tests for string."
    def test_string(self):
        "Read string."
        string1 = "\"asdf\""
        string2 = "\"asdf\"asdf\""
        string3 = "\"asdf\n\""
        string4 = """\"asdf
\""""
        self.assertEqual(SCMRead(io.StringIO(string1)),
                         make_string("asdf"))
        self.assertEqual(SCMRead(io.StringIO(string2)),
                         make_string("asdf"))
        self.assertEqual(SCMRead(io.StringIO(string3)),
                         make_string("asdf\n"))
        self.assertEqual(SCMRead(io.StringIO(string4)),
                         make_string("asdf\n"))


class TestTheEmptyList(unittest.TestCase):
    "Test for emptylist."
    def test_emptylist(self):
        "Read empty list."
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
    "Test for read pair."
    def test_pair(self):
        "Read pair."
        pair1 = "(0 . 1)"
        pair2 = "(0 1)"
        pair3 = "(0 . (1 . ()))"
        pair4 = "(0 . (1 . 2))"
        pair1_e = SCMCons(make_fixnum(0), make_fixnum(1))
        pair2_e = SCMCons(make_fixnum(0),
                          SCMCons(make_fixnum(1), SCMTheEmptyList))
        pair3_e = pair2_e
        pair4_e = SCMCons(make_fixnum(0), SCMCons(make_fixnum(1), make_fixnum(2)))
        self.assertEqual(SCMRead(io.StringIO(pair1)),
                         pair1_e)
        self.assertEqual(SCMRead(io.StringIO(pair2)),
                         pair2_e)
        self.assertEqual(SCMRead(io.StringIO(pair3)),
                         pair3_e)
        self.assertEqual(SCMRead(io.StringIO(pair4)),
                         pair4_e)


class TestSymbol(unittest.TestCase):
    "Test for symbol."
    def test_symbol(self):
        "Read symbol."
        symbol1 = "asdf"
        symbol1_e = make_symbol(symbol1)
        symbol2 = "scheme?"
        symbol2_e = make_symbol(symbol2)
        symbol3 = "scheme-p"
        symbol3_e = make_symbol(symbol3)
        self.assertEqual(SCMRead(io.StringIO(symbol1)), symbol1_e)
        self.assertEqual(SCMRead(io.StringIO(symbol2)), symbol2_e)
        self.assertEqual(SCMRead(io.StringIO(symbol3)), symbol3_e)


class TestIf(unittest.TestCase):
    "Test for if predicate."
    def setUp(self):
        self.ifexp = SCMRead(io.StringIO("(if #t 0 1)"))
        self.ifexp2 = SCMRead(io.StringIO("(if #t 0)"))

    def test_if(self):
        "Is if procedure."
        self.assertTrue(is_if(self.ifexp))

    def test_if_predicate(self):
        "Return the condition in a if procedure."
        self.assertIs(if_predicate(self.ifexp),
                      SCMTrue)

    def test_if_consequent(self):
        "Return the consequence when success."
        self.assertEqual(if_consequent(self.ifexp),
                         make_fixnum(0))

    def test_if_alternative(self):
        "Return the alternative."
        self.assertEqual(if_alternative(self.ifexp),
                         make_fixnum(1))
        self.assertIs(if_alternative(self.ifexp2), SCMFalse)


class TestTypePredicate(unittest.TestCase):
    "Type predicate."
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
        "Tell if it is a null."
        self.assertTrue(is_null_proc(self.opnull))
        self.assertFalse(is_null_proc(self.opints))

    def test_is_boolean_proc(self):
        "Is boolean?"
        self.assertTrue(is_boolean_proc(self.optrue))
        self.assertTrue(is_boolean_proc(self.opfalse))
        self.assertFalse(is_boolean_proc(self.opints))

    def test_is_symbol_proc(self):
        "Is symbol?"
        self.assertTrue(is_symbol_proc(self.opsymbol))
        self.assertFalse(is_symbol_proc(self.opints))

    def test_is_integer_proc(self):
        "Is integer?"
        self.assertTrue(is_integer_proc(self.opint))
        self.assertTrue(is_integer_proc(self.opints))
        self.assertFalse(is_integer_proc(self.optrue))

    def test_is_char_proc(self):
        "Is character?"
        self.assertTrue(is_char_proc(self.opchar))
        self.assertFalse(is_char_proc(self.opints))

    def test_is_string_proc(self):
        "Is string?"
        self.assertTrue(is_string_proc(self.opstring))
        self.assertFalse(is_string_proc(self.opchar))

    def test_is_pair_proc(self):
        "Is pair?"
        self.assertTrue(is_pair_proc(self.oppair))
        self.assertFalse(is_pair_proc(self.opnull))

    def test_is_procedure_proc(self):
        "Is procedure?"
        # TODO
        # self.assertTrue(is_procedure_proc(self.procedure))
        # self.assertFalse(is_procedure_proc(self.oppair))
        pass


class TestTypeConversion(unittest.TestCase):
    "Type Conversiont."
    def setUp(self):
        self.char = SCMRead(io.StringIO("(#\\a)"))
        self.integer = SCMRead(io.StringIO("(97)"))
        self.number = SCMRead(io.StringIO("(12345)"))
        self.string = SCMRead(io.StringIO("(\"12345\")"))
        self.symbol = SCMRead(io.StringIO("(abc)"))
        self.sybstr = SCMRead(io.StringIO("""("abc")"""))

    def test_char_and_integer(self):
        "Character to integer."
        self.assertEqual(char_to_integer_proc(self.char),
                         make_fixnum(97))
        self.assertEqual(integer_to_char_proc(self.integer),
                         make_character("a"))

    def test_number_and_string(self):
        "Number to string."
        self.assertEqual(number_to_string_proc(self.number),
                         make_string("12345"))
        self.assertEqual(string_to_number_proc(self.string),
                         make_fixnum(12345))

    def test_symbol_and_string(self):
        "Symbol to string."
        self.assertEqual(symbol_to_string_proc(self.symbol),
                         make_string("abc"))
        self.assertEqual(string_to_symbol_proc(self.sybstr),
                         make_symbol("abc"))


class TestArithmetic(unittest.TestCase):
    """Tests for primitive arithmetic procedures."""

    def setUp(self):
        self.opints = SCMRead(io.StringIO("(1 2)"))
        self.opints2 = SCMRead(io.StringIO("(9 2)"))

    def test_add_proc(self):
        "Add."
        self.assertEqual(add_proc(self.opints), make_fixnum(3))

    def test_sub_proc(self):
        "Minus."
        self.assertEqual(sub_proc(self.opints), make_fixnum(-1))

    def test_mul_proc(self):
        "Multiplication."
        self.assertEqual(mul_proc(self.opints), make_fixnum(2))

    def test_quotient_proc(self):
        "Quotient."
        self.assertEqual(quotient_proc(self.opints2), make_fixnum(4))
        self.assertEqual(quotient_proc(self.opints), make_fixnum(0))

    def test_remainder_proc(self):
        "Remainder."
        self.assertEqual(remainder_proc(self.opints), make_fixnum(1))
        self.assertEqual(remainder_proc(self.opints2), make_fixnum(1))


class TestComparision(unittest.TestCase):
    """Tests for primitive comparison procedures."""

    def setUp(self):
        self.eqnums = SCMRead(io.StringIO("(1 1 1 1 1)"))
        self.lessnums = SCMRead(io.StringIO("(1 2 3)"))
        self.greaternums = SCMRead(io.StringIO("(3 2 1)"))

    def test_is_number_equal_proc(self):
        "Is two numbers equal?"
        self.assertTrue(is_number_equal_proc(self.eqnums))
        self.assertFalse(is_number_equal_proc(self.lessnums))

    def test_is_less_than_proc(self):
        "Less than?"
        self.assertTrue(is_less_then_proc(self.lessnums))
        self.assertFalse(is_less_then_proc(self.greaternums))

    def test_greater_then_proc(self):
        "Greater than?"
        self.assertTrue(is_greater_then_proc(self.greaternums))
        self.assertFalse(is_greater_then_proc(self.lessnums))


class TestListProc(unittest.TestCase):
    """Tests for list procedures."""
    def setUp(self):
        self.abc = SCMRead(io.StringIO("(1 2)"))
        self.hij = SCMRead(io.StringIO("((1 2) 3)"))
        self.lmn = SCMRead(io.StringIO("((1 2) (7 8))"))
        self.opq = SCMRead(io.StringIO("((1 2))"))

    def test_cons_proc(self):
        "Scheme cons."
        self.assertEqual(cons_proc(self.abc),
                         SCMCons(make_fixnum(1), make_fixnum(2)))

    def test_car_proc(self):
        "Scheme car."
        self.assertEqual(car_proc(self.opq), make_fixnum(1))

    def test_cdr_proc(self):
        "Scheme cdr."
        self.assertEqual(cdr_proc(self.opq),
                         SCMCons(make_fixnum(2), SCMTheEmptyList))

    def test_set_car_proc(self):
        "Set! car."
        self.assertEqual(set_car_proc(self.hij), SCMOkSymbol)

    def test_set_cdr_proc(self):
        "Set! cdr."
        self.assertEqual(set_cdr_proc(self.lmn), SCMOkSymbol)

    def test_list_proc(self):
        "Scheme list."
        self.assertEqual(list_proc(self.abc),
                         self.abc)


class TestEqual(unittest.TestCase):
    def setUp(self):
        self.nums1 = SCMRead(io.StringIO("(1 1)"))
        self.nums2 = SCMRead(io.StringIO("(1 2)"))
        self.chars1 = SCMRead(io.StringIO("(#\\a #\\a)"))
        self.chars2 = SCMRead(io.StringIO("(#\\a #\\b)"))
        self.string1 = SCMRead(io.StringIO("""("string" "string")"""))
        self.string2 = SCMRead(io.StringIO("""("qwer" "asdf")"""))
        self.difftype = SCMRead(io.StringIO("(1 #\\a)"))

    def test_num_eq(self):
        "Check is_eq_proc for numbers."
        self.assertIs(is_eq_proc(self.nums1), SCMTrue)
        self.assertIs(is_eq_proc(self.nums2), SCMFalse)

    def test_char_eq(self):
        "Check is_eq_proc for characters."
        self.assertIs(is_eq_proc(self.chars1), SCMTrue)
        self.assertIs(is_eq_proc(self.chars2), SCMFalse)

    def test_string_eq(self):
        "Check `is_eq_proc` for strings."
        self.assertIs(is_eq_proc(self.string1), SCMTrue)
        self.assertIs(is_eq_proc(self.string2), SCMFalse)

    def test_not_eq(self):
        "Check type checking."
        self.assertIs(is_eq_proc(self.difftype), SCMFalse)


class TestCompoundProc(unittest.TestCase):
    "Tests for compound proc."

    def test_make_compound_proc(self):
        "Make a compound proc"
        comproc = make_compound_proc("parameters", "body", "env")
        self.assertTrue(isinstance(comproc, SCMObject))
        self.assertEqual(comproc.data.value["parameters"], "parameters")
        self.assertEqual(comproc.data.value["body"], "body")
        self.assertEqual(comproc.data.value["env"], "env")


class TestLambda(unittest.TestCase):
    "Tests for lambda."
    def setUp(self):
        self.lambdaproc = make_lambda("parameters", "body")

    def test_lambda(self):
        "Test for lambda."
        lambda_ = make_lambda("parameters", "body")
        self.assertTrue(isinstance(lambda_, SCMObject))
        self.assertTrue(is_lambda(lambda_))

    def test_lambda_para(self):
        "Test for lambda parameters."
        self.assertEqual(lambda_parameters(self.lambdaproc),
                         "parameters")
        self.assertEqual(lambda_body(self.lambdaproc),
                         "body")


class TestDefinition(unittest.TestCase):
    "Tests for definition."
    def setUp(self):
        self.define = SCMRead(io.StringIO("(define (add1 a) (+ x 1))"))

    def test_def_var(self):
        "Test definition variable"
        self.assertEqual(definition_variable(self.define),
                         make_symbol("add1"))

    def test_def_val(self):
        "Test definition value"
        self.assertEqual(definition_value(self.define),
                         make_lambda(SCMCons(make_symbol("a"), SCMTheEmptyList),
                                     SCMRead(io.StringIO("((+ x 1))"))))


class TestExp(unittest.TestCase):
    "Tests for S expression."
    def setUp(self):
        self.seq = SCMCons(SCMCons("qwer", "asdf"), SCMCons("asdf", SCMTheEmptyList))

    def test_is_last_exp(self):
        "Test last exp"
        self.assertTrue(is_last_exp(SCMCdr(self.seq)))

    def test_first_exp(self):
        "Test first exp"
        self.assertEqual(first_exp(self.seq),
                         SCMCons("qwer", "asdf"))

    def test_rest_exp(self):
        "Test rest exp"
        self.assertEqual(rest_exp(self.seq),
                         SCMCons("asdf", SCMTheEmptyList))


class TestBegin(unittest.TestCase):
    "Tests for begin expressions."
    def setUp(self):
        self.beginexp = SCMRead(io.StringIO("(begin 1 2 3)"))
        self.beginactions = SCMRead(io.StringIO("(1 2 3)"))

    def test_begin(self):
        "Test for begin"
        self.assertEqual(self.beginexp, make_begin(self.beginactions))

    def test_is_begin(self):
        "Test for `is_begin`."
        self.assertTrue(is_begin(self.beginexp))
        self.assertFalse(is_begin(self.beginactions))

    def test_begin_actions(self):
        "Test for `begin_actions`."
        self.assertEqual(begin_actions(self.beginexp),
                         self.beginactions)

    def test_eval(self):
        "Test for evaluate begin procedures."
        exp = SCMRead(io.StringIO("(begin (define a 1) (+ a a))"))
        self.assertEqual(SCMEval(exp, SCMTheGlobalEnvironment), make_fixnum(2))


class TestCond(unittest.TestCase):
    "Tests for condition."
    def setUp(self):
        self.condexp = SCMRead(io.StringIO("""(cond ((< 1 2) #t)
                                                    ((= 1 2) #f)
                                                    (else "else"))"""))
        self.ifexp = SCMRead(io.StringIO("(if (< 1 2) #t #f)"))
        self.pred1 = SCMRead(io.StringIO("(< 1 2)"))
        self.conseq1 = SCMRead(io.StringIO("#t"))
        self.alt1 = SCMRead(io.StringIO("#f"))
        self.clauses = cond_clauses(self.condexp)
        self.clauses_e = SCMRead(io.StringIO("(((< 1 2) #t) ((= 1 2) #f) (else \"else\"))"))

    def test_make_if(self):
        "Test for `make_if` which is used to convert a condition to if."
        self.assertEqual(make_if(self.pred1, self.conseq1, self.alt1),
                         self.ifexp)

    def test_is_cond(self):
        "Test for `is_cond`."
        self.assertTrue(is_cond(self.condexp))
        self.assertFalse(is_cond(self.ifexp))

    def test_cond_clauses(self):
        "Test for `cond_clauses`."
        self.assertEqual(self.clauses, self.clauses_e)

    def test_cond_predicate(self):
        "Test for `cond_predicate`."
        self.assertEqual(cond_predicate(SCMCar(self.clauses)),
                         self.pred1)

    def test_cond_actions(self):
        "Test for `cond_actions`."
        clause = SCMCar(self.clauses)
        self.assertEqual(cond_actions(clause),
                         SCMCons(self.conseq1, SCMTheEmptyList))

    def test_is_cond_else_clause(self):
        "Test for `is_cond_else_clause`."
        elseclause = SCMCar(SCMCdr(SCMCdr(self.clauses)))
        self.assertTrue(is_cond_else_clause(elseclause))
        self.assertFalse(is_cond_else_clause(SCMCar(self.clauses)))

    def test_sequence_to_exp(self):
        "Test for `sequence_to_exp`."
        lastseq = SCMRead(io.StringIO("((+ 1 1))"))
        lastseq_1 = SCMRead(io.StringIO("(+ 1 1)"))
        self.assertEqual(sequence_to_exp(SCMTheEmptyList), SCMTheEmptyList)
        self.assertEqual(sequence_to_exp(lastseq), lastseq_1)
        self.assertTrue(is_begin(sequence_to_exp(self.clauses)))

    def test_expand_clauses(self):
        "Test for `expand_clauses`."
        nestedif = make_if(SCMRead(io.StringIO("(= 1 2)")),
                           SCMFalse,
                           make_string("else"))
        self.assertEqual(expand_clauses(self.clauses),
                         make_if(self.pred1,
                                 SCMTrue,
                                 nestedif))


class TestLet(unittest.TestCase):
    "Tests for let expression."
    def setUp(self):
        self.app = SCMRead(io.StringIO("(+ 1 2)"))
        self.operater = make_symbol("+")
        self.operands = SCMRead(io.StringIO("(1 2)"))
        self.letexp = SCMRead(io.StringIO("(let ((a 1) (b 2)) (+ a b))"))
        self.letbindings = SCMRead(io.StringIO("((a 1) (b 2))"))
        self.letarguments = SCMRead(io.StringIO("(1 2)"))
        self.letbody = SCMRead(io.StringIO("((+ a b))"))
        self.binding = SCMRead(io.StringIO("(a 1)"))
        self.bindings = SCMRead(io.StringIO("((a 1) (b 2))"))

    def test_make_application(self):
        "Test for `make_application`."
        self.assertEqual(make_application(self.operater, self.operands),
                         self.app)

    def test_is_let(self):
        "Test for `is_let`."
        self.assertTrue(is_let(self.letexp))
        self.assertFalse(is_let(self.app))

    def test_let_bindings(self):
        "Test for `let_bindings`."
        self.assertEqual(let_bindings(self.letexp), self.letbindings)

    def test_let_body(self):
        "Test for `let_body`."
        self.assertEqual(let_body(self.letexp), self.letbody)

    def test_binding_parameter(self):
        "Test for `binding_parameter`"
        self.assertEqual(binding_parameter(self.binding), make_symbol("a"))

    def test_binding_argument(self):
        "Test for `binding_argument`."
        self.assertEqual(binding_argument(self.binding), make_fixnum(1))

    def test_bindings_parameters(self):
        "Test for `bindings_parameters`."
        self.assertEqual(bindings_parameters(self.bindings),
                         SCMRead(io.StringIO("(a b)")))

    def test_bindings_arguments(self):
        "Test for `bindings_arguments`."
        self.assertEqual(bindings_arguments(self.bindings),
                         SCMRead(io.StringIO("(1 2)")))

    def test_let_parameters(self):
        "Test for `let_parameters`."
        self.assertEqual(let_parameters(self.letexp),
                         bindings_parameters(self.bindings))

    def test_let_arguments(self):
        "Test for `let_arguments`."
        self.assertEqual(let_arguments(self.letexp),
                         bindings_arguments(self.bindings))

    def test_let_to_application(self):
        "Test for `let_to_application`."
        lambdaexp = make_lambda(bindings_parameters(self.letbindings),
                                self.letbody)
        self.assertEqual(let_to_application(self.letexp),
                         make_application(lambdaexp, self.letarguments))


class TestAndAndOr(unittest.TestCase):
    "Tests for and and or expression."
    def setUp(self):
        self.andexpt = SCMRead(io.StringIO("(and #t #t #t)")) # Returns true
        self.andtestst = SCMRead(io.StringIO("(#t #t #t)"))
        self.andexpf = SCMRead(io.StringIO("(and #f #t #t)")) # Returns false
        self.andtestsf = SCMRead(io.StringIO("(#f #t #t)"))
        self.orexpt = SCMRead(io.StringIO("(or #t #f #t)"))   # Returns true
        self.ortestst = SCMRead(io.StringIO("(#t #f #t)"))
        self.orexpf = SCMRead(io.StringIO("(or #f #f #f)"))   # Returns false
        self.ortestsf = SCMRead(io.StringIO("(#f #f #f)"))

    def test_is_and(self):
        "Test for `is_and`."
        self.assertTrue(is_and(self.andexpt))
        self.assertTrue(is_and(self.andexpf))
        self.assertFalse(is_and(self.orexpt))
        self.assertFalse(is_and(self.orexpf))

    def test_is_or(self):
        "Test for `is_or`."
        self.assertTrue(is_or(self.orexpt))
        self.assertTrue(is_or(self.orexpt))
        self.assertFalse(is_or(self.andexpt))
        self.assertFalse(is_or(self.andexpf))

    def test_and_tests(self):
        "Test for `and_tests`."
        self.assertEqual(and_tests(self.andexpt), self.andtestst)
        self.assertEqual(and_tests(self.andexpf), self.andtestsf)

    def test_or_tests(self):
        "Test for `or_tests`."
        self.assertEqual(or_tests(self.orexpt), self.ortestst)
        self.assertEqual(or_tests(self.orexpf), self.ortestsf)

    def test_eval(self):
        "Test for evaluate and and or expressions."
        self.assertIs(SCMEval(self.andexpt, SCMTheGlobalEnvironment), SCMTrue)
        self.assertIs(SCMEval(self.andexpf, SCMTheGlobalEnvironment), SCMFalse)
        self.assertIs(SCMEval(self.orexpt, SCMTheGlobalEnvironment), SCMTrue)
        self.assertIs(SCMEval(self.orexpf, SCMTheGlobalEnvironment), SCMFalse)


if __name__ == "__main__":
    unittest.main()
