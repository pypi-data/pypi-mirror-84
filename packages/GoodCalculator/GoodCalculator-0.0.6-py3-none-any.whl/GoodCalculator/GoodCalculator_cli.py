from GoodCalculator.calculator import Calculator
# import sys
import click

@run_cli.command()
@click.argument('equation')
def run_cli(equation):
	calc = Calculator()
	# equation = ''
	# for arg in sys.argv[1:]:
	# 	equation += arg
	if equation == '':
		print("Empty input")
	else:
		calc.parse_equation(equation)
		click.echo(calc.evaluate())

if __name__ == "__main__":
	run_cli()