__author__ = "Bugy"
__license__ = "MIT"
__maintainer__ = "Bugy"
__email__ = ["matejbugy@gmail.com", "achjoj5@gmail.com"]
__status__ = "Dev"
__version__ = "1.1.4"

import tkinter
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

import re
import json

import subprocess

import requests
from bs4 import BeautifulSoup

import random
import threading

import psutil

from highlighter import *
from parser import *

try: import notify2
except Exception: pass

try:
	import platform, ctypes

	if int(platform.release()) >= 8:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)

	CONTROL_KEYSYM = 262156
	WINDOW_MARGIN = 0
except Exception:
	CONTROL_KEYSYM = None
	WINDOW_MARGIN = 24

class win(tkinter.Tk):
	""" main object of Nix text editor"""
	def __init__(self, file=None):
		super().__init__()
		self.theme_options = {
			"cake": {"window": {"bg" : "#000000", "fg": "#AAAAAA", "insertbg": "#555555", "selectbg": "#220022", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A500FF", "logical_keywords": "#ff00bb", "functions": "#3023DD", "upcase_b": "#3055BB","numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#220022", "command_out_insert_bg": "#555555"}},

			 "retro_cake": {"window": {"bg" : "#000000", "fg": "#CDAB81", "insertbg": "#AAAAAA", "selectbg": "#332233", "selectfg": "#AAAAAA", "widget_fg": "#CDAB81", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A500FF", "logical_keywords": "#ff00bb", "functions": "#3023DD", "upcase_b": "#3055BB","numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#220022", "command_out_insert_bg": "#555555"}},

			 "nat": {"window": {"bg" : "#070304", "fg": "#AAAAAA", "insertbg": "#005500", "selectbg": "#001500", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A53300", "logical_keywords": "#2090F0", "functions": "#E0AF60", "upcase_b": "#BB5522","numbers": "#BB9900", "operators": "#f75f00", "special_chars": "#00A000", "quotes": "#00DCFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#001500", "command_out_insert_bg": "#005500"}},

			 "lens": {"window": {"bg" : "#070304", "fg": "#AAAAAA", "insertbg": "#005500", "selectbg": "#001500", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#E4D8B4", "logical_keywords": "#2090F0", "functions": "#83B799", "upcase_b": "#BB5522","numbers": "#E86F68", "operators": "#DE7E44", "special_chars": "#6C566D", "quotes": "#E2CD6D", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#001500", "command_out_insert_bg": "#6f8ea9"}},

			 "tea": {"window": {"bg" : "#070304", "fg": "#AAAAAA", "insertbg": "#005500", "selectbg": "#001500", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A53300", "logical_keywords": "#2090F0", "functions": "#83B799", "upcase_b": "#BB5522","numbers": "#E86F68", "operators": "#f75f00", "special_chars": "#00A000", "quotes": "#E2CD6D", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000",  "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#113311", "command_out_insert_bg": "#005500"}},

			"thorfinn": {"window": {"bg" : "#020518", "fg": "#dde2e3", "insertbg": "#6f8ea9", "selectbg": "#120512", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#6f8ea9", "logical_keywords": "#b37c57", "functions": "#60412b", "upcase_b": "#796878", "numbers": "#3f5e89", "operators": "#f75c57", "special_chars": "#9aacb8", "quotes": "#005577", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#4F6CA5", "command_out_insert_bg": "#6f8ea9"}},

			"muffin" : {"window": {"bg" : "#CCCCCC", "fg": "#000000", "insertbg": "#111111", "selectbg": "#111111", "selectfg": "#FFFFFF", "widget_fg": "#000000", "select_widget": "#000000", "select_widget_fg": "#FFFFFF"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#00BABA", "functions": "#3023DD", "logical_keywords": "#ff00bb", "upcase_b": "#3055BB", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#74091D", "comments": "#111111", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#000000", "command_out_insert_bg": "#111111"}},

			"toast" : {"window": {"bg" : "#000000", "fg": "#9F005F", "insertbg": "#FFFFFF", "selectbg": "#555555", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#f70000", "logical_keywords": "#ff00bb", "functions": "#3023DD", "upcase_b": "#3055BB", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#555555", "command_out_insert_bg": "#FFFFFF"}},

			"groove": {"window": {"bg" : "#080808", "fg": "#EBDBB2", "insertbg": "#3055BB", "selectbg": "#242020", "selectfg": "#EBDBB2", "widget_fg": "#EBDBB2", "select_widget": "#FFFFAA", "select_widget_fg": "#1D2021"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#458588", "logical_keywords": "#CC241D", "functions": "#D65D0E", "upcase_b": "#3055BB", "numbers": "#B16286", "operators": "#9EC07C", "special_chars": "#D5C4A1", "quotes": "#689D6A", "comments": "#3C3836", "command_keywords": "#FFFFFF", "pair_bg": "#FB4934", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#555555", "command_out_insert_bg": "#FFFFFF"}},

			"spacey": {"window": {"bg" : "#080808", "fg": "#b2b2b2", "insertbg": "#AF00D7", "selectbg": "#181022", "selectfg": "#EBDBB2", "widget_fg": "#b2b2b2", "select_widget": "#FFFFAA", "select_widget_fg": "#1D2021"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#d70040", "logical_keywords": "#397c80", "functions": "#AF00D7", "upcase_b": "#3055BB", "numbers": "#AF87D7", "operators": "#D7875F", "special_chars": "#D5C4A1", "quotes": "#689D6A", "comments": "#490648", "command_keywords": "#FFFFFF", "pair_bg": "#FB4934", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#555555", "command_out_insert_bg": "#FFFFFF"}},

			"mono": {"window": {"bg" : "#080808", "fg": "#b2b2b2", "insertbg": "#FFFFFF", "selectbg": "#222222", "selectfg": "#929292", "widget_fg": "#b2b2b2", "select_widget": "#FFFFAA", "select_widget_fg": "#CCCCCC"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#CCCCCC", "logical_keywords": "#CCCCCC", "functions": "#CCCCCC", "upcase_b": "#FFFFFF", "numbers": "#999999", "operators": "#888888", "special_chars": "#FFFFFF", "quotes": "#777777", "comments": "#222222", "command_keywords": "#FFFFFF", "pair_bg": "#444444", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#555555", "command_out_insert_bg": "#FFFFFF"}},

			"hurty": {"window": {"bg" : "#b2b2b2", "fg": "#000000", "insertbg": "#000000", "selectbg": "#222222", "selectfg": "#999999", "widget_fg": "#000000", "select_widget": "#0000000", "select_widget_fg": "#FFFFFF"},
			 "highlighter": {"whitespace": "#111111", "keywords_b": "#555555", "logical_keywords": "#555555", "functions_b": "#555555", "upcase_b": "#000000", "numbers": "#222222", "operators": "#111111", "special_chars": "#000000", "quotes": "#444444", "comments": "#222222", "command_keywords": "#FFFFFF", "pair_bg": "#444444", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#555555", "command_out_insert_bg": "#FFFFFF"}},
			}

		self.theme = self.theme_options["spacey"]

		self.commands = {
			"lget":"gets total amount of lines", "l":"use: l[number|number.number] :: puts your cursor on line[number]",
			"q":"quits", "quit":"quits", "temp":"updates temperature", "alpha": "use: alpha [number] \n sets how see through your window is \n 0 is completely transparent :: 100 is completely opaque",
			"convert": "use: convert [number] (decimal|hex|binary) \n converts [number] into decimal, hex and binary", "save":"saves your current file",
			"saveas":"use: saveas [name] :: saves your current file as [name]", "open":"use:  open [name] :: opens file with name[name]", "theme": "use: theme :: shows all theme names || use: theme [themename] :: sets theme",
			"lyrics": "use: lyrics [artist],[song name] :: scrapes lyrics off of a website (if possible)",
			"sys": "use: sys [arguments] :: starts a subprocess [arguments] as if in a terminal",
			"split": "use: split [option] (horizontal/h|vertical/v|n) :: splits buffers",
			"unsplit": "use: unsplit :: unsplits buffers",
			"ls": "shows files in current directory"
			}

		self.scroll_multiplier = 0

		self.line_count = None

		self.tab_offset = 0
		self.tab_lock = False
		self.tab_size = 4

		self.selection_start_index = None
		self.queue = []
		self.found = []
		self.found_index = 0
		self.cursor_index = ["1", "0"]
		self.current_line = ""
		self.last_index = "0.0"
		self.text_len = 0

		self.underline_pairs = False
		self.backup_files = False
		self.highlighting = True
		self.command_highlighting = True
		self.fullscreen = False
		self.split_mode = 0

		self.show_speed = True
		self.show_time = True
		self.show_temperature = True
		self.show_lineno = True

		self.suggest = True
		
		self.run = True

		self.font_size = 12
		self.sfont_size = self.font_size - 2
		self.font_set()
		
		#configuring main window
		# self.wm_attributes("-type", "splash")
		self.resizable(True,True)
		self.geometry(f"{self.font.measure(' ')*80}x{self.font.metrics('linespace')*32}")
		self.wm_minsize(20, 0)
		self.update_win()
		self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_x()+self.winfo_x()//3}+{(self.winfo_screenheight()-self.winfo_height())//2}") #CENTERING MAGIC #PROLLY DOESN'T WORK THOUGH
		
		# try: self.iconbitmap("icon.ico")
		# except Exception as e: print(e)
		try: self.tk.call('wm', 'iconphoto', self._w, tkinter.PhotoImage(file="/usr/local/bin/Nix/icon.png"))
		except Exception as e: print(e)
		
		self.parser = PARSER(self)

		self.file_handler = FILE_HANDLER(self)
		self.video_handler = VIDEO_HANDLER(self)

		self.suggest_widget = SUGGEST_WIDGET(self)

		self.init()

	def init(self):
		""" a completely useless initialize function """
		self.update_win()
		# self.wm_attributes("-alpha", 1)
		self.canvas = tkinter.Canvas()
		self.canvas.place(x=0, y=0, relwidth=1, height=45)

		self.time_label = tkinter.Label()
		self.time_label_value = tkinter.StringVar()
		self.time_label_value.set("0:0:0")
		self.temperature_label = tkinter.Label(text="(-273.15°C)")
		self.line_no = tkinter.Label()
		self.fps_label = tkinter.Label()
		self.key_label = tkinter.Label()

		# see widgets.py
		self.find_entry = FIND_ENTRY(self)
		self.command_entry = COMMAND_ENTRY(self)
		self.command_out = COMMAND_OUT(self)

		self.buffer_tab_frame = tkinter.Frame(self)

		self.txt = None #file_handler.init functions uses this txt variable so if it's not declared before running the function it's going to break 
		self.file_handler.init(".~scratch") #see handlers.py/FILE_HANDLER
		self.curs = tkinter.Label(self.txt, bg=self.theme["window"]["fg"])

		# self.music_player = MUSIC_PLAYER(self)

		self.bind("<Control-Escape>", self.win_destroy)
		self.bind("<Configure>", self.reposition_widgets) #repositions the text widget to be placed correctly

		self.theme_load()
		self.update_buffer()

		if (len(sys.argv) > 1): [self.file_handler.load_file(filename=arg) for arg in sys.argv[1:]]
		
	def theme_make(self):
		if (type(self.txt) != TEXT): return
		for key in self.theme["highlighter"].items():
			if (key[0][-2:] == "bg"):
				self.txt.tag_configure(key[0], background=key[1], foreground=self.theme["window"]["bg"], font=self.txt.font)
				self.command_out.tag_configure(key[0], background=key[1], foreground=self.theme["window"]["bg"], font=self.command_out.font)
				
			elif (key[0][-2:] == "_b"):
				self.txt.tag_configure(key[0][:-2], foreground=key[1], font=self.txt.font_bold)
				self.command_out.tag_configure(key[0][:-2], foreground=key[1], font=self.command_out.font_bold)
				
			else:
				self.txt.tag_configure(key[0], foreground=key[1], font=self.txt.font)
				self.command_out.tag_configure(key[0], foreground=key[1], font=self.command_out.font)

		self.command_entry.tag_configure("command_keywords", foreground=self.theme["highlighter"]["command_keywords"])
		# self.txt.tag_lower("comments", "keywords")

	def theme_set(self, theme=None):
		if (type(theme) == list): theme = theme[-1] #failsave switch when selecting multiple themes through command_out widget
		self.theme = self.theme_options[theme]
		self.theme_load()
		self.highlight_chunk()

	def theme_load(self):
		self.theme_make()
		self.configure(bg=self.theme["window"]["bg"], cursor=None)

		self.canvas.configure(bg=self.theme["window"]["bg"], bd=0, highlightthickness=0)
		self.buffer_tab_frame.configure(bg=self.theme["window"]["bg"], bd=0, highlightthickness=0)

		self.txt.configure_self()

		self.time_label.configure(fill=None, anchor="w", justify="left", font=self.widget_font, textvariable=self.time_label_value,
		 bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.temperature_label.configure(fill=None, anchor="w", justify="left", font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.line_no.configure(fill=None, anchor="w", justify="left", font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.fps_label.configure(text="<0.0KHz>", fill=None, anchor="w", justify="left", font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.key_label.configure(fill=None, anchor="w", justify="left", font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])

		self.command_entry.configure_self()
		self.find_entry.configure_self()
		self.command_out.configure_self()

		for buffer_tab in self.file_handler.buffer_tab_list:
			buffer_tab.configure_self()

		if (self.file_handler.buffer_tab): self.file_handler.buffer_tab.focus_highlight()

		self.update_win()

	def font_set(self, arg=None, family="Noto Mono", retro=False):
		if (retro): self.font_family = ["Ac437 IBM VGA 9x8", "normal", "bold", "roman"]
		else: self.font_family = [family, "normal", "bold", "roman"]
		self.font = font.Font(family=self.font_family[0], size=self.font_size, weight=self.font_family[1], slant=self.font_family[3])
		self.font_bold = font.Font(family=self.font_family[0], size=self.font_size, weight="bold", slant=self.font_family[3]) 
		self.smaller_font = font.Font(family=self.font_family[0],size=self.sfont_size, weight=self.font_family[1])
		self.smaller_font_bold = font.Font(family=self.font_family[0],size=self.sfont_size, weight="bold")
		self.widget_font = font.Font(family=self.font_family[0], size=self.font_size, weight=self.font_family[2])

		#lazy workaround
		try: self.theme_load()
		except Exception: pass

	def reposition_widgets(self, arg=None):
		fs = self.widget_font.metrics("linespace")
		top_bar_y = fs//1.5+3
		txt_y = fs*2+2

		# TODO(@bugy): make separate frame for topbar info and use pack instead of place for more customizability
		if (self.command_entry.winfo_viewable()): self.command_entry_place()
		if (self.command_out.winfo_viewable()): self.command_out_set(resize=True)
		if (self.show_time): self.time_label.place(x=self.temperature_label.winfo_x(), y=0, height=top_bar_y, anchor="ne")
		if (self.show_temperature): self.temperature_label.place(x=self.line_no.winfo_x()-10, y=0, height=top_bar_y, anchor="ne")
		if (self.show_lineno): self.line_no.place(x=self.winfo_width()-self.line_no.winfo_width()-10, y=0, height=top_bar_y, anchor="nw")
		if (self.show_speed): self.fps_label.place(x=self.time_label.winfo_x()-10, y=0, height=top_bar_y, anchor="ne")
		self.key_label.place(x=0, y=0, height=top_bar_y, anchor="nw")
		self.buffer_tab_frame.place(x=0, y=top_bar_y+3, width=self.winfo_width(), height=fs, anchor="nw")

		if (self.split_mode == 0): self.txt.place(x=0,y=txt_y, width=self.winfo_width(), height=self.winfo_height()-45, anchor="nw") # self.txt.change_coords([2, 45, self.winfo_width()-2, self.winfo_height()-50])
		elif (self.split_mode == 1): self.txt.place(x=2,y=txt_y, width=self.winfo_width()//2-2, height=self.winfo_height()-50, anchor="nw"); self.txt_1.place(x=self.winfo_width()//2,y=txt_y, width=self.winfo_width()//2-2, height=self.winfo_height()-50, anchor="nw")
		elif (self.split_mode == 2): self.txt.place(x=2,y=txt_y, width=self.winfo_width()-2, height=self.winfo_height()//2-50, anchor="nw"); self.txt_1.place(x=2,y=self.winfo_height()//2, width=self.winfo_width()-2, height=self.winfo_height()//2, anchor="nw")

		self.canvas.delete("all")
		self.canvas.create_line(0, fs-1, self.winfo_width(), fs-1, fill=self.theme["window"]["fg"], smooth=1)
		self.canvas.create_line(0, fs*2, self.winfo_width(), fs*2, fill=self.theme["window"]["fg"], smooth=1)


	def flashy_loading_bar(self, arg=None):
		def a():
			x = ""
			r = 100
			for i in range(r):
				time.sleep(0.2)
				x = "["+chr(9608)*i+"."*(r-i)+"]"
				self.command_out_set(x, justify="center")

		threading.Thread(target=a, daemon=True).start()

	def win_destroy(self, arg=None) -> str:
		self.file_handler.closing_sequence()
		self.run = False
		self.quit()
		return "break"

	def convert_line_index(self, type: str, index=None) -> (int, float):
		""" gets the cursor's position """
		if (not index): index = self.cursor_index[0]
		if (type == "int"): return int(float(index))
		elif (type == "float"): return float(index)

	def get_line_count(self, arg=None):
		""" returns total amount of lines in opened text """
		return sum(1 for line in self.txt.get("1.0", "end").split("\n"))

	def get_word_count(self, arg=None):
		t = self.txt.get("1.0", "end-1c")
		return [len(t.split(" ")), len(t)/5]

	def get_selection_count(self, arg=None):
		self.command_out_set(f"len: {len(self.selection_get())}")
		return "break"

	def inline_index_sort(self, index1, index2):
		if (int(index1.split(".")[1]) <= int(index2.split(".")[1])): return (index1, index2)
		else: return (index2, index1)

	def multiline_index_sort(self, index1, index2):
		self.queue = [self.convert_line_index("int", index1), self.convert_line_index("int", index2)]
		self.queue.sort()
		return self.queue[0], self.queue[1] + 1

	def sameline_check(self, index1, index2):
		return self.convert_line_index("int", index1) == self.convert_line_index("int", index2)

	def precise_index_sort(self, index1, index2):
		print(index1, index2)
		s1, s2 = index1, index2
		if (self.sameline_check(s1, s2)):
			if (int(s1.split(".")[1]) <= int(s2.split(".")[1])): return (index1, index2)
			else: return (index2, index1)
		else:
			if (self.convert_line_index("int", s1) <=  self.convert_line_index("int", s2)): (index1, index2)
			else: return (index2, index1)
			
	def del_selection(self):
		self.selection_start_index = None
		self.txt.mark_unset(self.txt.mark_names()[-1])
		self.txt.tag_remove("sel", "1.0", "end")

	def queue_get(self, arg=None):
		self.queue = [self.convert_line_index("int", self.selection_start_index), self.convert_line_index("int", self.txt.index("insert"))]
		self.queue.sort()
		return self.queue[0], self.queue[1] + 1

	def moving(func): #something something event queue something
		def wrapped_func(self, *args, **kwargs):
			self.txt.tag_remove("cursor", "1.0", "end")
			func(self, *args, **kwargs)
			self.txt.tag_add("cursor", "insert")
			return "break"

		return wrapped_func

	@moving
	def move(self, arg=None, mod=[]):
		key = arg.keysym
		suffix = ["Line", "Char"]
		prefix = ""
		
		if ("control" in mod):
			suffix = ["Para", "Word"]

		if ("shift" in mod):
			prefix = "Select"

		if (key == "Up"):
			self.txt.event_generate(f"<<{prefix}Prev{suffix[0]}>>")
			self.txt.see(self.convert_line_index("float")-5)

		elif (key == "Down"):
			self.txt.event_generate(f"<<{prefix}Next{suffix[0]}>>")
			self.txt.see(self.convert_line_index("float")+5)

		elif (key == "Left"):
			self.txt.event_generate(f"<<{prefix}Prev{suffix[1]}>>")

		elif (key == "Right"):
			self.txt.event_generate(f"<<{prefix}Next{suffix[1]}>>")

		if (prefix == ""): self.selection_start_index = None; del self.queue[:]
		else: self.selection_start_index = self.txt.index(self.txt.mark_names()[-1])
		self.update_index()
		# if (self.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.command_out.place_forget()

		return "break"

	def move_standard(self, arg=None):
		self.move(arg)
		return "break"

	def move_jump(self, arg=None):
		self.move(arg, ["control"])
		return "break"

	def move_select(self, arg=None):
		self.move(arg, ["shift"])
		return "break"

	def move_jump_select(self, arg=None):
		self.move(arg, ["control", "shift"])
		return "break"

	#text manipulation bindings
	@moving
	def cut(self, arg=None):
		""" Control-X """
		self.txt.event_generate("<<Cut>>")
		return "break"
		
	@moving
	def undo(self, arg=None):
		""" Control-Z """
		chunk_size = self.get_line_count()
		self.txt.event_generate("<<Undo>>")
		start_index = self.convert_line_index("int")
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	@moving
	def redo(self, arg=None):
		""" Control-Y """
		chunk_size = self.get_line_count()
		self.txt.event_generate("<<Redo>>")
		start_index = self.convert_line_index("int")
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	@moving
	def copy(self, arg=None):
		""" Control-C """
		self.txt.event_generate("<<Copy>>")
		return "break"

	@moving
	def paste(self, arg=None):
		""" Control-V """
		to_paste = self.clipboard_get()
		start_index = self.convert_line_index("int", self.txt.index("insert"))
		self.txt.insert("insert", to_paste)
		self.highlight_chunk(start_index=start_index, stop_index=self.convert_line_index("int", self.txt.index("insert")))

		self.txt.event_generate("<<SelectNone>>")
		return "break"

	def select_all(self, arg=None):
		""" Control-A """
		self.txt.event_generate("<<SelectAll>>")
		return "break"

	@moving
	def home(self, arg=None):
		""" Home """
		index = ""
		i = 0
		for i, char in enumerate(self.current_line, 0):
			if (not re.match(r"\s", char)): index = f"{self.cursor_index[0]}.{i}"; break
		
		if (self.txt.index("insert") == index): self.txt.event_generate("<<LineStart>>")
		else: self.txt.mark_set("insert", index)
		self.txt.event_generate("<<SelectNone>>")
		return "break"

	@moving
	def home_select(self, arg=None):
		""" Shift-Home """
		index = ""
		i = 0
		for i, char in enumerate(self.current_line, 0):
			if (not re.match(r"\t", char)): index = f"{self.cursor_index[0]}.{i}"; break

		if (self.txt.index("insert") == index):
			self.txt.event_generate("<<SelectLineStart>>")
		
		elif (self.txt.index("insert") != index):
			self.txt.event_generate("<<SelectLineStart>>")
			[self.txt.event_generate("<<SelectNextChar>>") for i in range(i)]
		return "break"

	@moving
	def end(self, arg=None):
		self.txt.event_generate("<<LineEnd>>")
		self.txt.event_generate("<<SelectNone>>")
		return "break"

	@moving
	def end_select(self, arg=None):
		self.txt.event_generate("<<SelectLineEnd>>")
		return "break"

	@moving
	def mouse_left(self, arg=None):
		self.txt.mark_set("insert", "current")
		self.del_selection()
		self.update_buffer()
		return "break"

	def mouse_left_motion(self, arg=None):
		if (not self.selection_start_index):
			self.selection_start_index = self.txt.index("insert")
		self.txt.mark_set("insert", "current")
		self.update_buffer()

	def set_cursor_mode(self, arg=None):
		""" Insert """
		# don't ask

		self.txt.configure(insertwidth=1)
		
		# self.txt.cursor_mode -= -1 if self.txt.cursor_mode < 2 else 2 #I fucking hate this :DDD
		self.txt.cursor_mode += 1
		if (self.txt.cursor_mode >= 3):
			self.txt.cursor_mode = 0
			
		if (self.txt.cursor_mode == 0): #LINE
			self.txt.tag_delete("cursor")
			self.txt.block_cursor = False
			self.txt.terminal_like_cursor = False
			
		elif (self.txt.cursor_mode == 1): #NORMAL BLOCK
			self.txt.block_cursor = True
			self.txt.terminal_like_cursor = False

		elif (self.txt.cursor_mode == 2): #TERMINAL-LIKE BLOCK
			self.txt.block_cursor = True
			self.txt.terminal_like_cursor = True
		
		else:
			self.txt.cursor_mode = 2
			self.txt.block_cursor = True
			self.txt.terminal_like_cursor = True

		self.txt.configure(blockcursor=self.txt.block_cursor)
		return "break"

	def change_case(self, arg=None):
		self.selection_start_index = self.txt.index(self.txt.mark_names()[-1])
		index_range = [self.selection_start_index, self.txt.index("insert")]

		index_range = self.inline_index_sort(*index_range)
		
		if (arg.state == 20): # without shift
			text = self.txt.get(index_range[0], index_range[1])
			self.txt.delete(index_range[0], index_range[1])
			text = text.lower()
			self.txt.insert(index_range[0], text)

		elif (arg.state == 21): # shift
			text = self.txt.get(index_range[0], index_range[1])
			self.txt.delete(index_range[0], index_range[1])
			text = text.upper()
			self.txt.insert(index_range[0], text)

		self.highlight_chunk(start_index=float(index_range[0]), stop_index=float(index_range[1]))

		del index_range
		del text
		return "break"

	def char_enclose(self, arg=None) -> str:
		self.selection_start_index = self.txt.index(self.txt.mark_names()[-1])
		index = self.inline_index_sort(self.txt.index("insert"), self.selection_start_index)

		if (arg.keysym == "parenleft"): c1 = "("; c2 = ")"
		elif (arg.keysym == "bracketleft"): c1 = "["; c2 = "]"
		elif (arg.keysym == "braceleft"): c1 = "{"; c2 = "}"
		elif (arg.keysym == "apostrophe" or arg.keysym == "quotedbl"): c1 = "\""; c2 = "\""
		self.txt.insert(index[1], c2)
		self.txt.insert(index[0], c1)

		return "break"

	def comment_line(self, arg=None) -> str:
		""" I wish I knew what the fuck is going on in here I am depressed """
		
		start_index, stop_index = self.queue_get()

		comment_len = len(self.txt.highlighter.comment_sign)

		for line_no in range(start_index, stop_index):
			current_line = self.txt.get(float(line_no), f"{line_no}.0 lineend+1c")
			for i, current_char in enumerate(current_line, 0):
				if (self.txt.highlighter.commment_regex.match(current_char+current_line[i+1:i+1+comment_len])):
					if (self.txt.get(f"{line_no}.{i+comment_len}", f"{line_no}.{i+1+comment_len}") == " "):
						self.txt.delete(f"{line_no}.{i}", f"{line_no}.{i+1+comment_len}")
					else:
						self.txt.delete(f"{line_no}.{i}", f"{line_no}.{i+comment_len}")
					break

				elif (not re.match("\s", current_char)):
					self.txt.insert(f"{line_no}.{i}", self.txt.highlighter.comment_sign+" ")
					break

		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break" # returning "break" prevents system/tkinter to call default bindings

	def indent(self, arg=None):
		""" Tab """
		start_index, stop_index = self.queue_get()
		index = 0
		if (start_index+1 == stop_index): index = self.cursor_index[1]

		for line_no in range(start_index, stop_index):
			self.txt.insert(f"{line_no}.{index}", "\t")

		return "break"
		
	def unindent(self, arg=None):
		""" Checks if the first character in line is \t (tab) and deletes it accordingly """
		start_index, stop_index = self.queue_get()

		for line_no in range(start_index, stop_index):
			if (re.match(r"\t", self.txt.get(f"{line_no}.0", f"{line_no}.1"))):
				self.txt.delete(f"{line_no}.0", f"{line_no}.1")
		
		return "break"

	#window operation bindings
	def window_select(self, widget="", arg=None):
		if (widget == "file_menu"): self.file_menubar_label.focus_set(); self.file_menubar_label.configure(bg=self.theme["window"]["select_widget"], fg=self.theme["window"]["select_widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		elif (widget == "settings_menu"): self.settings_menubar_label.focus_set(); self.settings_menubar_label.configure(bg=self.theme["window"]["select_widget"], fg=self.theme["window"]["select_widget_fg"]); self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		elif (widget == "text"): self.txt.focus_set(); self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])

		return "break"

	def set_fullscreen(self, arg=None):
		""" set the window to be fullscreen F11 """
		self.fullscreen = not self.fullscreen
		self.attributes("-fullscreen", self.fullscreen)

		return "break"

	def set_dimensions(self, arg=None, expand=True): # I do understand that this is a terrible, hideous thing but I couldn't come up with a better solution
		""" changes window size accordingly to keys pressed Alt-Curses """
		key = arg.keysym
		# print(arg.state)
		if (expand):
			margin = 20
			if (key == "Right"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}")
			elif (key == "Left"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{self.winfo_x()-margin}+{self.winfo_y()-WINDOW_MARGIN}")
			elif (key == "Up"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{self.winfo_x()}+{self.winfo_y()-margin-WINDOW_MARGIN}")
			elif (key == "Down"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}")

		elif (not expand):
			margin = -20
			if (key == "Right"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{self.winfo_x()-margin}+{self.winfo_y()-WINDOW_MARGIN}")
			if (key == "Left"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{self.winfo_x()}+{self.winfo_y()-WINDOW_MARGIN}")
			if (key == "Up"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{self.winfo_x()}+{self.winfo_y()-WINDOW_MARGIN}")
			if (key == "Down"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{self.winfo_x()}+{self.winfo_y()-margin-WINDOW_MARGIN}")
		
		return "break"	

	def win_expand(self, arg=None):
		self.set_dimensions(arg)
		return "break"

	def win_shrink(self, arg=None):
		self.set_dimensions(arg, expand=False)
		return "break"

	def nt_place(self, arg=None): # why nt???
		self.file_handler.ls()

	@moving
	def scroll(self, arg, multiplier=1):
		""" scrolls through the text widget MouseWheel && Shift-MouseWheel for speedy scrolling """
		if (arg.num == 5 or arg.delta < 0):
			self.txt.mark_set("insert", f"{int(self.cursor_index[0])+3*multiplier}.{self.cursor_index[1]}")
	
		elif (arg.num == 4 or arg.delta > 0):
			self.txt.mark_set("insert", f"{int(self.cursor_index[0])-3*multiplier}.{self.cursor_index[1]}")
		
		# hides widgets that could be in the way
		self.txt.focus_set()
		self.txt.see("insert")
		self.command_out.place_forget()
		self.command_entry.place_forget()
		
		self.del_selection()
		self.update_index()

	def popup(self, arg=None):
		""" gets x, y position of mouse click and places a menu accordingly """
		self.right_click_menu.tk_popup(arg.x_root+5, arg.y_root)

	def command_entry_place(self, arg=None):
		""" Shows command entry widget """
		h = self.command_entry.font.metrics("linespace")
		self.command_entry.place(x=-1, y=self.winfo_height()-h-5, width=self.winfo_width()+2, height=h+5, anchor="nw")
		self.command_out.place_forget()
		self.command_entry.tkraise(); self.command_entry.focus_set()
			
		return "break"

	def find_place(self, arg=None, text=""):
		h = self.find_entry.font.metrics("linespace")
		self.find_entry.place(x=0, y=self.winfo_height()-h-40, width=self.winfo_width(), height=h+5, anchor="nw")
		self.find_entry.find_mode_set()
		self.find_entry.tkraise(); self.find_entry.focus_set()

		return "break"

	def command_out_set(self, arg=None, tags=None, resize=False, focus=True, justify="left"):
		# honestly this is a really shitty function, but it works somehow, so you shouldn't question it, if you poke around with it it's most probably going to break
		""" sets the text in command output """
		
		if (not resize):
			self.command_out.stdout(arg=arg, tags=tags, justify=justify)

		h = ((self.command_out.font.metrics("linespace")+self.command_out.cget("spacing3"))*len(self.command_out.arg.split("\n")))
		
		if (len(self.command_out.arg.split("\n")) == 1):
			if (self.focus_get() == self.txt and focus): self.txt.focus_set()

		if (len(self.command_out.arg.split("\n")) >= 3):
			self.command_out.focus_set()
			self.command_out.tag_add("command_out_insert_bg", "insert linestart", "insert lineend")
	
		if (len(self.command_out.arg.split("\n")) >= 10):
			# h = (self.font.metrics("linespace")+self.command_out.cget("spacing3")*self.winfo_height()//10)
			h = (self.command_out.font.metrics("linespace")+self.command_out.cget("spacing3")*self.winfo_height()//10)

		# self.command_out.configure(padx=self.command_out.winfo_width()//2-self.command_out.font.measure(self.command_out.arg+" ")//2) # shitty centering
		self.command_out.tkraise(); self.command_out.place(x=0, y=self.winfo_height(), width=self.winfo_width(), height=h, anchor="sw")

		return "break"

	def cmmand(self, arg):
		# gets input from the command_entry widget, checks if there's any actual input or if it's an empty string
		# if it's not an empty string it sends it to the parser class and if it's a valid command defined in the "commands" dictionary
		# and if it's defined it runs the function related to that name
		""" """
		
		command = self.command_entry.get("1.0", "end-1c").split()#turns command into a list of arguments
		
		if (not command): self.command_entry.unplace(); return #if no input/argument were provided hide the command entry widget and break function
		if (command != self.command_entry.input_history[-1]): self.command_entry.input_history.append(command)
		self.parser.parse_argument(command)

		#sets focus back to text widget
		self.txt.see("insert")
		self.command_entry.delete("1.0", "end") #deletes command line input

		#set command history to newest index
		self.command_entry.input_history_index = 0
		self.command_entry.unplace()

	def hide_text_widget(self, arg=None):
		""" I have no idea why this is a separate function """
		self.txt.place_forget()

	def get_rand_temperature(self):
		""" generates a random temperature depending on the current month """
		month = datetime.datetime.now().date().month
		temperature = 0
		if (month == 12 or month <= 2):
			temperature = random.randint(-17, 14)
		elif (month > 2 and month <= 5):
			temperature = random.randint(14, 28)
		elif (month > 5 and month <= 8):
			temperature = random.randint(20, 35)
		elif (month > 8 and month <= 11):
			temperature = random.randint(3, 20)

		return f"{temperature}°C"


	def get_temperature(self):
		""" scrapes the current temperature of Stockholm """
		def temp():
			try:
				url = "https://www.bbc.com/weather/2673730" #link to Stockholm's weather data
				html = requests.get(url).content #gets the html of the url
				x = "("+BeautifulSoup(html, features="html.parser").find("span", class_="wr-value--temperature--c").text+"C)" # looks for the temperature value and puts it in a string "([value and degree sign]C)"
				self.temperature_label.configure(text=x)
			except Exception: #dunno if it won't crash the app if there's no internet connection
				self.temperature_label.configure(text=self.get_rand_temperature())

		threading.Thread(target=temp, daemon=True).start()

	def get_time(self):
		""" gets time and parses to make it look the way I want it to """

		d_time = datetime.datetime.now().time()
		if (int(self.time_label_value.get().split(":")[2]) == d_time.second): return # checks if it's still the same second as the last time the function was executed, not very efficient, but still more efficient than running a bunch of string formatting every few miliseconds
		hour = ""
		minute = ""
		second = ""
		if (d_time.second < 10):
			second = f"0{d_time.second}"
		else:
			second = f"{d_time.second}"

		if (d_time.minute < 10):
			minute = f"0{d_time.minute}:"
		else:
			minute = f"{d_time.minute}:"

		if (d_time.hour < 10):
			hour = f"0{d_time.hour}:"
		else:
			hour = f"{d_time.hour}:"

		time = hour+minute+second
	
		if (d_time.minute % 10 == 0 and d_time.second == 10): #checks if it's time for updating the temperature
			self.get_temperature()

		self.time_label_value.set(time)# return time #updates the time label/widget to show current time


	def update_index(self, arg=None):
		# called upon every keypress
		if (self.txt.index("insert") == self.selection_start_index): self.selection_start_index = None

		self.cursor_index = self.txt.index("insert").split(".") # gets the cursor's position and makes it into a tuple/list [line, column]
		self.line_no.configure(text=f"[{self.txt.index('insert')}]") #updates the line&column widget to show current cursor index/position
		if (self.selection_start_index): # show selection index on the top of the window if a selection is active
			self.line_no.configure(text=f"[{self.selection_start_index}][{self.txt.index('insert')}]")

		self.txt.highlighter.bracket_pair_make(self.txt.get("insert")) # highlights matching brackets
		self.txt.highlighter.bracket_pair_highlight(self.cursor_index[0], self.current_line)

		self.current_line = self.txt.get(f"insert linestart", f"insert lineend+1c") #+1c so the line includes the newline character
		# custom cursor thingy
		# coords = self.txt.bbox("insert")
		# self.curs.place(x=coords[0]-2, y=coords[1]-2, w=1, h=self.txt.font.metrics("linespace"))
		# self.curs.place(x=coords[0]-2, y=coords[1]+self.txt.font.metrics("linespace")-2, w=self.txt.font_size-3, h=1)
		# threading.Thread(target=t, args=(self.cursor_index[0],), deamon=True).start()
		
		if (arg): return "break"

	def update_buffer(self, arg=None):
		""" updates some of the widgets when a character is typed in """
		# called upon every keypress

		if (arg): # shows the characters that were released (eg. Control: D), but it can't handle more than one character (eg. Control: b-w)
			text = re.sub("\|*Mod2", "", re.search("state=[a-zA-Z0-9\|]+", f"{arg}").group()[6:]) # magic with regex to show the keys you pressed in a nicer format
			self.key_label["text"] = f"{text}: {arg.keysym}"
			if (arg.keysym in ("Up", "Down", "Left", "Right")): return # ends function if it was triggered by arrow keys (as they have different functions to handle them)
		
		self.update_index()
		if (self.txt.change_index != len(self.txt.get("1.0", "end"))): # checks if any changes have been made to the text
			self.title(f"Nix: <*{self.txt.name}>")
			self.file_handler.buffer_tab.change_name(extra_char="*")
			self.txt.change_index = len(self.txt.get("1.0", "end"))
			self.txt.typing_index_set() # Alt-N: sets your cursor to the position you were last typing in
			self.txt.lexer.lex() # lex text for variables, functions, structures and class etc.

			# if the following widgets are not focused they are hidden
			if (self.focus_displayof() != self.command_entry):
				self.command_entry.place_forget()
			if (self.focus_displayof() != self.command_out):
				self.command_out.place_forget()

			if (self.suggest): self.txt.highlighter.suggest(self.cursor_index[0], self.current_line)

		self.txt.highlighter.highlight(self.cursor_index[0], self.current_line) # highlight current line

		# this is not very effective and doesn't even work properly
		if (self.txt.terminal_like_cursor):
			try: self.txt.configure(insertbackground=self.theme["highlighter"][self.txt.tag_names("insert")[-2]]) #Checks if there are any tags available on current character and if so it sets the cursor color to that tag 
			except Exception: self.txt.configure(insertbackground=self.theme["window"]["insertbg"])
			self.txt.tag_configure("cursor", foreground=self.theme["window"]["bg"])
			
		elif (not self.txt.terminal_like_cursor and self.txt.cursor_mode == 1):
			self.txt.configure(insertbackground=self.theme["window"]["insertbg"])
			self.txt.tag_configure("cursor", foreground=self.theme["window"]["bg"])

	def update_win(self):
		""" updates the window whole window (all of it's widgets)"""
		self.update()
		self.update_idletasks()

	def main(self):
		""" reconfigures(updates) some of the widgets to have specific values and highlights the current_line"""
		self.txt.focus_set()
		t0 = time.time(); self.c = 0
		def a(): # some annoying notifications
			time.sleep(1650)
			# try:
			self.command_out_set("POSTURE CHECK! You've been programming for half an hour now. Consider stretching for a bit")
				# notify2.init("Nix")
				# notify2.Notification("POSTURE CHECK", "You've been programming for half an hour now. Consider stretching for a bit").show()
			# except Exception:
			# 	self.commmand_out_set("Consider downloading the notify2 module"); return
			time.sleep(1650)
			# try:
			self.command_out_set("You've been programming for an hour now. Consider taking a break")
			# 	notify2.init("Nix")
			# 	notify2.Notification("BREAK TIME", "You've been programming for an hour now. Consider taking a break").show()
			# except Exception:
			# 	self.commmand_out_set("Consider downloading the notify2 module"); return
			a()

		# def b():
			# while (self.run):
				# time.sleep(1)
				# self.get_time()
				# self.fps_label.configure(text=f"<{round(self.c/1000, 2)}KHz>")
				# self.c = 0

		threading.Thread(target=a, daemon=True).start()
		# threading.Thread(target=b, daemon=True).start()
		
		while (self.run):
			self.update_win()
			self.get_time()

			if (int(time.time()-t0) >= 1): # updates the processor frequency value every second
				def a():
					self.fps_label.configure(text=f"<{round(psutil.cpu_freq().current/100*psutil.cpu_percent(), 2)}MHz> <{psutil.sensors_temperatures()['coretemp'][0].current}>")
				threading.Thread(target=a, daemon=True).start()
				t0 = time.time()

	@moving	
	def keep_indent(self, arg=None):
		""" gets the amount of tabs in the last line and puts them at the start of a new one """
		#this functions gets called everytime Enter/Return has been pressed
		self.txt.see(self.convert_line_index("float")+3)
		offset = "\n"
		
		if (match := re.search(r"^\t+", self.current_line)):
			offset += match.group()

		# I am seeing a lot of horrible code in this project
		# sometimes I look back at my code and wonder if I am insane
		# magic with brackets
		# basically automatic indenting
		if (re.match(r"[\:]", self.txt.get("insert-1c"))): 
			self.txt.insert(self.txt.index("insert"), offset+"\t")
			
		elif (re.match(r"[\{\[\(]", self.txt.get("insert-1c"))):
			if (re.match(r"[\}\]\)]", self.txt.get("insert"))):
				self.txt.insert(self.txt.index("insert"), offset+"\t"+offset)
				self.txt.mark_set("insert", f"insert-{len(offset)}c")
			else:
				self.txt.insert(self.txt.index("insert"), offset+"\t")
				
		elif (re.match(r"[\{\[\(]", self.txt.get("insert"))):
			if (re.match(r"[\}\]\)]", self.txt.get("insert+1c"))):
				self.txt.insert(self.txt.index("insert"), offset)
				self.txt.mark_set("insert", "insert+1c")
				self.txt.insert(self.txt.index("insert"), offset+"\t"+offset)
				self.txt.mark_set("insert", f"insert-{len(offset)}c")
			else:
				self.txt.insert(self.txt.index("insert"), offset)
				self.txt.mark_set("insert", f"insert+{len(offset)+2}c")
		
		else:
			if (re.match(r"\t+\n", self.current_line)):
				self.txt.delete(f"{self.cursor_index[0]}.0", "insert") #removes extra tabs if the line is empty
			self.txt.insert(self.txt.index("insert"), offset)
		
		return "break"

	def highlight_chunk(self, arg=None, start_index=None, stop_index=None):
		if (not start_index): start_index = 1
		if (not stop_index): stop_index = self.get_line_count()+1 #+1 becuace for loops don't iterate over the last element or something in that sense
		self.convert_line_index("int", start_index)
		self.convert_line_index("int", stop_index)
		def highlight(text):
			if self.highlighting:
				for i in range(start_index, stop_index+1):
					text.highlighter.highlight(i)
					text.highlighter.lex_line(i)
		threading.Thread(target=highlight, args=(self.txt, ), daemon=True).start()
		
	def unhighlight_chunk(self, arg=None, start_index=None, stop_index=None):
		if (not start_index): start_index = 1
		if (not stop_index): stop_index = self.get_line_count()
		def unhighlight():
			[self.txt.highlighter.unhighlight(i) for i in range(start_index, stop_index+1)]
		threading.Thread(target=unhighlight, daemon=True).start()

if __name__ == "__main__":
	main_win = win()
	main_win.after(0, main_win.main)
	main_win.mainloop()

	print("thank you for using Nix")



