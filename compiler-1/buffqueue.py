from collections import deque

class StreamBuf:
    def __init__(self, stream):
        self.stream = stream
        self.deque = deque()

    def pop(self):
        self.deque.appendleft(self.stream.read(1))
        try:
            r = self.deque.pop()
        except IndexError:
            return None
        return r

    def push(self, c):
        self.deque.append(c)



if __name__ == "__main__":
    import unittest, io

    class TestStreamBuf(unittest.TestCase):
        def setUp(self):
            s = io.StringIO("afv")
            self.d = StreamBuf(s)

        def test_pop(self):
            r = self.d.pop()
            self.assertEqual(r, "a")
            self.assertEqual("f", self.d.pop())
            self.assertEqual("v", self.d.pop())
            self.assertEqual('', self.d.pop())

        def test_push(self):
            self.d.push("a")
            self.d.push("b")
            self.assertEqual("b", self.d.pop())
            self.assertEqual("a", self.d.pop())

    unittest.main()
