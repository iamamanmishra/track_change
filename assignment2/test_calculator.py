import unittest

from calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(self.calculator.add(3, 4), 7)

    def test_subtract(self):
        self.assertEqual(self.calculator.subtract(5, 2), 3)

    def test_multiply(self):
        self.assertEqual(self.calculator.multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(self.calculator.divide(8, 2), 4)
        with self.assertRaises(ValueError):
            self.calculator.divide(5, 0)

    def test_square_root(self):
        self.assertEqual(self.calculator.square_root(25), 5)
        with self.assertRaises(ValueError):
            self.calculator.square_root(-9)

    def test_power(self):
        self.assertEqual(self.calculator.power(2, 3), 8)
        self.assertEqual(self.calculator.power(5, 0), 1)

    def test_logarithm(self):
        self.assertEqual(self.calculator.logarithm(2, 8), 3)
        with self.assertRaises(ValueError):
            self.calculator.logarithm(1, 5)
            self.calculator.logarithm(2, -1)

    def test_sin(self):
        self.assertAlmostEqual(self.calculator.sin(30), 0.5, places=5)

    def test_cos(self):
        self.assertAlmostEqual(self.calculator.cos(60), 0.5, places=5)

    def test_tan(self):
        self.assertAlmostEqual(self.calculator.tan(45), 1, places=5)
        with self.assertRaises(ValueError):
            self.calculator.tan(90)

if __name__ == "__main__":
    unittest.main()