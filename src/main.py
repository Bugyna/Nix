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
import os, sys

import requests
from bs4 import BeautifulSoup

import random
import threading

from highlighter import highlighter
from handlers import *
from widgets import *

try: import notify2
except Exception: print("consider downloading the notify2 module")

try:
	import platform, ctypes

	if int(platform.release()) >= 8:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)

	CONTROL_KEYSYM = 262156
	WINDOW_MARGIN = 0
except Exception:
	CONTROL_KEYSYM = None
	WINDOW_MARGIN = 24


# class settings_win(tkinter.Tk):
# 	def __init__(self):
# 		super().__init__()
# 		self.font_size = 11
# 		self.sfont_size = self.font_size - 2

# 		self.wm_attributes("-type", "splash")
# 		self.resizable(True,True)
# 		self.tk.call("tk","scaling", self.sharpness)
# 		self.geometry(f"600x400")
# 		self.wm_minsize(20, 0)
# 		self.update_win()
# 		self.geometry(self.winfo_geometry())
# 		self.title(f"Nix: Settings")

# class settings_widget(BUFFER):
# 	def __init__(self, parent):
# 		self.name = "%NIX_SETTINGS%"
# 		super().__init__(parent, self.name)

# 		self.label = tkinter.Label(text="text")

class win(tkinter.Tk):
	""" main object of Nix text editor"""
	def __init__(self, file=None):
		super().__init__()
		# "cake": {"window": {"bg" : "#000000", "fg": "#AAAAAA", "insertbg": "#AAAAAA", "selectbg": "#555555", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
		# 	 "highlighter": {"whitespace": "#111111", "keywords": "#A500FF", "logical_keywords": "#ff00bb", "functions": "#3023DD", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},
		# with open("/home/bugy/projs/neditor/config.nix", "r") as config:
		# 	self.theme_options = json.load(config)["themes"]

		#sick fucking colors #A500FF; #FF103A
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

			"thorfinn": {"window": {"bg" : "#000522", "fg": "#dde2e3", "insertbg": "#6f8ea9", "selectbg": "#120512", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#6f8ea9", "logical_keywords": "#b37c57", "functions": "#60412b", "upcase_b": "#796878", "numbers": "#3f5e89", "operators": "#f75c57", "special_chars": "#9aacb8", "quotes": "#005577", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#4F6CA5", "command_out_insert_bg": "#6f8ea9"}},

			"muffin" : {"window": {"bg" : "#CCCCCC", "fg": "#000000", "insertbg": "#111111", "selectbg": "#111111", "selectfg": "#FFFFFF", "widget_fg": "#000000", "select_widget": "#000000", "select_widget_fg": "#FFFFFF"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#00BABA", "functions": "#3023DD", "logical_keywords": "#ff00bb", "upcase_b": "#3055BB", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#74091D", "comments": "#111111", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#000000", "command_out_insert_bg": "#111111"}},

			"toast" : {"window": {"bg" : "#000000", "fg": "#9F005F", "insertbg": "#FFFFFF", "selectbg": "#555555", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#f70000", "logical_keywords": "#ff00bb", "functions": "#3023DD", "upcase_b": "#3055BB", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#555555", "command_out_insert_bg": "#FFFFFF"}},

			 "custom": {"window": {"bg" : "#070304", "fg": "#AAAAAA", "insertbg": "#005500", "selectbg": "#001500", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords_b": "#A53300", "logical_keywords": "#2090F0", "functions": "#83B799", "upcase_b": "#BB5522","numbers": "#E86F68", "operators": "#f75f00", "special_chars_b": "#00A000", "quotes": "#E2CD6D", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000",  "found_bg": "#145226", "found_select_bg": "#FFFFFF", "command_out_select_bg": "#113311", "command_out_insert_bg": "#005500"}},
			}

		self.theme = self.theme_options["custom"]

		# self.command_keywords = ["l", "lget", "highlighting", "q", "quit", "temp", "sharpness", "alpha", "convert", "save", "saveas", "open", "find", "theme"]
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

		self.backup_files = True
				
		self.highlighting = False #now its turned off by default # turned on by default because it finally works (still, fuck regex (less than before tho))
		self.command_highlighting = False
		self.fullscreen = False
		self.split_mode = 0 # 0 means it's turned off / 1 is for vertically split text buffers / 2 is for horizontally split text buffers

		self.suggest = True
		
		self.run = True
		self.sharpness = 1.35

		self.font_size = 11
		self.sfont_size = self.font_size - 2
		
		#configuring main window
		# self.wm_attributes("-type", "splash")
		self.resizable(True,True)
		self.tk.call("tk","scaling", self.sharpness)
		self.geometry(f"800x600")
		self.wm_minsize(20, 0)
		self.update_win()
		print("vrootwidth: ", self.winfo_x()//4)
		self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_x()+self.winfo_x()//3}+{(self.winfo_screenheight()-self.winfo_height())//2}") #CENTERING MAGIC
		self.wm_attributes("-type", "normal")
		
		# try: self.iconbitmap("icon.ico")
		# except Exception as e: print(e)
		try: self.tk.call('wm', 'iconphoto', self._w, tkinter.PhotoImage(file="icon.png"))
		except Exception as e: print(e)

		self.tk.call("wm", "title", self._w, "Nix")
		
		self.parser = PARSER(self)
		self.file_handler = FILE_HANDLER(self)
		self.video_handler = VIDEO_HANDLER(self)

		self.init()

	def init(self):
		""" a completely useless initialize function """
		self.update_win()
		# self.wm_attributes("-alpha", 1)
		self.canvas = tkinter.Canvas()
		self.canvas.place(x=0, y=0, relwidth=1, height=45)
		
		# self.font_family = ["Px437 IBM CGA", "normal", "bold", "roman"]
		self.font_family = ["Consolas", "normal", "bold", "roman"]
		self.font = font.Font(family=self.font_family[0], size=self.font_size, weight=self.font_family[1], slant=self.font_family[3])
		self.font_bold = font.Font(family=self.font_family[0], size=self.font_size, weight="bold", slant=self.font_family[3]) 
		self.smaller_font = font.Font(family=self.font_family[0],size=self.sfont_size, weight=self.font_family[1])
		self.smaller_font_bold = font.Font(family=self.font_family[0],size=self.sfont_size, weight="bold")
		self.widget_font = font.Font(family=self.font_family[0], size=self.font_size, weight=self.font_family[2])

		self.time_label = tkinter.Label()
		self.time_label_value = tkinter.StringVar()
		self.time_label_value.set("0:0:0")
		self.temperature_label = tkinter.Label(text="("+self.get_rand_temperature()+")")
		self.line_no = tkinter.Label()
		self.fps_label = tkinter.Label()


		# see widgets.py
		self.find_entry = FIND_ENTRY(self)
		self.command_entry = COMMAND_ENTRY(self)
		self.command_out = COMMAND_OUT(self)
		
		#right click pop-up menu
		# self.right_click_menu = tkinter.Menu()
		# self.right_click_menu.add_command(label="Copy             Control-C", font=self.smaller_font, command=self.copy)
		# self.right_click_menu.add_command(label="Paste            Control-V", font=self.smaller_font, command=self.paste)
		# self.right_click_menu.add_command(label="Cut              Control-X", font=self.smaller_font, command=self.cut)
		# self.right_click_menu.add_command(label="Comment          Control-/", font=self.smaller_font, command=self.comment_line)
		# self.right_click_menu.add_command(label="Show definition  Control-Q", font=self.smaller_font, command=self.test_function)
		# self.right_click_menu.add_separator()

		#menubar
		self.file_menubar_label = MENUBAR_LABEL(self, "file_menu")
		self.file_menubar_label.place(x=2, y=2, height=20, anchor="nw")

		self.settings_menubar_label = MENUBAR_LABEL(self, "settings_menu")
		self.settings_menubar_label.place(x=60, y=2, height=20, anchor="nw")


		#dropdown for menubar
		self.file_dropdown = tkinter.Menu()
		self.file_dropdown.add_command(label="New file",command=self.file_handler.new_file)
		self.file_dropdown.add_command(label="Open file",command=self.file_handler.load_file)
		self.file_dropdown.add_command(label="Save file",command=self.file_handler.save_file)
		self.file_dropdown.add_command(label="Save file as",command=self.file_handler.save_file_as)

		self.txt = None #file_handler.init functions uses this txt variable so if it's not declared before running the function it's going to break 
		#BASICALLY
		self.file_handler.init(".~scratch") #see handlers.py/FILE_HANDLER

		try:
			self.music_player = music_player(self)
		except Exception:
			pass

		self.command_entry.tag_configure("command_keywords", foreground=self.theme["highlighter"]["command_keywords"])

		self.file_menubar_label.bind("<Right>", lambda arg: self.window_select("settings_menu"))
		self.file_menubar_label.bind("<Left>", lambda arg: self.window_select("text"))
		self.settings_menubar_label.bind("<Right>", lambda arg: self.window_select("text"))
		self.settings_menubar_label.bind("<Left>", lambda arg: self.window_select("file_menu"))
	
		# self.txt.bind("<Control-space>", self.command_entry_set)
		self.bindable_widgets = [self.file_menubar_label, self.settings_menubar_label, self.find_entry, self.command_entry, self.command_out]
		for widget in self.bindable_widgets:
			widget.bind("<Control-space>", self.command_entry_place)
			widget.bind("<Control-Shift-space>", lambda arg: self.command_out_set(resize=True))
			widget.bind("<F11>", self.set_fullscreen)
			widget.bind("<Alt-Right>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Left>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Up>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Down>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Shift-Right>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Left>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Up>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Down>", lambda arg: self.set_dimensions(arg, False))

		self.bind("<Control-Escape>", self.win_destroy)
		self.bind("<Configure>", self.reposition_widgets) #repositions the text widget to be placed correctly

		self.theme_load()
		self.update_buffer()

		if (len(sys.argv) > 1): [self.file_handler.load_file(filename=arg) for arg in sys.argv[1:]]

	def test_function(self, arg=None):		
		f = f"self.command_out_set(arg={self.selection_get()}.__doc__)"
		try:
			exec(f)
		except Exception:
			self.command_out_set(arg="None")
		return "break"

	def theme_make(self):
		if (type(self.txt) != TEXT): return
		for key in self.theme["highlighter"].items():
			if (key[0][-2:] == "bg"):
				self.txt.tag_configure(key[0], background=key[1], foreground=self.theme["window"]["bg"])
				self.command_out.tag_configure(key[0], background=key[1], foreground=self.theme["window"]["bg"])
				
			elif (key[0][-2:] == "_b"):
				self.txt.tag_configure(key[0][:-2], foreground=key[1], font=self.txt.font_bold)
				self.command_out.tag_configure(key[0][:-2], foreground=key[1], font=self.command_out.font)
				
			else:
				self.txt.tag_configure(key[0], foreground=key[1]); self.command_out.tag_configure(key[0], foreground=key[1])

	def theme_set(self, theme=None):
		if (type(theme) == list): theme = theme[-1] #failsave switch
		self.theme = self.theme_options[theme]
		self.theme_load()
		self.highlight_chunk()

	def theme_load(self):
		self.theme_make()
		self.configure(bg=self.theme["window"]["bg"], cursor=None)

		self.canvas.configure(bg=self.theme["window"]["bg"], bd=0, highlightthickness=0)

		self.txt.configure_self()

		self.time_label.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, textvariable=self.time_label_value,
		 bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.temperature_label.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.line_no.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.fps_label.configure(text="<0.0KHz>", fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])

		self.command_entry.configure_self()
		self.find_entry.configure_self()
		self.command_out.configure_self()
		
		# self.right_click_menu.configure(tearoff=0, font=self.smaller_font, bg=self.theme["window"]["bg"], fg="#ffffff")
		self.file_menubar_label.configure(text="File", font=self.widget_font, bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.settings_menubar_label.configure(text="Settings" ,font=self.widget_font, bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.file_dropdown.configure(font=self.widget_font, tearoff=False,fg="#FFFFFF", bg=self.theme["window"]["bg"], bd=0)

		for buffer_tab in self.file_handler.buffer_tab_list:
			buffer_tab.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"], highlightcolor=self.theme["window"]["widget_fg"])
			buffer_tab.menu.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])

		if (self.file_handler.buffer_tab): self.file_handler.buffer_tab.focus_highlight()

		self.update_win()

	def reposition_widgets(self, arg=None):
		if (self.command_entry.winfo_viewable()): self.command_entry.place(x=-1, y=self.winfo_height(), width=self.winfo_width()+2, height=20, anchor="sw")
		if (self.command_out.winfo_viewable()): self.command_out_set(resize=True) # self.command_out.place(x=0, y=self.winfo_height(), width=self.winfo_width(), anchor="sw")
		self.time_label.place(x=self.temperature_label.winfo_x()-self.time_label.winfo_width(), y=2, height=20, anchor="nw")
		self.temperature_label.place(x=self.line_no.winfo_x()-self.temperature_label.winfo_width()-10, y=2, height=20, anchor="nw")
		self.line_no.place(x=self.winfo_width()-self.line_no.winfo_width()-10, y=2, height=20, anchor="nw")
		self.fps_label.place(x=self.time_label.winfo_x()-self.fps_label.winfo_width()-10, y=2, height=20, anchor="nw")

		if (self.split_mode == 0): self.txt.place(x=0,y=45, width=self.winfo_width(), height=self.winfo_height()-45, anchor="nw") # self.txt.change_coords([2, 45, self.winfo_width()-2, self.winfo_height()-50])
		elif (self.split_mode == 1): self.txt.place(x=2,y=45, width=self.winfo_width()//2-2, height=self.winfo_height()-50, anchor="nw"); self.txt_1.place(x=self.winfo_width()//2,y=45, width=self.winfo_width()//2-2, height=self.winfo_height()-50, anchor="nw")
		elif (self.split_mode == 2): self.txt.place(x=2,y=45, width=self.winfo_width()-2, height=self.winfo_height()//2-50, anchor="nw"); self.txt_1.place(x=2,y=self.winfo_height()//2, width=self.winfo_width()-2, height=self.winfo_height()//2, anchor="nw")

		self.canvas.create_line(0, 23, self.winfo_width(), 23, fill=self.theme["window"]["fg"], smooth=1)
		self.canvas.create_line(0, 44, self.winfo_width(), 44, fill=self.theme["window"]["fg"], smooth=1)


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
		self.run = False
		self.quit()
		self.destroy()
		return "break"

	def convert_line_index(self, type: str, index=None) -> (int, float):
		""" gets the cursor's position """
		if (not index): index = self.cursor_index[0]
		if (type == "int"): return int(float(index))
		elif (type == "float"): return float(index)

	def get_line_count(self, arg=None):
		""" returns total amount of lines in opened text """
		return sum(1 for line in self.txt.get("1.0", "end").split("\n"))

	def get_selection_count(self, arg=None):
		self.command_out_set(f"len: {len(self.selection_get())}")
		return "break"

	def index_sort(self, index1, index2):
		if (int(index1.split(".")[1]) <= int(index2.split(".")[1])): return (index1, index2)
		else: return (index2, index1)
			
	def del_selection(self):
		start_index, stop_index = self.queue_get()

		for line_no in range(start_index, stop_index):
			self.txt.delete(f"{line_no}.0", f"{line_no} lineend")

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
	def move(self, arg=None, prefix=""):
		key = arg.keysym
		suffix = ["Line", "Char"]
		
		if (arg.state == CONTROL_KEYSYM or arg.state == 20 or arg.state == 21):
			suffix = ["Para", "Word"]

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

		# if (self.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.command_out.place_forget()

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

		if (self.selection_start_index): start_index = self.selection_start_index; self.del_selection()
		else: start_index = self.txt.index("insert")
		stop_index = float(start_index)+len(to_paste.split("\n"))

		self.txt.insert(start_index, to_paste)
		self.highlight_chunk(start_index=start_index, stop_index=stop_index)

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
		self.txt.mark_unset(self.txt.mark_names()[-1])
		self.update_buffer()
		return "break"

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

		index_range = self.index_sort(*index_range)
		
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
		index = self.index_sort(self.txt.index("insert"), self.selection_start_index)

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

		self.command_out_set(f"{start_index, stop_index}")
		comment_len = len(self.txt.highlighter.comment_sign)

		for line_no in range(start_index, stop_index):
			current_line = self.txt.get(float(line_no), f"{line_no}.0 lineend+1c")
			if (len(current_line) <= 1): continue
			
			for i, current_char in enumerate(current_line, 0):
				if (self.txt.highlighter.commment_regex.match(current_char+current_line[i+1])):
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

	def find_place(self, arg=None, text=""):
		self.find_entry.place(x=0, y=self.winfo_height()-40, relwidth=0.5, height=20, anchor="nw")
		self.find_entry.insert("1.0", "?"+text)
		self.find_entry.tkraise(); self.find_entry.focus_set()

	def nt_place(self, arg=None):
		self.file_handler.ls()

	@moving
	def scroll(self, arg, multiplier=1):
		""" scrolls through the text widget MouseWheel && Shift-MouseWheel for speedy scrolling """
		next_index = float(self.txt.index("insert"))
		if (arg.num == 5 or arg.delta < 0):
			self.txt.mark_set("insert", next_index+3*multiplier)
	
		elif (arg.num == 4 or arg.delta > 0):
			self.txt.mark_set("insert", next_index-3*multiplier)
		
		# hides widgets that could be in the way
		self.txt.focus_set()
		self.txt.see("insert")
		self.command_out.place_forget()
		self.command_entry.place_forget()

		self.update_index()

	def popup(self, arg=None):
		""" gets x, y position of mouse click and places a menu accordingly """
		self.right_click_menu.tk_popup(arg.x_root+5, arg.y_root)
		
	def file_menu_popup(self, widget):
		""" places a dropdown menu accordingly to menubar option clicked """
		if (widget == "file_menu"): 
			self.file_dropdown.tk_popup(self.file_menubar_label.winfo_rootx(), self.file_menubar_label.winfo_rooty()+self.file_menubar_label.winfo_height())
		
		elif (widget == "settings_menu"):
			self.file_dropdown.tk_popup(self.settings_menubar_label.winfo_rootx(), self.settings_menubar_label.winfo_rooty()+self.settings_menubar_label.winfo_height())

	def command_entry_place(self, arg=None):
		""" Shows command entry widget """
		self.command_entry.place(x=-1, y=self.winfo_height(), width=self.winfo_width()+2, height=20, anchor="sw")
		self.command_out.place_forget()
		self.command_entry.tkraise(); self.command_entry.focus_set()
			
		return "break"

	def command_out_set(self, arg=None, tags=None, resize=False, focus=True, justify="left"):
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
				x = "("+BeautifulSoup(html, features="html.parser").find("span", class_="wr-value--temperature--c").text+"C)"
				self.temperature_label.configure(text=x) #returns the scraped temperature
				# self.command_out_set("temperature changed")
			except Exception: #dunno if it won't crash the app if there's no internet connection
				pass

		threading.Thread(target=temp).start()

	def get_time(self):
		""" gets time and parses to make it look the way I want it to """

		d_time = datetime.datetime.now().time()
		if (int(self.time_label_value.get().split(":")[2]) == d_time.second): return
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
	
		if (d_time.minute % 10 == 0 and d_time.second == 10 and d_time.microsecond >= 51000 and d_time.microsecond <= 52000): #checks if it's time for updating the temperature
			self.get_temperature()

		self.time_label_value.set(time)# return time #updates the time label/widget to show current time


	def update_index(self, arg=None):
		def t(line_no):
			time.sleep(0.5)
			if (self.cursor_index[0] == line_no):
				if (self.txt.font.measure(self.current_line) >= self.txt.winfo_width()):
					self.txt.configure(wrap="word")
				else:
					self.txt.configure(wrap="none")

				self.txt.see("insert")
					
		if (self.txt.index("insert") == self.selection_start_index): self.selection_start_index = None

		self.cursor_index = self.txt.index("insert").split(".") # gets the cursor's position
		self.line_no.configure(text=f"[{self.txt.index('insert')}]") #updates the line&column widget to show current cursor index/position
		if (self.selection_start_index):
			self.line_no.configure(text=f"[{self.selection_start_index}][{self.txt.index('insert')}]")

		self.txt.highlighter.bracket_pair_make(self.txt.get("insert"))
		self.txt.highlighter.bracket_pair_highlight(self.cursor_index[0], self.current_line)

		self.current_line = self.txt.get(f"insert linestart", f"insert lineend+1c") #+1c so the line includes the newline character
		# threading.Thread(target=t, args=(self.cursor_index[0],)).start()
		
		if (arg): return "break"

	def update_buffer(self, arg=None):
		""" updates some of the widgets when a character is typed in """
		#and arg.keysym not in self.banned_keysyms
		self.update_index()
		if (self.file_handler.current_file_name and self.txt.change_index != len(self.txt.get("1.0", "end"))): #if statement to prevent an error because there is no file at the start of the app other && if a new character has been typed in put an asterisk to the title to show that the file hasn't been updated yet
			self.title(f"Nix: <*{self.txt.name}>")
			self.file_handler.buffer_tab.change_name(extra_char="*")
			self.txt.change_index = len(self.txt.get("1.0", "end"))
			self.txt.highlighter.lex_line(self.cursor_index[0], self.current_line)

			if (self.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.txt.see("insert")

			# if the following widgets are not focused they are hidden
			if (self.focus_displayof() != self.command_entry):
				self.command_entry.place_forget()

			if (self.focus_displayof() != self.command_out):
				self.command_out.place_forget()

			if (self.suggest): self.txt.highlighter.suggest(self.cursor_index[0], self.current_line)

		self.txt.highlighter.highlight(self.cursor_index[0], self.current_line)

		if (self.txt.terminal_like_cursor): #not so horrible anymore
			try: self.txt.configure(insertbackground=self.theme["highlighter"][self.txt.tag_names("insert")[-2]]) #Checks if there are any tags available 
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
		def a():
			time.sleep(1650)
			try:
				self.command_out_set("POSTURE CHECK! You've been programming for half an hour now. Consider stretching for a bit")
				notify2.init("Nix")
				notify2.Notification("POSTURE CHECK", "You've been programming for half an hour now. Consider stretching for a bit").show()
			except Exception:
				self.commmand_out_set("Consider downloading the notify2 module"); return
			time.sleep(1650)
			try:
				self.command_out_set("You've been programming for an hour now. Consider taking a break")
				notify2.init("Nix")
				notify2.Notification("BREAK TIME", "You've been programming for an hour now. Consider taking a break").show()
			except Exception:
				self.commmand_out_set("Consider downloading the notify2 module"); return
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

			self.c += 1
			if (int(time.time()-t0) >= 1): # I guess this is supposed to count elapsed cycles
				self.fps_label.configure(text=f"<{round(self.c/1000, 2)}KHz>")
				t0 = time.time()
				self.c = 0

	@moving	
	def keep_indent(self, arg=None):
		""" gets the amount of tabs in the last line and puts them at the start of a new one """
		#this functions gets called everytime Enter/Return has been pressed
		self.txt.see(self.convert_line_index("float")+3)
		offset = "\n"
		
		if (match := re.search(r"^\t+", self.current_line)):
			offset += match.group()

		# I am seeing a lot of horrible code in this project
		# magic with brackets
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
			# t0 = time.time() # timer gets current time in miliseconds
			if self.highlighting:
				for i in range(start_index, stop_index+1):
					text.highlighter.highlight(i)
					text.highlighter.lex_line(i)
					
			# t1 = time.time() # timer gets current time in miliseconds
			# print(t1-t0)

		threading.Thread(target=highlight, args=(self.txt, )).start()
		
	def bracket_pair_make(self, arg=None):
		def pair_make():
			self.txt.highlighter.bracket_pair_make()
		threading.Thread(target=pair_make).start()
		
	def unhighlight_chunk(self, arg=None, start_index=None, stop_index=None):
		if (not start_index): start_index = 1
		if (not stop_index): stop_index = self.get_line_count()
		def unhighlight():
			[self.txt.highlighter.unhighlight(i) for i in range(start_index, stop_index+1)] #+1 becuace for loops don't iterate over the last element or something in that sense

		threading.Thread(target=unhighlight).start()

if __name__ == "__main__":
	main_win = win()
	main_win.after(0, main_win.main)
	main_win.mainloop()



