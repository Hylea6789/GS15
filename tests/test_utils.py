import unittest
from utils import exponentiation_rapide, bourrage_zero


class ExponentiationTest(unittest.TestCase):
    def test_simple(self):
        res = exponentiation_rapide(25, 6, 18)
        self.assertEqual(res, (25**6) % 18)


class BourrageZeroTest(unittest.TestCase):
    def test_simple(self):
        res = bourrage_zero("101", 5)
        self.assertEqual(res, "00101")

    def test_lower_size(self):
        res = bourrage_zero("101", 1)
        self.assertEqual(res, "101")

    def test_size_zero(self):
        res = bourrage_zero("101", 0)
        self.assertEqual(res, "101")

    def test_empty_string(self):
        self.assertRaises(ValueError, lambda: bourrage_zero("", 5))

    def test_prefixed_with_zeros(self):
        res = bourrage_zero("00110", 7)
        self.assertEqual(res, "0000110")

    def test_not_binary(self):
        self.assertRaises(ValueError, lambda: bourrage_zero("001190", 7))

    def test_int(self):
        res = bourrage_zero(0b11001100, 10)
        self.assertEqual(res, "0011001100")
