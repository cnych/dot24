# -*- coding: utf-8 -*-
import unittest
from dot24 import *


class TestDot24(unittest.TestCase):
    def setUp(self):
       self.seq1 = [3, 3, 6, 6]
       self.noseq = [3, 2, 3, 4]
       self.seq2 = [5, 5, 6, 6]
       self.seq3 = [3, 3, 6, 6, 2]

    def test_poland(self):
        print '======test poland start======'
        expr = ['3', '6', '6', '3', '/', '+', '*']
        val = 3 * (6 + 6 / 3)
        self.assertEquals(poland(expr), val)
        print '======test poland end======'

    def test_unpoland(self):
        print '======test unpoland start======'
        expr = ['3', '6', '6', '3', '/', '+', '*']
        self.assertEquals(unpoland(expr), ['3 * (6 + (6 / 3))'])
        print '======test unpoland end======'

    def test_calculate(self):
        print '======test calculate start======'
        print calculate(self.seq1, 24)
        print calculate(self.noseq, 12)
        print calculate(self.seq2, 24)
        print calculate(self.seq3, 26)
        print '======test calculate end======'


if __name__ == '__main__':
    unittest.main()
