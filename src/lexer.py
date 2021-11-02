import string
import re
import os

# how is this any more readable
az         = [*string.ascii_letters, "_"]
num        = string.digits
alphanum   = [*az, *num]
whitespace = [" ", "\t"]


class LEXER:
	def __init__(self, parent, txt):
		self.parent = parent
		self.buffer = txt

		# unsigned int eq(int a, int b) 
		# {
		#	return (unsigned int)(a == b);
		# }	

		# = type: unsigned int
		# name: eq
		# parameters: int a int b
		# local: None

		self.index = 0

		self.types = []
		self.modifiers = []
		self.keywords = ["if", "else", "while", "switch", "case"]
		self.vars = []
		self.functions = []
		self.objects  = []
		self.scopes  = {}

	def lex(self, text=None):
		# should iterate through characters make a token and then parse the token
		# I should probably just use tree sitter or something though
		if (text): self.text = text
		else: self.text = self.buffer.get("1.0", "end")
		self.row_index = 1
		self.column_index = 0


		self.in_whitespace = False
		self.in_comment = False
		self.line = ""
		self.prev_word = ""
		self.word = ""
		self.last_char = ""

		for self.index, char in enumerate(self.text, 0):
			if (self.in_comment):
				if (char == "\n"): self.in_comment = False
				else: continue

			if (self.in_whitespace):
				if (char not in whitespace):
					self.in_whitespace = False
					self.handle_separator()
					
			elif (char in whitespace):
				self.in_whitespace = True
				continue

			if (char == "\n"):
				self.handle_separator()

			elif ((not self.word and char in az) or (self.word and char in alphanum)):
				if (self.in_whitespace): self.in_whitespace = False; self.handle_separator()
				self.word += char

			elif (char == "="):
				self.make_var()

			elif (char == "("):
				self.make_function()

			elif (char in ["[", "]", "{", "}", ")", ";"]):
				self.prev_word = self.word = ""

			self.last_char = char
			# print("prev: ", self.prev_word, "word: ", self.word)

	def handle_separator(self):
		if (self.word == ""):
			return
		else:
			# print(f"word: {self.word} ({self.prev_word})")
			self.prev_word = self.word
			self.word = ""

	def make_var(self):
		# if (re.match(r"[a-zA-Z_][0-9_]+", self.prev_word) and re.match(r"[a-zA-Z_][0-9_]+", self.prev_word)):
		# w = f"{self.word} ({self.prev_word})"
		w = self.word
		# print("making var: ", w)
		if ((w not in self.vars) and (self.word not in self.keywords)):
			self.vars.append(w)

	def make_function(self):
		# w = f"{self.word} ({self.prev_word})"
		w = self.word
		# print("making func: ", w)
		if ((w not in self.functions) and (self.word not in self.keywords)):
			self.functions.append(w)

	# def check_keyword(self):
		# return self.word in self.keywords

	def print_res(self):
		print("FNCS: ", self.functions)
		print("OBJS: ", self.objects)
		print("VARS: ", self.vars)
		s = "FNCS: \n"
		for word in self.functions:
			s += "\t"+word+"\n"
		s += "OBJS: \n"
		for word in self.objects:
			s += "\t"+word+"\n"
		s += "VARS: \n"
		for word in self.vars:
			s += "\t"+word+"\n"

		# self.parent.command_out_set(s)

class PY_LEXER(LEXER):
	""" basic lexing """
	def __init__(self, parent, txt):
		super().__init__(parent, txt)

	def lex(self, text=None):
		if (text): self.text = text
		else: self.text = self.buffer.get("1.0", "end-1c")
		row_index = 1
		char_index = 0

		in_comment = False
		
		brackets = {
			"(": 0,
			"[": 0,
			"{": 0,
		}

		line = []
		prev_word = ""
		word = ""

		for self.index, char in enumerate(self.text, 0):
			if (in_comment):
				if (char == "\n"): in_comment = False
				else: continue 

			if (char == " " or char == "\t"):
				self.make_func(prev_word, word)
					
				line.append(word)
				prev_word = word
				word = ""
				
			elif (char == "\n"):
				self.make_func(prev_word, word)
				line = []
				prev_word = ""
				word = ""
				
				row_index += 1
				char_index = 0
				continue

			elif (char == "#"):
				in_comment = True

			elif (char in az):
				word += char

			elif (word and char in num):
				word += char

			elif (char in ("(", "[", "{")):
				brackets[char] = brackets[char]+1
				if (char == "("):
					self.make_func(prev_word, word)

				prev_word = word
				word = ""

			elif (char == "."):
				line.append(word)
				word = ""
				
			elif (char == "="):
				self.make_var(prev_word, word)

				word = ""
				prev_word = word

			# elif (char in (")", "]", "}")):
				# brackets[char] = brackets[char]-1

			char_index += 1

	def print_res(self):
		print("FNCS: ", self.functions)
		print("OBJS: ", self.objects)
		print("VARS: ", self.vars)

	def make_func(self, prev_word, word):
		if (prev_word == "def"):
			self.functions.append(word)

		elif (prev_word == "class" or prev_word == "import"):
			self.objects.append(word)

	def make_var(self, prev_word, word):
		if (self.text[self.index+1] != "="): self.vars.append(word)


