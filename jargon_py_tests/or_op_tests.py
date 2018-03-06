import unittest

from jargon_py import OrOp


class OrOpTests(unittest.TestCase):

    def test_or_op_simple(self):
        or_op = OrOp()
        or_op.left = lambda x: x == 1
        or_op.right = lambda x: x == 2

        self.assertTrue(or_op.execute(1))
        self.assertTrue(or_op.execute(2))
        self.assertFalse(or_op.execute(3))

    def test_left_or_op(self):
        left_or_op = OrOp()
        left_or_op.left = lambda x: x == 'A'
        left_or_op.right = lambda x: x == 'B'

        or_op = OrOp()
        or_op.left = left_or_op
        or_op.right = lambda x: x == 'C'

        self.assertTrue(or_op.execute('A'))
        self.assertTrue(or_op.execute('B'))
        self.assertTrue(or_op.execute('C'))
        self.assertFalse(or_op.execute('D'))

if __name__ == '__main__':
    unittest.main()
