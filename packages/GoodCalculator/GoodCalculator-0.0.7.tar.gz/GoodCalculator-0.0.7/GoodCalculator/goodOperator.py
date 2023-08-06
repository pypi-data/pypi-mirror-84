############################################
#	Operator object
############################################
class Operator():
	def __init__(self):
		self.binary_operator = ['<add>','<subtract>','<multiply>','<divide>']
		self.unary_operator = ['<backspace>','<reciprocal>','<square>','<sqrt>','<percentage>']
		self.equal_operator = ['<equal>']

	def op_type(self, op):
		if op in self.binary_operator:
			return 'binary'
		elif op in self.unary_operator:
			return 'unary'
		elif op in self.equal_operator:
			return 'equal'
		else:
			return None

	def binary_op_evaluate(self, op, left, right):
		if op == '<add>':
			return left + right
		elif op == '<subtract>':
			return left - right
		elif op == '<multiply>':
			return left * right
		elif op == '<divide>':
			return left / right

	def unary_op_evaluate(self, op, left):
		if op == '<backspace>':
			return float(int(left/10))
		elif op == '<reciprocal>':
			return 1 / left
		elif op == '<square>':
			return left ** 2
		elif op == '<sqrt>':
			return left ** (1/2)
		elif op == '<percentage>':
			return left / 100


