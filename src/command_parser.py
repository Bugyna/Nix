# A START OF SOMETHING TRULY HORRIBLE
import re
import os
import sys
import threading
import requests
try: from bs4 import BeautifulSoup # usually don't get imported when running as root
except Exception: pass

from gr import *
from widgets import *
from handlers import *
from highlighter import *

def wrap(func):
	def wrapped_func(*args, **kwargs):
		ret = func(*args, **kwargs)
		return ret

	return wrapped_func

# I have no idea why I did it this way
# Like sure it's kinda extendable and you can kinda add new functions easily, but it's like really fucking annoying
# I'll remake it someday, probably, maybe, hopefully, not really
# I have like 4 more things to remake and I am lazy

def ld(s, t, n):
	if (n >= 25): return 25
	n += 1
	if not s: return len(t)
	if not t: return len(s)
	if s[0] == t[0]: return ld(s[1:], t[1:], n)
	l1 = ld(s, t[1:], n)
	l2 = ld(s[1:], t, n)
	l3 = ld(s[1:], t[1:], n)
	if (n >= 25): return 25
	return 1 + min(l1, l2, l3)

class PARSER:
	def __init__(self, parent):
		""" OOP GONE WRONG NOT CLICKBAIT I HATE THIS """
		# this really is completely utterly shit and it's really badly extensible if you want to write an extra library or something
		# I have no idea how to make this extensible
		self.parent = parent

		# if you want to add more functions to react with widgets of the main window you'll have to write a "wrapper" for them in here
		# becuase if you do something like 
		# self.commands = {
			# "replace_tab": self.parent.buffer.replace_tabs,
		# }
		# then it will only work with the text widget that was referenced at the time of declaration of this class

		self.commands = { 
			'help' : [self.help, 'help'],
			'suggest' : [self.suggest_set, 'toggles suggesting'],
			'([0-9]+)|(^l[0-9]+$)|(^l[0-9]+.[0-9]+$)' : [self.l, 'moves to line | usage: [line number] or [line number].[column number]'],
			'lget|get_line_count' : [self.l_get, 'gets line count'],
			'word_count(_get)*' : [self.word_count_get, 'gets word count'],
			'fget|fsize|file_size' : [self.file_size_get, 'gets file size'],
			'lyrics' : [self.lyrics_get, 'scrapes lyrics | usage: lyrics [artist name], [song name]'],
			'split' : [self.split, 'splits buffers | usage: split [vertical|horizontal]'],
			'unsplit' : [self.unsplit, 'unsplits buffers'],
			'q|quit' : [self.win_quit, 'exits editor'],
			'alpha|transparency' : [self.alpha_set, 'set window alpha | usage: alpha [number 0-100]'],
			'convert' : [self.convert, 'converts number into other numeral systems | usage: convert 0x[number] for hexadecimal or 0b[number] for binary or [number] for decimal'],
			'resize' : [self.win_resize, 'resizes window | usage: resize [width px] [height px]'],
			'buffers' : [self.buffer_list, 'lists all opened buffers'],
			'(buffer_)*close' : [self.buffer_close, 'closes current buffer'],
			'save' : [self.file_save, 'saves current file'],
			'save(_)*as' : [self.file_save_as, 'save current file as | usage: saveas [filename]'],
			'open|load' : [self.file_load, 'loads file | usage: open [filename]'],
			'reopen|reload' : [self.file_reload, 'reloads current file'],
			'rm|del' : [self.file_delete, 'delete file | usage: rm [filename]'],
			'sys' : [self.system_execute, 'run system commands (as if in a normal terminal) | usage: sys [command]'],
			'exec' : [self.python_execute, 'executes python code | usage: exec [python code]'],
			'buffer_exec|bexec' : [self.buffer_execute, 'executes python code in current buffer'],
			'ls|dir' : [self.ls, 'list currrent directory'],
			'cd' : [self.cd, 'changes directory | usage: cd [directory name]'],
			'mkdir|new_dir(ectory)' : [self.new_directory, 'creates directory | usage: mkdir [directory name]'],
			'rmdir|rm_dir(ectory)' : [self.delete_directory, 'deletes directory | usage: rmdir [directory name]'],
			'theme' : [self.theme, 'changes theme interactively or to the specified one | usage: theme (interactive) | theme [theme name]'],
			'tab_size|set_tab|set_tab_size' : [self.tab_size_set, 'sets tab size | usage: tab_size: [number]'],
			'replace_space(s*)' : [self.replace_spaces, 'replaces all indentaion(spaces) with tabs'],
			'replace_tab(s*)' : [self.replace_tabs, 'replaces all tabs with spaces'],
			'init' : [self.initialize_file, 'initializes file with standard code for current filetype by extension'],
			'lex' : [self.lex, 'use lexer'],
			'lex_print' : [self.lex_print, 'print lexer results'],
			'lexer' : [self.lexer_switch, 'change lexer | usage lexer [lexer type]'],
			'tag(_add)*' : [self.add_tag, 'adds a tag to selected text | usage: tag_add [tag name]'],
			'tag_remove' : [self.remove_tag, 'removes a tag in selected text | usage: tag_remove [tag name]'],
			'lf' : [self.lf, 'converts all line feed to LF'],
			'crlf' : [self.crlf, 'converts all line feed to CRLF'],
			'toggle_filebar' : [self.toggle_buffer_tab_show, 'toggles a UI bar with opened file'],
			'make' : [self.make, 'runs a make in your current directory'],
			'conf|conf_file|config|config_file' : [self.open_conf_file, 'open file with config'],
			'keybindings|keybinds' : [self.open_keybindings_file, 'open file with keybindings'],
			'reload_conf(ig)*(_file)*' : [self.reload_conf, 'reloads the conf file'],
			'reload_keybinds' : [self.reload_keybinds, 'reloads keybindings'],
			'reload_modules' : [self.reload_modules, 'reloads external modules'],
			'load_modules_from' : [self.load_modules_from, 'loads external modules from directory | usage: load_modules_from [directory]'],
			'font' : [self.change_font, 'change font | usage: font | font [font name]'],
			'(set_)*timer' : [self.set_timer, 'sets timer | usage: timer [time in seconds]'],
			'(write_)*hack' : [self.write_hack, 'inserts a comment saying HACK | usage: hack | hack [explanation]'],
			'(write_)*todo' : [self.write_todo, 'inserts a comment saying TODO | usage: todo | todo [explanation]'],
			'(write_)*note' : [self.write_note, 'inserts a comment saying note | usage: note | note [explanation]'],
			'todo_set' : [self.todo_set, 'todo'],
			'(list_)*(sub)*proc' : [self.list_subprocess, 'subproc'],
			'create_temp(_buffer)*' : [self.create_temp_buffer, 'creates temporary buffer | usage: create_temp | create_temp [buffer name]'],
			'(add_|create_)*mark' : [self.create_mark, 'creates a mark you can jump to with the \'jump\' command'],
			'list_mark': [self.list_mark, 'lists all marks in current buffer'],
			'jump(_to)*' : [self.jump_to, 'jump to a created mark or an index'],
		}

		# for i in range(len(self.commands.values())): # autogenerate power go brr
			# print(f"'{list(self.commands.keys())[i]}' : [self.{list(self.commands.values())[i].__name__}, '{list(self.docs.values())[i]}'],")


	def has_argument(func, arg=None):
		def new_func(self, arg=None):
			if (not arg[1:]): self.parent.error(f"{self.get_docs(arg[0:])}"); return
			func(self, arg)

		return new_func

	def parse_argument(self, arg=None):
		# O(n) somethign because fuck speed all I want is trash features
		for key in self.commands.keys():
			if (re.match(f"\\b({key})\\b", arg[0])):
				arg_f = arg
				
				for i in range(len(arg)):
					if (re.search(r"\*", arg[i])):
						a = arg.pop(i)
						for file in self.parent.file_handler.directory_list_get(expr=a)[::-1]:
							arg.insert(i, file)

				self.command_execute = self.commands[key]
				
				if (type(self.command_execute) == list or type(self.command_execute) == tuple):
					self.command_execute = self.commands[key][0]
					
				try:
					self.command_execute(arg)
					
				except Exception as e: self.parent.error(f"{e}\n{self.get_docs(key)}")
				break
		else:
			self.command_execute = self.command_not_found
			self.command_execute(arg)

	def get_docs(self, arg=None):
		if (type(arg) == str): arg = [arg]
		
		try: return arg[0] + " : " + self.commands[arg[0]][1]
		except Exception: return arg[0] + " : "

	def help(self, arg=None):
		if (not arg[1:]):
			x = ""
			for c in self.commands.keys():
				x += "\n"+self.get_docs(c)
			self.parent.command_out_set(x)
		else:
			self.parent.notify(self.get_docs(arg[1:]))

	def suggest_set(self, arg=None):
		self.parent.conf["suggest"] = not self.parent.conf["suggest"]

	def l(self, arg=None):
		arg = "".join(arg)
		if (arg[0] == "l"): arg = arg[1:]
		if (len(arg.split(".")) < 2): arg = float(arg)
		index = self.parent.buffer.index(arg)
		self.parent.buffer.mark_set("insert", index)
		self.parent.buffer.see(index)
		self.parent.notify(f"moved to: {index}")

	def l_get(self, arg=None):
		self.parent.notify(f"{self.parent.buffer.get_line_count()}")

	def word_count_get(self, arg=None):
		self.parent.notify(f"{self.parent.buffer.get_word_count()}")

	def file_size_get(self, arg=None) -> None:
		self.parent.notify(f"buffer size: {len(self.parent.buffer.get('1.0', 'end'))+1}B >>>> file size: {os.path.getsize(self.parent.buffer.full_name)}B")

	def lyrics_get(self, arg=None):
		if (not arg[1:]): self.parent.notify("Usage: lyrics [artist name], [song name]"); return
		self.parent.notify("scraping.../")
		def lyr():
			command1 = ""
			for word in arg[1:]:
				command1 += "-"+word
			command1 = command1.split(",")
			url = f"http://www.songlyrics.com/{command1[0]}/{command1[1]}-lyrics/"
			html = requests.get(url).content #gets the html of the url
			lyrics = BeautifulSoup(html, features="html.parser").find(id="songLyricsDiv").text
			self.parent.command_out_set(lyrics)
			
		threading.Thread(target=lyr).start()

	def temp(self, arg=None):
		self.parent.get_temperature()
		self.parent.buffer.focus_set()

	def time_set(self, arg=None):
		self.parent.notify(self.parent.get_time(), tags=[["1.0", "end"]])

	def blink(self, arg=None): #wonky as fuck
		if (arg[1] == "on"):
			for buffer in self.parent.file_handler.buffer_list:
				buffer[0]["insertontime"] = 500
				buffer[0]["insertofftime"] = 500

		elif (arg[1] == "off"):
			for buffer in self.parent.file_handler.buffer_list:
				buffer[0]["insertontime"] = 1
				buffer[0]["insertofftime"] = 0

		else:
			self.parent.notify(f"ERROR: Invalid argument {arg[1:]}", tags=[["1.0", "1.7"]])
			
		self.parent.buffer.focus_set()

	def split(self, arg=None): #also wonky as fuck
		if (arg[1] == "n"):
			self.unsplit(arg)

		elif (arg[1] == "vertical" or arg[1] == "v"):
			self.parent.split_mode = "vertical"
			self.parent.notify("split vertically")

		elif (arg[1] == "horizontal" or arg[1] == "h"):
			self.parent.split_mode = "horizontal"
			self.parent.notify("split horizontally")

		try:
			self.parent.buffer_render_index += 1
			self.parent.file_handler.load_buffer(buffer_index=self.parent.buffer.buffer_index+1)
		except IndexError: pass

		self.parent.reposition_widgets()

	def unsplit(self, arg=None):
		p = self.parent.buffer
		self.parent.buffer_unplace()
		self.parent.buffer_render_list = [p]
		self.parent.split_mode = "nosplit"
		self.parent.buffer_render_index = 0
		self.parent.file_handler.load_buffer(buffer_name=self.parent.buffer.full_name)
		self.parent.reposition_widgets()

	def win_quit(self, arg=None):
		self.parent.run = False
		self.parent.quit()
		# self.destroy()

	def sharpness_set(self, arg=None):
		self.parent.sharpness = arg[1]
		self.parent.tk.call("tk", "scaling", arg[1])
		self.parent.notify(f"sharpness: {arg[1]}")

	def alpha_set(self, arg=None):
		if (arg[1] == "default"): arg[1] = 90
		self.parent.alpha_set(int(arg[1]))
		self.parent.notify(f"alpha set to {arg[1]}")

	def convert(self, arg=None):
		try:
			if (arg[1][:2] == "0x"):
				decimal = int(arg[1], 16)
			elif (arg[1][:2] == "0b"):
				decimal = int(arg[1], 2)
			else:
				decimal = int(arg[1], 10)

			self.parent.notify(f"DECIMAL: {decimal}, HEXADECIMAL: {hex(decimal)}, BINARY: {bin(decimal)}")
		except ValueError:
			self.parent.error(f"{self.get_docs[arg[0]]}")

	def video_capture(self, arg=None):
		if (arg[1] == "start"):
			self.parent.process = self.parent.video_handler.video_record_start(self.parent)
		
		elif (arg[1] == "stop"):
			self.parent.video_handler.video_record_stop(self.parent.process)
			self.parent.notify("screen capture terminated")
	
	def screenshot(self, arg=None):
		self.parent.video_handler.screenshot(self)
	
	def win_resize(self, arg=None):
		self.parent.update_win()
		self.parent.geometry(f"{int(arg[1])}x{int(arg[2])}")
		
	def buffer_list(self, arg=None):
		if (not arg[1:]):
			self.parent.file_handler.list_buffer()
		else:
			self.parent.file_handler.load_buffer(arg[1:])

	def buffer_close(self, arg=None):
		self.parent.file_handler.close_buffer()

	def file_save(self, arg=None):
		self.parent.file_handler.save_file()
	
	def file_save_as(self, arg=None):
		self.parent.file_handler.save_file_as(new_filename=arg[1])

	def file_load(self, arg=None):
		self.parent.file_handler.load_file(filename="".join(arg[1:]))

	def file_reload(self, arg=None):
		self.parent.file_handler.load_file(filename=self.parent.buffer.full_name)

	def file_delete(self, arg=None):
		self.parent.file_handler.del_file(filename="".join(arg[1:]))
		
	def music_play(self, arg=None):
		self.parent.music_player.load_song(arg[1:])

	def music_pause(self, arg=None):
		self.parent.music_player.pause_song()

	def music_unpause(self, arg=None):
		self.parent.music_player.pause_song(unpause=True)

	def music_stop(self, arg=None):
		self.parent.music_player.stop_song()

	def system_execute(self, arg=None):
		if (not arg[1:]): self.parent.error(f"{self.get_docs(arg[0])}"); return
		self.parent.buffer.run_subprocess(argv=arg[1:])

	def python_execute(self, arg=None):
		print("ARGS: ", " ".join(arg[1:]))
		exec(" ".join(arg[1:]))

	def buffer_execute(self, arg=None):
		arg = self.parent.buffer.get("1.0", "end-1c")
		exec(arg)

	def ls(self, arg=None):
		self.parent.nt_place(arg)

	def cd(self, arg=None):
		arg = "\ ".join(arg[1:])
		path = os.path.abspath(f"{self.parent.file_handler.current_dir}/{arg}")
			
		if (not self.parent.file_handler.cd(path)):
			path = os.path.abspath(arg)
			self.parent.file_handler.cd(path)

	def new_directory(self, arg=None):
		if (arg[1:]):
			arg = "\ ".join(arg[1:])
			self.parent.file_handler.new_directory(filename=arg)
		else:
			self.parent.notify("error: no name specified")

	def delete_directory(self, arg=None):
		if (arg[1:]):
			self.parent.file_handler.delete_directory(filename=arg[1])
		else:
			self.parent.notify("error: no name specified")

	def theme(self, arg=None):
		if (arg[1:]):
			self.parent.theme_set(arg[1:])
		else:
			self.parent.command_out.change_ex(self.parent.theme_set)
			result = ""
			for key in self.parent.theme_options.keys():
				result += key+"\n"
			self.parent.command_out_set(result, [["1.0", "end"]])

	def tab_size_set(self, arg=None):
		if (arg[1:]):
			self.parent.conf["tab_size"] = int(arg[1])
			self.parent.buffer.configure_self()
			self.parent.notify(f"Current size: {self.parent.conf['tab_size']}")
		else:
			self.parent.notify(f"please, specify new size. Current size: {self.parent.conf['tab_size']}")

	def replace_spaces(self, arg=None):
		self.parent.buffer.replace_x_with_y(" "*self.parent.conf["tab_size"], "\t")

	def replace_tabs(self, arg=None):
		self.parent.buffer.replace_x_with_y("\t", " "*self.parent.conf["tab_size"])

	def initialize_file(self, arg=None):
		for init in list(self.parent.buffer.highlighter.language_init.keys()):
			if (re.match(init, self.parent.buffer.highlighter.lang)):
				self.parent.buffer.insert("1.0", self.parent.buffer.highlighter.language_init[init])
				break

		self.parent.highlight_chunk()

	def delete_empty_files(self, arg=None): #TODO
		pass

	def lex(self, arg=None):
		self.parent.buffer.lexer.lex()

	def lex_print(self, arg=None):
		self.parent.buffer.lexer.print_res()

	def lexer_switch(self, arg=None): # TEMPORARY UNTIL I COMPLETELY IMPLEMENT LEXERS
		if (arg[1].lower() == "python"):
			self.parent.buffer.lexer = LEXER(self.parent, self.parent.buffer)
		elif (arg[1].lower() == "c"):
			self.parent.buffer.lexer = C_LEXER(self.parent, self.parent.buffer)

	def add_tag(self, arg=None):
		index = self.parent.buffer.index_sort(self.parent.buffer.index("insert"), self.parent.buffer.mark_names()[-1])
		self.parent.buffer.tag_raise(arg[1])
		self.parent.buffer.tag_add(arg[1], index[0], index[1])

	def remove_tag(self, arg=None):
		index = self.parent.buffer.index_sort(self.parent.buffer.index("insert"), self.parent.buffer.mark_names()[-1])
		self.parent.buffer.tag_remove(arg[1], index[0], index[1])

	def lf(self, arg=None):
		self.parent.convert_to_lf()

	def crlf(self, arg=None):
		self.parent.convert_to_crlf()

	def toggle_buffer_tab_show(self, arg=None):
		self.parent.conf["show_buffer_tab"] = not self.parent.conf["show_buffer_tab"]
		self.parent.buffer_tab.place_forget()
		self.parent.reposition_widgets()

	def make(self, arg=None):
		self.system_execute("sys make".split())

	def open_conf_file(self, arg=None):
		self.parent.file_handler.load_file(filename=f"{os.path.dirname(__file__)}/conf")
	
	def open_keybindings_file(self, arg=None):
		self.parent.file_handler.load_file(filename=f"{os.path.dirname(__file__)}/keybinds_conf.json")

	def reload_conf(self, arg=None):
		self.parent.load_conf()

	def reload_keybinds(self, arg=None):
		for w in self.parent.winfo_children():
			if (w.winfo_children()):
				for ww in self.parent.winfo_children():
					bind_keys_from_conf(w)
			bind_keys_from_conf(w)

	def reload_modules(self, arg=None):
		self.parent.reload_modules()

	def reload_themes(self, arg=None):
		self.parent.theme_options = laod_themes()

	def load_modules_from(self, arg=None):
		if (not arg[1:]): self.parent.error(f"{self.get_docs(arg[0:])}"); return
		arg = "".join(arg[1:])
		self.parent.reload_modules(dir=arg)

	def change_font(self, arg=None):
		if (not arg[1:]): arg.append(self.parent.conf["font"])
		arg = " ".join(arg[1:])
		self.parent.font_set(family=arg)
		self.parent.notify(f"font was changed to {arg}")

	def set_timer(self, arg=None):
		if (not arg[1:]): self.parent.error(f"{self.get_docs(arg[0:])}"); return

		def timer(self):
			time.sleep(int(arg[1]))
			self.parent.command_out_set(arg="TIME UP", tags=[["1.0", "end", "error"]])

		threading.Thread(target=timer, args=(self, ), daemon=True).start()

	def write(self, arg=None):
		self.parent.buffer.insert("insert", arg)

	def write_hack(self, arg=None):
		self.write(self.parent.buffer.highlighter.comment_sign+" HACK: ")
		if (arg[1:]): self.write(" ".join(arg[1:]))

	def write_todo(self, arg=None):
		self.write(self.parent.buffer.highlighter.comment_sign+" TODO: ")
		if (arg[1:]): self.write(" ".join(arg[1:]))

	def write_note(self, arg=None):
		self.write(self.parent.buffer.highlighter.comment_sign+" NOTE: ")
		if (arg[1:]): self.write(" ".join(arg[1:]))

	def todo_set(self, arg=None):
		if (arg[1:]): arg = " ".join(arg[1:])
		else: arg = None
		self.parent.buffer.todo_set(text=arg)

	def list_subprocess(self, arg=None):
		s = ""
		if (not self.parent.subprocesses): self.parent.command_out_set(arg="None"); return
		
		for proc in self.parent.subprocesses:
			s += f"proc: {proc.args} id: {proc.pid}\n"
		self.parent.command_out_set(arg=s)

	def create_temp_buffer(self, arg=None):
		if (not arg[1:]): arg = f"{time.time()}"
		else: arg = " ".join(arg[1:])
		self.parent.file_handler.new_buffer(buffer_name=arg, buffer_type="temp")

	@has_argument
	def create_mark(self, arg=None):
		# if (not arg[1:]): self.parent.error(f"{self.get_docs(arg[0:])}"); return
		self.parent.buffer.mark_set(arg[1], self.parent.buffer.index("insert"))

	def list_mark(self, arg=None):
		s = ""

		for name in self.parent.buffer.mark_names():
			s += f"{name}: {self.parent.buffer.index(name)}\n"
		self.parent.notify(s)

	@has_argument
	def jump_to(self, arg=None):
		self.parent.buffer.mark_set("insert", arg[1])

	def command_not_found(self, arg=None):
		res = ""
		for c in arg:
			res += c+" "
		self.parent.notify(f"command <{res[:-1]}> not found", [["1.0", "1.7"], [f"1.{8+len(res)+2}", "end"]])





