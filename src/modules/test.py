class TEST_MODULE:
	def __init__(self, parent):
		self.parent = parent
		self.test = "test"
		self.new_commands = {
			"big_test": self.testf,
		}

		self.add_self()
		# or just 
		# self.parent.parser.commands.update(self.new_commands)
		# but I figured a function would be kinda better in special use cases

	def testf(self, arg=None):
		print(self.test)
		self.parent.command_out_set(f"{self.test}")
		self.parent.command_out.change_ex(self.do_sumn)

	def do_sumn(self, arg=None):
		self.parent.command_out_set(f"{arg}: bruh")

	def add_self(self):
		self.parent.parser.commands.update(self.new_commands)