import string
import re
import os
import threading
import pickle
import tempfile

import tree_sitter
import tree_sitter_python as tspython
import tree_sitter_c as tsc
import tree_sitter_rust as tsrust
import tree_sitter_html as tshtml
import tree_sitter_php as tsphp

from util import *

C_LANGUAGE = tree_sitter.Language(tsc.language())
PHP_LANGUAGE = tree_sitter.Language(tsphp.language_php())
HTML_LANGUAGE = tree_sitter.Language(tshtml.language())
RUST_LANGUAGE = tree_sitter.Language(tsrust.language())
PYTHON_LANGUAGE = tree_sitter.Language(tspython.language())

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
		self.multiline_comment_sign = ""
		self.multiline_comment_sign_end = ""
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
		if (key not in self.defines):
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



class LEXER(EMPTY_LEXER):
	def __init__(self, parent, buffer_widget, type="c"):
		super().__init__(parent, buffer_widget, type)

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


	def construct_lang_and_query(self, lang_type):
		if (type(lang_type) == list): lang_type = lang_type[0]
		query, language = None, None

		if (lang_type in ["c", "h", "cpp", "hpp", "cc", "hh", "ino"] and "C_LANGUAGE" in globals()):
			lang_type = "c"
			language = C_LANGUAGE
			with open(f"{SOURCE_PATH}/ts_queries/c.scm", "r") as file:
				query = language.query(file.read())

		elif (lang_type == "py" and "PYTHON_LANGUAGE" in globals()):
			language = PYTHON_LANGUAGE
			with open(f"{SOURCE_PATH}/ts_queries/python.scm", "r") as file:
				query = language.query(file.read())

		elif (lang_type == "php"):
			language = PHP_LANGUAGE
			with open(f"{SOURCE_PATH}/ts_queries/php.scm", "r") as file:
				query = language.query(file.read())

		elif (lang_type == "html"):
			language = HTML_LANGUAGE
			with open(f"{SOURCE_PATH}/ts_queries/html.scm", "r") as file:
				query = language.query(file.read())

		elif (lang_type == "rs"):
			language = RUST_LANGUAGE
			with open(f"{SOURCE_PATH}/ts_queries/rust.scm", "r") as file:
				query = language.query(file.read())

		elif (lang_type == "lb"):
			language = tree_sitter.Language(tslisp.language(), 'Common Lisp')
			with open(f"{SOURCE_PATH}/ts_queries/lisp.scm", "r") as file:
				query = language.query(file.read())

		elif (lang_type in ["cpp", "hpp", "cc", "hh"]):
			language = C_LANGUAGE
			with open(f"{SOURCE_PATH}/ts_queries/c.scm", "r") as file:
				query = language.query(file.read())


		return language, query



	def set_language(self, lang_type):
		if (type(lang_type) == list): lang_type = lang_type[0]

		self.query = None
		self.language = None

		self.comment_sign = "//"
		self.multiline_comment_sign = "/*"
		self.multiline_comment_sign_end = "*/"

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


		elif (lang_type == "(cpp|hpp|cc|hh)$"):
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

			self.build_argv = ["cargo", "build"]
			self.run_argv = ["cargo", "run"]
			


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
			l, q = self.construct_lang_and_query('html')
			p = tree_sitter.Parser(l)
			# p.set_language(l)
			self.active_lexers['html'] = [p, q, l]
			
			# self.keywords = [
				 # '__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch', 'class', 'clone', 'const', 'continue', 'declare', 'default',
				 # 'die', 'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile', 'eval', 'exit', 'extends', 'final', 'for', 'foreach',
				 # 'function', 'global', 'goto', 'if', 'implements', 'include', 'include_once', 'instanceof', 'insteadof', 'interface', 'isset', 'list', 'namespace', 'new', 'or', 'print',
				 # 'private', 'protected', 'public', 'require', 'require_once', 'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset', 'use', 'var', 'while', 'xor'
			# ]
			self.build_argv = []
			self.run_argv = []



		elif (lang_type == "html"):
			self.force_multiline_comment = True
			self.multiline_comment_sign = "<!--"
			self.multiline_comment_sign_end = "-->"



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



		elif (lang_type in ["py", "pyw"]):
			lang_type = "py"
			self.build_argv = ["python3", self.buffer.name]
			self.run_argv = self.build_argv

			self.comment_sign = "#"
			self.multiline_comment_sign = ""
			self.multiline_comment_sign_end = ""

		# elif lang_type == "tex" or type == "bbl":
			# self.keywords = [
				# 'chap', 'par', 'begtt', 'endtt', 'hisyntax', 
			# ]

			# self.logical_keywords = [
				# 'sec', 'cite', 'em'
			# ]

			# self.numerical_keywords = [
				# 'secc', 'item', 'bf', 'url'
			# ]

			# self.comment_sign = "%%"
			# self.multiline_comment_sign = ""
			# self.multiline_comment_sign_end = ""


		self.comment_regex = re.compile(fr"{self.comment_sign}")
		self.language, self.query = self.construct_lang_and_query(lang_type)



		self.text_type = lang_type
		# self.index_extern = False
		self.index_extern = True

		print("set highlighter to: ", lang_type)

		if (self.language):
			self.parser = tree_sitter.Parser(self.language)
			# self.parser.set_language(self.language)

		if (self.parser not in self.active_lexers):
			self.active_lexers[self.text_type] = [self.parser, self.query, self.language]

		self.lex()


	def debug(self, text=None, start_file="", index=["1.0", "end"], should_highlight=True):
		if (not self.language): return

		# self.text_index = self.buffer.index("insert-1c")

		offset_pos = 1
		# self.curr_file = start_file
		if (text):
			# self.text = text
			offset_pos = int(index[0].split(".")[0])

		else:
			# index = ["1.0", "end"]
			# self.text = self.buffer.get(*index) + " "
			# self.indexed_files.append(self.buffer.full_name)

			if (index == ["1.0", "end"]): pass
			else:
				offset_pos = int(index[0].split(".")[0])

		# self.current_scope = self.scopes["global"]
		# self.tree = self.parser.parse(bytes(self.text, 'utf-8'))
		last = ["1.0" ,"1.0"]
		last_type = []

		# r = tree_sitter.Range((4, 0), (6, 0))
		# self.results = self.query.captures(self.tree.root_node)
		if (index == ["1.0", "end"]): self.full_results = self.results
		scope_list = []

		s = ""
		for index, (node, catch_type) in enumerate(self.results):
			start = f"{node.start_point[0]+offset_pos}.{node.start_point[1]}"
			end = f"{node.end_point[0]+offset_pos}.{node.end_point[1]}"
			print(node, catch_type, node.text)
			s += f"{node} {catch_type} {node.text}\n"

		self.parent.command_out_set(s)


	def highlight(self, text, index, lexer):
		# print("HIGHLIGHT START: ", index)
		if (not lexer): return

		text_index = self.buffer.index("insert-1c")

		offset_pos = 1
		offset_pos = int(index[0].split(".")[0])

		# if (start_file or not should_highlight):
			# self.parse_quotes = self.parse_quotes_simple
			# self.handle_word_end = self.handle_word_end_without_highlight

		# else:
			# self.parse_quotes = self.parse_quotes_complex
			# self.handle_word_end = self.handle_word_end_with_highlight

		if (type(text) == str):
			text = bytes(text, 'utf-8')
		tree = lexer[0].parse(text)
		# if (self.tree == None):
			# self.tree = self.parser.parse(bytes(self.text, 'utf-8'))
		# else:
			# self.tree.edit(start_point=(1, 0))
		# if (tree != None):
			# print("CHNAGED: ", tree.changed_ranges(self.tree))
		last = ["1.0" ,"1.0"]
		last_type = []

		# r = tree_sitter.Range((4, 0), (6, 0))
		results = lexer[1].captures(tree.root_node)
		scope_list = []
		# print("_--------START--------_")
		# for index, (node, catch_type) in enumerate(results):
		for catch_type in self.results.keys():
			for index, node in enumerate(self.results[catch_type]):
				# parent = node.parent
				# if (parent and parent != tree.root_node):
					# print("parent: ", parent, parent.text, node.text)
				# print(i, node.parent)
	
				start = f"{node.start_point[0]+offset_pos}.{node.start_point[1]}"
				end = f"{node.end_point[0]+offset_pos}.{node.end_point[1]}"
				# start = f"{node.start_point[0]}.{node.start_point[1]}"
				# end = f"{node.end_point[0]}.{node.end_point[1]}"
				# print("##> ", catch_type, index, node, start, end)
				# print(node, catch_type, node.text)
				inside = False
	
				# if (self.buffer.compare(self.text_index, ">=", start) and self.buffer.compare(self.text_index, "<=", end)):
					# # print("inside: True, ", start, end, node)
					# inside = True
					# self.parent.notify(self.walk_scopes(node))
					# self.parent.code_location_label["text"] = self.walk_scopes(node)
	
				if (catch_type == "keyword"):
					self.buffer.tag_add("keywords", start, end)
	
				elif (catch_type == "function"):
					self.buffer.tag_add("functions", start, end)
	
				elif (catch_type == "operator"):
					self.buffer.tag_add("operators", start, end)
	
				elif (catch_type == "string"):
					self.buffer.tag_add("quotes", start, end)
	
				elif (catch_type == "function.method"):
					self.buffer.tag_add("functions", start, end)
	
				elif (catch_type == "number"):
					self.buffer.tag_add("numbers", start, end)
	
				elif (catch_type == "comment"):
					self.buffer.tag_add("comments", start, end)
	
				elif (catch_type == "parenthesis" or catch_type == "special_chars" or catch_type == "delimeter" or catch_type == "tag"):
					self.buffer.tag_add("special_chars", start, end)
	
				elif (catch_type == "upcase"):
					self.buffer.tag_add("upcase", start, end)
	
				elif (catch_type == "type" or node.type == "type_parameters"):
					self.buffer.tag_add("special_chars", start, end)
	
				elif (catch_type == "special_keywords" or catch_type == "command_keywords" or catch_type == "attribute"):
					self.buffer.tag_add("command_keywords", start, end)
	
				elif (catch_type == "proc_keywords"):
					self.buffer.tag_add("found", start, end)
	
				elif (catch_type == "logical_keywords"):
					self.buffer.tag_add(catch_type, start, end)
	
				elif (catch_type == "numerical_keywords"):
					self.buffer.tag_add("numbers", start, end)
	
				elif (catch_type == "constant.builtin"):
					self.buffer.tag_add("keywords", start, end)


	def lex(self, text=None, start_file="", index=["1.0", "end"], should_highlight=True, allow_lexing=True):
		if (not self.language): return

		self.text_index = self.buffer.index("insert-1c")

		offset_pos = 1
		self.curr_file = start_file
		if (text):
			self.text = text
			offset_pos = int(index[0].split(".")[0])

		else:
			# index = ["1.0", "end"]
			self.text = self.buffer.get(*index) + " "
			self.indexed_files.append(self.buffer.full_name)

			if (index == ["1.0", "end"]):
				# self.buffer.parent.unhighlight_chunk_main_thread()
				self.unhighlight_all()
				# TODO: delete all stored information on new lex of whole file
			else:
				offset_pos = int(index[0].split(".")[0])

		# if (start_file or not should_highlight):
			# self.parse_quotes = self.parse_quotes_simple
			# self.handle_word_end = self.handle_word_end_without_highlight

		# else:
			# self.parse_quotes = self.parse_quotes_complex
			# self.handle_word_end = self.handle_word_end_with_highlight

		self.blocks = {}
		self.scopes = {"global" : {}}
		self.current_scope = self.scopes["global"]
		# print(dir(self.parser))

		# tree = self.tree
		self.tree = self.parser.parse(bytes(self.text, 'utf-8'))
		# if (self.tree == None):
			# self.tree = self.parser.parse(bytes(self.text, 'utf-8'))
		# else:
			# self.tree.edit(start_point=(1, 0))
		# if (tree != None):
			# print("CHNAGED: ", tree.changed_ranges(self.tree))
		last = ["1.0" ,"1.0"]
		last_type = []

		# r = tree_sitter.Range((4, 0), (6, 0))
		self.results = self.query.captures(self.tree.root_node)
		if (index == ["1.0", "end"]): self.full_results = self.results
		scope_list = []
		# print(self.results["special_keywords"] if "special_keywords" in self.results else None)
		
		#return
		# print("_--------START--------_")
		for catch_type in self.results.keys():
			for index, node in enumerate(self.results[catch_type]):
				# parent = node.parent
				# if (parent and parent != tree.root_node):
					# print("parent: ", parent, parent.text, node.text)
				# print(i, node.parent)

				start = f"{node.start_point[0]+offset_pos}.{node.start_point[1]}"
				end = f"{node.end_point[0]+offset_pos}.{node.end_point[1]}"
				# print("LEX: ", start, end)
				# print(node, catch_type, node.text)
				inside = False

				# if (self.buffer.compare(self.text_index, ">=", start) and self.buffer.compare(self.text_index, "<=", end)):
					# # print("inside: True, ", start, end, node)
					# inside = True
					# self.parent.notify(self.walk_scopes(node))
					# self.parent.code_location_label["text"] = self.walk_scopes(node)

				if (catch_type == "keyword"):
					self.buffer.tag_add("keywords", start, end)

				elif (catch_type == "function"):
					self.buffer.tag_add("functions", start, end)

					if (allow_lexing):
						self.add_function(node.text.decode())
						self.add_define(node.text.decode(), ["", node.text.decode(), ""])
					
					self.current_scope[node.text.decode()] = {}
					self.current_scope = self.current_scope[node.text.decode()]
					# if (inside): self.current_scope = 

				elif (catch_type == "operator"):
					self.buffer.tag_add("operators", start, end)

				elif (catch_type == "string"):
					self.buffer.tag_add("quotes", start, end)

				elif (catch_type == "function.method"):
					self.buffer.tag_add("functions", start, end)

				elif (catch_type == "number"):
					self.buffer.tag_add("numbers", start, end)

				elif (catch_type == "comment"):
					self.buffer.tag_add("comments", start, end)

				elif (catch_type == "parenthesis" or catch_type == "special_chars" or catch_type == "delimeter" or catch_type == "tag"):
					self.buffer.tag_add("special_chars", start, end)

				elif (catch_type == "upcase"):
					self.buffer.tag_add("upcase", start, end)

				elif (catch_type == "type" or node.type == "type_parameters"):
					self.buffer.tag_add("special_chars", start, end)

				elif (catch_type == "special_keywords" or catch_type == "command_keywords" or catch_type == "attribute"):
					self.buffer.tag_add("command_keywords", start, end)

				elif (catch_type == "proc_keywords"):
					self.buffer.tag_add("found", start, end)

				elif (catch_type == "logical_keywords"):
					self.buffer.tag_add(catch_type, start, end)

				elif (catch_type == "numerical_keywords"):
					self.buffer.tag_add("numbers", start, end)

				elif (catch_type == "constant.builtin"):
					self.buffer.tag_add("keywords", start, end)


				elif (catch_type in self.active_lexers and node.type == "text"):
					self.highlight(node.text, [start, end], self.active_lexers[catch_type])
					# print(dir(node))
					# print(node.grammar_name)

				# elif (node.type == "identifier"):
					# if (node.text.decode() in self.keywords):
						# self.buffer.tag_add("keywords", start, end)

				if (catch_type == "variable" and allow_lexing):
					self.add_var(node.text.decode())
					self.add_define(node.text.decode(), ["", node.text.decode(), ""])
					

				if ((catch_type == "property" or catch_type == "delimeter")):
					# print("proprety: ", node, catch_type)
					self.current_scope[node.text.decode()] = node.parent.text.decode()
					if ("parenthesis" not in last_type and node.type != "field_identifier"):
						self.buffer.tag_add("command_keywords", *last)


				## handle struct, class, enum, etc. indexing

				if (catch_type == "definition.class"):
					name = self.handle_struct_definition(node)
					self.current_scope[name] = {}
					self.current_scope = self.current_scope[name]
					# pass
					# print("blopck: ", node.is_named)
					# self.block[node.text.decode()

				elif (catch_type == "function_declarator"):
					if (allow_lexing):
						self.handle_function_definition(node)
					self.current_scope[name] = {}
					self.current_scope = self.current_scope[name]

				# if (index < len(self.results)-1):
				# 	if (node.start_point != self.results[index+1][0].start_point and node.end_point != self.results[index+1][0].end_point):
				# 		last = [start, end]
				# 		last_type = []
				# 		last_type.append(node.type)
				# 		last_type.append(catch_type)
				# 	else:
				# 		last_type.append(node.type)
				# 		last_type.append(catch_type)

				# self.walk_scopes(node)

				# if (node.start_point == (0, 0)): continue
				# node.start_point = (node.start_point[0]+1, node.start_point[1])
				# node.end_point = (node.end_point[0]+1, node.end_point[1])
				# self.buffer.tag_add("keywords", f"{node.start_point[0]+1}.{node.start_point[1]}", f"{node.end_point[0]+1}.{node.end_point[1]}")


		# print("blocks: ", self.blocks)
		# print("_----------------_")
		# print(self.scopes)
		# print(dir(self.tree), self.tree.included_ranges)

	def print_res(self):
		s = "VARS:"
		for var in self.vars.items():
			s += "\t{var}"
		print(self.vars)
		print(self.functions)
		print(self.scopes)

		self.parent.command_out_set(s)

	
	def walk_scopes(self, node):
		# print("start walking: ", node)
		nodes = []
		s = []
		while 1:
			if node == None or node.type == "translation_unit" or node.type == "module":	
				break

			# if (node.type == "function_declarator"):
			if (node.type == "function_definition" or node.type == "class_definition"):
				# print("declarator: ", node.children)
				for c in node.children[1:]:
					if (c.type == "ERROR"): break
					if (c.type == "identifier" or c.type == "function_declarator"):
						nodes.append(node)
						s.append(c.text.decode())
						break

			elif (node.type == "struct_specifier" or node.type == "enum_specifier"):
				# print(node.children)
				nodes.append(node)
				for c in node.children:
					# print("c: ", c)
					if (c.type == "type_identifier"):
						s.append(c.text.decode())
						break
				# s.append(node.text.decode())
				# print("struct: ", node, node.text.decode())

			node = node.parent


			# print("walking: ", node, node.text.decode())
		
		self.current_scope = self.scopes["global"]
		for scope in s:
			if (scope not in self.current_scope): self.current_scope[scope] = {}
			self.current_scope = self.current_scope[scope]
		s.append("global")
		# print("ended walking: ", s[::-1])
		# nodes.append("global")
		# self.current_scope_location = nodes[::-1][-1]
		return " -> ".join(s[::-1])


	def update_code_location(self):
		return
		text_index = self.buffer.index("insert")
		starting_point_offset = 0
		row = int(text_index.split(".")[0])-1
		column = int(text_index.split(".")[1])

		# l = len(bytes(self.buffer.get("1.0", index), 'utf8'))
		# l1 = len(self.text) - l
		# print(self.tree.root_node_with_offset(l, (row, column)))
		
		if (not self.full_results):
			self.parent.code_location_label["text"] = "global"
			return

		query = self.full_results
		reverse = False
		step = 1

		if (self.last_node_cursor_was_inside_of and self.last_node_cursor_was_inside_of[0] and self.last_node_cursor_was_inside_of[1]):
			starting_point_offset = self.last_node_cursor_was_inside_of[1]
			# print("start: ", starting_point_offset, text_index)

			if (row == self.last_node_cursor_was_inside_of[0].start_point[0] or row == self.last_node_cursor_was_inside_of[0].end_point[0]):
				# print("early return")
				# return
				pass

			elif (row > self.last_node_cursor_was_inside_of[0].start_point[0]):
				query = query[starting_point_offset:]
				# print("forward start", starting_point_offset)

			else:
				reverse = True
				step = -1
				query = query[starting_point_offset::-1]
				# print("reverse start")
				# print("query: ", query)

		offset_pos = 1
		last_was_less = True
		last_node = None

		for index, (node, other)	in enumerate(query, starting_point_offset):
			start = f"{node.start_point[0]+offset_pos}.{node.start_point[1]}"
			end = f"{node.end_point[0]+offset_pos}.{node.end_point[1]}"
			# TODO: iterate sibling(left) -> goto parent and start over
			#		 ^-------------------------------------------^
			# start from last node cursor was inside

			# print("ttrying: ", start, end, index, node, text_index)

			if (self.buffer.compare(text_index, ">=", start) and self.buffer.compare(text_index, "<=", end)):
				self.parent.code_location_label["text"] = self.walk_scopes(node)
				if (not reverse): self.last_node_cursor_was_inside_of = [node, index]
				else: self.last_node_cursor_was_inside_of = [node, starting_point_offset-(index-starting_point_offset)]
				# print("ending: ", node, self.last_node_cursor_was_inside_of[1])
				break


			elif (not reverse and self.buffer.compare(text_index, "<", start) and self.buffer.compare(text_index, "<", end)):
				# print("special end")
				self.parent.code_location_label["text"] = self.walk_scopes(last_node)
				self.last_node_cursor_was_inside_of = [last_node, index-1]
				break

			elif (reverse and self.buffer.compare(text_index, ">", start) and self.buffer.compare(text_index, ">", end)):
				# print("special end 1", starting_point_offset-(index-starting_point_offset))
				self.parent.code_location_label["text"] = self.walk_scopes(node)
				self.last_node_cursor_was_inside_of = [node, starting_point_offset-(index-starting_point_offset)]
				break

			last_node = node

		# print("---------------------------")

	def iterate_node_left(self, node):
		offset_pos = 1
		while 1:
			if (node == None):
				node = node.parent
				if (node == None or node.type == "translation_unit" or node.type == "module"): break
				continue

			elif (self.buffer.compare(text_index, ">=", start) and self.buffer.compare(text_index, "<=", end)):
				self.parent.code_location_label["text"] = self.walk_scopes(node)
				return node

			start = f"{node.start_point[0]+offset_pos}.{node.start_point[1]}"
			end = f"{node.end_point[0]+offset_pos}.{node.end_point[1]}"

			node in node.prev_sibling

		return None

	def set_code_location(self, node, block_name):
		self.last_node_cursor_was_inside_of = node

	def handle_struct_definition(self, parent):
		name = ""
		for c in parent.children:
			print("\tblock: ", c)
			if (c.type == "type_identifier"):
				name = c.text.decode()

			elif (c.type == "field_declaration_list"):
				# self.blocks[name] = c.parent.text.decode()
				self.blocks[name] = c.text.decode()

		return name


	def handle_function_definition(self, node):
		print("function: ", node, node.parent)
		name = ""
		self.add_function(node.text.decode())
		self.add_define(node.text.decode(), ["", node.text.decode(), ""])




