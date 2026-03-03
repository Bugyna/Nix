import string
import re
import os
import threading
import pickle
import tempfile




# how is this any more readable
az         = string.ascii_letters + "_"
num        = string.digits
alphanum   = az + num
whitespace = " \t\n\r"
# operators = "+-*/"
logic_operators = "!=<>"
operators_text = "+-=|<>./?*%^&!~:"
operators = re.compile(r"^[+-=|<>./?*%^&!~:]+$")
separator = re.compile(r"[.;]|(->)|(::)")
brackets = "()[]{}"
left_brackets = "([{"
right_brackets = ")]}"
special_char_regex = re.compile(r"[\$\@\\]+")
brackets_regex = re.compile(r"[\{\}\[\]\(\)]+")
upcase_regex = re.compile(r"^[A-Z_][A-Z_]+$")
word_regex = re.compile(r"[_A-Za-z][_A-Za-z0-9]*")
colon = ":"
semicolon = ";"
dot = "."
comma = ","
single_quote = "'"
double_quote = "\""
hashtag = "#"

# lock = threading.Lock()

class __LEXER:
	def __init__(self, parent, buffer_widget, lang_type="c"):
		self.parent = parent
		self.buffer = buffer_widget
		self.defines = {}
		self.function_regex = re.compile(r"(([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]+)*([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*[\[\]\*]*[\ \t]+))([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*)(\((.*\n*)*\))")

		self.text = ""
		self.indexed_files = []
		self.row = 0
		self.column = 1
		self.file_queue = set()
		self.to_index = []

		self.functions = {}
		self.vars = {}
		self.objs = {}
		self.defines = {}

		self.curr_file = ""
		self.keywords = []
		self.logical_keywords = []
		self.numerical_keywords = []
		self.special_keywords = []

		self.force_multiline_comment = False

		self.scopes = {
			"global": {
				
			}
		}
		self.current_scope = self.scopes["global"]

		self.current_scope_location = []


		self.comment_sign = "#"
		self.multiline_comment_sign = ""
		self.multiline_comment_sign_end = ""
		# self.multiline_sign = "/*"
		# self.multiline_sign_end = "*/"

		self.build_argv = ["make"]
		self.run_argv = ["./main"]
		
		self.available_languages = ["c", "cpp", "php", "py", "html", "rs", "hs"]

		# self.index_extern = False
		self.index_extern = True

		self.index = 0

		self.types = []
		self.modifiers = []

		self.identifier = r"\b[a-zA-Z_]+[a-zA-Z_0-9_]*\b"
		self.statement = {
			"keywords" : r"\b(for|while|if|else|case|switch|do|elif)",
			"rule" : "newline",
		}

		self.set_language(lang_type)



	def set_language(self, lang_type):
		print("LEXER,, setting language:", lang_type)
		if (type(lang_type) == list): lang_type = lang_type[0]

		if (lang_type in ["c", "h", "cpp", "hpp", "cc", "hh"]):
			lang_type = "c"
			self.keywords = [
				'auto', 'char', 'default', 'double',
			 	'float', 'int', 'long', 'return', 'short', 'sizeof',
					'struct', 'union', 'void',
				"size_t", "u8", "u16", "u32", "u64", "bool",
		 		]
	
			self.numerical_keywords = [
				"false", "true", "enum", "NULL", 'signed', 'unsigned'
			]
	
			self.logical_keywords = [
				"switch", "case", "if", "else", "goto", "for", "while", 'continue', 'break', 'do'
			]

			self.special_keywords = [
				"asm", "__attribute__", "const", "extern", "volatile",
				'typedef', 'static', 'register'
			]

			self.build_argv = ["make"]
			self.run_argv = ["./main"]

			self.comment_sign = "//"
			self.multiline_comment_sign = "/*"
			self.multiline_comment_sign_end = "*/"

		elif (lang_type in ["cpp", "hpp", "cc", "hh", "ino"]):
			self.keywords = [
				"alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool", "break", "case",
				 "catch", "char", "char8_t", "char16_t", "char32_t", "class", "compl", "concept", "const", "const_cast",
				 "consteval", "constexpr", "constint", "continue", "co_await", "co_return", "co_yield", "decltype",
				 "default", "delete", "do", "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern",
				 "false", "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace", "new",
				 "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "register",
				 "reinterpret_cast", "requires", "return", "short", "signed", "sizeof", "static", "static_assert", "static_cast",
				 "struct", "switch", "template", "this", "thread_local", "throw", "true", "try", "typedef", "typeid", "typename",
				 "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"
			]

			self.numerical_keywords = [
				"false", "true", "enum", "NULL", 
			]
	
			self.logical_keywords = [
				"switch", "case", "if", "else", "goto", "for", "while"
			]

			self.special_keywords = [
				"asm", "__attribute__", "const", "extern", "volatile", "internal", "private", "public"
			]

			self.comment_sign = "//"
			self.multiline_comment_sign = "/*"
			self.multiline_comment_sign_end = "*/"

		elif (lang_type in ["cs"]):
			self.keywords = [
				"alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool", "break", "case",
				 "catch", "char", "char8_t", "char16_t", "char32_t", "class", "compl", "concept", "const", "const_cast",
				 "consteval", "constexpr", "constint", "continue", "co_await", "co_return", "co_yield", "decltype",
				 "default", "delete", "do", "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern",
				 "false", "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace", "new",
				 "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "register",
				 "reinterpret_cast", "requires", "return", "short", "signed", "sizeof", "static", "static_assert", "static_cast",
				 "struct", "switch", "template", "this", "thread_local", "throw", "true", "try", "typedef", "typeid", "typename",
				 "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"
			]

			self.numerical_keywords = [
				"false", "true", "enum", "NULL", 
			]
	
			self.logical_keywords = [
				"switch", "case", "if", "else", "goto", "for", "while"
			]

			self.special_keywords = [
				"asm", "__attribute__", "const", "extern", "volatile", "internal", "private", "public"
			]

			self.comment_sign = "//"
			self.multiline_comment_sign = "/*"
			self.multiline_comment_sign_end = "*/"

			self.build_argv = ["dotnet build"]
			self.run_argv = ["dotnet run"]


		elif (lang_type == "rs"):
			self.keywords = [
				"self", "return", "impl", "struct", "fn", "mod", "move", "ref", "super", "trait", "type",
				'abstract', 'alignof', 'macro', 'offsetof', 'final', 'box', 'override', 'priv', 'pure',
				'sizeof', 'typeof', 'unsized', 'virtual', 'yield', 'union', 'dyn', 'let', 'var',
				 'i8', 'i16', 'i32', 'i64', 'f32', 'f64'
			]

			self.numerical_keywords = [
				"false", "true", "enum", "NULL", "Self",
			]

			self.logical_keywords = [
				"switch", "case", "if", "else", "goto", "loop", "for", 'while', 'continue', 'break', 'do', "match"
			]

			self.special_keywords = [
				"use", "mut", "in", "as", "crate", "Self", "unsafe", "extern", "pub", "private", "const", "where"
			]

		elif (lang_type == "hs"):
			self.keywords = [
				'as', 'case', 'of', 'class', 'data', 'data', 'family', 'instance',
				'default', 'deriving', 'instance', 'do', 'forall', 'foreign', 'hiding',
				'if, then, else', 'import', 'infix' ,'infixl', 'infixr', 'instance', 'let', 'in',
				'mdo', 'module', 'newtype', 'proc', 'qualified', 'rec', 'type', 'family', 'where'
			]

			self.logical_keywords = [
				'case', 'of'
			]

			self.special_keywords = [
				
			]

		elif (lang_type == "php"):
			self.keywords = [
				 '__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch', 'class', 'clone', 'const', 'continue', 'declare', 'default',
				 'die', 'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile', 'eval', 'exit', 'extends', 'final', 'for', 'foreach',
				 'function', 'global', 'goto', 'if', 'implements', 'include', 'include_once', 'instanceof', 'insteadof', 'interface', 'isset', 'list', 'namespace', 'new', 'or', 'print',
				 'private', 'protected', 'public', 'require', 'require_once', 'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset', 'use', 'var', 'while', 'xor'
			]
			self.comment_sign = "//";
			self.multiline_comment_sign = "/*";
			self.multiline_comment_sign_end = "*/";

		elif lang_type == "js":
			self.keywords = ['abstract', 'arguments', 'await', 'boolean', 'break', 'byte', 'catch',
				'char', 'const', 'continue', 'debugger', 'default', 'delete', 'double', 'else',
				'export', 'final', 'finally', 'float', 'function',
				'implements', 'import', 'in', 'instanceof', 'int', 'interface', 'let', 'long',
				'native', 'package', 'return', 'short', 'static',
				'super', 'synchronized', 'throw', 'throws', 'transient', 'typeof',
				'var'
			]
			self.numerical_keywords = [
				"false", "true", "enum", "NULL", 'null',
			]
	
			self.logical_keywords = [
				"switch", "case", "if", "else", "goto", "for", "while", 'try', 'with', 'do'
			]

			self.special_keywords = [
				'this', 'void', 'volatile', 'yield', 'new', 'private', 'protected', 'public', 'class', 'extends'
			]


		elif lang_type == "lb":
			self.keywords = [
				'let', 'fn', 'progn', 'type', 'len', 'nth', 'list', 'use', 'load', 'help', 'exit', 'print', 'xor', 'random-num', 'map-get', 'map-add', 'car', 'cdr',
				'input', 'obj-name', 'eq'
			]

			self.logical_keywords = [
				'if', 'loop', '?', 'else'
			]

			self.numerical_keywords = [
				'true', 'false', 'NIL', 'PI', 
			]

			self.comment_sign = ";;"
			self.multiline_comment_sign = ""
			self.multiline_comment_sign_end = ""


		elif (lang_type in ["py", "pyc", "pyw"]):
			self.keywords = [
				'await', 'import', 'pass', 'break', 'in',
				'raise', 'class', 'is', 'return', 'continue', 'lambda', 'as', 'def', 'from',
				'nonlocal', 'assert', 'del', 'global', 'async', 'yield'
			]
	
			self.numerical_keywords = ['False', 'True', 'None']
			self.logical_keywords = [
				'and', 'or', 'not', 'if', 'elif', 'else', 'for', 'try', 'except', 'finally','while', 'with', 'self'] 
			
			self.comment_sign = "#"
			self.multiline_comment_sign = ""
			self.multiline_comment_sign_end = ""


		elif lang_type == "tex" or type == "bbl":
			self.keywords = [
				'chap', 'par', 'begtt', 'endtt', 'hisyntax', 
			]

			self.logical_keywords = [
				'sec', 'cite', 'em'
			]

			self.numerical_keywords = [
				'secc', 'item', 'bf', 'url'
			]

			self.comment_sign = "%%"
			self.multiline_comment_sign = ""
			self.multiline_comment_sign_end = ""

		self.text_type = type
		self.comment_regex = re.compile(fr"{self.comment_sign}")
		

	def lex(self, text=None, file="", index=["1.0", "end"], allow_lexing=False):
		# should iterate through characters make a token and then parse the token
		# I should probably just use tree sitter or something though
		if (text): self.text = text
		else: self.text = self.buffer.get(*index)
		self.row = 1
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
			self.vars[name] = self.curr_file

	def make_function(self):
		# w = f"{self.word} ({self.prev_word})"
		w = self.word
		# print("making func: ", w)
		# if ((w not in self.functions) and (self.word not in self.keywords)):
			# self.functions.append(w)
		if (name and name not in self.functions and self.word not in self.keywords):
			self.functions[name] = self.curr_file

	# def check_keyword(self):
		# return self.word in self.keywords

	def print_res(self):
		print("FNCS: ", self.functions)
		print("OBJS: ", self.objs)
		print("VARS: ", self.vars)

		s = "FNCS: \n"
		for word in self.functions:
			s += "\t"+word+"\n"

		s += "OBJS: \n"
		for word in self.objs:
			s += "\t"+word+"\n"

		self.parent.command_out_set(s)

	def update_code_location(self, *args, **kwargs):
		pass

	def unhighlight(self, line_no = None, line: str=None):
		if (not line_no):
			line_no = self.buffer.cursor_index[0]

		if (not line):
			line = self.buffer.get(f"{line_no}.0", f"{line_no}.0 lineend")

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.0 lineend"
		
		self.buffer.tag_remove(["quotes"], last_separator, line_end_index)
		self.buffer.tag_remove(["functions"], last_separator, line_end_index)
		self.buffer.tag_remove(["keywords"], last_separator, line_end_index)
		self.buffer.tag_remove(["logical_keywords"], last_separator, line_end_index)
		self.buffer.tag_remove(["numerical_keywords"], last_separator, line_end_index)
		self.buffer.tag_remove(["numbers"], last_separator, line_end_index)
		self.buffer.tag_remove(["special_chars"], last_separator, line_end_index)
		self.buffer.tag_remove(["comments"], last_separator, line_end_index)
		self.buffer.tag_remove(["operators"], last_separator, line_end_index)
		self.buffer.tag_remove(["upcase"], last_separator, line_end_index)
		self.buffer.tag_remove(["separator"], last_separator, line_end_index)
		self.buffer.tag_remove(["command_keywords"], last_separator, line_end_index)

	def unhighlight_all(self):
		self.buffer.tag_remove(["quotes"], "1.0", "end")
		self.buffer.tag_remove(["functions"], "1.0", "end")
		self.buffer.tag_remove(["keywords"], "1.0", "end")
		self.buffer.tag_remove(["logical_keywords"], "1.0", "end")
		self.buffer.tag_remove(["numerical_keywords"], "1.0", "end")
		self.buffer.tag_remove(["numbers"], "1.0", "end")
		self.buffer.tag_remove(["special_chars"], "1.0", "end")
		self.buffer.tag_remove(["comments"], "1.0", "end")
		self.buffer.tag_remove(["operators"], "1.0", "end")
		self.buffer.tag_remove(["upcase"], "1.0", "end")
		self.buffer.tag_remove(["separator"], "1.0", "end")
		self.buffer.tag_remove(["command_keywords"], "1.0", "end")



