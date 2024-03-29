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

		self.command_keywords = list(parent.parser.commands.keys())

		self.py_keywords = [
			'await', 'import', 'pass', 'break', 'in',
			'raise', 'class', 'is', 'return', 'continue', 'lambda', 'as', 'def', 'from',
			'nonlocal', 'assert', 'del', 'global', 'async', 'yield'
		]

		self.py_numerical_keywords = ['False', 'True', 'None']
		self.py_logical_keywords = [
			'and', 'or', 'not', 'if', 'elif', 'else', 'for', 'try', 'except', 'finally','while', 'with', 'self'] 
		self.py_var_keywords = [
			"object", "int", "str", "float", "list", "Any", 
		]
 		# self.py_keyword_regex = (r'\b(?:\|)\b'.join(self.py_keywords)) #re.compile('|'.join(self.py_keywords))

		# self.py_keyword_regex = r"(__bases__|__builtin__|__class__|__debug__|__dict__|__doc__|__file__|__members__|__methods__|__name__|__self__|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\y"
		
		self.java_keywords = [
			 'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue',
			 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if',
			 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private',
			 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw',
			 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null'
		]

		self.javascript_keywords = [
			'async', 'await', 'break', 'case', 'catch', 'const', 'continue', 'debugger', 'default',
			'delete', 'do', 'else', 'export', 'finally', 'for', 'get', 'if', 'import', 'from', 'in', 'of',
			'instanceof', 'let', 'new', 'reject', 'resolve', 'return', 'set', 'static', 'super', 'switch',
			'this', 'throw', 'try', 'typeof', 'var', 'void', 'while', 'with', 'yield', 'enum', 'implements',
			'interface', 'package', 'private', 'protected', 'public', 'globalThis', 'Infinity', 'null', 'undefined',
			'NaN', 'true', 'false', 'Array', 'Boolean', 'Date', 'Enumerator', 'Error', 'Function', 'Generator', 'Map',
			'Math', 'Number', 'Object', 'Promise', 'Proxy', 'Reflect', 'RegExp', 'Set', 'String', 'Symbol', 'WeakMap',
			'WeakSet', 'alert', 'decodeURI', 'decodeURIComponent', 'document', 'encodeURI', 'encodeURIComponent', 'escape',
			'eval', 'isFinite', 'isNaN', 'parseFloat', 'parseInt', 'unescape', 'uneval', 'window'	
		]


		self.c_keywords = [
			'auto', 'break', 'char', 'const', 'continue', 'default', 'do', 'double',
		 	'extern', 'float', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
		  	'static', 'struct', 'typedef', 'union', 'unsigned', 'void', 'volatile', "size_t", "u8", "u16", "u32", "u64", "bool"
   		]

		self.c_numerical_keywords = [
			"false", "true", "enum", "NULL", 
		]

		self.c_logical_keywords = [
			"switch", "case", "if", "else", "goto", "for", "while"
		]

		self.cpp_keywords = [
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

		self.go_keywords = [
			 'break', 'func', 'interface', 'select', 'defer', 'go', 'map', 'struct', 'chan',
			 'package', 'const', 'fallthrough', 'range', 'type', 'continue', 'import', 'return', 'var',
			 "uint", "uint8", "uint16", "uint32", "uint64", "uintptr", "rune", "byte", "int", "int8", "int16",
			 "int32", "int64", "float32", "float64", "complex64", "complex128", "bool", "string"
		]

		self.go_numerical_keywords = [
			"true", "false"
		]

		self.go_logical_keywords = [
			"if", "else", "switch", "case", 'default', "for", "while", "goto"
		]

		self.rust_keywords = [
		 'abstract', 'alignof', 'as', 'become', 'box', 'break', 'const', 'continue', 'crate', 'do', 'dyn', 'else', 'enum', 'extern', 'false',
		 'final', 'fn', 'for', 'if', 'impl', 'in', 'let', 'loop', 'macro', 'match', 'mod', 'move', 'mut', 'offsetof', 'override', 'priv', 'pub', 'pure', 'ref', 'return', 'sizeof',
		 'static', 'self', 'struct', 'super', 'true', 'trait', 'type', 'typeof', 'unsafe', 'unsized', 'use', 'virtual', 'where', 'while', 'yield', 'bool', 'str', 'isize', 'usize',
		 'i8', 'i16', 'i32', 'i64', 'f32', 'f64'
		]

		self.sh_keywords = ['expression', 'alias', 'bg', 'bind', 'builtin', 'caller', 'case', 'command', 'compgen',
		 'complete', 'continue', 'declare', 'dirs', 'disown', 'echo', 'enable', 'eval', 'exec', 'exit',
		 'export', 'false', 'fc', 'fg', 'for', 'getopts', 'hash', 'help', 'history', 'if', 'jobs', 'kill', 'let',
		 'local', 'logout', 'popd', 'printf', 'pushd', 'pwd', 'read', 'readonly', 'return', 'select', 'set', 'shift',
		 'shopt', 'source', 'suspend', 'test', 'time', 'times', 'trap', 'true', 'type', 'typeset', 'ulimit', 'umask',
		 'unalias', 'unset', 'until', 'variables', 'while'
		]

		# BATCH IS FUCKING RETARDED
		# self.bat_keywords = ['adprep', 'append', 'arp', 'assoc', 'at', 'atmadm', 'attrib', 'auditpol', 'autochk',
		 # 'autoconv', 'autofmt', 'bcdboot', 'bcdedit', 'bdehdcfg', 'bitsadmin', 'bootcfg', 'break', 'break', 'cacls',
		 # 'cd', 'certreq', 'certutil', 'chcp', 'change', 'choice', 'cipher', 'chdir', 'chkdsk', 'chkntfs', 'chglogon',
		 # 'chgport', 'chgusr', 'clip', 'cls', 'clscluadmin', 'cluster', 'cmd', 'cmdkey', 'cmstp', 'color',
		 # 'comp', 'compact', 'convert', 'copy', 'cprofile', 'cscript', 'csvde', 'date', 'dcdiag', 'dcgpofix', 'dcpromo',
		 # 'defra', 'del', 'dfscmd', 'dfsdiag', 'dfsrmig', 'diantz', 'dir', 'dirquota', 'diskcomp', 'diskcopy', 'diskpart',
		 # 'diskperf', 'diskraid', 'diskshadow', 'dispdiag', 'doin', 'dnscmd', 'doskey', 'driverquery', 'dsacls', 'dsadd',
		 # 'dsamain', 'dsdbutil', 'dsget', 'dsmgmt', 'dsmod', 'dsmove', 'dsquery', 'dsrm', 'echo', 'edit', 'endlocal', 'erase',
		 # 'esentutl', 'eventcreate', 'eventquery', 'eventtriggers', 'evntcmd', 'expand', 'extract', 'fc', 'filescrn', 'find',
		 # 'findstr', 'finger', 'flattemp', 'fonde', 'forfiles', 'format', 'freedisk', 'fs', 'fsutil', 'ftp', 'ftype', 'fveupdate',
		 # 'getmac', 'gettype', 'gpfixup', 'gpresult', 'gpupdate', 'graftabl', 'hashgen', 'hep', 'help', 'helpctr', 'hostname',
		 # 'icacls', 'iisreset', 'inuse', 'ipconfig', 'ipxroute', 'irftp', 'ismserv', 'jetpack', 'keyb', 'klist', 'ksetup',
		 # 'ktmutil', 'ktpass', 'label', 'ldifd', 'ldp', 'lodctr', 'logman', 'logoff', 'lpq', 'lpr', 'macfile', 'makecab',
		 # 'manage-bde', 'mapadmin', 'md', 'mkdir', 'mklink', 'mmc', 'mode', 'more', 'mount', 'mountvol', 'move', 'mqbup', 'mqsvc',
		 # 'mqtgsvc', 'msdt', 'msg', 'msiexec', 'msinfo32', 'mstsc', 'nbtstat', 'net computer', 'net group', 'net localgroup',
		 # 'net print', 'net session', 'net share', 'net start', 'net stop', 'net use', 'net user', 'net view', 'net', 'netcfg',
		 # 'netdiag', 'netdom', 'netsh', 'netstat', 'nfsadmin', 'nfsshare', 'nfsstat', 'nlb', 'nlbmgr', 'nltest', 'nslookup',
		 # 'ntackup', 'ntcmdprompt', 'ntdsutil', 'ntfrsutl', 'openfiles', 'pagefileconfig', 'path', 'pathping', 'pause',
		 # 'pbadmin', 'pentnt', 'perfmon', 'ping', 'pnpunatten', 'pnputil', 'popd', 'powercfg', 'powershell', 'powershell_ise',
		 # 'print', 'prncnfg', 'prndrvr', 'prnjobs', 'prnmngr', 'prnport', 'prnqctl', 'prompt', 'pubprn', 'pushd',
		 # 'pushprinterconnections', 'pwlauncher', 'qappsrv', 'qprocess', 'nquery', 'quser', 'qwinsta', 'rasdial', 'rcp',
		 # 'rd', 'rdpsign', 'regentc', 'recover', 'redircmp', 'redirusr', 'reg', 'regini', 'regsvr32', 'relog', 'ren',
		 # 'rename', 'rendom', 'repadmin', 'repair-bde', 'replace', 'reset', 'restore', 'rxec', 'risetup', 'rmdir',
		 # 'robocopy', 'route', 'rpcinfo', 'rpcping', 'rsh', 'runas', 'rundll32', 'rwinsta', 'scp', 'sc', 'setlocal',
		 # 'session', 'schtasks', 'scwcmd', 'secedit', 'serverceipoptin', 'servrmanagercmd', 'serverweroptin', 'set', 'setspn', 'setx',
		 # 'sfc', 'shadow', 'shift', 'showmount', 'shutdown', 'sort', 'ssh', 'start', 'storrept', 'subst', 'sxstrace', 'ysocmgr',
		 # 'systeminfo', 'takeown', 'tapicfg', 'taskkill', 'tasklist', 'tcmsetup', 'telnet', 'tftp', 'time', 'timeout',
		 # 'title', 'tlntadmn', 'tpmvscmgr', 'tpmvscmgr', 'tacerpt', 'tracert', 'tree', 'tscon', 'tsdiscon', 'tsecimp',
		 # 'tskill', 'tsprof', 'type', 'typeperf', 'tzutil', 'uddiconfig', 'umount', 'unlodctr', 'ver', 'verify', 'verifier',
		 # 'verif', 'vol', 'vssadmin', 'w32tm', 'waitfor', 'wbadmin', 'wdsutil', 'wecutil', 'wevtutil', 'where', 'whoami', 'winnt',
		 # 'winnt32', 'winpop', 'winrm', 'winrs', 'winsat', 'wlbs', 'mic', 'wscript', 'xcopy'
		 # ]

		self.php_keywords = [
		 '__halt_compiler', 'abstract', 'and', 'array', 'as', 'break', 'callable', 'case', 'catch', 'class', 'clone', 'const', 'continue', 'declare', 'default',
		 'die', 'do', 'echo', 'else', 'elseif', 'empty', 'enddeclare', 'endfor', 'endforeach', 'endif', 'endswitch', 'endwhile', 'eval', 'exit', 'extends', 'final', 'for', 'foreach',
		 'function', 'global', 'goto', 'if', 'implements', 'include', 'include_once', 'instanceof', 'insteadof', 'interface', 'isset', 'list', 'namespace', 'new', 'or', 'print',
		 'private', 'protected', 'public', 'require', 'require_once', 'return', 'static', 'switch', 'throw', 'trait', 'try', 'unset', 'use', 'var', 'while', 'xor'
		]


		self.comment_keywords = ["todo", "note"]

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


		# self.all_regex = r"[A-Z_0-9]{2,}|#(.)*|([\%\+\-\*\/\=\<\>\!\^\&\|]+)|[\@\$\\]+|[\{\}\[\]\(\)]+|[^a-zA-Z]*[0-9]{1,}|([\"\']|\"(.)*\"|\'(.)\')|\y(__bases__|__builtin__|__class__|__debug__|__dict__|__doc__|__file__|__members__|__methods__|__name__|__self__|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\y"
		self.all_regex = r"\w+(?=\()|\b[A-Z_0-9]{2,}\b|#(.)*|([\%\+\-\*\/\=\<\>\!\^\&\|]+)|[\@\$\\]+|[\{\}\[\]\(\)]+|\b[0-9]+\b|((\"(.)*\")|(\'(.)*\'))|\b(self|True|False|None|__bases__|__builtin__|__class__|__debug__|__dict__|__doc__|__file__|__members__|__methods__|__name__|__self__|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b"
		
		self.keyword_regex = re.compile(r"(__bases__|__builtin__|__class__|__debug__|__dict__|__doc__|__file__|__members__|__methods__|__name__|__self__|as|assert|async|await|break|class|continue|def|del|from|global|import|in|is|lambda|nonlocal|pass|raise|return|yield)")
		self.numerical_keyword_regex = re.compile(r"\b(False|True|None)\b")
		self.logical_keyword_regex = re.compile(r"\b(and|or|not|if|elif|else|for|try|except|finally|while|with|self|xor)\b")
			
		self.upcase_regex = re.compile(r"\b([A-Z_]{2,}|[A-Z_]+[A-Z_0-9]+)\b")
		self.function_identifier_regex = re.compile(r"\w+")

		self.buffer = buffer
		self.parent = parent
		self.theme = parent.theme

		self.in_quote = False
		self.in_comment = False
		
		self.human_error = []
		self.brackets = [[],[],[]]
		self.bracket_pairs = {}
		self.bracket_pair_type = {
			"(" : ")",
			"[" : "]",
			"{" : "}",
			")" : "(",
			"]" : "[",
			"}" : "{",
		}

		self.vars = []
		self.objs = []
		self.funcs = []
		self.pattern = ""
		self.last_pattern = ""

		# compiled regexes used by the highlighting functions
		self.quote_regex = re.compile(r"((\"(.)*\")|(\'(.)*\'))")
		self.quote_regex = re.compile(r"\"|\'")
		self.comment_regex = re.compile(r"#(.)*")
		self.abc_regex = re.compile(r"[a-zA-Z_]")
		self.abc_upcase_regex = re.compile(r"^[A-Z_]+$") #|^[A-Z]+_[A-Za-z0-9]+")
		self.separator_regex = re.compile(r"[\s\.\,\:\;]")
		self.number_regex = re.compile(r"[0-9]+")
		self.special_number_regex = re.compile(r"^0b+[0-1]+$|^0x+[0-9a-fA-F]+$")
		self.special_char_regex = re.compile(r"[\$\&\^\|\@\$\\]+")
		self.brackets_regex = re.compile(r"[\{\}\[\]\(\)]+")
		self.left_brackets_regex = re.compile(r"[\(\[\{]")
		self.right_brackets_regex = re.compile(r"[\)\]\}]")
		self.function_separator_regex = re.compile(r"[\(]")
		self.operator_regex = re.compile(r"[\%\+\-\*\/\=\<\>\!]+")
		self.string_special_char_regex = re.compile(r"[\\\{\}]")
		self.whitespace_regex = re.compile(r"[\t]")
		self.c_preprocessor_regex = re.compile(r"\#")

		self.html_separator_regex = re.compile(r"[\;\ \=]")
		self.html_tag_start_regex = re.compile(r"[\<]")
		self.html_tag_end_regex = re.compile(r"[\>]")
		self.html_number_regex = re.compile(r"\#*[0-9A-Fa-f]")
		self.html_L_bracket_regex = re.compile(r"[\{]")
		self.html_R_bracket_regex = re.compile(r"[\}]")
		self.html_color_number_regex = re.compile(r"^\#[0-9A-Fa-f]+$|^\-*[0-9]+[a-z]*$|^[0-9]*deg$")
		self.html_comment_start_regex = re.compile(r"<!--")
		self.html_comment_end_regex = re.compile(r"-->")

		self.color_code_regex = re.compile(r"(^\#[0-9a-fA-F]{6}$)")

		self.language_options = {
			"(c|h)$": {"keywords": self.c_keywords, "numerical_keywords": self.c_numerical_keywords, "logical_keywords": self.c_logical_keywords, "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["make"]},
			"(cpp|hpp|cc|hh)$": {"keywords": self.cpp_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["make"]},
			"cs": {"keywords": self.cpp_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["mcs", f"{self.buffer.full_name}"]},
			"(py|pyw)$": {"keywords": self.py_keywords, "numerical_keywords": self.py_numerical_keywords, "logical_keywords": self.py_logical_keywords, "highlight": self.python_highlight, "comment_sign": "#", "make_argv": ["python3", f"{self.buffer.full_name}"]},
			"html|htm|css": {"keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.html_highlight, "comment_sign": "<!-- ", "make_argv": ["firefox -new-window", self.buffer.full_name]},
			"java|jsp|class": {"keywords": self.java_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["firefox", "-new-window", self.buffer.full_name]},
			"cs": {"keywords": self.java_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["msc", self.buffer.full_name]},
			"php": {"keywords": self.php_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ""},
			"js": {"keywords": self.javascript_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ""},
			"go": {"keywords": self.go_keywords, "numerical_keywords": self.go_numerical_keywords, "logical_keywords": self.go_logical_keywords, "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["go", "run", f"{self.buffer.full_name}"]},
			"rs": {"keywords": self.rust_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.c_highlight, "comment_sign": "//", "make_argv": ["cargo", "build"]},
			"sh": {"keywords": self.sh_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "#", "make_argv": [f"./{self.buffer.full_name}"]},
			"bat|cmd": {"keywords": self.sh_keywords, "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "::", "make_argv": [f"./{self.buffer.full_name}"]},
			"json": {"keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "//", "make_argv": ""},
			"asm": {"keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": ";;", "make_argv": ""},
			"None": {"keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "#", "make_argv": ""},
		}

		# self.language_options = {
			# "(py|pyw)$": {"regex": {"keywords": ["if|else"], "numerical_keywords": [], "logical_keywords": [], "comments": ["\#(.)*"], "special_chars": ["\(|\)"], "numbers": "^[0-9]+$", "quotes": ["('(.)*')|(\A\"(.)*\"?)"]}, "highlight": self.new_highlight, "comment_sign": "#", "make_argv": ["python3", f"{self.buffer.full_name}"]},
			# "None": {"regex": {}, "keywords": [], "numerical_keywords": [], "logical_keywords": [], "highlight": self.script_highlight, "comment_sign": "#", "make_argv": ""},
		# }

	def set_languague(self, arg: str=None):
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
		
		if (key != "None" and key != "(py|pyw)$"): self.buffer.lexer = C_LEXER(self.parent, self.buffer)
		elif (key == "(py|pyw)$"): self.buffer.lexer = PY_LEXER(self.parent, self.buffer)
		else: self.buffer.lexer = EMPTY_LEXER(self.parent, self.buffer)
		# self.buffer.lexer.keywords = self.keywords	

	def set_pattern(self, pattern):
		if (self.pattern): self.last_pattern = self.pattern
		self.pattern = pattern

	def suggest(self, line_no: int = None, line: str = None) -> None:
		# if (not line):
			# line = self.buffer.get(float(line_no), self.get_line_lenght(line_no))

		token = self.buffer.current_token
		if (re.match(r"[a-zA-Z_]+([0-9])*", token)):
			ret = ""
			for m in self.vars:
				if (re.match(token, m)):
					ret += m+":variable | "
			for m in self.funcs:
				if (re.match(token, m)):
					ret += m+":function | "
	
			if (ret): self.parent.notify(ret)
		else: return
				
		# token = ""
		# for i, current_char in enumerate(line, 0):
			# if (self.abc_regex.match(current_char)):
				# token += current_char
				
				# tt = ""
				# for m in self.vars:
					# if (re.match(token, m)):
						# tt += m+":variable | "
				# for m in self.funcs:
					# if (re.match(token, m)):
						# tt += m+":function | "

				# self.parent.notify(tt)

			# else:
				# token = ""


	def lex_line(self, line_no: int = None, line: str = None) -> None:
		if (not line):
			line = self.buffer.get(float(line_no), self.get_line_lenght(line_no))
			
		token = ""
		last_token = ""
		index = ""
		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		
		for i, current_char in enumerate(line, 0):
			if (self.abc_regex.match(current_char)):
				token += current_char

			elif (self.operator_regex.match(current_char)):
				index = f"{line_no}.{i}"

				if (current_char == "=" and last_token != "" and last_token not in self.vars):
					self.vars.append(last_token)
				
				last_token = token
				token = ""
				
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.brackets_regex.match(current_char)):
				index = f"{line_no}.{i}"
				if (self.function_separator_regex.match(current_char) and last_token == "def" and token not in self.funcs):
					self.funcs.append(token)

				last_token = token
				token = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				
				last_token = token
				token = ""
				
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue

			elif (self.separator_regex.match(current_char)):
				index = f"{line_no}.{i}"
			
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				last_token = token
				token = ""
		

	def get_line_lenght(self, line_no: int):
		""" gets the length of current line """
		return f"{line_no}.0 lineend+1c"

	def no_highlight(self, line_no, line=None):
		pass

	def command_highlight(self, line: str=None):
		last_separator = "1.0"
		command_pattern = ""
		if (line == None):
			line = self.parent.command_entry.get("1.0", "end")

		self.parent.command_entry.tag_remove("command_keywords", "1.0", "end")

		for i, current_char in enumerate(line, 0):
			if (self.abc_regex.match(current_char)):
				command_pattern += current_char
				continue

			elif (self.separator_regex.match(current_char)):
				for c in self.command_keywords:
					if (re.match(c, command_pattern)):
						index = f"1.{i}"
						self.parent.command_entry.tag_add("command_keywords", last_separator, index)
				last_separator = f"1.{i}"
				

	def bracket_pair_highlight(self) -> None:
		# self.buffer.tag_remove("pair", "1.0", "end")
	
		index = self.buffer.index("insert")
		# try: print("curr index: ", index, "potent: ", self.bracket_pairs[index]) 
		# except KeyError as e: print("Keyerror: ", e)
		if (self.brackets_regex.match(self.buffer.get(index))):
			try:
				self.buffer.tag_add("pair", self.bracket_pairs[index])
				# if (self.parent.sameline_check(index, self.bracket_pairs[index])):
					# i1, i2 = self.parent.inline_index_sort(index, self.bracket_pairs[index])
					# if (self.parent.underline_pairs): self.buffer.tag_add("underline", f"{i1}+1c", i2)
			except Exception: pass
				# self.bracket_pairs.pop(self.bracket_pairs[index])
				# self.bracket_pairs.pop(index)
		# try: self.buffer.tag_add("pair", self.bracket_pairs[self.buffer.index("insert")])
		# except Exception:
			# try: self.buffer.tag_add("pair", self.bracket_pairs[self.buffer.index("insert-1c")])
			# except Exception: pass


	# def bracket_pair_make(self, char: str):
	def bracket_pair_make(self, index=None):
		self.brackets = [] #clearing useless things
		self.human_error = []
		# self.bracket_pairs = {}
		self.buffer.tag_remove("pair", "1.0", "end")

		if (not index): index="insert"


		for p in ["", "-1c", "+1c"]:
			if (self.buffer.get(index+p) in "()[]{}"):
				index = self.buffer.index(index+p)
				break
			

		char = self.buffer.get(index)

		if (char not in "()[]{}"): return
		elif (char in "([{"):
			self.seek_bracket_after(index)

		elif (char in ")]}"):
			self.seek_bracket_before(index)
		
		# else:
			# index = self.buffer.index("insert")
			# try: self.bracket_pairs.pop(self.bracket_pairs[index]); self.bracket_pairs.pop(index)
			# except Exception: pass
			# return

		# self.bracket_pair_highlight()

	def seek_bracket_before(self, index=None):
		i = 1
		if (not index): index = "insert"
		origin_index = index
		c = 0
		
		t = self.buffer.get(f"{origin_index} linestart", f"{origin_index}")[::-1]
		for index, char in enumerate(t, 1):
			if (char not in "()[]{}"): continue
			if (char in "([{"):
				if (c <= 0):
					self.buffer.tag_add("pair", f"{origin_index} -{index}c")
					return
					break

				c -= 1

			elif (char in ")]}"):
				c += 1

		while (i < 800):
			t = self.buffer.get(f"{origin_index}-{i}l linestart", f"{origin_index}-{i}l lineend")[::-1]
			for index, char in enumerate(t, 1):
				if (char not in "()[]{}"): continue
				if (char in "([{"):
					if (c <= 0):
						self.buffer.tag_add("pair", f"{origin_index}-{i}l lineend -{index}c")
						return
						break
	
					c -= 1
	
				elif (char in ")]}"):
					c += 1

			i += 1


		# while (i <= 50000):
			# index = f"{origin_index}-{i}c"
			# pattern = self.buffer.get(index)
			# if (pattern not in "()[]{}"): i+=1; continue

			# if (pattern in "([{"):

				# self.bracket_pairs[self.buffer.index(index)] = self.brackets[-1]
				# self.bracket_pairs[self.brackets[-1]] = self.buffer.index(index)

				# self.brackets.pop()
				# if (not self.brackets):
					# self.buffer.tag_add("pair", index)
					# break

			# elif (pattern in ")]}"):
				# self.brackets.append(self.buffer.index(index))
			
			# i += 1

	def seek_bracket_after(self, index=None):
		i = 1
		if (not index): index = "insert"
		origin_index = index
		c = 0

		t = self.buffer.get(index, f"{index}lineend")
		for index, char in enumerate(t, 0):
			if (char not in "()[]{}"): continue
			if (char in ")]}"):
				c -= 1
				if (c <= 0):
					self.buffer.tag_add("pair", f"{origin_index}+{index}c")
					return

			elif (char in "([{"):
				c += 1


		while (i < 800):
			t = self.buffer.get(f"{origin_index}+{i}l linestart", f"{origin_index}+{i}l lineend")
			for index, char in enumerate(t, 0):
				if (char not in "()[]{}"): continue
				if (char in ")]}"):
					c -= 1
					if (c <= 0):
						self.buffer.tag_add("pair", f"{origin_index}+{i}l linestart +{index}c")
						return
	
				elif (char in "([{"):
					c += 1

			i += 1
		# i = 0
		# if (not index): index = "insert"
		# origin_index = index
		# while (i <= 50000):
			# index = f"{origin_index}+{i}c"
			# pattern = self.buffer.get(index)
			# if (pattern not in "()[]{}"): i+=1; continue
			
			# elif (pattern in "([{"):
				# self.brackets.append(self.buffer.index(index))

			# elif (pattern in ")]}"):

				# self.bracket_pairs[self.buffer.index(index)] = self.brackets[-1]
				# self.bracket_pairs[self.brackets[-1]] = self.buffer.index(index)

				# self.brackets.pop()
				# if (not self.brackets):
					# self.buffer.tag_add("pair", index)
					# break

			# i += 1

	def rm_highlight(self, last_separator, line_end_index):
		self.buffer.tag_remove("functions", last_separator, line_end_index)
		self.buffer.tag_remove("keywords", last_separator, line_end_index)
		self.buffer.tag_remove("logical_keywords", last_separator, line_end_index)
		self.buffer.tag_remove("numerical_keywords", last_separator, line_end_index)
		self.buffer.tag_remove("numbers", last_separator, line_end_index)
		self.buffer.tag_remove("special_chars", last_separator, line_end_index)
		self.buffer.tag_remove("comments", last_separator, line_end_index)
		self.buffer.tag_remove("operators", last_separator, line_end_index)
		self.buffer.tag_remove("quotes", last_separator, line_end_index)
		self.buffer.tag_remove("upcase", last_separator, line_end_index)
		for tag in self.buffer.tag_names():
			if (tag[0] == "#"): self.buffer.tag_remove(tag, last_separator, line_end_index)

	def highlight_keyword(self, last_separator, index) -> None:
		# print(self.last_pattern+self.pattern, " : ", self.color_code_regex.match(self.last_pattern+self.pattern))
		
		if (not self.in_comment and not self.in_quote):
			if (self.pattern in self.logical_keywords):
				self.buffer.tag_add("logical_keywords", last_separator, index)
	
			elif (self.pattern in self.numerical_keywords):
				self.buffer.tag_add("numbers", last_separator, index)

			elif (self.pattern in self.keywords): #self.pattern in self.keywords #self.py_keywords_regex.match(self.pattern)
				self.buffer.tag_add("keywords", last_separator, index)
	
			elif (self.pattern in self.objs):
				self.buffer.tag_add("functions", last_separator, index)
	
			elif (self.abc_upcase_regex.match(self.pattern) and len(self.pattern) > 1):
				self.buffer.tag_add("upcase", last_separator, index)
	
			elif (self.special_number_regex.match(self.pattern)):
				self.buffer.tag_add("numbers", last_separator, index)
		
		# elif (self.color_code_regex.match(self.last_pattern+self.pattern)):
			# self.buffer.tag_configure(self.last_pattern+self.pattern, background=self.last_pattern+self.pattern)
			# self.buffer.tag_add(self.last_pattern+self.pattern, last_separator, index)

		elif (self.in_comment and self.pattern in self.comment_keywords):
			print("comment_keyword found")
			self.buffer.tag_configure("comment_keyword", foreground="#FFFFFF")
			self.buffer.tag_add("comment_keyword", last_separator, index)



	def empty_highlight(self, line_no=None, line=None):
		pass

	def new_highlight(self, line_no=None, line=None):
		try: self.parent.unhighlight_chunk_no_threading()
		except Exceptions: pass
		count = tkinter.IntVar()
		for color, regex in self.new.items():
			if (type(regex) == list):
				for keyword in regex:
					# keyword = "\A"+keyword+"\M"
					self.buffer.mark_set("match_end", "1.0")
					while (1):
						try:
							index = self.buffer.search(keyword, "match_end", "end", regexp=True, count=count)
							index_end = f"{index}+{count.get()}c"
							# print("a: ", index, index_end)
							if (index and count.get != 0):
								self.buffer.mark_set("match_end", index_end)
								self.buffer.tag_add(color, index, self.buffer.index(index_end))
								# print("pass", self.buffer.get(index, index_end))
			
							else: break
			
						except tkinter.TclError as e:
							self.parent.notify(f"{e}")
							# print("shitfuck")
							break

		self.buffer.mark_unset("match_end")

	def universal_highlight(self, line_no, line=None):
		# motherfucking bullshit I need to make this work with regex so it's more extensible
		# the current highlighting sucks major ass
		linestart = f"{line_no}.0"
		lineend = f"{line_no}.0 lineend +1c"
		# self.buffer.mark_set("match_end", linestart)
		count = tkinter.IntVar()
		self.rm_highlight(linestart, lineend)
		delimeter = 0

		line = self.buffer.get(linestart, lineend)
		while (True):
			match = re.search(self.all_regex, line[delimeter:])
			if (not match): break
			match_start = int(match.span()[0])
			match_end = int(match.span()[1])
			
			match_start_int = match_start
			match_end_int = match_end

			match_start = f"{line_no}.{delimeter+match_start_int}"
			match_end = f"{line_no}.{delimeter+match_end_int}"

			delimeter = delimeter+match.pos+match_end_int
			# print(match, match_start, match_end, delimeter)

			match = match.group()
			if (self.keyword_regex.match(match)):
				self.buffer.tag_add("keywords", match_start, match_end)

			elif (self.logical_keyword_regex.match(match)):
				self.buffer.tag_add("logical_keywords", match_start, match_end)

			elif (self.numerical_keyword_regex.match(match)):
				self.buffer.tag_add("numbers", match_start, match_end)
			
			elif (self.number_regex.match(match)):
				self.buffer.tag_add("numbers", match_start, match_end)
			
			elif (self.operator_regex.match(match)):
				self.buffer.tag_add("operators", match_start, match_end)
			
			elif (self.special_char_regex.match(match)):
				self.buffer.tag_add("special_chars", match_start, match_end)

			elif (self.brackets_regex.match(match)):
				self.buffer.tag_add("special_chars", match_start, match_end)

			elif (self.comment_regex.match(match)):
				self.buffer.tag_add("comments", match_start, match_end)
				
			elif (self.quote_regex.match(match)):
				self.buffer.tag_add("quotes", match_start, match_end)

			elif (self.upcase_regex.match(match)):
				self.buffer.tag_add("upcase", match_start, match_end)

			elif (self.function_identifier_regex.match(match)):
				# print(match, match_start, match_end, delimeter)
				self.buffer.tag_add("functions", match_start, match_end)

		# weird tcl regex rules: https://tcl.tk/man/tcl8.5/TclCmd/re_syntax.htm#M50
		# \y in tcl syntax means mathcing only at the beggining or the end of the word
		# so it's \y(word)\y or \m(word)\M instead of \b(word)\b

		# while (True):
			# match_start = self.buffer.search(self.all_regex, "match_end", lineend, regexp=True, count=count, exact=True)
			# if (match_start == "" or count.get() == 0): break
			# match_end = f"{match_start}+{count.get()}c"
			# match = self.buffer.get(match_start, match_end)
			
			# if (self.keyword_regex.match(match)):
				# self.buffer.tag_add("keywords", match_start, match_end)
			
			# elif (self.number_regex.match(match)):
				# self.buffer.tag_add("numbers", match_start, match_end)
			
			# elif (self.operator_regex.match(match)):
				# self.buffer.tag_add("operators", match_start, match_end)
			
			# elif (self.special_char_regex.match(match)):
				# self.buffer.tag_add("special_chars", match_start, match_end)

			# elif (self.brackets_regex.match(match)):
				# self.buffer.tag_add("special_chars", match_start, match_end)

			# elif (self.comment_regex.match(match)):
				# self.buffer.tag_add("comments", match_start, match_end)
				
			# elif (self.quote_regex.match(match)):
				# self.buffer.tag_add("quotes", match_start, match_end)

			# elif (self.upcase_regex.match(match)):
				# self.buffer.tag_add("upcase", match_start, match_end)
			
			# self.buffer.mark_set("match_end", match_end)

		# self.buffer.mark_unset("match_end")
								
	def python_highlight(self, line_no=None, line: str=None):
		""" highlighting for python language """
		if (not line_no):
			line_no = self.buffer.cursor_index[0]

		if (not line):
			line = self.buffer.get(f"{line_no}.0", f"{line_no}.0 lineend +1c")

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.0 lineend"
		quote_start_index = f""
		self.last_pattern = ""
		self.pattern = ""
		self.in_quote = False
		self.in_comment = False
		
		self.rm_highlight(last_separator, line_end_index)

		for i, current_char in enumerate(line, 0):
			index = f"{line_no}.{i}"

			if (self.in_quote): self.buffer.tag_add("quotes", index)
			
			if (self.abc_regex.match(current_char)):
				self.pattern += current_char

			elif (self.commment_regex.match(current_char)): #comments
				if (not self.in_quote):
					self.buffer.tag_add("comments", index, line_end_index)
					self.in_comment = True
					
				self.set_pattern("#")

			elif (self.quote_regex.match(current_char) and not self.in_comment):
				self.buffer.tag_add("quotes", index)

				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.highlight_keyword(quote_start_index, index)

				self.pattern = ""
				if (self.in_quote): self.in_quote = False
				elif (not self.in_quote): self.in_quote = True; quote_start_index = last_separator

			elif (self.number_regex.match(current_char)): #numbers
				if (not self.in_comment and not self.in_quote and not self.pattern or self.number_regex.match(self.pattern)):
					self.buffer.tag_add("numbers", index)
					
				self.pattern += current_char
				self.highlight_keyword(last_separator, index)
			
			elif (self.operator_regex.match(current_char)):
				self.highlight_keyword(last_separator, index)
				if (not self.in_comment and not self.in_quote): self.buffer.tag_add("operators", index)
				
				self.set_pattern("")
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
			
			elif (self.brackets_regex.match(current_char)):
				self.highlight_keyword(last_separator, index)
				if (not self.in_comment and not self.in_quote): self.buffer.tag_add("special_chars", index)
				if (self.function_separator_regex.match(current_char)):
					self.buffer.tag_add("functions", last_separator, index)

				self.set_pattern("")
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				if (not self.in_comment and not self.in_quote): self.buffer.tag_add("special_chars", index)
				self.set_pattern("")
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
	
			elif (self.separator_regex.match(current_char)):
				self.highlight_keyword(last_separator, index)
			
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.set_pattern("")

	def c_highlight(self, line_no=None, line: str=None):
		""" highlighting for C-like languages """
		if (not line_no):
			line_no = self.buffer.cursor_index[0]

		if (not line):
			line = self.buffer.get(f"{line_no}.0", f"{line_no}.0 lineend +1c")

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.0 lineend"
		self.pattern = ""
		self.in_quote = False
		special_highlighting_mode = 0

		self.rm_highlight(last_separator, line_end_index)
		
		for i, current_char in enumerate(line, 0):

			try:
				if (self.commment_regex.match(current_char+line[i+1])): #comments
					index = f"{line_no}.{i}"
					self.buffer.tag_add("comments", index, line_end_index)
					break

			except Exception:
				pass

			if (i == 0 and self.c_preprocessor_regex.match(current_char)):
				if (special_highlighting_mode == 0): special_highlighting_mode = 1
			
			if (special_highlighting_mode != 0):
				index = f"{line_no}.{i}"
				if (re.match(r" ", current_char) and special_highlighting_mode == 1): special_highlighting_mode = 2
				if (special_highlighting_mode == 1):
					self.buffer.tag_add("logical_keywords", index)
				elif (special_highlighting_mode == 2):
					self.buffer.tag_add("upcase", index)
				continue

			if (self.quote_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.buffer.tag_add("quotes", index)
				if (self.in_quote):
					self.in_quote = False
				else:
					self.in_quote = True
				# self.in_quote = not self.in_quote

			elif (self.in_quote):
				index = f"{line_no}.{i}"
				self.buffer.tag_add("quotes", index)
				continue
			
			elif (self.abc_regex.match(current_char)):
				self.pattern += current_char
				# print(self.pattern)
				continue	

			elif (self.number_regex.match(current_char)): #numbers
				index = f"{line_no}.{i}"
				if (not self.pattern or self.number_regex.match(self.pattern)):
					self.buffer.tag_add("numbers", index)
				self.pattern += current_char
				self.highlight_keyword(last_separator, index)
				continue
			
			elif (self.operator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.buffer.tag_add("operators", index)
				self.highlight_keyword(last_separator, index)
				self.set_pattern("")
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.brackets_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.buffer.tag_add("special_chars", index)
				if (self.function_separator_regex.match(current_char)):
					self.buffer.tag_add("functions", last_separator, index)

				self.set_pattern("")
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				self.buffer.tag_add("special_chars", index)
				self.set_pattern("")
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue

			if (self.separator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
			
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				self.set_pattern("")


	def script_highlight(self, line_no: int = None, line: str=None):
		if (not line_no):
			line_no = self.buffer.cursor_index[0]

		if (not line):
			line = self.buffer.get(f"{line_no}.0", f"{line_no}.0 lineend +1c")

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.0 lineend"
		self.pattern = ""
		
		self.in_quote = False
		self.in_comment = False

		self.rm_highlight(last_separator, line_end_index)

		for i, current_char in enumerate(line, 0):
			if (self.commment_regex.match(current_char)): #comments
				index = f"{line_no}.{i}"
				self.buffer.tag_add("comments", index, line_end_index)
				break

			if (self.quote_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.buffer.tag_add("quotes", index)
				if (self.in_quote):
					self.in_quote = False
				else:
					self.in_quote = True
				# self.in_quote = not self.in_quote

			elif (self.in_quote):
				index = f"{line_no}.{i}"
				self.buffer.tag_add("quotes", index)
				continue

			elif (self.abc_regex.match(current_char)):
				self.pattern += current_char
				# print(self.pattern)
				continue
			
			elif (self.brackets_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.buffer.tag_add("special_chars", index)
				if (self.function_separator_regex.match(current_char)):
					self.buffer.tag_add("functions", last_separator, index)

				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				self.buffer.tag_add("special_chars", index)
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
		if (not line_no):
			line_no = self.buffer.cursor_index[0]

		if (not line):
			line = self.buffer.get(f"{line_no}.0", f"{line_no}.0 lineend +1c")

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.0 lineend"

		tag_start_index = f""
		tag_end_index = f""
		in_tag = False
		in_comment = False
		in_special_tag = False
		last_pattern = ""
		self.pattern = ""
		self.in_quote = False
		tag_argument_index = 0

		self.rm_highlight(last_separator, line_end_index)
		
		for i, current_char in enumerate(line, 0):
			self.pattern += current_char

			# if (self.html_abc_regex.match(current_char)):
			# self.pattern += current_char
			if (self.html_separator_regex.match(current_char)):
				last_pattern = self.pattern
				self.pattern = ""
				last_separator_index = i
				last_separator = f"{line_no}.{i}"
				if (in_tag):
					if (tag_argument_index < 1): tag_argument_index += 1

			if (self.quote_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.buffer.tag_add("special_chars", index)
				self.in_quote = not self.in_quote
				# self.in_quote = not self.in_quote

			if (self.in_quote):
				index = f"{line_no}.{i}"
				self.buffer.tag_add("special_chars", index)
				continue

			if (self.html_color_number_regex.match(self.pattern)):
				index = f"{line_no}.{i-len(self.pattern)}"
				index1 = f"{line_no}.{i+1}"
				try:  
					self.buffer.tag_configure(self.pattern, background=self.pattern)
				except Exception:
					pass
				self.buffer.tag_add("numbers", index, index1)
				self.buffer.tag_add(self.pattern, index)

			if (self.html_comment_start_regex.match(self.pattern)):
				index = f"{line_no}.{i+1}"
				self.buffer.tag_add("comments", tag_start_index, index)
				in_comment = True

			if (in_comment):
				index = f"{line_no}.{i}"
				self.buffer.tag_add("comments", index)

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
					self.buffer.tag_add("keywords", index)
				elif (tag_argument_index == 1):
					self.buffer.tag_add("quotes", index)



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

