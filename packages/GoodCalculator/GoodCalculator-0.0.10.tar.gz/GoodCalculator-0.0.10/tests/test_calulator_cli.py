from unittest import TestCase
from click.testing import CliRunner
from GoodCalculator.GoodCalculator_cli import run_cli

class TestConsole(TestCase):
	def test_basic(self):
		runner = CliRunner()
		result = runner.invoke(run_cli, "1+2+2")
		self.assertEqual(float(result.output), 5)