class EMPTY_LEXER:
	def __init__(self, parent, buffer_widget, type="c"):
		self.parent = parent
		self.buffer = buffer_widget
		
		self.text = ""
		self.indexed_files = []
		self.row = 0
		self.column = 1
		self.file_queue = set()
		self.to_index = []

		self.functions = {}
		self.vars = {}
		self.objs = {}
		self.defines = {}

		self.curr_file = ""
		self.keywords = []
		self.logical_keywords = []
		self.numerical_keywords = []
		self.special_keywords = []

		self.tree = None
		self.results = []
		self.full_results = []

		self.force_multiline_comment = False

		self.injection_lexers = {}
		self.active_lexers = {}


		self.last_node_cursor_was_inside_of = None

		self.scopes = {
			"global": {
				
			}
		}
		self.current_scope = self.scopes["global"]

		self.current_scope_location = []


		self.comment_sign = "#"
		self.multiline_sign = ""
		self.multiline_sign_end = ""
		# self.multiline_sign = "/*"
		# self.multiline_sign_end = "*/"

		self.build_argv = ["make"]
		self.run_argv = ["./main"]
		
		# self.available_languages = ["c", "cpp", "php", "py", "html", "rs", "hs"]
		self.language = None
		self.parser = None
		self.query = None

		self.set_language(type)

		self.text_type = type
		# self.index_extern = False
		self.index_extern = True

	def set_language(self, type):
		return

	def add_object(self, name):
		if (name and name not in self.objs):
			# self.objs.append(name)
			self.objs[name] = self.curr_file

	def add_define(self, key, val):
		self.defines[key] = val

	def add_function(self, name):
		if (name and name not in self.functions):
			self.functions[name] = self.curr_file

	def add_var(self, name):
		if (name and name not in self.vars):
			self.vars[name] = self.curr_file
			# self.vars.append(name)
			# self.indexed_info["vars"]


	def lex(*args, **kwargs):
		return

	def unhighlight(self, line_no = None, line: str=None):
		if (not line_no):
			line_no = self.buffer.cursor_index[0]

		if (not line):
			line = self.buffer.get(f"{line_no}.0", f"{line_no}.0 lineend")

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.0 lineend"
		
		self.buffer.tag_remove(["quotes"], last_separator, line_end_index)
		self.buffer.tag_remove(["functions"], last_separator, line_end_index)
		self.buffer.tag_remove(["keywords"], last_separator, line_end_index)
		self.buffer.tag_remove(["logical_keywords"], last_separator, line_end_index)
		self.buffer.tag_remove(["numerical_keywords"], last_separator, line_end_index)
		self.buffer.tag_remove(["numbers"], last_separator, line_end_index)
		self.buffer.tag_remove(["special_chars"], last_separator, line_end_index)
		self.buffer.tag_remove(["comments"], last_separator, line_end_index)
		self.buffer.tag_remove(["operators"], last_separator, line_end_index)
		self.buffer.tag_remove(["upcase"], last_separator, line_end_index)
		self.buffer.tag_remove(["separator"], last_separator, line_end_index)
		self.buffer.tag_remove(["command_keywords"], last_separator, line_end_index)

	def unhighlight_all(self):
		self.buffer.tag_remove(["quotes"], "1.0", "end")
		self.buffer.tag_remove(["functions"], "1.0", "end")
		self.buffer.tag_remove(["keywords"], "1.0", "end")
		self.buffer.tag_remove(["logical_keywords"], "1.0", "end")
		self.buffer.tag_remove(["numerical_keywords"], "1.0", "end")
		self.buffer.tag_remove(["numbers"], "1.0", "end")
		self.buffer.tag_remove(["special_chars"], "1.0", "end")
		self.buffer.tag_remove(["comments"], "1.0", "end")
		self.buffer.tag_remove(["operators"], "1.0", "end")
		self.buffer.tag_remove(["upcase"], "1.0", "end")
		self.buffer.tag_remove(["separator"], "1.0", "end")
		self.buffer.tag_remove(["command_keywords"], "1.0", "end")


