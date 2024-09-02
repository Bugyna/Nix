import string
import re
import os
import threading
import pickle
import tempfile

import tree_sitter
import tree_sitter_python as tspython
import tree_sitter_c as tsc

class LEXER:
	def __init__(self, parent, type="(c|h)$"):
		self.parent = parent
		
		self.text = ""
		self.indexed_files = []
		self.row = 0
		self.column = 1
		self.file_queue = set()
		self.to_index = []

		self.functions = {}
		self.vars = {}
		self.objs = {}
		self.curr_file = ""
		self.keywords = []
		self.logical_keywords = []
		self.numerical_keywords = []
		self.special_keywords = []

		self.query = None
		self.language = None

		if (type == "(c|h)$"):
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

			self.language = tree_sitter.Language(tsc.language(), 'C')
			self.query = self.language.query(
			'''
			(identifier) @variable
			
			((identifier) @constant
			 (#match? @constant "^[A-Z][A-Z\\d_]*$"))

			((identifier) @upcase
			 (#match? @upcase "^[A-Z_][A-Z_1-9]+$"))

			[
				"asm"
				"__attribute__"
				"const"
				"extern"
				"volatile"
				"typedef"
				"static"
				"register"
			] @special_keywords
			
			"#define" @keyword
			"#elif" @keyword
			"#else" @keyword
			"#endif" @keyword
			"#if" @keyword
			"#ifdef" @keyword
			"#ifndef" @keyword
			"#include" @keyword
			(preproc_directive) @keyword
			
			"--" @operator
			"-" @operator
			"-=" @operator
			"->" @operator
			"=" @operator
			"!=" @operator
			"*" @operator
			"&" @operator
			"&&" @operator
			"+" @operator
			"++" @operator
			"+=" @operator
			"<" @operator
			"==" @operator
			">" @operator
			"||" @operator
			
			"." @delimiter
			"->" @delimeter
			";" @semicolon

			[
				"("
				")"
				"["
				"]"
				"{"
				"}"
				"~"
			] @parenthesis
			
			(string_literal) @string
			(system_lib_string) @string
			
			(null) @constant
			(number_literal) @number
			(char_literal) @number
			
			(field_identifier) @property
			(statement_identifier) @label
			(type_identifier) @type
			(primitive_type) @type
			(sized_type_specifier) @type
			
			(call_expression
			  function: (identifier) @function)
			(call_expression
			  function: (field_expression
			    field: (field_identifier) @function))
			(function_declarator
			  declarator: (identifier) @function)
			(preproc_function_def
			  name: (identifier) @function.special)
			
			(comment) @comment

			(struct_specifier name: (type_identifier) @name body:(_)) @definition.class

			(declaration type: (union_specifier name: (type_identifier) @name)) @definition.class
			
			(function_declarator declarator: (identifier) @name) @definition.function
			
			(type_definition declarator: (type_identifier) @name) @definition.type
			
			(enum_specifier name: (type_identifier) @name) @definition.type
			'''
			)

		elif (type == "(cpp|hpp|cc|hh)$"):
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

			self.query = c_query

		elif (type == "rs"):
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

		elif (type == "hs"):
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

		elif (type == "php"):
			self.keywords = [
				 '__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch', 'class', 'clone', 'const', 'continue', 'declare', 'default',
				 'die', 'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile', 'eval', 'exit', 'extends', 'final', 'for', 'foreach',
				 'function', 'global', 'goto', 'if', 'implements', 'include', 'include_once', 'instanceof', 'insteadof', 'interface', 'isset', 'list', 'namespace', 'new', 'or', 'print',
				 'private', 'protected', 'public', 'require', 'require_once', 'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset', 'use', 'var', 'while', 'xor'
			]

		elif type == "js":
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

		elif type == "lb":
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

		elif (type == "(py|pyw)$"):
			
			self.language = tree_sitter.Language(tspython.language(), 'Python')
			self.query = self.language.query(
				'''
				; Identifier naming conventions
			
			(identifier) @variable
			
			((identifier) @constructor
			 (#match? @constructor "^[A-Z]"))

			((identifier) @upcase
			 (#match? @upcase "^[A-Z_][A-Z_]+$"))
			
			((identifier) @constant
			 (#match? @constant "^[A-Z][A-Z_]*$"))
			
			; Function calls
			
			(decorator) @function
			
			(call
			  function: (attribute attribute: (identifier) @function.method))
			(call
			  function: (identifier) @function)
			
			; Builtin functions
			
			((call
			  function: (identifier) @function.builtin)
			 (#match?
			   @function.builtin
			   "^(abs|all|any|ascii|bin|bool|breakpoint|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip|__import__)$"))
			
			; Function definitions
			
			(function_definition
			  name: (identifier) @function)
			
			(attribute attribute: (identifier) @property)
			(type (identifier) @type)
			
			; Literals
			
			[
			  (none)
			  (true)
			  (false)
			] @constant.builtin
			
			[
			  (integer)
			  (float)
			] @number
			
			(comment) @comment
			(string) @string
			(escape_sequence) @escape
			
			(interpolation
			  "{" @punctuation.special
			  "}" @punctuation.special) @embedded
			
			[
			  "-"
			  "-="
			  "!="
			  "*"
			  "**"
			  "**="
			  "*="
			  "/"
			  "//"
			  "//="
			  "/="
			  "&"
			  "&="
			  "%"
			  "%="
			  "^"
			  "^="
			  "+"
			  "->"
			  "+="
			  "<"
			  "<<"
			  "<<="
			  "<="
			  "<>"
			  "="
			  ":="
			  "=="
			  ">"
			  ">="
			  ">>"
			  ">>="
			  "|"
			  "|="
			  "~"
			  "@="
			  "and"
			  "in"
			  "is"
			  "not"
			  "or"
			] @operator
			
			[
				"("
				")"
				"["
				"]"
				"{"
				"}"
				"~"
				"@"
			] @parenthesis
			
			[
			  "as"
			  "assert"
			  "async"
			  "await"
			  "break"
			  "class"
			  "continue"
			  "def"
			  "del"
			  "elif"
			  "else"
			  "except"
			  "exec"
			  "finally"
			  "for"
			  "from"
			  "global"
			  "if"
			  "import"
			  "lambda"
			  "nonlocal"
			  "pass"
			  "print"
			  "raise"
			  "return"
			  "try"
			  "while"
			  "with"
			  "yield"
			  "match"
			  "case"
			] @keyword
			
			'''
			)
			
			self.comment_sign = "#"
			self.multiline_comment_sign = ""
			self.multiline_comment_sign_end = ""

		# elif type == "tex" or type == "bbl":
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

		self.text_type = type
		# self.index_extern = False
		self.index_extern = True

		self.parser = tree_sitter.Parser(self.language)
		self.parser.set_language(self.language)

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

	def lex(self, buffer_widget=None, text=None, start_file="", index=["1.0", "end"], should_highlight=True):
		if (buffer_widget): self.buffer= buffer_widget

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
				self.buffer.highlighter.unhighlight_all()
				# TODO: delete all stored information on new lex of whole file
			else:
				offset_pos = int(index[0].split(".")[0])

		if (start_file or not should_highlight):
			self.parse_quotes = self.parse_quotes_simple
			self.handle_word_end = self.handle_word_end_without_highlight

		else:
			self.parse_quotes = self.parse_quotes_complex
			self.handle_word_end = self.handle_word_end_with_highlight

		tree = self.parser.parse(bytes(self.text, 'utf-8'))
		last = ["1.0" ,"1.0"]
		results = self.query.captures(tree.root_node)

		for index, i in enumerate(results):

			start = f"{i[0].start_point[0]+offset_pos}.{i[0].start_point[1]}"
			end = f"{i[0].end_point[0]+offset_pos}.{i[0].end_point[1]}"
			print(i, i[0].text, start)

			if (i[1] == "keyword"):
				self.buffer.tag_add("keywords", start, end)

			elif (i[1] == "function"):
				self.buffer.tag_add("functions", start, end)
				self.add_function(i[0].text.decode())
				self.add_define(i[0].text.decode(), ["", i[0].text.decode(), ""])

			elif (i[1] == "operator"):
				self.buffer.tag_add("operators", start, end)

			elif (i[1] == "string"):
				self.buffer.tag_add("quotes", start, end)

			elif (i[1] == "constant.builtin"):
				self.buffer.tag_add("keywords", start, end)

			elif (i[1] == "function.method"):
				self.buffer.tag_add("functions", start, end)

			elif (i[1] == "number"):
				self.buffer.tag_add("numbers", start, end)

			elif (i[1] == "comment"):
				self.buffer.tag_add("comments", start, end)

			elif (i[1] == "parenthesis" or i[1] == "special_chars"):
				self.buffer.tag_add("special_chars", start, end)

			elif (i[1] == "upcase"):
				self.buffer.tag_add("upcase", start, end)

			elif (i[1] == "type"):
				self.buffer.tag_add("keywords", start, end)

			elif (i[1] == "special_keywords"):
				self.buffer.tag_add("command_keywords", start, end)

			# elif (i[0].type == "identifier"):
				# if (i[0].text.decode() in self.keywords):
					# self.buffer.tag_add("keywords", start, end)

			if (i[1] == "property" or i[1] == "delimeter"):
				self.buffer.tag_add("command_keywords", *last)


			## handle struct, class, enum, etc. indexing

			if (i[1] == "definition.class"):
				pass

			if (index < len(results)-1):
				if (i[0].start_point != results[index+1][0].start_point and i[0].end_point != results[index+1][0].end_point):
					last = [start, end]

			# if (i[0].start_point == (0, 0)): continue
			# i[0].start_point = (i[0].start_point[0]+1, i[0].start_point[1])
			# i[0].end_point = (i[0].end_point[0]+1, i[0].end_point[1])
			# self.buffer.tag_add("keywords", f"{i[0].start_point[0]+1}.{i[0].start_point[1]}", f"{i[0].end_point[0]+1}.{i[0].end_point[1]}")
		return