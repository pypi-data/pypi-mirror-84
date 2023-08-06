from GoodCalculator.goodOperator import Operator

############################################
#	Calculator object
############################################
class Calculator():
	def __init__(self):
		self.equation_list = []
		self.equation_result = 0.0
		self.operator_map = [
			['<-', '<backspace>'],
			['1/x', '<reciprocal>'],
			['x^2', '<square>'],
			['sqrt(x)', '<sqrt>'],
			['+', '<add>'],
			['-', '<subtract>'],
			['*', '<multiply>'],
			['/', '<divide>'],
			['%', '<percentage>'],
			['=', '<equal>'],
		]
		self.operator_tag = [self.operator_map[i][1] for i in range(len(self.operator_map))]
		# initialize operator object
		self.operator = Operator()

	def parse_equation(self, equation):
		# replace symbol to tag
		for i in range(len(self.operator_map)):
			equation = equation.replace(self.operator_map[i][0],' '+self.operator_map[i][1]+' ')

		# remove empty string
		self.equation_list = equation.split(' ')
		while('' in self.equation_list): self.equation_list.remove('')

		# oprand to float
		for i in range(len(self.equation_list)):
			if self.equation_list[i] not in self.operator_tag:
				self.equation_list[i] = float(self.equation_list[i])

		# first negative number
		if not isinstance(self.equation_list[0], float):
			self.equation_list.pop(0)
			self.equation_list[0] = -self.equation_list[0]

		# negative sign after binary operator and right in the equation
		del_operator_idx = []
		for i in range(len(self.operator.binary_operator)):
			for j in range(len(self.equation_list)):
				if self.operator.binary_operator[i] == self.equation_list[j] and self.equation_list[j+1] == '<subtract>':
					del_operator_idx.append(j+1)
					self.equation_list[j+2] = -self.equation_list[j+2]
		temp = []
		for i in range(len(self.equation_list)):
			if i not in del_operator_idx:
				temp.append(self.equation_list[i])
		self.equation_list = temp

	def evaluate(self):
		# get oprand and oprator list
		oprand_list = []
		oprator_list = []
		for e in self.equation_list:
			if isinstance(e, float):
				oprand_list.append(e)
			else:
				oprator_list.append(e)

		# evaluate result
		for op in oprator_list:
			if self.operator.op_type(op) == 'binary':
				result = self.operator.binary_op_evaluate(op,oprand_list.pop(0),oprand_list.pop(0))
				oprand_list.insert(0, result)
			elif self.operator.op_type(op) == 'unary':
				result = self.operator.unary_op_evaluate(op,oprand_list.pop(0))
				oprand_list.insert(0, result)
			elif self.operator.op_type(op) == 'equal':
				pass
			else:
				raise ValueError("Invalid oprator!")
		
		print(oprand_list[0])