class PY_LEXER(__LEXER):
	""" basic lexing """
	def __init__(self, parent, buffer_widget, lang_type="py"):
		super().__init__(parent, buffer_widget, lang_type)

	def lex(self, text=None, file="", index=["1.0", "end"]):
		if (text): self.text = text
		else: self.text = self.buffer.get(*index)
		row_index = 1
		self.row = 1
		self.column = 0
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
		expr = ""
		in_quote = in_quote_ = False

		for self.index, char in enumerate(self.text, 0):
			if (in_comment):
				if (char == "\n"): in_comment = False
				else: continue 

			elif (in_quote or in_quote_):
				expr += char
				self.index += 1
				if (in_quote and char == "\""):
					in_quote = False
					word_count = 0
					continue

				elif (in_quote_ and char == "'"):
					in_quote_ = False
					word_count = 0
					continue

				else:
					continue

			if (char == " " or char == "\t"):
				# self.make_func(prev_word, word, expr)
				line.append(word)
				prev_word = word
				word = ""
				expr += " "
				
			elif (char == "\n"):
				# self.make_func(prev_word, word, expr)
				line = []
				prev_word = ""
				word = ""
				expr = ""
				
				self.row += 1
				char_index = 0
				self.column = 0
				continue

			elif (char == "\""):
				in_quote = not in_quote
				self.index += 1
				expr += char
				continue

			elif (char == "'"):
				in_quote_ = not in_quote_
				self.index += 1
				expr += char
				continue

			elif (char == "#"):
				in_comment = True

			elif (char in az):
				word += char
				expr += char

			elif (word and char in num):
				word += char
				expr += char


			elif (char in ")]}"):
				expr += char
				if (char == ")"):
					self.make_func(prev_word, word, expr)

				expr = ""
				prev_word = word
				word = ""


			elif (char in ("(", "[", "{")):
				# brackets[char] = brackets[char]+1
				expr += char
				# if (char == "("):
					# self.make_func(prev_word, word)

				prev_word = word
				word = ""

			elif (char == "."):
				line.append(word)
				word = ""
				expr += char

			elif (char == ","):
				expr += char
				
			elif (char == "="):
				expr += char
				self.make_var(prev_word, word, expr)

				word = ""
				prev_word = word

			elif (char == ":"):
				expr += char
				if (self.text[self.index+1] == "\n"): self.make_func(prev_word, word, expr)
				expr = ""

			# elif (char in (")", "]", "}")):
				# brackets[char] = brackets[char]-1

			char_index += 1

	def print_res(self):
		print("FNCS: ", self.functions)
		print("OBJS: ", self.objs)
		print("VARS: ", self.vars)


	def handle_newline(self):
		self.row += 1
		self.column = 0
		self.handle_expression(self, self.expr)
		self.expr = ""


	def handle_expression(self):
		self.expression_table[self.expr[0]]()


	def make_func(self, prev_word, word, expr):
		if (re.search("def", expr)):
			# expr = re.sub("\s+", " ", expr)
			# group 1 is the full type
			# group 3 is the last part of the type
			# group 4 is the function name
			# group 5 are parameters
			expr = expr.strip()
			# print(expr)
			m = self.function_regex.match(expr)
			# m = re.match(r"(([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]+)*([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*[\[\]\*]*[\ \t]+))([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*)(\((.*\n*)*\))", expr)
			# print(m)

			if (m):
				x = ('', m.group(4), m.group(5))
				# print(m.groups())
				if (m.group(4) not in self.defines):
					self.defines[m.group(4)] = x
					# self.functions.append(m.group(4))

		elif (prev_word == "class" or prev_word == "import"):
			self.objs.append(word)

	def make_var(self, prev_word, word, expr):
		pass
		# if (self.text[self.index+1] != "="): self.vars.append(word)


