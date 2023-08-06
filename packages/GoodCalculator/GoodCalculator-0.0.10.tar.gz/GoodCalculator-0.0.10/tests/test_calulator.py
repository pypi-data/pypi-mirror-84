from unittest import TestCase
from GoodCalculator.calculator import Calculator

class CalculatorTestCase(TestCase):
	# function name start with "test"
	def test_add_num(self):
		calc = Calculator()
		calc.parse_equation("1+1")
		result = calc.evaluate()
		self.assertEqual(result, 2)

	def test_subtract_num(self):
		calc = Calculator()
		calc.parse_equation("2-1")
		result = calc.evaluate()
		self.assertEqual(result, 1)

	def test_multiply_num(self):
		calc = Calculator()
		calc.parse_equation("2*3")
		result = calc.evaluate()
		self.assertEqual(result, 6)

	def test_divide_num(self):
		calc = Calculator()
		calc.parse_equation("8/2")
		result = calc.evaluate()
		self.assertEqual(result, 4)
