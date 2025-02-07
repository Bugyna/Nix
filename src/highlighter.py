import threading
import tkinter
import string
import re
import os

from lexer import *

az = [*string.ascii_letters, "_"]
num = string.digits
alphanum = [*az, *num]

class highlighter(object):
	""" highlighter class storing all of the highlighting functions (and functions needed by the highlighting function) && keywords for each language """
	def __init__(self, parent, buffer):
		self.lang = "NaN"
		self.supported_languagues = [
			"NaN", "py", "cc", "hh", "cpp", "hpp", "c", "h", "txt", "html", "htm", "java", "jsp", "class", "css", "go",
			"sh", "diary", "bat", "json"
		]

		# FOR FUTURE REFERENCE
		# self.language_options = {
			# "(c|h)$":
			# "(cpp|hpp|cc|hh)$":
			# "(py|pyw)$":
			# "html|htm|css":
			# "java|jsp|class":
			# "php":
			# "go":
			# "sh":
			# "bat|cmd":
			# "diary": 
		# }

		# I could've totally fit this in normal strings... Too late now
		self.language_init = {
			"(c|h)$": "#include <stdlib.h>\n#include <stdio.h>\n\nint main (int argc, char* argv[]) {\n\n\treturn 0;\n}",
			#I have no idea how c++ strings work :D
			"(cpp|hpp|cc|hh)$": "#include <iostream>\n\nint main(int argc, char* argv[]) {\t\n\t\n\treturn 0;\n}",
			"(py|pyw)$": "\n\ndef main():\n\tpass\n\nif __name__ == \"__main__\":\n\tmain()",
			"html|htm|css": "<!DOCTYPE HTML>\n<html lang=\"en\">\n<head>\n\t<title> placeholder </title>\n\n</head>\n\n<body>\n\n</body>\n</html>",
			"java|jsp|class": "",
			"cs": "",
			"php": "<!DOCTYPE HTML>\n<html lang=\"en\">\n<head>\n\t<title> placeholder </title>\n\n</head>\n\n<body>\n\n\t<?php\n\t\t\n\t?>\n</body>\n</html>",
			"js": "<!DOCTYPE HTML>\n<html lang=\"en\">\n<head>\n\t<title> placeholder </title>\n\n</head>\n\n<body>\n\n\t<script>\n\t\t\n\t</script>\n</body>\n</html>",
			"go": "",
			"sh": "\n",
			"bat|cmd": "",
			"diary": "",
		}

		self.buffer = buffer
		self.parent = parent
		self.theme = parent.theme


		self.language_options = {
			"(c|h)$": {"comment_sign": "//", "make_argv": ["make"]},
			"(cpp|hpp|cc|hh)$": {"keywords": self.cpp_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["make"]},
			"lb": {"keywords": self.c_keywords, "numerical_keywords": self.c_numerical_keywords, "logical_keywords": self.c_logical_keywords, "highlight": self.c_highlight, "comment_sign": ";;", "make_argv": ["./main", f"{self.buffer.full_name}"]},
			# "tex|bbl": {"keywords": self.c_keywords, "numerical_keywords": self.c_numerical_keywords, "logical_keywords": self.c_logical_keywords, "highlight": self.c_highlight, "comment_sign": "%%", "make_argv": ["./main", f"{self.buffer.full_name}"]},
			"cs": {"keywords": self.cpp_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["mcs", f"{self.buffer.full_name}"]},
			"(py|pyw)$": {"keywords": self.py_keywords, "numerical_keywords": self.py_numerical_keywords, "logical_keywords": self.py_logical_keywords, "highlight": self.python_highlight, "comment_sign": "#", "make_argv": ["python3", f"{self.buffer.full_name}"]},
			"html|htm|css": {"keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.html_highlight, "comment_sign": "<!-- ", "make_argv": ["firefox -new-window", self.buffer.full_name]},
			"java|jsp|class": {"keywords": self.java_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["firefox", "-new-window", self.buffer.full_name]},
			"cs": {"keywords": self.java_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["msc", self.buffer.full_name]},
			"php": {"keywords": self.php_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ""},
			"js": {"keywords": self.javascript_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ""},
			"go": {"keywords": self.go_keywords, "numerical_keywords": self.go_numerical_keywords, "logical_keywords": self.go_logical_keywords, "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["go", "run", f"{self.buffer.full_name}"]},
			"rs": {"keywords": self.rust_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["cargo", "build"], 'run_argv': ["cargo", "run"]},
			"hs": {"keywords": self.rust_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["make"]},
			"sh": {"keywords": self.sh_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "#", "make_argv": [f"./{self.buffer.full_name}"]},
			"bat|cmd": {"keywords": self.sh_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "::", "make_argv": [f"./{self.buffer.full_name}"]},
			"json": {"keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "//", "make_argv": ""},
			"asm": {"keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": ";;", "make_argv": ""},
			"None": {"keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "#", "make_argv": ""},
		}

	def set_languague(self, arg: str=None):
		if (self.lang == arg): return
		self.lang = arg

		for key in self.language_options:
			if (re.match(key, self.lang)):
				self.set_lang_options(key)
				return
		
		self.set_lang_options("None")

	def set_lang_options(self, key):
		lang_set = self.language_options[key]
		# self.new = lang_set["regex"]
		self.keywords = lang_set["keywords"]
		self.numerical_keywords = lang_set["numerical_keywords"]
		self.logical_keywords = lang_set["logical_keywords"]
		self.highlight = lang_set["highlight"]
		self.comment_sign = lang_set["comment_sign"]
		self.commment_regex = re.compile(rf"{self.comment_sign}")
		self.buffer.make_argv = lang_set["make_argv"]
		if "run_argv" in lang_set:
			self.buffer.run_argv = lang_set["run_argv"]
			print("run_argv", self.buffer.run_argv)

		else:
			self.buffer.run_argv = ["./main"]
		
		if (key != "None"): self.buffer.lexer = C_LEXER(self.parent, self.buffer, key)
		# elif (key == "(py|pyw)$"): self.buffer.lexer = C_LEXER(self.parent, self.buffer)
		elif (key == "tex|bbl"): self.buffer.lexer = PY_LEXER(self.parent, self.buffer)
		else: self.buffer.lexer = EMPTY_LEXER(self.parent, self.buffer)
		# self.buffer.lexer.keywords = self.keywords	

	def set_pattern(self, pattern):
		if (self.pattern): self.last_pattern = self.pattern
		self.pattern = pattern
	
	

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