class LEXER(__LEXER):
	def __init__(self, parent, buffer_widget, lang_type="c"):
		if (lang_type == "py"):
			self.lex = self.py_lex
			self.handle_expression = self.py_handle_expression
			self.make_func = self.py_make_func

		super().__init__(parent, buffer_widget, lang_type)
		# QUICK HACK
		# TODO: FIX
		self.text = ""
		self.indexed_files = []
		self.row = 0
		self.column = 1
		self.file_queue = set()
		self.to_index = []
		self.expression_actions = {
			"typedef": self.handle_typedef,
		}

		# self.index_extern = False
		self.index_extern = True

		if (self.buffer):
			self.index_extern = True
			if (os.path.exists(f"/tmp/.tmp_{self.buffer.name}")):
				print('LOADING FROM SAVE: ', f"/tmp/.tmp_{self.buffer.name}")
				# self.index_extern = False
				f = open(f"/tmp/.tmp_{self.buffer.name}", "rb")
				ll = pickle.load(f)
				# self.types, self.modifiers, self.vars, self.functions, self.objs, self.defines, self.indexed_files = ll
				# print(self.objs, self.functions)
				f.close()

		self.set_language(type)

	def py_handle_expression(self):
		self.expression_table[self.expr[0]]()


	def py_make_func(self, prev_word, word, expr):
		if (re.search("def", expr)):
			# expr = re.sub("\s+", " ", expr)
			# group 1 is the full type
			# group 3 is the last part of the type
			# group 4 is the function name
			# group 5 are parameters
			expr = expr.strip()
			# print(expr)
			m = self.function_regex.match(expr)
			# m = re.match(r"(([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]+)*([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*[\[\]\*]*[\ \t]+))([a-zA-Z_]+[a-zA-Z_0-9]*[\ \t]*)(\((.*\n*)*\))", expr)
			# print(m)
	
			if (m):
				x = ('', m.group(4), m.group(5))
				# print(m.groups())
				if (m.group(4) not in self.defines):
					self.defines[m.group(4)] = [m.group(4), ""]
					# self.functions.append(m.group(4))
					self.functions[m.group(4)] = self.curr_file
					

		# elif (prev_word == "class" or prev_word == "import"):
			# self.objs.append(word)


	def py_lex(self, text=None, file="", index=["1.0", "end"]):
		if (text): self.text = text
		else: self.text = self.buffer.get(*index)
		row_index = 1
		self.row = 1
		self.column = 0
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
		expr = ""
		in_quote = in_quote_ = False

		for self.index, char in enumerate(self.text, 0):
			if (in_comment):
				if (char == "\n"): in_comment = False
				else: continue 

			elif (in_quote or in_quote_):
				expr += char
				self.index += 1
				if (in_quote and char == "\""):
					in_quote = False
					word_count = 0
					continue

				elif (in_quote_ and char == "'"):
					in_quote_ = False
					word_count = 0
					continue

				else:
					continue

			if (char == " " or char == "\t"):
				# self.make_func(prev_word, word, expr)
				line.append(word)
				prev_word = word
				word = ""
				expr += " "
				
			elif (char == "\n"):
				# self.make_func(prev_word, word, expr)
				line = []
				prev_word = ""
				word = ""
				expr = ""
				
				self.row += 1
				char_index = 0
				self.column = 0
				continue

			elif (char == "\""):
				in_quote = not in_quote
				self.index += 1
				expr += char
				continue

			elif (char == "'"):
				in_quote_ = not in_quote_
				self.index += 1
				expr += char
				continue

			elif (char == "#"):
				in_comment = True

			elif (char in az):
				word += char
				expr += char

			elif (word and char in num):
				word += char
				expr += char


			elif (char in ")]}"):
				expr += char
				if (char == ")"):
					self.make_func(prev_word, word, expr)

				expr = ""
				prev_word = word
				word = ""


			elif (char in ("(", "[", "{")):
				# brackets[char] = brackets[char]+1
				expr += char
				# if (char == "("):
					# self.make_func(prev_word, word)

				prev_word = word
				word = ""

			elif (char == "."):
				line.append(word)
				word = ""
				expr += char

			elif (char == ","):
				expr += char
				
			elif (char == "="):
				expr += char
				self.make_var(prev_word, word, expr)

				word = ""
				prev_word = word

			elif (char == ":"):
				expr += char
				if (self.text[self.index+1] == "\n"): self.make_func(prev_word, word, expr)
				expr = ""

			# elif (char in (")", "]", "}")):
				# brackets[char] = brackets[char]-1

			char_index += 1


	def lex(self, text=None, start_file="", index=["1.0", "end"], should_highlight=True, allow_lexing=True):
		print("heere")
		offset_pos = 1
		self.curr_file = start_file
		if (text):
			self.text = text
			offset_pos = int(index[0].split(".")[0])
		else:
			self.text = self.buffer.get(*index) + " "
			self.indexed_files.append(self.buffer.full_name)

			if (index == ["1.0", "end"]):
				# self.buffer.parent.unhighlight_chunk_main_thread()
				self.unhighlight_all()
				# TODO: delete all stored information on new lex of whole file
			else:
				offset_pos = int(index[0].split(".")[0])

		if (start_file or not should_highlight):
			self.parse_quotes = self.parse_quotes_simple
			self.handle_word_end = self.handle_word_end_without_highlight

		else:
			self.parse_quotes = self.parse_quotes_complex
			self.handle_word_end = self.handle_word_end_with_highlight
		
		self.in_comment = False
		self.in_multiline_comment = False
		self.in_quote = False # "
		self.in_quote_ = False # '
		self.in_nested_quote_maybe = self.in_nested_quote = False
		self.in_format_quote_maybe = self.in_format_quote = False
		
		self.brackets = {
			"(": 0,
			"[": 0,
			"{": 0,
		}

		self.line = []	
		self.prev_word = ""
		self.word = ""

		self.expr = ""
		self.expr_type = ""
		# self.expr_as_list = []
		self.index = 0

		self.row = int(index[0].split(".")[0])
		self.column = int(index[0].split(".")[1])-1


		self.word_count = 0
		flag = 0
		self.prev_char = ""
		self.char = ""

		self.word_start = [self.row, self.column]
		self.word_end = [self.row, self.column]

		self.prev_word_start = [self.row, self.column]
		self.prev_word_end = [self.row, self.column]

		self.expr_start = [self.row, self.column]
		self.expr_end = [self.row, self.column]

		file_queue = set()
		self.in_whitespace = False
		# print("length: ", len(self.text), start_file)
		
		# for self.index in range(len(self.text)-1):
		while (self.index < len(self.text)-1):
			self.column += 1
			self.prev_char = self.text[self.index-1]
			self.char = self.text[self.index]
			# self.next_char = self.text[self.index+1]
			# if (flag): print("FLAG: ", f"|{char}|", self.index, f"|{self.expr}|"); flag = 0

			# print(self.row, self.column, self.index, f"|{char}|")


			if (self.in_whitespace):
				if (self.char in " \t"):
					self.index += 1
					continue
				else:
					self.in_whitespace = False
					self.handle_word_end()


			if (self.in_comment):
				self.index += 1

				if (self.char == "\n"):
					self.in_comment = False
					self.expr_end = [self.row, self.column]
					
					if (not start_file): self.highlight_comment()
					self.handle_new_line()
					# self.del_expression()
					continue

				continue

			elif (self.in_multiline_comment):
				if (self.char + self.text[self.index+1] == self.multiline_comment_sign_end):
					self.column += 2

					self.in_multiline_comment = False
					self.word_count = 0
					self.index += 2
					self.expr_end = [self.row, self.column]
					if (not start_file): self.highlight_comment()
					# self.del_expression()
					continue

				elif (self.char == "\n"):
					self.handle_new_line()
					self.index += 1
					continue

				else: self.index += 1; continue


			elif (self.in_quote or self.in_quote_):
				self.parse_quotes()
				continue
				

			elif (self.char == " " or self.char == "\t"):
				self.in_whitespace = True
				# self.ignore_whitespace()
				# if (self.text[self.index+1] == "="): self.make_var(prev_word, word, index=self.index+1)
				# if (self.text[self.index+1] in whitespace and self.search_whitespace(self.index+1)): pass
				if (self.expr): self.expr += " "
				self.handle_word_end()
				# if (self.next_char not in " \t"): self.handle_word_end()


			elif (self.char == ","):
				self.handle_word_end()
				self.word = self.char
				self.handle_word_end()
				self.expr += self.char



			elif (self.char == "\""):
				self.expr_start = [self.row, self.column]
				self.in_quote = not self.in_quote
				self.index += 1
				continue


			elif (self.char == "'"):
				self.expr_start = [self.row, self.column]
				self.in_quote_ = not self.in_quote_
				self.index += 1
				continue
				

			elif (self.char == "\n"):
				# if (prev_word and prev_word[0] == "#"):
					# prev_word = word
					# word = ""

				if (self.expr): self.expr += "\n"
				self.handle_word_end()
				self.handle_new_line()
				# self.index += 1
				# continue


			# elif (self.char == self.comment_sign[0]):
			elif ((self.char+self.text[self.index+1]) == self.comment_sign):
				# if ((self.char+self.text[self.index+1]) == self.comment_sign):
					self.expr_start = [self.row, self.column]
					self.in_comment = True

			elif ((self.char+self.text[self.index+1]) == self.multiline_comment_sign):
				self.expr_start = [self.row, self.column]
				self.in_multiline_comment = True

			
					


			elif (self.char == "#" and self.prev_char == "\n"):
				self.handle_word_end()
				self.handle_preprocessor(file_queue)
				# self.index += 1
				# print("define expr: ", self.expr)
				self.del_expression()
				# flag = 1

				continue


			elif (self.char in az):
				if (self.word and self.prev_char not in az and self.prev_char not in num and self.prev_char != "<"):
					self.handle_word_end()
				self.word += self.char
				self.expr += self.char

			# elif (self.word and char in num):
				# self.word += char
				# self.expr += char

			elif (self.char in num):
				if (self.word and self.prev_char not in az and self.prev_char not in num):
					self.handle_word_end()
				self.word += self.char
				self.expr += self.char

			elif (self.char in operators_text):
				if (self.word and self.char != ">" and self.prev_char not in operators_text):
					self.handle_word_end()

				self.expr += self.char
				self.word += self.char

			elif (self.char in "@#$|\\"):
				if (self.word and self.prev_char not in "@#$|\\"):
					self.handle_word_end()

				self.expr += self.char
				self.word += self.char

			elif (self.char in "([{"):
				# if (self.word and prev_char not in "([{"):
				if (self.char == "{"):
					self.expr_type = "{"
				self.handle_word_end()
				
				self.brackets[self.char] = self.brackets[self.char]+1
				self.word = self.char
				self.expr += self.char

			elif (self.char in ")]}"):
				self.handle_word_end()

				self.expr += self.char
				self.word = self.char
				# self.handle_word_end()

				if (self.char == ")"):
					# self.make_func(prev_word, word)

					self.brackets["("] -= 1
					# print("brackets: ", brackets["("])
					if self.brackets["("] == 0:
						self.make_func_new(self.expr)
						# self.del_expression()

				elif (self.char == "]"):
					self.brackets["["] -= 1
					# if self.brackets["["] == 0:
						# self.expr = ""

				elif (self.char == "}"):
					self.brackets["{"] -= 1
					self.expr_type = ""
					# if self.brackets["{"] == 0:
						# self.expr = ""


			elif (self.char == "."):
				self.handle_word_end()
				self.expr += self.char

			elif (self.char == "="):
				self.make_var(self.prev_word, self.word)
				self.expr += self.char

				self.handle_word_end()

			# elif (self.char == ":" and self.prev_char == ":"):
				# self.handle_word_end()
				# self.word = "::"
				# self.column += 1
				# self.handle_word_end()
				# self.column -= 1
				# # self.expr += "::"

			elif (self.char in ";"):
				self.handle_word_end()
				self.word = self.char
				if (not start_file): self.highlight_word()
				self.word = ""
				# self.handle_word_end()
				# print("expr: ", self.expr)
				if (self.expr_type != "{"): self.handle_expression()
				

				
			self.index += 1
			# print("i: ", self.index, char, word, file)


		# print("lexing ended")


		# if (self.buffer):
			# for object in self.objs:
				# if (object not in self.buffer.highlighter.keywords): self.buffer.highlighter.keywords.append(object)
	
			# self.parent.command_out_set("lex finished")
	
		# file_queue += self.file_queue.copy()
		# print("file Q: ", file_queue)

		# file_queue = self.file_queue.copy()
		# indexed_files = self.indexed_files.copy()

		if (self.index_extern):
			for file in file_queue:
				if (file not in self.indexed_files):
					print(f"indexing: {file}")
					# self.parent.command_out_set(f"file {file} is a file")
					self.indexed_files.append(file)
					if (self.buffer):
						path = f"{os.path.dirname(self.buffer.full_name)}/{file}"
					else:
						path = file
	
					self.indexed_files.append(file)
					if (os.path.isfile(path)):
						# print("path: ", path)
						f = open(path, "r")
						ttt = f.read()
						f.close()
						self.lex(ttt, path)

					else:
						path = f"/usr/include/{file}"
						# print("path1: ", path)
						if (os.path.isfile(path)):
							f = open(path, "r")
							# self.indexed_files.append(file)
							# t = threading.Thread(target=self.lex, args=(f.read(), path))
							# t.start()
							ttt = f.read()
							f.close()
							self.lex(ttt, path)
							# threading.Thread(target=self.lex, args=(ttt, path)).start()
							# self.parent.after(0, lambda: self.lex(ttt, path))


			if (self.buffer):
				ll = [self.types, self.modifiers, self.vars, self.functions, self.objs, self.defines, self.indexed_files]
				f = open(f"/tmp/.tmp_{self.buffer.name}", "wb")
				f.write(pickle.dumps(ll))
				f.close()

		# print("\n\n\n\n----------------------------\n\n\n\n")
		# print(f"FINISHED LEXING {start_file}, {self.file_queue}")
		# self.print_res()

	def print_res(self):
		# print("INDEXED: ", self.indexed_files)
		# print("FNCS: ", self.functions)
		# print("OBJS: ", self.objs)
		# print("VARS: ", self.vars)

		s = "INDEXED: \n"
		for word in self.indexed_files:
			s += "\t"+word+"\n"

		s = "FNCS: \n"
		for word, path in self.functions.items():
			s += f"\t{word} :: {path}\n"

		s += "OBJS: \n"
		for word, path in self.objs.items():
			s += f"\t{word} :: {path}\n"

		s += "VARS: \n"
		for word, path in self.vars.items():
			s += f"\t{word} :: {path}\n"

		# s = "VARS: \n"
		# for word in self.vars:
			# s += "\t"+word+"\n"
		print(s)
		
		if (self.parent): self.parent.command_out_set(s)

	def print_functions(self, args=[]):
		if (not args):
			s = "FNCS: \n"
			for word, path in self.functions.items():
				s += f"\t{word} :: {path}\n"
		else:
			word, path = args[0], self.functions[args[0]]
			s = f"\t{word} :: {path}\n"

		if (self.parent): self.parent.command_out_set(s)

	def print_objs(self, args=[]):
		if (not args):
			s = "OBJS: \n"
			for word, path in self.objs.items():
				s += f"\t{word} :: {path}\n"
		else:
			word, path = args[0], self.objs[args[0]]
			s = f"\t{word} :: {path}\n"

		if (self.parent): self.parent.command_out_set(s)

	def print_vars(self, args=[]):
		if (not args):
			s = "VARS: \n"
			for word, path in self.vars.items():
				s += f"\t{word} :: {path}\n"
		else:
			word, path = args[0], self.vars[args[0]]
			s = f"\t{word} :: {path}\n"

		if (self.parent): self.parent.command_out_set(s)


	def handle_new_line(self):
		# print("newline!!!: ", self.row, self.column)
		self.row += 1
		self.column = -1
		self.handle_word_end()

	def handle_new_line_o(self):
		self.row += 1
		self.column = -1


	def handle_expression(self):
		if (not self.expr or not self.line): return
		# print("line: ", self.line, '|', self.expr, '|', "\n\n")
		if (self.line[0] in self.expression_actions):
			self.expression_actions[self.line[0]]()
		self.del_expression()


	def del_expression(self):
		# print("line: ", self.line, '|', self.expr, '|', "\n\n")

		self.expr_end = [self.row, self.column]
		del self.line[:]
		self.expr = ""
		self.word_count = 0
		self.expr_start = [self.row, self.column]
		# self.word_start = [self.row, self.column]

	def handle_typedef(self):
		# print("typedef happpened", self.line)
		if (self.line[-1] not in self.defines):
			self.add_object(self.line[-1])
			self.add_define(self.line[-1], self.line[1:])
			# print(self.defines[self.line[-1])
		print("typedef happpened", self.line, self.defines[self.line[-1]])

	def highlight_comment(self):
		self.buffer.tag_add("comments", f"{self.expr_start[0]}.{self.expr_start[1]}", f"{self.expr_end[0]}.{self.expr_end[1]}")

	def highlight_quote(self):
		self.buffer.tag_add("quotes", f"{self.expr_start[0]}.{self.expr_start[1]}", f"{self.expr_end[0]}.{self.expr_end[1]}")

	def highlight_preprocessor(self):
		pass

	def highlight_word(self, tag=None):
		# self.buffer.parent.notify(f"aaaaaaaaa {self.word_start} - {self.word_end} : {self.word}")
		if (self.buffer):
			if (tag): self.buffer.tag_add(tag, f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")

			elif (self.in_quote or self.in_quote_ and self.word[0] in "'\"{%"):
				self.buffer.tag_add("keywords", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")

			elif (self.word in self.objs and word_regex.match(self.word)): self.buffer.tag_add("upcase", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (self.word in self.functions): self.buffer.tag_add("functions", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (self.word in self.keywords): self.buffer.tag_add("keywords", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (self.word in self.logical_keywords): self.buffer.tag_add("logical_keywords", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (self.word in self.numerical_keywords): self.buffer.tag_add("numbers", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (self.word in self.special_keywords): self.buffer.tag_add("command_keywords", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (separator.match(self.word)):
				if word_regex.match(self.prev_word): self.buffer.tag_add("quotes", f"{self.prev_word_start[0]}.{self.prev_word_start[1]}", f"{self.prev_word_end[0]}.{self.prev_word_end[1]}")
				self.buffer.tag_add("command_keywords", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
				# print("separator: ", self.word_start, self.word_end, self.word)
				
			elif (self.word[0] in num): self.buffer.tag_add("numbers", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (operators.match(self.word)): self.buffer.tag_add("operators", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			
			
			elif (self.word[0] in "("):
				self.buffer.tag_add("functions", f"{self.prev_word_start[0]}.{self.prev_word_start[1]}", f"{self.prev_word_end[0]}.{self.prev_word_end[1]}")
				self.buffer.tag_add("special_chars", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
				
			elif (special_char_regex.match(self.word) or self.word in brackets):
				# print("brackets: ", self.word, self.word_start)
				self.buffer.tag_add("special_chars", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")

			elif (upcase_regex.match(self.word)): self.buffer.tag_add("upcase", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (self.word[0] == "#"):
				# print('preproc: ', self.word, f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
				self.buffer.tag_add("numbers", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			elif (self.word[0] == "<"):
				print("bs", self.word, f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
				self.buffer.tag_add("keywords", f"{self.word_start[0]}.{self.word_start[1]}", f"{self.word_end[0]}.{self.word_end[1]}")
			
	
	def handle_word_end(self):
		pass

	def handle_word_end_without_highlight(self):
		if (self.word):
			# print("word: ", self.word, self.word_start, self.word_end)

			self.word_count += 1
			self.prev_word = self.word
			self.line.append(self.word)
			self.word = ""
		

	def handle_word_end_with_highlight(self):
		self.prev_word_end = self.word_end
		self.word_end = [self.row, self.column]

		if (self.word):
			# print("word: ", f"[{self.word}]", self.word_start, self.word_end)
			self.highlight_word()

			self.word_count += 1
			self.prev_word = self.word
			self.line.append(self.word)
			self.word = ""

		self.prev_word_start = self.word_start
		self.word_start = [self.row, self.column]


	# def handle_preprocessor(self, file_queue):
		# word = ""
		# command = ""
		# ignore_next = False
		# i = 1
		# self.word = ""
		# self.handle_word_end()
		# self.word = "#"
		# in_if = False
		# in_if_end_maybe = False
		
		# for char in self.text[self.index+i:]:
			# self.column += 1
			
			# if ((not command or command == "include") and char in az or char in "/.\\"):
				# word += char

			# elif (command == "define" and char != "\\"):
				# word += char

			# elif (command == "ignore"):
				# pass

			# # elif (command in ["ifdef", "ifndef", "if"]):
				# # break

			
			# if (char == " " and not command and word):
				# # self.highlight_word("upcase")
				# self.word = "#" + word
				# self.handle_word_end()
				# # print("fff", f"[{word}]", f"[{self.word}]", self.word_start)
				
				# if (word == "include" or word == "define"):
					# command = word
					# word = ""
				# else: command = "ignore"


			# elif (not ignore_next and char == "\\"):
				# ignore_next = True

			# elif (ignore_next):
				# ignore_next = False

			# elif (char == "\n" and not ignore_next):
				# if (command == "include"):
					# self.word = "<"+word
					# self.handle_word_end()

				# self.handle_new_line()
				# break

			# if (char == "\n"):
				# self.handle_new_line()
			# i += 1

		# # self.parent.command_out_set(f"file {word} was added to queue")

		# # print("end: ", command, word, i)
		# # print("before: ", self.index)
		# self.index += i+1
		# # print("after: ", self.index)
		# # if (command == "include" and word not in self.indexed_files and word not in file_queue): print(f"adding {word} to file queue"); file_queue.append(word)
		# if (command == "include" and word):
			# # with lock:
				# # file_queue.add(word)
				# # print(f"adding {word} to file queue", word not in self.indexed_files, word not in file_queue)
			# if (word not in self.indexed_files and word not in self.file_queue): self.file_queue.add(word)

		# elif (command == "define"):
			# x = self.parse_macro_define(word)
			# if (x[0] not in self.defines):
				# self.add_object(x[0])
				# self.add_define(x[0], x)


	def handle_preprocessor(self, file_queue):
		word = ""
		command = ""
		ignore_next = False
		i = 1
		self.word = ""
		self.handle_word_end()
		self.word = "#"
		in_if = False
		in_if_end_maybe = False
		escaped = False

		print("macro start: ", word, self.row, self.column)
		# for c in self.text[self.index+i:]:
		while (self.index+i < len(self.text)):
			c = self.text[self.index+i]
			self.index += 1
			self.column += 1

			if (c == "\n"):
				self.handle_new_line()


			if (c not in " \t\n"):
				word += c
			
			else:
				if (c == "\n"): print("what##############"); self.index += 1; break
				self.word = "#" + word
				self.handle_word_end()
				# print("macro start: ", word)
				if (word == "define"): self.parse_macro_define()
				elif (word == "include"): self.parse_macro_include(file_queue)
				elif (word == "ifndef"): self.parse_macro_ifndef()
				elif (word == "ifdef"): self.parse_macro_ifdef()
				elif (word == "if"): self.parse_macro_if()
				# elif (word == "endif"): self.index += i+1; break
				else: self.parse_macro_undefined()
				# if (self.text[self.index] == "\n"): self.index+=1
				break

			if (escaped): escaped = False

		# self.index -= 1
		# self.index += 1
		# print("macro end: ", word, self.row, self.column, self.index, self.index+i, len(self.text))
		



	def parse_macro_undefined(self):
		i = 0
		word = ""
		escaped = False
		ignore_whitespace = True

		while (self.index+i < len(self.text)):
			c = self.text[self.index+i]
			self.column += 1

			if (ignore_whitespace):
				if (c in " \t"):
					i += 1
					continue
				else:
					ignore_whitespace = False

			if (c == "\\" and self.text[self.index+i+1] == "\\"):
				self.column += 1
				i += 2
				escaped = True
				print("escaped: ", self.text[self.index+i])
				continue

			elif (c == "\n"):
				self.handle_new_line_o();
				if not escaped: i += 1; break
				else: ignore_whitespace = True

			elif (c in " \t"):
				ignore_whitespace = True

			else:
				word += c

			if (escaped): escaped = False
			
			i += 1


		print("macro ignored: ", word)
		self.index += i




	def parse_macro_define(self):
		i = 0
		word = ""
		escaped = False
		ignore_whitespace = True
		in_brackets = False
		bracket_count = 0
		stopped = False

		while (self.index+i < len(self.text)):
			c = self.text[self.index+i]
			self.column += 1

			if (ignore_whitespace):
				if (c in " \t"):
					i += 1
					continue
				else:
					ignore_whitespace = False

			if (c == "\\" and self.text[self.index+i+1] == "\\"):
				self.column += 1
				i += 2
				escaped = True
				print("escaped: ", self.text[self.index+i])
				continue

			elif (c == "\n"):
				self.handle_new_line_o();
				if not escaped: i += 1; break
				else: ignore_whitespace = True

			elif (c == "("):
				if not stopped: word += c
				in_brackets = True
				bracket_count += 1

			elif (c == ")"):
				if not stopped: word += c
				bracket_count -= 1
				if (bracket_count == 0):
					stopped = True

			elif (c in " \t"):
				if not stopped: word += c
				ignore_whitespace = True

			else:
				if not stopped: word += c

			if (escaped): escaped = False
			i += 1


		# self.word = "<"+word
		# self.handle_word_end()


		word += " "
		print("macro define: ", word, self.row, self.column)
		x = word.split(" ")
		if (x[0] not in self.defines):
				self.add_object(word)
				self.add_define(word, (word, ""))
		
		self.index += i




	def parse_macro_include(self, file_queue):
		i = 0
		word = ""
		escaped = False
		ignore_whitespace = True
		in_quotes = False
		stopped = False

		print("include start: ", self.text[self.index+i])
		self.word = ""
		self.handle_word_end_without_highlight()

		while (self.index+i < len(self.text)):
			c = self.text[self.index+i]
			self.column += 1

			
			if (ignore_whitespace):
				if (c in " \t"):
					i += 1
					continue
				else:
					ignore_whitespace = False

			if (c == "\\" and self.text[self.index+i+1] == "\\"):
				self.column += 1
				i += 2
				escaped = True
				print("escaped: ", self.text[self.index+i])
				continue

			elif (c == "\n"):
				self.handle_new_line_o();
				if not escaped: i += 1; break
				else: ignore_whitespace = True

			elif (c == "\""):
				# in_quotes = not in_quotes
				if (in_quotes): in_quotes = False; stopped = True
				else: in_quotes = True

			elif (c == "<"):
				pass

			elif (c == ">"):
				stopped = True

			elif (c in " \t"):
				ignore_whitespace = True

			else:
				if (not stopped): word += c

			if (escaped): escaped = False
			i += 1



		self.word = "<" + word
		if (word not in self.indexed_files and word not in file_queue): file_queue.add(word)
		print("macro include: ", word, self.word, self.row, self.column)
		self.handle_word_end()
		self.index += i




	def parse_macro_ifndef(self):
		i = 0
		word = ""
		escaped = False
		ignore_whitespace = True
		in_quotes = False

		while (self.index+i < len(self.text)):
			c = self.text[self.index+i]
			self.column += 1

			
			if (ignore_whitespace):
				if (c in " \t"):
					i += 1
					continue
				else:
					ignore_whitespace = False

			if (c == "\\" and self.text[self.index+i+1] == "\\"):
				self.column += 1
				i += 2
				escaped = True
				print("escaped: ", self.text[self.index+i])
				continue

			elif (c == "\n"):
				if not escaped: self.handle_new_line(); i += 1; break
				else: self.handle_new_line(); ignore_whitespace = True

			elif (c in " \t"):
				ignore_whitespace = True

			else:
				word += c

			if (escaped): escaped = False
			i += 1

			
		print("macro ifndef: ", word)

		endif_word_maybe = ""
		endif_word = ""
		# print(word in self.defines, self.defines)
		if (word in self.defines):
			print("aa")
			while (self.index+i < len(self.text)):
				c = self.text[self.index+i]
				self.column += 1

				if (c == "\n"):
					self.handle_new_line()

				if (c == "#"):
					endif_word_maybe = True

				elif (endif_word_maybe):
					print(endif_word)
					if (c not in " \t\n"):
						 endif_word += c
					
					elif (endif_word == "endif"):
						print("endif found!!")
						i += 1
						break

					else:
						endif_word = ""

				i += 1


		self.index += i






	def parse_macro_ifdef(self):
		i = 0
		word = ""
		escaped = False
		ignore_whitespace = True
		in_quotes = False

		while (self.index+i < len(self.text)):
			c = self.text[self.index+i]
			self.column += 1


			if (ignore_whitespace):
				if (c in " \t"):
					i += 1
					continue
				else:
					ignore_whitespace = False

			if (c == "\\" and self.text[self.index+i+1] == "\\"):
				self.column += 1
				i += 2
				escaped = True
				print("escaped: ", self.text[self.index+i])
				continue

			elif (c == "\n"):
				if not escaped: self.handle_new_line(); i += 1; break
				else: self.handle_new_line(); ignore_whitespace = True

			elif (c in " \t"):
				ignore_whitespace = True

			else:
				word += c

			if (escaped): escaped = False
			i += 1

			
		print("macro ifdef: ", word)

		# TODO: CHECK if not def and go to endif

		endif_word_maybe = ""
		endif_word = ""
		if (word in self.defines):
			while (self.index+i < len(self.text)):
				c = self.text[self.index+i]
				self.column += 1

				if (c == "\n"):
					self.handle_new_line()

				if (c == "#"):
					endif_word_maybe = True

				elif (endif_word_maybe):
					if (c not in " \t\n"):
						 endif_word += c
					
					elif (endif_word == "endif"):
						i += 1
						break

					else:
						endif_word = ""

				i += 1
			
		self.index += i




	def parse_macro_if(self):
		i = 0
		print("start: ", self.row, self.column, i)
		word = ""
		escaped = False
		ignore_whitespace = True
		in_quotes = False

		while (self.index+i < len(self.text)):
			c = self.text[self.index+i]
			self.column += 1


			if (ignore_whitespace):
				if (c in " \t"):
					i += 1
					continue
				else:
					ignore_whitespace = False

			if (c == "\\" and self.text[self.index+i+1] == "\\"):
				self.column += 1
				i += 2
				escaped = True
				print("escaped: ", self.text[self.index+i])
				continue

			elif (c == "\n"):
				if not escaped: self.handle_new_line(); i += 1; break
				else: self.handle_new_line(); ignore_whitespace = True

			elif (c in " \t"):
				ignore_whitespace = True

			else:
				word += c

			if (escaped): escaped = False
			i += 1

			
		print("macro if: ", word)

		
		endif_word_maybe = ""
		endif_word = ""
		# print(word in self.defines, self.defines)
		print("aa")
		while (self.index+i < len(self.text)):
			c = self.text[self.index+i]
			self.column += 1

			if (c == "\n"):
				self.handle_new_line()

			if (c == "#"):
				endif_word_maybe = True

			elif (endif_word_maybe):
				# print(endif_word)
				if (c not in " \t\n"):
					 endif_word += c
				
				elif (endif_word == "endif"):
					print("endif found!!")
					self.word = "#endif"
					self.handle_word_end()
					i += 1
					break

				else:
					endif_word = ""

			i += 1

		self.index += i
		




	# def parse_macro_define(self, macro):
		# ignore_whitespace = True
		# ignore_next = False
		# word = ""
		# i = 0
		# print("macro: ", macro)
		# # for c in macro:
			# # i += 1
			# # if (ignore_whitespace and c in "\n \t"): continue
			# # word += c

		# return word, macro[i:].replace("\\", "")


	def add_file_to_queue(self, file_queue):
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
		# if (word not in self.indexed_files and word not in file_queue): file_queue.append(word)
		if (word):
			file_queue.add(word)


	def parse_quotes(self):
		pass

	def parse_quotes_simple(self):
		self.expr += self.char
		self.index += 1

		if (self.in_quote_ and self.prev_char == "<" and self.text_type == "rs"):
			print("what the fuck: ", self.row, self.column, self.prev_char)
			self.in_quote = False
			self.in_quote_ = False
			return


		if (self.in_quote and self.char == "\""):
			self.in_quote = False
			self.del_expression()

		elif (self.in_quote_ and self.char == "'"):
			self.in_quote_ = False
			self.del_expression()

		elif (self.char == "\n"):
			self.handle_new_line()


	def parse_quotes_complex(self):
		self.expr += self.char
		self.index += 1
		if (self.in_quote_ and self.text[self.index-3] in "<&" and self.text_type == "rs"):
			self.in_quote = False
			self.in_quote_ = False
			return

		if (self.char == "%"):
			tmp_word = self.word
			tmp_word_start = self.word_start
			tmp_word_end = self.word_end

			
			self.word_start = [self.row, self.column]
			self.word_end = [self.row, self.column+1]
			self.word = "%"
			# self.parent.notify(f"{self.in_quote or self.in_quote_} {(self.word[0] in '{%')}")
			self.highlight_word()

			self.word = tmp_word
			self.word_start = tmp_word_start
			self.word_end = tmp_word_end

		if (self.in_quote and self.char == "\""):
			self.in_quote = False
			self.in_nested_quote = False
			self.in_format_quote = False
			self.word = ""
			self.handle_word_end_without_highlight()
			self.word_count = 0

			self.expr_end = [self.row, self.column+1]
			self.highlight_quote()
			self.del_expression()

		if (self.in_quote_ and self.char == "'"):
			self.in_quote_ = False
			self.in_nested_quote = False
			self.in_format_quote = False
			self.word = ""
			self.handle_word_end_without_highlight()
			self.word_count = 0

			self.expr_end = [self.row, self.column+1]
			self.highlight_quote()
			self.del_expression()

		
		if (self.char == "\n"):
			self.word = ""
			self.in_nested_quote = False
			self.in_format_quote = False
			self.handle_new_line()


		if (not self.in_format_quote_maybe and self.char == "{"):
			self.word = ""
			self.handle_word_end()
			self.word = self.char
			self.in_format_quote_maybe = True


		elif (self.in_format_quote_maybe):
			self.word += self.char
			if (self.char == "}"):
				self.in_format_quote = 1
				self.column += 1
				self.handle_word_end()
				self.column -= 1
				self.in_format_quote = 0
				self.in_format_quote_maybe = 0


		if (not self.in_nested_quote_maybe and (self.in_quote and self.char == "'" or self.in_quote_ and self.char == "\"")):
			self.word = ""
			self.handle_word_end()
			self.word = self.char
			self.in_nested_quote_maybe = True


		elif (self.in_nested_quote_maybe):
			self.word += self.char
			if (self.in_quote and self.char == "'" or self.in_quote_ and self.char == "\""):
				self.in_nested_quote = 1
				self.column += 1
				self.handle_word_end()
				self.column -= 1
				self.in_nested_quote = 0
				self.in_nested_quote_maybe = 0




	def search_whitespace(self, index) -> bool:
		for char in self.text[index:]:
			if (char == " " or char == "\t"):
				pass
			elif (char == "\n"):
				return False
			else:
				return True
			self.column += 1
			self.index += 1

	def add_object(self, name):
		if (name and name not in self.objs):
			# self.objs.append(name)
			self.objs[name] = self.curr_file

	def add_define(self, key, val):
		self.defines[key] = val

	def add_function(self, name):
		if (name and name not in self.functions):
			self.functions[name] = self.curr_file

	def add_var(self, name):
		if (name and name not in self.vars):
			self.vars[name] = self.curr_file
			# self.vars.append(name)
			# self.indexed_info["vars"]


	def make_func_new(self, expr):
		# print("EXPR: ", expr)
		if (re.search(r"=|return", expr)): return
		# if (re.match(r"([a-zA-Z_]+[a-zA-Z_0-9]+\ )+ \(([a-zA-Z_]+[a-zA-Z_0-9]+\ )+\)", expr)): print("ok")
		# if (re.match(r"((([a-zA-Z_]+[a-zA-Z_0-9]*\ +)*([a-zA-Z_]+[a-zA-Z_0-9]*))\((.)*\))", expr)): print("ok")
		# if (re.match(r"([[a-zA-Z_]+[a-zA-Z_0-9]*\ +]*[a-zA-Z_]+[a-zA-Z_0-9]*)\(.*\)", expr)): pass

		# expr = expr.replace("\n", "")
		# expr = expr.replace("\t", " ")

		expr = re.sub("\s+", " ", expr)
		# group 1 is the full type
		# group 3 is the last part of the type
		# group 4 is the function name
		# group 5 are parameters
		# print("\n\nfunc: ", expr)
		m = self.function_regex.match(expr)

		if (m):
			# print("dwadw\n\n")
			x = (m.group(1), m.group(4), m.group(5))
			# print(m.groups())
			if (m.group(4) not in self.defines):
				self.add_define(m.group(4), x)
				self.add_function(m.group(4))

	
	def make_func(self, prev_word, word):
		if (prev_word == "#define"):
			self.add_object(word)

		elif (prev_word == "struct"):
			self.add_object(word)

		elif (word == "struct"):
			self.add_object(self.get_struct_name())

		# elif (self.text[self.index] == "("):
			# self.add_function(word)

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






if __name__ == "__main__":
	l = LEXER(None, None)
	print("\n-----------------------------------------------------------------------------------\n                #################  TESTING LEXER  ####################\n-----------------------------------------------------------------------------------\n")
	try:
		f = open("lexer_test/gui.c", "r")
		text = f.read()
		f.close()
		l.lex(text=text, start_file="gui.c", should_highlight=False)
		l.print_res()
	except Exception as e:
		print(e)



