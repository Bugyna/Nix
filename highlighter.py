import threading
import tkinter
import re

class highlighter(object):
	""" highlighter class storing all of the highlighting functions (and functions needed by the highlighting function) && keywords for each language """
	def __init__(self, parent, txt):
		self.lang = "NaN"
		self.supported_languagues = [
			"NaN", "py", "cc", "hh", "cpp", "hpp", "c", "h", "txt", "html", "htm", "java", "jsp", "class", "css", "go",
			"sh", "diary", "bat"
			]

		self.command_keywords = list(parent.commands.keys())

		self.Py_keywords = [
			'await', 'import', 'pass', 'break', 'in',
			'raise', 'class', 'is', 'return', 'continue', 'lambda', 'as', 'def', 'from',
			'nonlocal', 'assert', 'del', 'global', 'async', 'yield'
			]

		self.Py_numerical_keywords = ['False', 'True', 'None']
		self.Py_logical_keywords = [
			'and', 'or', 'not', 'if', 'elif', 'else', 'for', 'try', 'except', 'finally','while', 'with', 'self'] 
		self.Py_var_keywords = [
			"object", "int", "str", "float", "list"
		]
		# self.Py_keywords_regex = re.compile('|'.join(self.Py_keywords))#(r'\b(?:\|)\b'.join(self.Py_keywords))
		
		self.Java_keywords = [
			 'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'continue',
			 'default', 'do', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if',
			 'implements', 'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private',
			 'protected', 'public', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw',
			 'throws', 'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null'
			]

		self.C_keywords = [
			'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
		 	'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
		  	'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
   		]

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

		self.Go_keywords = [
			 'break', 'func', 'interface', 'select', 'defer', 'go', 'map', 'struct', 'chan',
			 'package', 'const', 'fallthrough', 'range', 'type', 'continue', 'import', 'return', 'var',
			 "uint", "uint8", "uint16", "uint32", "uint64", "uintptr", "rune", "byte", "int", "int8", "int16",
			 "int32", "int64", "float32", "float64", "complex64", "complex128", "bool", "string"
		]

		self.Go_numerical_keywords = [
			"true", "false"
		]

		self.Go_logical_keywords = [
			"if", "else", "switch", "case", 'default', "for", "while", "goto"
		]

		self.sh_keywords = ['expression', 'alias', 'bg', 'bind', 'builtin', 'caller', 'case', 'command', 'compgen',
		 'complete', 'continue', 'declare', 'dirs', 'disown', 'echo', 'enable', 'eval', 'exec', 'exit',
		 'export', 'false', 'fc', 'fg', 'for', 'getopts', 'hash', 'help', 'history', 'if', 'jobs', 'kill', 'let',
		 'local', 'logout', 'popd', 'printf', 'pushd', 'pwd', 'read', 'readonly', 'return', 'select', 'set', 'shift',
		 'shopt', 'source', 'suspend', 'test', 'time', 'times', 'trap', 'true', 'type', 'typeset', 'ulimit', 'umask',
		 'unalias', 'unset', 'until', 'variables', 'while']

		# BATCH IS FUCKING RETARDED
		self.bat_keywords = ['adprep', 'append', 'arp', 'assoc', 'at', 'atmadm', 'attrib', 'auditpol', 'autochk',
		 'autoconv', 'autofmt', 'bcdboot', 'bcdedit', 'bdehdcfg', 'bitsadmin', 'bootcfg', 'break', 'break', 'cacls',
		 'cd', 'certreq', 'certutil', 'chcp', 'change', 'choice', 'cipher', 'chdir', 'chkdsk', 'chkntfs', 'chglogon',
		 'chgport', 'chgusr', 'clip', 'cls', 'clscluadmin', 'cluster', 'cmd', 'cmdkey', 'cmstp', 'color',
		 'comp', 'compact', 'convert', 'copy', 'cprofile', 'cscript', 'csvde', 'date', 'dcdiag', 'dcgpofix', 'dcpromo',
		 'defra', 'del', 'dfscmd', 'dfsdiag', 'dfsrmig', 'diantz', 'dir', 'dirquota', 'diskcomp', 'diskcopy', 'diskpart',
		 'diskperf', 'diskraid', 'diskshadow', 'dispdiag', 'doin', 'dnscmd', 'doskey', 'driverquery', 'dsacls', 'dsadd',
		 'dsamain', 'dsdbutil', 'dsget', 'dsmgmt', 'dsmod', 'dsmove', 'dsquery', 'dsrm', 'echo', 'edit', 'endlocal', 'erase',
		 'esentutl', 'eventcreate', 'eventquery', 'eventtriggers', 'evntcmd', 'expand', 'extract', 'fc', 'filescrn', 'find',
		 'findstr', 'finger', 'flattemp', 'fonde', 'forfiles', 'format', 'freedisk', 'fs', 'fsutil', 'ftp', 'ftype', 'fveupdate',
		 'getmac', 'gettype', 'gpfixup', 'gpresult', 'gpupdate', 'graftabl', 'hashgen', 'hep', 'help', 'helpctr', 'hostname',
		 'icacls', 'iisreset', 'inuse', 'ipconfig', 'ipxroute', 'irftp', 'ismserv', 'jetpack', 'keyb', 'klist', 'ksetup',
		 'ktmutil', 'ktpass', 'label', 'ldifd', 'ldp', 'lodctr', 'logman', 'logoff', 'lpq', 'lpr', 'macfile', 'makecab',
		 'manage-bde', 'mapadmin', 'md', 'mkdir', 'mklink', 'mmc', 'mode', 'more', 'mount', 'mountvol', 'move', 'mqbup', 'mqsvc',
		 'mqtgsvc', 'msdt', 'msg', 'msiexec', 'msinfo32', 'mstsc', 'nbtstat', 'net computer', 'net group', 'net localgroup',
		 'net print', 'net session', 'net share', 'net start', 'net stop', 'net use', 'net user', 'net view', 'net', 'netcfg',
		 'netdiag', 'netdom', 'netsh', 'netstat', 'nfsadmin', 'nfsshare', 'nfsstat', 'nlb', 'nlbmgr', 'nltest', 'nslookup',
		 'ntackup', 'ntcmdprompt', 'ntdsutil', 'ntfrsutl', 'openfiles', 'pagefileconfig', 'path', 'pathping', 'pause',
		 'pbadmin', 'pentnt', 'perfmon', 'ping', 'pnpunatten', 'pnputil', 'popd', 'powercfg', 'powershell', 'powershell_ise',
		 'print', 'prncnfg', 'prndrvr', 'prnjobs', 'prnmngr', 'prnport', 'prnqctl', 'prompt', 'pubprn', 'pushd',
		 'pushprinterconnections', 'pwlauncher', 'qappsrv', 'qprocess', 'nquery', 'quser', 'qwinsta', 'rasdial', 'rcp',
		 'rd', 'rdpsign', 'regentc', 'recover', 'redircmp', 'redirusr', 'reg', 'regini', 'regsvr32', 'relog', 'ren',
		 'rename', 'rendom', 'repadmin', 'repair-bde', 'replace', 'reset', 'restore', 'rxec', 'risetup', 'rmdir',
		 'robocopy', 'route', 'rpcinfo', 'rpcping', 'rsh', 'runas', 'rundll32', 'rwinsta', 'scp', 'sc', 'setlocal',
		 'session', 'schtasks', 'scwcmd', 'secedit', 'serverceipoptin', 'servrmanagercmd', 'serverweroptin', 'set', 'setspn', 'setx',
		 'sfc', 'shadow', 'shift', 'showmount', 'shutdown', 'sort', 'ssh', 'start', 'storrept', 'subst', 'sxstrace', 'ysocmgr',
		 'systeminfo', 'takeown', 'tapicfg', 'taskkill', 'tasklist', 'tcmsetup', 'telnet', 'tftp', 'time', 'timeout',
		 'title', 'tlntadmn', 'tpmvscmgr', 'tpmvscmgr', 'tacerpt', 'tracert', 'tree', 'tscon', 'tsdiscon', 'tsecimp',
		 'tskill', 'tsprof', 'type', 'typeperf', 'tzutil', 'uddiconfig', 'umount', 'unlodctr', 'ver', 'verify', 'verifier',
		 'verif', 'vol', 'vssadmin', 'w32tm', 'waitfor', 'wbadmin', 'wdsutil', 'wecutil', 'wevtutil', 'where', 'whoami', 'winnt',
		 'winnt32', 'winpop', 'winrm', 'winrs', 'winsat', 'wlbs', 'mic', 'wscript', 'xcopy'
		 ]

		# self.html_keywords = ['<!-->', '<!DOCTYPE>', '<a>', '<abbr>', '<acronym>', '<address>', '<applet>', '<area>',
		#  '<article>', '<aside>', '<audio>', '<b>', '<base>', '<basefont>', '<bdi>', '<bdo>', '<big>', '<blockquote>',
		#  '<body>', '<br>', '<button>', '<canvas>', '<caption>', '<center>', '<cite>', '<code>', '<col>',
		#  '<colgroup>', '<data>', '<datalist>', '<dd>', '<del>', '<details>', '<dfn>', '<dialog>', '<dir>', '<div>',
		#  '<dl>', '<dt>', '<em>', '<embed>', '<fieldset>', '<figcaption>', '<figure>', '<font>', '<footer>', '<form>',
		#  '<frame>', '<frameset>', '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<head>', '<header>', '<hr>', '<html>',
		#  '<i>', '<iframe>', '<img>', '<input>', '<ins>', '<kbd>', '<label>', '<legend>', '<li>', '<link>', '<main>',
		#  '<map>', '<mark>', '<meta>', '<meter>', '<nav>', '<noframes>', '<noscript>', '<object>', '<ol>', '<optgroup>',
		#  '<option>', '<output>', '<p>', '<param>', '<picture>', '<pre>', '<progress>', '<q>', '<rp>', '<rt>', '<ruby>',
		#  '<s>', '<samp>', '<script>', '<section>', '<select>', '<small>', '<source>', '<span>', '<strike>', '<strong>',
		#  '<style>', '<sub>', '<summary>', '<sup>', '<svg>', '<table>', '<tbody>', '<td>', '<template>', '<textarea>',
		#  '<tfoot>', '<th>', '<thead>', '<time>', '<title>', '<tr>', '<track>', '<tt>', '<u>', '<ul>', '<var>', '<video>',
		#  '<wbr>', '</!-->', '</!DOCTYPE>', '</a>', '</abbr>', '</acronym>', '</address>', '</applet>', '</area>',
		#  '</article>', '</aside>', '</audio>', '</b>', '</base>', '</basefont>', '</bdi>', '</bdo>', '</big>',
		#  '</blockquote>', '</body>', '</br>', '</button>', '</canvas>', '</caption>', '</center>', '</cite>',
		#  '</code>', '</col>', '</colgroup>', '</data>', '</datalist>', '</dd>', '</del>', '</details>', '</dfn>',
		#  '</dialog>', '</dir>', '</div>', '</dl>', '</dt>', '</em>', '</embed>', '</fieldset>', '</figcaption>', '</figure>',
		#  '</font>', '</footer>', '</form>', '</frame>', '</frameset>', '</h1>', '</h2>', '</h3>', '</h4>',
		#  '</h5>', '</h6>', '</head>', '</header>', '</hr>', '</html>', '</i>', '</iframe>', '</img>', '</input>', '</ins>',
		#  '</kbd>', '</label>', '</legend>', '</li>', '</link>', '</main>', '</map>', '</mark>', '</meta>', '</meter>',
		#  '</nav>', '</noframes>', '</noscript>', '</object>', '</ol>', '</optgroup>', '</option>', '</output>', '</p>',
		#  '</param>', '</picture>', '</pre>', '</progress>', '</q>', '</rp>', '</rt>', '</ruby>', '</s>', '</samp>', '</script>',
		#  '</section>', '</select>', '</small>', '</source>', '</span>', '</strike>', '</strong>', '</style>', '</sub>',
		#  '</summary>', '</sup>', '</svg>', '</table>', '</tbody>', '</td>', '</template>', '</textarea>', '</tfoot>',
		#  '</th>', '</thead>', '</time>', '</title>', '</tr>', '</track>', '</tt>', '</u>', '</ul>', '</var>', '</video>',
		#  '</wbr>']


		self.txt = txt
		self.parent = parent
		self.command_entry = parent.command_entry
		self.theme = parent.theme

		self.countingQuomarks = False
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

		# compiled regexes used by the highlighting functions
		self.quote_regex = re.compile(r"[\"\']")
		self.abc_regex = re.compile(r"[a-zA-Z_]")
		self.abc_upcase_regex = re.compile(r"^[A-Z_]+$") #|^[A-Z]+_[A-Za-z0-9]+")
		self.separator_regex = re.compile(r"[\s\.\,\:\;]")
		self.num_regex = re.compile(r"[0-9]")
		self.special_num_regex = re.compile(r"^0b+[0-1]+$|^0x+[0-9a-fA-F]+$")
		self.special_char_regex = re.compile(r"[\!\&\^\|\@\$]")
		self.brackets_regex = re.compile(r"[\{\}\[\]\(\)]")
		self.left_brackets_regex = re.compile(r"[\(\[\{]")
		self.right_brackets_regex = re.compile(r"[\)\]\}]")
		self.function_separator_regex = re.compile(r"[\(]")
		self.operator_regex = re.compile(r"[\%\+\-\*\/\=\<\>]")
		self.string_special_char_regex = re.compile(r"[\\\{\}]")
		self.whitespace_regex = re.compile(r"[\t]")
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
		if (self.lang == "c" or self.lang == "h"):
			self.keywords = self.C_keywords
			self.numerical_keywords = []
			self.logical_keywords = []
			self.highlight = self.C_highlight
			self.comment_sign = "//"
			self.highlight = self.C_highlight

		elif (self.lang == "cpp" or self.lang == "cc" or self.lang == "hpp" or self.lang == "hh"):
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

		elif (self.lang == "html" or self.lang == "htm" or self.lang == "css"):
			self.keywords = self.html_keywords
			self.highlight = self.html_highlight
			self.comment_sign = "<!-- -->"

		elif (self.lang == "java" or self.lang == "jsp" or self.lang == "class"):
			self.keywords = self.Java_keywords
			self.numerical_keywords = []
			self.logical_keywords = []
			self.highlight = self.C_highlight
			self.comment_sign = "//"

		elif (self.lang == "go"):
			self.keywords = self.Go_keywords
			self.numerical_keywords = self.Go_numerical_keywords
			self.logical_keywords = self.Go_logical_keywords
			self.highlight = self.C_highlight
			self.comment_sign = "//"

		elif (self.lang == "sh"):
			self.keywords = self.sh_keywords
			self.numerical_keywords = []
			self.logical_keywords = []
			self.highlight = self.script_highlight
			self.comment_sign = "#"

		elif (self.lang == "bat"):
			self.keywords = self.sh_keywords
			self.numerical_keywords = []
			self.logical_keywords = []
			self.highlight = self.script_highlight
			self.comment_sign = "::"

		elif (self.lang == "diary"):
			self.keywords = ["Hello"]
			self.numerical_keywords = []
			self.logical_keywords = []
			self.highlight = self.diary_highlight
			self.comment_sign = "~$"

		elif (self.lang == "NaN" or self.lang == "txt"):
			self.comment_sign = "\t"
			self.highlight = self.no_highlight
		else:
			self.comment_sign = "\t"
			self.highlight = self.no_highlight
		
		self.commment_regex = re.compile(rf"{self.comment_sign}")

	def get_line_lenght(self, line_no: int):
		""" gets the length of current line """
		return f"{line_no}.0 lineend+1c"

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
				

	def bracket_pair_highlight(self, line_no: int, line: str) -> None: 
		self.txt.tag_remove("pair_bg", "1.0", "end")

		index = self.txt.index(tkinter.INSERT)

		if (self.brackets_regex.match(self.txt.get(index))):
			try:
				self.txt.tag_add("pair_bg", self.bracket_pairs[index])
			except Exception:
				pass


	def bracket_pair_make(self, char: str = None):
		self.brackets = [] #clearing useless things
		self.human_error = []
		self.bracket_pairs = {}

		if (self.left_brackets_regex.match(char)):
			direction = 1

		elif (self.right_brackets_regex.match(char)):
			direction = -1
		
		else: return
		
		i = 0
		index = "insert"

		# I am stoopid and this is a botch and a workaround
		while (True):
			if (i >= 5000): break #self.txt.tag_add("error_bg", self.brackets[-1]); 
			index = f"insert+{i}c" if direction == 1 else f"insert-{i}c"
			pattern = self.txt.get(index)
			if (not self.brackets_regex.match(pattern)): i+=1; continue
			
			if (direction == 1):
				if (self.left_brackets_regex.match(pattern)):
					self.brackets.append(self.txt.index(index))

				elif (self.right_brackets_regex.match(pattern)):

					self.bracket_pairs[self.txt.index(index)] = self.brackets[-1]
					self.bracket_pairs[self.brackets[-1]] = self.txt.index(index)

					self.brackets.pop()
					if (not self.brackets):
						break

			else:
				if (self.left_brackets_regex.match(pattern)):

					self.bracket_pairs[self.txt.index(index)] = self.brackets[-1]
					self.bracket_pairs[self.brackets[-1]] = self.txt.index(index)

					self.brackets.pop()
					if (not self.brackets):
						break

				elif (self.right_brackets_regex.match(pattern)):
					self.brackets.append(self.txt.index(index))
			
			i += 1

	def rm_highlight(self, last_separator, line_end_index):
		self.txt.tag_remove("functions", last_separator, line_end_index)
		self.txt.tag_remove("keywords", last_separator, line_end_index)
		self.txt.tag_remove("logical_keywords", last_separator, line_end_index)
		self.txt.tag_remove("numerical_keywords", last_separator, line_end_index)
		self.txt.tag_remove("numbers", last_separator, line_end_index)
		self.txt.tag_remove("special_chars", last_separator, line_end_index)
		self.txt.tag_remove("comments", last_separator, line_end_index)
		self.txt.tag_remove("operators", last_separator, line_end_index)
		self.txt.tag_remove("quotes", last_separator, line_end_index)
		self.txt.tag_remove("upcase", last_separator, line_end_index)

	def highlight_keyword(self, last_separator, index):
		if (self.pattern in self.keywords): #self.pattern in self.keywords #self.Py_keywords_regex.match(self.pattern)
			self.txt.tag_add("keywords", last_separator, index)
		
		elif (self.pattern in self.logical_keywords):
			self.txt.tag_add("logical_keywords", last_separator, index)

		elif (self.pattern in self.numerical_keywords):
			self.txt.tag_add("numbers", last_separator, index)

		elif (self.abc_upcase_regex.match(self.pattern) and len(self.pattern) > 1):
			self.txt.tag_add("upcase", last_separator, index)

		elif (self.special_num_regex.match(self.pattern)):
			self.txt.tag_add("numbers", last_separator, index)

					
	def python_highlight(self, line_no: int ,line: str=None):
		""" highlighting for python language """
		if (not line):
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))
			# print(line)

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)}"
		self.pattern = ""
		self.countingQuomarks = False
		
		self.rm_highlight(last_separator, line_end_index)


		for i, current_char in enumerate(line, 0):
			if (self.quote_regex.match(current_char)):
				self.txt.tag_add("quotes", f"{line_no}.{i}")
				self.countingQuomarks = not self.countingQuomarks

			elif (self.countingQuomarks):
				self.txt.tag_add("quotes", f"{line_no}.{i}")
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
				if (not self.pattern or self.num_regex.match(self.pattern)):
					self.txt.tag_add("numbers", index)
				self.pattern += current_char
				self.highlight_keyword(last_separator, index)
				continue
			
			elif (self.operator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.txt.tag_add("operators", index)
				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.brackets_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.txt.tag_add("special_chars", index)
				if (self.function_separator_regex.match(current_char)):
					self.txt.tag_add("functions", last_separator, index)

				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				self.txt.tag_add("special_chars", index)
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
		""" highlighting for C-like languages """
		if (not line):
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)+1}"
		self.pattern = ""
		self.countingQuomarks = False
		special_highlighting_mode = 0

		self.rm_highlight(last_separator, line_end_index)
		
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
					self.txt.tag_add("special_chars", index)
				elif (special_highlighting_mode == 2):
					self.txt.tag_add("upcase", index)
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
				index = f"{line_no}.{i}"
				if (not self.pattern or self.num_regex.match(self.pattern)):
					self.txt.tag_add("numbers", index)
				self.pattern += current_char
				self.highlight_keyword(last_separator, index)
				continue
			
			elif (self.operator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.txt.tag_add("operators", index)
				self.highlight_keyword(last_separator, index)
				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.brackets_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.txt.tag_add("special_chars", index)
				if (self.function_separator_regex.match(current_char)):
					self.txt.tag_add("functions", last_separator, index)

				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				self.txt.tag_add("special_chars", index)
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


	def script_highlight(self, line_no: int=None, line: str=None):
		if (not line):
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)+1}"
		self.pattern = ""
		self.countingQuomarks = False

		self.rm_highlight(last_separator, line_end_index)

		for i, current_char in enumerate(line, 0):
			if (self.commment_regex.match(current_char)): #comments
				index = f"{line_no}.{i}"
				self.txt.tag_add("comments", index, line_end_index)
				break

			elif (self.abc_regex.match(current_char)):
				self.pattern += current_char
				# print(self.pattern)
				continue
			
			elif (self.brackets_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.txt.tag_add("special_chars", index)
				if (self.function_separator_regex.match(current_char)):
					self.txt.tag_add("functions", last_separator, index)

				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				self.txt.tag_add("special_chars", index)
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
		if (not line):
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))

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
				self.txt.tag_add("special_chars", index)
				self.countingQuomarks = not self.countingQuomarks
				# self.countingQuomarks = not self.countingQuomarks

			if (self.countingQuomarks):
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


	def diary_highlight(self, line_no: int, line:str = None):
		if (not line):
			line = self.txt.get(float(line_no), self.get_line_lenght(line_no))
			# print(line)

		last_separator_index = 0
		last_separator = f"{line_no}.{last_separator_index}"
		line_end_index = f"{line_no}.{len(line)+1}"
		self.pattern = ""
		self.countingQuomarks = False
		
		self.rm_highlight(last_separator, line_end_index)

		for i, current_char in enumerate(line, 0):
			if (self.abc_regex.match(current_char)):
				self.pattern += current_char
				continue

			elif (self.commment_regex.match(current_char)): #comments
				index = f"{line_no}.{i}"
				self.txt.tag_add("comments", index, line_end_index)
				break
			
			elif (self.num_regex.match(current_char)): #numbers
				index = f"{line_no}.{i}"
				if (not self.pattern or self.num_regex.match(self.pattern)):
					self.txt.tag_add("numbers", index)
				self.pattern += current_char
				self.highlight_keyword(last_separator, index)
				continue
			
			elif (self.operator_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.txt.tag_add("operators", index)
				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.brackets_regex.match(current_char)):
				index = f"{line_no}.{i}"
				self.highlight_keyword(last_separator, index)
				self.txt.tag_add("special_chars", index)
				if (self.function_separator_regex.match(current_char)):
					self.txt.tag_add("functions", last_separator, index)

				self.pattern = ""
				last_separator_index = i+1
				last_separator = f"{line_no}.{last_separator_index}"
				continue
			
			elif (self.special_char_regex.match(current_char)): #special chars[\[\]\{\}\-\+\*\/\%\^\&\(\)\|\=]
				index = f"{line_no}.{i}"
				self.txt.tag_add("special_chars", index)
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
		
		












































