import re
from random import randint

class TEST_MODULE:
	def __init__(self, parent):
		self.parent = parent
		self.test = "test"
		self.new_commands = {
			"big_test": self.testf,
			"simple_calc_test": self.simple_calc_test,
			"calc": self.calc,
			"bcalc|buffer_calc": self.buffer_calc,
			"show_var": self.show_var,
			"var_exist": self.var_exist,
			"error": self.error,
			"(go_)*wild": self.go_wild,
		}

		self.add_self()
		# or just 
		# self.parent.parser.commands.update(self.new_commands)
		# but I figured a function would be kinda better in special use cases

	def show_var(self, arg=None):
		s = ""
		for var in self.parent.buffer.highlighter.vars:
			s += var+"\n"
		self.parent.notify(s)

	def error(self, arg=None):
		self.parent.error(f"{arg}")

	def go_wild(self, arg=None):
		w = self.parent.winfo_width()
		h = self.parent.winfo_height()
		for w_ in self.parent.winfo_children():
			for w_1 in w_.winfo_children():
				try: w_1.place(x=randint(0, w), y=randint(0,h), width=randint(0,w), height=randint(0,h))
				except Exception: pass
				
			try: w_.place(x=randint(0, w), y=randint(0,h), width=randint(0,w), height=randint(0,h))
			except Exception: pass

	def var_exist(self, arg=None):
		if (not arg): self.parent.error("No arguments"); return
		s = ""
		for a in arg:
			if (a in self.parent.buffer.highlighter.vars):
				s += f"Var: {a} exists\n"

		self.parent.notify(s)

	def testf(self, arg=None):
		print(self.test)
		self.parent.command_out_set(f"{self.test}")
		self.parent.command_out.change_ex(self.do_sumn)

	def do_sumn(self, arg=None):
		self.parent.command_out_set(f"{arg}: bruh")

	def simple_calc_test(self, arg=None):
		if (not arg[1:]): self.parent.error("No arguments"); return
		arg = "".join(arg[1:]).strip(" ").split("+")
		self.parent.notify(f"{float(arg[0]) + float(arg[1])}")

	def get_expression(self, arg, i):
		for j in range(i+1, len(arg)):
			if (arg[j] == "("):
				a, x, y = self.get_expression(arg, i)
				arg[x:y] = self.eval(a)
			
			elif (arg[j] == ")"):
				print("get_expression: ", arg[i+1:j])
				return (arg[i+1:j], i+1, j)

	def eval(self, expression):
		print("expression: ", expression)
		ret = 0
		skip_start = 0
		skip_end = 0
		skip = False
		i = 0

		# while (i < len(expression)):
			# last = expression[i-1] if (i == 1) else ret
			# current = expression[i]
			# next = expression[i+1] if (i+1 < len(expression)) else None
			# if (next == "("):
				# skip=True
				# next, skip_start, skip_end = self.get_expression(expression, i+1)
				# next = self.eval(next)
			
			# if (current == "*"): ret = float(last) * float(next)
			# elif (current == "/"): ret = float(last) / float(next)
			# elif (current == "%"): ret = float(last) % float(next)
			# elif (current == "^"): ret = float(last) ** float(next)

			# if (skip):
				# i = skip_end; skip = False
			# else:
				# i += 1
		
		while (i < len(expression)):
			last = expression[i-1] if (i == 1) else ret
			current = expression[i]
			next = expression[i+1] if (i+1 < len(expression)) else None
			if (next == "("):
				skip=True
				next, skip_start, skip_end = self.get_expression(expression, i+1)
				next = self.eval(next)
			
			if (current == "+"): ret = float(last) + float(next)
			elif (current == "-"): ret = float(last) - float(next)

			if (skip):
				i = skip_end; skip = False
			else:
				i += 1

		return ret

	def calc(self, arg=None):
		if (not arg[1:]): self.parent.command_out_set("Error: No arguments"); return
		arg = "".join(arg[1:]).strip(" ")
		arg = re.split("([\+\-\*\/\%\^\(\)])", arg)
		for i in range(len(arg)-1):
			if (arg[i] == ""): arg.pop(i)
			
		self.parent.notify(f"{self.eval(arg)}")

	def buffer_calc(self, arg=None):
		if (not arg[1:]):
			arg=self.parent.buffer.get("1.0", "end-1c")
		else:
			try: arg=self.parent.file_handler.buffer_dict[arg[1:]].get("1.0", "end-1c")
			except Exception: arg=self.parent.buffer.get("1.0", "end-1c")

		self.calc(["bcalc", arg])

	def add_self(self):
		self.parent.parser.commands.update(self.new_commands)

		