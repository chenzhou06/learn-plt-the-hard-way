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



if __name__ == "__main__":
    unittest.main()
