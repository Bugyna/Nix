import re
import tkinter
from itertools import chain


class highlighter(object):
	""" highlighter class storing all of the highlighting functions (and functions needed by the highlighting function) && keywords for each language """
	def __init__(self, parent, root):
		self.lang = "NaN"
		self.supported_languagues = ["NaN", "py", "cc", "cpp", "c", "txt", "html", "htm", "java", "jsp", "class"]

		self.command_keywords = parent.command_keywords
		print(self.command_keywords)

		self.Py_keywords = [
			'await', 'import', 'pass', 'break', 'in',
			'raise', 'class', 'is', 'return', 'continue', 'lambda', 'as', 'def', 'from',
			'nonlocal', 'assert', 'del', 'global', 'async', 'yield', "self"
			]

		self.Py_numerical_keywords = ['False', 'True', 'None']
		self.Py_logical_keywords = ['and', 'or', 'not', 'if', 'elif', 'else', 'for', 'try', 'except', 'finally', 'while', 'with'] 
		
		self.Py_keywords_regex = re.compile('|'.join(self.Py_keywords))#(r'\b(?:\|)\b'.join(self.Py_keywords))

		self.Java_keywords = [
			 'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue',
			 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if',
			 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private',
			 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw',
			 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null'
			]

		self.Java_keywords_regex = re.compile('|'.join(self.Java_keywords))


		self.C_keywords = [
			'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
		 	'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
		  	'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
   		]

		self.C_keywords_regex = re.compile('|'.join(self.C_keywords))

		self.Cplus_keywords = [
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

		# x = ['!--', '!DOCTYPE', 'a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'b', 'base', 'basefont', 'bdi', 'bdo', 'big', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 'wbr']
		# self.html_keywords = ['!--', '!DOCTYPE', 'a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'b', 'base', 'basefont', 'bdi', 'bdo', 'big', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'dir', 'div', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'link', 'main', 'map', 'mark', 'meta', 'meter', 'nav', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td', 'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 'wbr']
		self.html_keywords = ['<!-->', '<!DOCTYPE>', '<a>', '<abbr>', '<acronym>', '<address>', '<applet>', '<area>', '<article>', '<aside>', '<audio>', '<b>', '<base>', '<basefont>', '<bdi>', '<bdo>', '<big>', '<blockquote>', '<body>', '<br>', '<button>', '<canvas>', '<caption>', '<center>', '<cite>', '<code>', '<col>', '<colgroup>', '<data>', '<datalist>', '<dd>', '<del>', '<details>', '<dfn>', '<dialog>', '<dir>', '<div>', '<dl>', '<dt>', '<em>', '<embed>', '<fieldset>', '<figcaption>', '<figure>', '<font>', '<footer>', '<form>', '<frame>', '<frameset>', '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<head>', '<header>', '<hr>', '<html>', '<i>', '<iframe>', '<img>', '<input>', '<ins>', '<kbd>', '<label>', '<legend>', '<li>', '<link>', '<main>', '<map>', '<mark>', '<meta>', '<meter>', '<nav>', '<noframes>', '<noscript>', '<object>', '<ol>', '<optgroup>', '<option>', '<output>', '<p>', '<param>', '<picture>', '<pre>', '<progress>', '<q>', '<rp>', '<rt>', '<ruby>', '<s>', '<samp>', '<script>', '<section>', '<select>', '<small>', '<source>', '<span>', '<strike>', '<strong>', '<style>', '<sub>', '<summary>', '<sup>', '<svg>', '<table>', '<tbody>', '<td>', '<template>', '<textarea>', '<tfoot>', '<th>', '<thead>', '<time>', '<title>', '<tr>', '<track>', '<tt>', '<u>', '<ul>', '<var>', '<video>', '<wbr>', '</!-->', '</!DOCTYPE>', '</a>', '</abbr>', '</acronym>', '</address>', '</applet>', '</area>', '</article>', '</aside>', '</audio>', '</b>', '</base>', '</basefont>', '</bdi>', '</bdo>', '</big>', '</blockquote>', '</body>', '</br>', '</button>', '</canvas>', '</caption>', '</center>', '</cite>', '</code>', '</col>', '</colgroup>', '</data>', '</datalist>', '</dd>', '</del>', '</details>', '</dfn>', '</dialog>', '</dir>', '</div>', '</dl>', '</dt>', '</em>', '</embed>', '</fieldset>', '</figcaption>', '</figure>', '</font>', '</footer>', '</form>', '</frame>', '</frameset>', '</h1>', '</h2>', '</h3>', '</h4>', '</h5>', '</h6>', '</head>', '</header>', '</hr>', '</html>', '</i>', '</iframe>', '</img>', '</input>', '</ins>', '</kbd>', '</label>', '</legend>', '</li>', '</link>', '</main>', '</map>', '</mark>', '</meta>', '</meter>', '</nav>', '</noframes>', '</noscript>', '</object>', '</ol>', '</optgroup>', '</option>', '</output>', '</p>', '</param>', '</picture>', '</pre>', '</progress>', '</q>', '</rp>', '</rt>', '</ruby>', '</s>', '</samp>', '</script>', '</section>', '</select>', '</small>', '</source>', '</span>', '</strike>', '</strong>', '</style>', '</sub>', '</summary>', '</sup>', '</svg>', '</table>', '</tbody>', '</td>', '</template>', '</textarea>', '</tfoot>', '</th>', '</thead>', '</time>', '</title>', '</tr>', '</track>', '</tt>', '</u>', '</ul>', '</var>', '</video>', '</wbr>']
		
		self.Cplus_keywords_regex = re.compile('|'.join(self.Cplus_keywords))


		self.txt = parent.txt
		self.command_entry = parent.command_entry
		self.theme = parent.theme

		self.countingQuomarks = False
		

		# compiled regexes used by the highlighting functions
		self.quote_regex = re.compile(r"[\"\']")
		self.abc_regex = re.compile(r"[a-zA-Z_]")
		self.abc_upcase_regex = re.compile(r"^[A-Z_]+$")
		self.separator_regex = re.compile(r"[\s\.\,\:\;]")
		self.num_regex = re.compile(r"[0-9]")
		self.hex_regex = re.compile(r"^[0-9]+x[0-9a-fA-F]+$")
		self.special_char_regex = re.compile(r"[\&\^\|\{\}\[\]\@\$\(\)]")
		self.L_bracket_regex = re.compile(r"[\(]")
		self.operator_regex = re.compile(r"[\%\+\-\*\/\=\<\>]")
		self.string_special_char_regex = re.compile(r"[\\\{\}]")
		self.whitespace_regex = re.compile(r"[\t]")
		# self.C_preprocessor_regex = re.compile(r"^\#[A-Za-z]+$")
		self.C_preprocessor_regex = re.compile(r"\#")

		self.html_separator_regex = re.compile(r"[\;\ \=]")
		self.html_tag_start_regex = re.compile(r"[\<]")
		self.html_tag_end_regex = re.compile(r"[\>]")
		self.html_num_regex = re.compile(r"\#*[0-9]")
		self.html_L_bracket_regex = re.compile(r"[\{]")
		self.html_R_bracket_regex = re.compile(r"[\}]")
		self.html_color_num_regex = re.compile(r"^\#[0-9A-Fa-f]+$|^\-*[0-9]+[a-z]*$|^[0-9]*deg$")
		self.html_comment_start_regex = re.compile(r"<!--")
		self.html_comment_end_regex = re.compile(r"-->")

	def set_languague(self, arg: str=None):
		self.lang = arg
		if (self.lang == "c"):
			self.keywords = self.C_keywords
			self.numerical_keywords = []
			self.logical_keywords = []
			self.highlight = self.C_highlight
			self.comment_sign = "//"
			self.highlight = self.C_highlight

		elif (self.lang == "cpp" or self.lang == "cc"):
			self.keywords = self.Cplus_keywords
			self.numerical_keywords = []
			self.logical_keywords = []
			self.highlight = self.C_highlight
			self.comment_sign = "//"

		elif (self.lang == "py"):
			self.keywords = self.Py_keywords
			self.numerical_keywords = self.Py_numerical_keywords
			self.logical_keywords = self.Py_logical_keywords
			self.highlight = self.python_highlight
			self.comment_sign = "#"

		elif (self.lang == "html" or self.lang == "htm"):
			self.keywords = self.html_keywords
			self.highlight = self.html_highlight
			self.comment_sign = "<!-- -->"

		elif (self.lang == "java" or self.lang == "jsp" or self.lang == "class"):
			self.keywords = self.Java_keywords
			self.numerical_keywords = []
			self.logical_keywords = []
			self.highlight = self.C_highlight
			self.comment_sign = "//"

		elif (self.lang == "NaN" or self.lang == "txt"):
			self.comment_sign = "\t"
			self.highlight = self.no_highlight
		
		self.commment_regex = re.compile(rf"{self.comment_sign}")

	def get_line_lenght(self, line_no: int):
		""" gets the length of current line """
		for i, char in enumerate(self.txt.get(float(line_no), "end"), 0):
			if (re.match(r"\n", char)):
				return f"{line_no}.{i}"

	def no_highlight(self, line_no, line=None):
		pass

	def command_highlight(self, line: str=None):
		last_separator = "1.0"
		command_pattern = ""
		if line == None:
			line = self.command_entry.get("1.0", "end")

		self.command_entry.tag_remove("command_keywords", "1.0", "end")

		for i, current_char in enumerate(line, 0):
			# print(i ,current_char)
			if (self.abc_regex.match(current_char)):
				command_pattern += current_char
				continue

			elif (self.separator_regex.match(current_char)):
				if (command_pattern in self.command_keywords):
					index = f"1.{i}"
					self.command_entry.tag_add("command_keywords", last_separator, index)
				last_separator = f"1.{i}"
				
				
	def highlight_keyword(self, last_separator, index):
		if (self.pattern in self.keywords): #self.pattern in self.keywords #self.Py_keywords_regex.match(self.pattern)
			self.txt.tag_add("keywords", last_separator, index)
		
		elif (self.pattern in self.logical_keywords):
			self.txt.tag_add("logical_keywords", last_separator, index)

		elif (self.pattern in self.numerical_keywords):
			self.txt.tag_add("numbers", last_separator, index)

		elif (self.abc_upcase_regex.match(self.pattern)):
			self.txt.tag_add("numbers", last_separator, index)

		elif (self.hex_regex.match(self.pattern)):
			self.txt.tag_add("numbers", last_separator, index)
					

	def python_highlight(self, line_no: int ,line: str=None):
		""" highlighting for python language """
		if line == None:
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))+"\n"
			# print(line)

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)}"
		self.pattern = ""
		self.countingQuomarks = False
		
		self.txt.tag_remove("functions", last_separator, line_end_index)
		self.txt.tag_remove("keywords", last_separator, line_end_index)
		self.txt.tag_remove("logical_keywords", last_separator, line_end_index)
		self.txt.tag_remove("numerical_keywords", last_separator, line_end_index)
		self.txt.tag_remove("numbers", last_separator, line_end_index)
		self.txt.tag_remove("special_chars", last_separator, line_end_index)
		self.txt.tag_remove("comments", last_separator, line_end_index)
		self.txt.tag_remove("operators", last_separator, line_end_index)
		self.txt.tag_remove("quotes", last_separator, line_end_index)


		for i, current_char in enumerate(line, 0):
		
			if (self.quote_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.txt.tag_add("quotes", index)
				self.countingQuomarks = not self.countingQuomarks
				# self.countingQuomarks = not self.countingQuomarks

			elif (self.countingQuomarks):
				index = f"{line_no}.{i}"
				self.txt.tag_add("quotes", index)
				continue
			
			elif (self.abc_regex.match(current_char)):
				self.pattern += current_char
				# print(self.pattern)
				continue
				

			elif (self.commment_regex.match(current_char)): #comments
				index = f"{line_no}.{i}"
				self.txt.tag_add("comments", index, line_end_index)
				break

			elif (self.num_regex.match(current_char)): #numbers
				index = f"{line_no}.{i}"
				self.pattern += current_char
				self.txt.tag_add("numbers", index)
				continue
			
			elif (self.operator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.txt.tag_add("operators", index)
				self.highlight_keyword(last_separator, index)
				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				self.txt.tag_add("special_chars", index)
				if (self.L_bracket_regex.match(current_char)):
					self.txt.tag_add("functions", last_separator, index)
				else: self.highlight_keyword(last_separator, index)
				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue

			elif (self.separator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
			
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.pattern = ""

	def C_highlight(self, line_no: int, line: str=None):
		""" highlighting for C and C++ languages """
		if line == None:
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))+"\n"

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)}"
		self.pattern = ""
		self.countingQuomarks = False
		special_highlighting_mode = 0

		self.txt.tag_remove("quotes", last_separator, line_end_index)
		self.txt.tag_remove("functions", last_separator, line_end_index)
		self.txt.tag_remove("keywords", last_separator, line_end_index)
		self.txt.tag_remove("numbers", last_separator, line_end_index)
		self.txt.tag_remove("special_chars", last_separator, line_end_index)
		self.txt.tag_remove("comments", last_separator, line_end_index)
		self.txt.tag_remove("operators", last_separator, line_end_index)
		
		
		for i, current_char in enumerate(line, 0):

			try:
				if (self.commment_regex.match(current_char+line[i+1])): #comments
					index = f"{line_no}.{i}"
					self.txt.tag_add("comments", index, line_end_index)
					break

			except Exception:
				pass

			if (self.C_preprocessor_regex.match(current_char)):
				if (special_highlighting_mode == 0): special_highlighting_mode = 1
			
			if (special_highlighting_mode != 0):
				index = f"{line_no}.{i}"
				if (re.match(r" ", current_char) and special_highlighting_mode == 1): special_highlighting_mode = 2
				if (special_highlighting_mode == 1):
					self.txt.tag_add("functions", index)
				elif (special_highlighting_mode == 2):
					self.txt.tag_add("quotes", index)
				continue

			if (self.quote_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.txt.tag_add("quotes", index)
				if (self.countingQuomarks):
					self.countingQuomarks = False
				else:
					self.countingQuomarks = True
				# self.countingQuomarks = not self.countingQuomarks

			elif (self.countingQuomarks):
				index = f"{line_no}.{i}"
				self.txt.tag_add("quotes", index)
				continue
			
			elif (self.abc_regex.match(current_char)):
				self.pattern += current_char
				# print(self.pattern)
				continue	

			elif (self.num_regex.match(current_char)): #numbers
				self.pattern += current_char	
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.txt.tag_add("numbers", index)
				continue
			
			elif (self.operator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.txt.tag_add("operators", index)
				self.highlight_keyword(last_separator, index)
				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				self.txt.tag_add("special_chars", index)
				
				if (self.L_bracket_regex.match(current_char)):
					self.txt.tag_add("functions", last_separator, index)

				else: self.highlight_keyword(last_separator, index)

				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue

			if (self.separator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
			
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.pattern = ""
				
	def html_highlight(self, line_no: int=None, line: str=None):
		""" I am crying while looking at this hideous thing """
		if line == None:
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))+"\n"


		tag_start_index = f""
		tag_end_index = f""
		last_separator_index = 0
		last_separator = f"{line_no}.0"
		line_end_index = f"{line_no}.{len(line)}"
		in_tag = False
		in_comment = False
		in_special_tag = False
		last_pattern = ""
		self.pattern = ""
		self.countingQuomarks = False
		tag_argument_index = 0

		self.txt.tag_remove("quotes", last_separator, line_end_index)
		self.txt.tag_remove("functions", last_separator, line_end_index)
		self.txt.tag_remove("keywords", last_separator, line_end_index)
		self.txt.tag_remove("numbers", last_separator, line_end_index)
		self.txt.tag_remove("special_chars", last_separator, line_end_index)
		self.txt.tag_remove("comments", last_separator, line_end_index)
		self.txt.tag_remove("operators", last_separator, line_end_index)
		
		
		for i, current_char in enumerate(line, 0):

			# if (self.html_abc_regex.match(current_char)):
			self.pattern += current_char

			# if (self.html_L_bracket_regex.match(current_char)):
			# 	index = f"{line_no}.{i-len(self.pattern+last_pattern)}"
			# 	index1 = f"{line_no}.{i}"
			# 	self.txt.tag_add("functions", index, index1)

			if (self.html_separator_regex.match(current_char)):
				last_pattern = self.pattern
				self.pattern = ""
				last_separator_index = i
				last_separator = f"{line_no}.{i}"
				if (in_tag):
					if (tag_argument_index < 1): tag_argument_index += 1

			if (self.quote_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.txt.tag_add("special_chars", index)
				self.countingQuomarks = not self.countingQuomarks
				# self.countingQuomarks = not self.countingQuomarks

			elif (self.countingQuomarks):
				index = f"{line_no}.{i}"
				self.txt.tag_add("special_chars", index)
				continue

			if (self.html_color_num_regex.match(self.pattern)):
				index = f"{line_no}.{i-len(self.pattern)}"
				index1 = f"{line_no}.{i+1}"
				try:
					self.txt.tag_configure(self.pattern, background=self.pattern)
				except Exception:
					pass
				self.txt.tag_add("numbers", index, index1)
				self.txt.tag_add(self.pattern, index)

			if (self.html_comment_start_regex.match(self.pattern)):
				index = f"{line_no}.{i+1}"
				self.txt.tag_add("comments", tag_start_index, index)
				in_comment = True

			if (in_comment):
				index = f"{line_no}.{i}"
				self.txt.tag_add("comments", index)

			if (self.html_comment_end_regex.match(self.pattern)):
				in_comment = False

			if (self.html_tag_start_regex.match(current_char)):
				tag_start_index = f"{line_no}.{i}"
				index = f"{line_no}.{i+1}"
				self.pattern = ""
				self.pattern += current_char
				last_separator_index = i
				last_separator = f"{line_no}.{i}"
				in_tag = True

			elif (self.html_tag_end_regex.match(current_char)):
				in_tag = False
				self.pattern = ""
				last_separator_index = i
				last_separator = f"{line_no}.{i}"
				tag_argument_index = 0

			elif (in_tag):
				index = f"{line_no}.{i}"
				if (tag_argument_index == 0):
					self.txt.tag_add("keywords", index)
				elif (tag_argument_index == 1):
					self.txt.tag_add("quotes", index)

	def unhighlight(self, line_no: int, line: str=None):
		if line == None:
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)}"
		
		self.txt.tag_remove(["quotes"], last_separator, line_end_index)
		self.txt.tag_remove(["functions"], last_separator, line_end_index)
		self.txt.tag_remove(["keywords"], last_separator, line_end_index)
		self.txt.tag_remove(["logical_keywords"], last_separator, line_end_index)
		self.txt.tag_remove(["numerical_keywords"], last_separator, line_end_index)
		self.txt.tag_remove(["numbers"], last_separator, line_end_index)
		self.txt.tag_remove(["special_chars"], last_separator, line_end_index)
		self.txt.tag_remove(["comments"], last_separator, line_end_index)
		self.txt.tag_remove(["operators"], last_separator, line_end_index)
		
		
