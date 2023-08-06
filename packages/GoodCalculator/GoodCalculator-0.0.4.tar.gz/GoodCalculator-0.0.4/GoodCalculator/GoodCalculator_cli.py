from GoodCalculator.calculator import Calculator
import sys

def run_cli():
	calc = Calculator()

	equ = ''
	for arg in sys.argv[1:]:
		equ += arg

	if equ == '':
		print("Empty input")
	else:
		calc.parse_equation(equ)
		calc.evaluate()

if __name__ == "__main__":
	run_cli()