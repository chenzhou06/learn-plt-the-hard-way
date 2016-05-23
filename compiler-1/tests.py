from scheme import SCMRead, make_fixnum, peek
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

    def test_peek(self):
        s = io.StringIO("abcdasdfasdf")
        c = peek(s)
        c2 = peek(s)
        print(c)
        print(c2)
        print("".join([c for c in s]))
        self.assertEqual(c, c2)
        self.assertEqual(s.read(1), "a")
        self.assertEqual(s.read(1), "b")

if __name__ == "__main__":
    unittest.main()
