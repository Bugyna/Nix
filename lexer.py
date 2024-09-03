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


		self.last_node_cursor_was_inside_of = None

		self.scopes = {
			"global": {
				
			}
		}
		self.current_scope = self.scopes["global"]

		self.current_scope_location = []


		self.comment_sign = "//"
		self.multiline_sign = ""
		self.multiline_sign_end = ""
		# self.multiline_sign = "/*"
		# self.multiline_sign_end = "*/"

		self.build_argv = ["make"]
		self.run_argv = ["./main"]
		
		
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

	def set_language(self, type):
		self.query = None
		self.language = None

		if (type in ["c", "h", "cpp", "hpp", "cc", "hh"]):
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
			
			"." @delimeter
			"->" @delimeter
			";" @delimiter

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

			self.build_argv = ["cargo", "build"]
			self.run_argv = ["cargo", "run"]

			self.language = tree_sitter.Language(tsrust.language(), 'rust')
			self.query = self.language.query('''
					(type_identifier) @type
					(primitive_type) @type.builtin
					(field_identifier) @property
					
					; Identifier conventions
					
					; Assume all-caps names are constants
					((identifier) @constant
					 (#match? @constant "^[A-Z][A-Z\\d_]+$'"))
					
					; Assume uppercase names are enum constructors
					((identifier) @constructor
					 (#match? @constructor "^[A-Z]"))
					
					; Assume that uppercase names in paths are types
					((scoped_identifier
					  path: (identifier) @type)
					 (#match? @type "^[A-Z]"))
					((scoped_identifier
					  path: (scoped_identifier
					    name: (identifier) @type))
					 (#match? @type "^[A-Z]"))
					((scoped_type_identifier
					  path: (identifier) @type)
					 (#match? @type "^[A-Z]"))
					((scoped_type_identifier
					  path: (scoped_identifier
					    name: (identifier) @type))
					 (#match? @type "^[A-Z]"))
					
					; Assume all qualified names in struct patterns are enum constructors. (They're
					; either that, or struct names; highlighting both as constructors seems to be
					; the less glaring choice of error, visually.)
					(struct_pattern
					  type: (scoped_type_identifier
					    name: (type_identifier) @constructor))
					
					; Function calls
					
					(call_expression
					  function: (identifier) @function)
					(call_expression
					  function: (field_expression
					    field: (field_identifier) @function.method))
					(call_expression
					  function: (scoped_identifier
					    "::"
					    name: (identifier) @function))
					
					(generic_function
					  function: (identifier) @function)
					(generic_function
					  function: (scoped_identifier
					    name: (identifier) @function))
					(generic_function
					  function: (field_expression
					    field: (field_identifier) @function.method))
					
					(macro_invocation
					  macro: (identifier) @function.macro
					  "!" @function.macro)
					
					; Function definitions
					
					(function_item (identifier) @function)
					(function_signature_item (identifier) @function)
					
					(line_comment) @comment
					(block_comment) @comment
					
					(line_comment (doc_comment)) @comment.documentation
					(block_comment (doc_comment)) @comment.documentation
					
					"(" @punctuation.bracket
					")" @punctuation.bracket
					"[" @punctuation.bracket
					"]" @punctuation.bracket
					"{" @punctuation.bracket
					"}" @punctuation.bracket
					
					(type_arguments
					  "<" @punctuation.bracket
					  ">" @punctuation.bracket)
					(type_parameters
					  "<" @punctuation.bracket
					  ">" @punctuation.bracket)
					
					"::" @punctuation.delimiter
					":" @punctuation.delimiter
					"." @punctuation.delimiter
					"," @punctuation.delimiter
					";" @punctuation.delimiter
					
					(parameter (identifier) @variable.parameter)
					
					(lifetime (identifier) @label)
					
					"as" @keyword
					"async" @keyword
					"await" @keyword
					"break" @keyword
					"const" @keyword
					"continue" @keyword
					"default" @keyword
					"dyn" @keyword
					"else" @keyword
					"enum" @keyword
					"extern" @keyword
					"fn" @keyword
					"for" @keyword
					"if" @keyword
					"impl" @keyword
					"in" @keyword
					"let" @keyword
					"loop" @keyword
					"macro_rules!" @keyword
					"match" @keyword
					"mod" @keyword
					"move" @keyword
					"pub" @keyword
					"ref" @keyword
					"return" @keyword
					"static" @keyword
					"struct" @keyword
					"trait" @keyword
					"type" @keyword
					"union" @keyword
					"unsafe" @keyword
					"use" @keyword
					"where" @keyword
					"while" @keyword
					"yield" @keyword
					(crate) @keyword
					(mutable_specifier) @keyword
					(use_list (self) @keyword)
					(scoped_use_list (self) @keyword)
					(scoped_identifier (self) @keyword)
					(super) @keyword
					
					(self) @variable.builtin
					
					(char_literal) @string
					(string_literal) @string
					(raw_string_literal) @string
					
					(boolean_literal) @constant.builtin
					(integer_literal) @constant.builtin
					(float_literal) @constant.builtin
					
					(escape_sequence) @escape
					
					(attribute_item) @attribute
					(inner_attribute_item) @attribute
					
					"*" @operator
					"&" @operator
					"'" @operator

					; ADT definitions
					
					(struct_item
					    name: (type_identifier) @name) @definition.class
					
					(enum_item
					    name: (type_identifier) @name) @definition.class
					
					(union_item
					    name: (type_identifier) @name) @definition.class
					
					; type aliases
					
					(type_item
					    name: (type_identifier) @name) @definition.class
					
					; method definitions
					
					(declaration_list
					    (function_item
					        name: (identifier) @name)) @definition.method
					
					; function definitions
					
					(function_item
					    name: (identifier) @name) @definition.function
					
					; trait definitions
					(trait_item
					    name: (type_identifier) @name) @definition.interface
					
					; module definitions
					(mod_item
					    name: (identifier) @name) @definition.module
					
					; macro definitions
					
					(macro_definition
					    name: (identifier) @name) @definition.macro
					
					; references
					
					(call_expression
					    function: (identifier) @name) @reference.call
					
					(call_expression
					    function: (field_expression
					        field: (field_identifier) @name)) @reference.call
					
					(macro_invocation
					    macro: (identifier) @name) @reference.call
					
					; implementations
					
					(impl_item
					    trait: (type_identifier) @name) @reference.implementation
					
					(impl_item
					    type: (type_identifier) @name
					    !trait) @reference.implementation
					'''
					)
			

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

		elif (type in ["py", "pyw"]):

			self.build_argv = ["python3", self.buffer.name]
			self.run_argv = self.build_argv

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


		self.comment_regex = re.compile(fr"{self.comment_sign}")



		self.text_type = type
		# self.index_extern = False
		self.index_extern = True

		if (self.language):
			self.parser = tree_sitter.Parser(self.language)
			self.parser.set_language(self.language)


	def lex(self, text=None, start_file="", index=["1.0", "end"], should_highlight=True):
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
		print(dir(self.parser))

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
		# print("_--------START--------_")
		for index, (node, catch_type) in enumerate(self.results):
			# parent = node.parent
			# if (parent and parent != tree.root_node):
				# print("parent: ", parent, parent.text, node.text)
			# print(i, node.parent)

			start = f"{node.start_point[0]+offset_pos}.{node.start_point[1]}"
			end = f"{node.end_point[0]+offset_pos}.{node.end_point[1]}"
			print(node, catch_type, node.text)
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
				self.add_function(node.text.decode())
				self.add_define(node.text.decode(), ["", node.text.decode(), ""])
				
				self.current_scope[node.text.decode()] = {}
				self.current_scope = self.current_scope[node.text.decode()]
				# if (inside): self.current_scope = 

			elif (catch_type == "operator"):
				self.buffer.tag_add("operators", start, end)

			elif (catch_type == "string"):
				self.buffer.tag_add("quotes", start, end)

			elif (catch_type == "constant.builtin"):
				self.buffer.tag_add("keywords", start, end)

			elif (catch_type == "function.method"):
				self.buffer.tag_add("functions", start, end)

			elif (catch_type == "number"):
				self.buffer.tag_add("numbers", start, end)

			elif (catch_type == "comment"):
				self.buffer.tag_add("comments", start, end)

			elif (catch_type == "parenthesis" or catch_type == "special_chars"):
				self.buffer.tag_add("special_chars", start, end)

			elif (catch_type == "upcase"):
				self.buffer.tag_add("upcase", start, end)

			elif (catch_type == "type"):
				self.buffer.tag_add("keywords", start, end)

			elif (catch_type == "special_keywords"):
				self.buffer.tag_add("command_keywords", start, end)

			# elif (node.type == "identifier"):
				# if (node.text.decode() in self.keywords):
					# self.buffer.tag_add("keywords", start, end)

			if ((catch_type == "property" or catch_type == "delimeter")):
				# print("proprety: ", i)
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
				self.handle_function_definition(node)
				self.current_scope[name] = {}
				self.current_scope = self.current_scope[name]

			if (index < len(self.results)-1):
				if (node.start_point != self.results[index+1][0].start_point and node.end_point != self.results[index+1][0].end_point):
					last = [start, end]
					last_type = []
					last_type.append(node.type)
					last_type.append(catch_type)
				else:
					last_type.append(node.type)
					last_type.append(catch_type)

			# self.walk_scopes(node)

			# if (node.start_point == (0, 0)): continue
			# node.start_point = (node.start_point[0]+1, node.start_point[1])
			# node.end_point = (node.end_point[0]+1, node.end_point[1])
			# self.buffer.tag_add("keywords", f"{node.start_point[0]+1}.{node.start_point[1]}", f"{node.end_point[0]+1}.{node.end_point[1]}")


		# print("blocks: ", self.blocks)
		# print("_----------------_")
		# print(self.scopes)
		# print(dir(self.tree), self.tree.included_ranges)

	
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

			if (row == self.last_node_cursor_was_inside_of[0].start_point[0] or row == self.last_node_cursor_was_inside_of[0].end_point[0]): print("early return"); return

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

		for index, (node, other)  in enumerate(query, starting_point_offset):
			start = f"{node.start_point[0]+offset_pos}.{node.start_point[1]}"
			end = f"{node.end_point[0]+offset_pos}.{node.end_point[1]}"
			# TODO: iterate sibling(left) -> goto parent and start over
			#       ^-------------------------------------------^
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