class C_LEXER(LEXER):
	def __init__(self, parent, txt):
		super().__init__(parent, txt)
		self.indexed_files = []

	def lex(self, text=None):
		if (text): self.text = text
		else: self.text = self.buffer.get("1.0", "end-1c")
		self.file_queue = []
		
		row_index = 1
		char_index = 0
		in_comment = False
		in_multiline_comment = False
		in_quote = False # "
		in_quote_ = False # '
		
		brackets = {
			"(": 0,
			"[": 0,
			"{": 0,
		}

		line = []	
		prev_word = ""
		word = ""

		last_index = ""
		index = ""

		for self.index in range(len(self.text)-1):
			char = self.text[self.index]
			if (in_comment):
				if (char == "\n"): in_comment = False
				else: continue

			if (char == " " or char == "\t"):
				# if (self.text[self.index+1] == "="): self.make_var(prev_word, word, index=self.index+1)
				if (self.search_whitespace(self.index+1)):
					line.append(word)
					prev_word = word
					word = ""

			elif (char == ","):
				line.append(word)
				prev_word = word
				word = ""

			elif (char == "\""):
				in_quote = not in_quote
				continue

			elif (char == "\'"):
				in_quote_ = not in_quote_
				continue
				
			elif (char == "\n"):
				if (prev_word and prev_word[0] == "#"):
					prev_word = word
					word = ""

				row_index += 1
				char_index = 0
				continue

			elif (char == "/"):
				if (self.text[self.index+1] == "/"):
					
					in_comment = True
				elif (self.text[self.index+1] == "*"): in_multiline_comment = not in_multiline_comment

			elif (not word and char == "#"):
				word += char
				self.add_file_to_queue()

			elif (char in az):
				word += char

			elif (word and char in num):
				word += char

			elif (char in ("(", "[", "{")):
				brackets[char] = brackets[char]+1
				if (char == "(" or char == "{"):
					self.make_func(prev_word, word)

				prev_word = word
				word = ""

			elif (char == "."):
				line.append(word)
				word = ""

			elif (char == "="):
				self.make_var(prev_word, word)

				word = ""
				prev_word = word

			elif (char == ";"):
				pass
				
			char_index += 1

		for object in self.objects:
			if (object not in self.buffer.highlighter.keywords): self.buffer.highlighter.keywords.append(object)

		# self.parent.command_out_set("lex finished")

		file_queue = self.file_queue
		for file in file_queue:
			if (file not in self.indexed_files):
				self.indexed_files.append(file)
				# self.parent.command_out_set(f"file {file} is a file")
				file = f"{os.path.dirname(self.buffer.full_name)}/{file}"
				if (os.path.isfile(file)):
					self.lex(text=open(file, "r").read())
			

		# self.print_res()

	def print_res(self):
		print("FNCS: ", self.functions)
		print("OBJS: ", self.objects)
		print("VARS: ", self.vars)

		s = "FNCS: \n"
		for word in self.functions:
			s += "\t"+word+"\n"

		s += "OBJS: \n"
		for word in self.objects:
			s += "\t"+word+"\n"

		self.parent.command_out_set(s)

	def add_file_to_queue(self):
		word = ""
		for char in self.text[self.index:]:
			if (char in az or char == "/" or char == "\\" or char == "."):
				word += char
			elif (char == " "):
				if (word != "include"): return
				else: word = ""
			elif (char == "\n"):
				break

		# self.parent.command_out_set(f"file {word} was added to queue")
		if (word not in self.indexed_files): self.file_queue.append(word)


	def search_whitespace(self, index) -> bool:
		for char in self.text[index:]:
			if (char == " " or char == "\t"):
				pass
			elif (char == "\n"):
				return False
			else:
				return True

	def add_object(self, name):
		if (name and name not in self.objects):
			self.objects.append(name)

	def add_function(self, name):
		if (name and name not in self.functions):
			self.functions.append(name)

	def add_var(self, name):
		if (name and name not in self.vars):
			self.vars.append(name)


	def make_func(self, prev_word, word):
		if (prev_word == "#define"):
			self.add_object(word)
			
		elif (prev_word == "struct"):
			self.add_object(word)

		elif (word == "struct"):
			self.add_object(self.get_struct_name())

		elif (self.text[self.index] == "("):
			self.add_function(word)

	def make_var(self, prev_word, word, override=False, index=None):
		if (not index): index = self.index
		if (self.text[index+1] != "="): self.add_var(word)
		if (override): self.add_var(word)

	def get_scope(self, type, name, index):
		pass		

	def get_struct_name(self):
		#haahah I have no idea what the fuck I am doing
		brackets = 0
		word = ""
		for index, char in enumerate(self.text[self.index:], self.index):
			if (char == "{"):
				brackets += 1

			elif (char == "}"):
				brackets -= 1
				if (brackets == 0):
					for char in self.text[index:]:
						if (char in az):
							word += char
						elif (word and char in num):
							word += char
						elif (char == ";" and word != ""):
							return word
						elif (char == "\n"):
							self.buffer.tag_add("error_bg", f"1.0+{index}c")
							return None

			self.buffer.tag_remove("error_bg", f"1.0+{index}c")
