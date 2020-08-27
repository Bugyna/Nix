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
		elif (lang == "py"):
			self.keywords = self.Py_keywords
			self.highlight = self.python_highlight

		self.other_chars = ["$","#","@","&","|","^","_","\\",r"\\",r"\[\]",r"[\\]"]
		# all_key = [keywords, other_chars]
		# all_key = list(chain.from_iterable(all_key))
		self.txt = text
		self.theme = theme

		self.countingQuomarks = False
		self.Quomark_count = 0



	# def sumn(self, st, index):
	# 	index1 = 0
	# 	for current_char in st:
	# 		if (re.match(r"[a-zA-Z]", current_char)):


	def python_highlight(self, line_no ,line=None):
		if line == None:
			line = self.txt.get(float(line_no), "end")

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		pattern = ""
		self.txt.tag_remove(self.theme["quotes"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["functions"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["keywords"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["numbers"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["special_chars"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["comments"], last_separator, f"{line_no}.{len(line)}")
		
		for i, current_char in enumerate(line, 0):
			index = f"{line_no}.{i}"
			# if (i == 0):
			# 	self.countingQuomarks = False
			
			if (re.match(r"[\"\']", current_char)):
				self.txt.tag_add(self.theme["quotes"], index)
				self.countingQuomarks = not self.countingQuomarks
				pattern = ""
			
			elif (self.countingQuomarks):
				continue

			elif (re.match(r"[a-zA-Z]", current_char)):
				pattern += current_char
			
			elif (re.match(r"[\s\.\,\:\(]", current_char)):
				if (pattern in self.keywords):
					self.txt.tag_add(self.theme["keywords"], last_separator, index)

				elif (re.match(r"\(", current_char)):
					self.txt.tag_add(self.theme["functions"], last_separator, index)
					
				last_separator_index = i+1
				last_separator = f"{line_no}.{i+1}"
				pattern = ""


			elif (re.match(r"[0-9]", current_char)): #numbers
				self.txt.tag_add(self.theme["numbers"], index) 
				pattern = ""
			
			elif (re.match(r"[\-\+\*\/\%\^\&\|\=\[\]\{\}]", current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				self.txt.tag_add(self.theme["special_chars"], index)
				pattern = ""

			elif (re.match(r"[\#]", current_char)): #comments
				self.txt.tag_add(self.theme["comments"], index, f"{line_no}.{i+1000}")
				break


	def C_highlight(self, line_no, line=None):
		if line == None:
			line = self.txt.get(float(line_no), "end")


		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		pattern = ""

		self.txt.tag_remove(self.theme["quotes"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["functions"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["keywords"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["numbers"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["special_chars"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["comments"], last_separator, f"{line_no}.{len(line)}")
		
		for i, current_char in enumerate(line, 0):
			index = f"{line_no}.{i}"
			if (i == 0):
				self.countingQuomarks = False

			# if (re.match(r'"', current_char)):
			#     self.Quomark_count = len(re.findall(current_char, self.txt.get(line_no+".0", "end")))


			#     if self.countingQuomarks and self.Quomark_count % 2 == 0:
			#         self.countingQuomarks = False 
			#     else:
			#         self.countingQuomarks = True
			# if (re.findall(r'"', self.txt.get(line_no+".0", "end")) % 2 == 0):

			try:
				if (re.match(r"//", current_char+line[i+1])): #comments
					self.txt.tag_add(self.theme["comments"], index, f"{line_no}.{i+1000}")
					break

			except Exception:
				pass

			if (re.match(r"[\"\']", current_char)):
				self.txt.tag_add(self.theme["quotes"], index)
				self.countingQuomarks = not self.countingQuomarks
				pattern = ""
			
			elif (self.countingQuomarks):
				continue

			elif (re.match(r"[a-zA-Z]", current_char)):
				pattern += current_char
			
			elif (re.match(r"[\s\.\,\:\(]", current_char)):
				if (pattern in self.keywords):
					self.txt.tag_add(self.theme["keywords"], last_separator, index)

				elif (re.match(r"\(", current_char)):
					self.txt.tag_add(self.theme["functions"], last_separator, index)
					
				last_separator_index = i+1
				last_separator = f"{line_no}.{i+1}"
				pattern = ""


			elif (re.match(r"[0-9]", current_char)): #numbers
				self.txt.tag_add(self.theme["numbers"], index) 
				pattern = ""
			
			elif (re.match(r"[\-\+\*\/\%\^\&\|\=\[\]\{\}]", current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				self.txt.tag_add(self.theme["special_chars"], index)
				pattern = ""


	def unhighlight(self, line_no, line=None):
		if line == None:
			line = self.txt.get(float(line_no), "end")

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		
		self.txt.tag_remove(self.theme["quotes"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["functions"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["keywords"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["numbers"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["special_chars"], last_separator, f"{line_no}.{len(line)}")
		self.txt.tag_remove(self.theme["comments"], last_separator, f"{line_no}.{len(line)}")