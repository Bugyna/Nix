import re
from itertools import chain




class highlighter():
	def __init__(self, text, theme, lang):
		self.Py_keywords = [
			'False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in',
			'raise', 'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for',
			'lambda', 'try', 'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del',
			'global', 'not', 'with', 'async', 'elif', 'if', 'or', 'yield', "self"
			]

		self.C_keywords = [
			'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
		 	'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
		  	'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
   		]
		
		self.keywords = []
		
		if (lang == "c"):
			self.keywords = self.C_keywords
			self.highlight = self.C_highlight
			self.commment_regex = re.compile(r"[//]")
		elif (lang == "py"):
			self.keywords = self.Py_keywords
			self.highlight = self.python_highlight
			self.commment_regex = re.compile(r"[\#]")

		self.other_chars = ["$","#","@","&","|","^","_","\\",r"\\",r"\[\]",r"[\\]"]

		self.txt = text
		self.theme = theme

		self.countingQuomarks = False
		self.Quomark_count = 0

		self.quote_regex = re.compile(r"[\"\']")
		self.abc_regex = re.compile(r"[a-zA-Z]")
		self.separator_regex = re.compile(r"[\s\.\,\(\)]")
		self.num_regex = re.compile(r"[0-9]")
		self.special_char_regex = re.compile(r"[\{\}\&\^\|]")
		self.equal_regex = re.compile(r"[\=]")
		self.operator_regex = re.compile(r"[\%\+\-\*\/]")
		self.string_special_char_regex = re.compile(r"[\\{\}]")
		
	def get_line_lenght(self, line_no):
		for i, char in enumerate(self.txt.get(float(line_no), "end"), 0):
			if (re.match(r"\n", char)):
				return f"{line_no}.{i}"

	def python_highlight(self, line_no ,line=None):
		if line == None:
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))
			# print(line)

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)}"
		self.pattern = ""
		
		self.txt.tag_remove(self.theme["functions"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["keywords"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["numbers"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["special_chars"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["comments"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["operators"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["quotes"], last_separator, line_end_index)
		
		for i, current_char in enumerate(line, 0):
			index = f"{line_no}.{i}"
			if (i == 0):
				self.countingQuomarks = False
			
			if (self.quote_regex.match(current_char)):
				self.txt.tag_add(self.theme["quotes"], index)
				if (self.countingQuomarks):
					self.countingQuomarks = False
				else:
					self.countingQuomarks = True
				# self.countingQuomarks = not self.countingQuomarks

			elif (self.countingQuomarks):
				self.txt.tag_add(self.theme["quotes"], index)
				continue
			
			elif (self.abc_regex.match(current_char)):
				self.pattern += current_char
				continue
			
			elif (self.separator_regex.match(current_char)):
				# print(self.pattern)
				if (re.match(r"\(", current_char)):
					self.txt.tag_add(self.theme["functions"], last_separator, index)
				elif (self.pattern in self.keywords):
					self.txt.tag_add(self.theme["keywords"], last_separator, index)
					
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.pattern = ""
				continue

			elif (self.commment_regex.match(current_char)): #comments
				self.txt.tag_add(self.theme["comments"], index, line_end_index)
				break

			elif (self.num_regex.match(current_char)): #numbers
				if (self.pattern == ""):
					self.txt.tag_add(self.theme["numbers"], index)
					self.pattern = ""
				else:
					self.pattern += current_char
				continue
			
			elif (self.operator_regex.match(current_char)):
				self.txt.tag_add(self.theme["operators"], index)
				self.pattern = ""
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				self.txt.tag_add(self.theme["special_chars"], index)
				self.pattern = ""
				continue
				
			elif (self.equal_regex.match(current_char)):
				self.txt.tag_add(self.theme["operators"], index)
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.pattern = ""

	def C_highlight(self, line_no, line=None):
		if line == None:
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)}"
		self.pattern = ""

		self.txt.tag_remove(self.theme["quotes"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["functions"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["keywords"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["numbers"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["special_chars"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["comments"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["operators"], last_separator, line_end_index)
		
		
		for i, current_char in enumerate(line, 0):
			index = f"{line_no}.{i}"
			if (i == 0):
				self.countingQuomarks = False


			try:
				if (self.commment_regex.match(r"//", current_char+line[i+1])): #comments
					self.txt.tag_add(self.theme["comments"], index, line_end_index)
					break

			except Exception:
				pass

			if (self.quote_regex.match(current_char)):
				self.txt.tag_add(self.theme["quotes"], index)
				if (self.countingQuomarks):
					self.countingQuomarks = False
				else:
					self.countingQuomarks = True
				# self.countingQuomarks = not self.countingQuomarks

			elif (self.countingQuomarks):
				self.txt.tag_add(self.theme["quotes"], index)
				# last_separator_index = i+2
				# last_separator = f"{line_no}.{last_separator_index}"
				# i = last_separator_index
				# if (self.string_special_char_regex.match(current_char)):
				# 	self.txt.tag_add(self.theme["special_chars"], index, last_separator)	
				# else:
				# 	self.txt.tag_add(self.theme["quotes"], index)
				continue
			
			elif (self.abc_regex.match(current_char)):
				self.pattern += current_char
				continue
			
			elif (self.separator_regex.match(current_char)):
				# print(self.pattern)
				if (re.match(r"\(", current_char)):
					self.txt.tag_add(self.theme["functions"], last_separator, index)
				elif (self.pattern in self.keywords):
					self.txt.tag_add(self.theme["keywords"], last_separator, index)
					
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.pattern = ""
				continue

			elif (self.commment_regex.match(current_char)): #comments
				self.txt.tag_add(self.theme["comments"], index, f"{line_no}.{i+1000}")
				break

			elif (self.num_regex.match(current_char)): #numbers
				if (self.pattern == ""):
					self.txt.tag_add(self.theme["numbers"], index)
					self.pattern = ""
				else:
					self.pattern += current_char
				continue

			elif (self.operator_regex.match(current_char)):
				self.txt.tag_add(self.theme["operators"], index)
				self.pattern = ""
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				self.txt.tag_add(self.theme["special_chars"], index)
				self.pattern = ""
				continue
				
			elif (self.equal_regex.match(current_char)):
				self.txt.tag_add(self.theme["operators"], index)
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.pattern = ""
				

	def unhighlight(self, line_no, line=None):
		if line == None:
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)}"
		
		self.txt.tag_remove(self.theme["quotes"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["functions"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["keywords"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["numbers"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["special_chars"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["comments"], last_separator, line_end_index)
		self.txt.tag_remove(self.theme["operators"], last_separator, line_end_index)