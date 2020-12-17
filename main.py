__author__ = "Bugy"
__license__ = "MIT"
__maintainer__ = "Bugy"
__email__ = ["matejbugy@gmail.com", "achjoj5@gmail.com"]
__status__ = "Production" 
__version__ = "1.1.3"
"""bugajma20"""

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
# from handlers import file_handler, music_player, video_record_start, video_record_stop, screenshot
from handlers import *
from widgets import *


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


class settings_widget(BUFFER):
	def __init__(self, parent):
		self.name = "%NIX_SETTINGS%"
		super().__init__(parent, self.name)

		self.label = tkinter.Label(text="text")

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
			 "highlighter": {"whitespace": "#111111", "keywords": "#A500FF", "logical_keywords": "#ff00bb", "functions": "#3023DD", "upcase_b": "#3055BB","numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			 "retro_cake": {"window": {"bg" : "#000000", "fg": "#CDAB81", "insertbg": "#AAAAAA", "selectbg": "#332233", "selectfg": "#AAAAAA", "widget_fg": "#CDAB81", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A500FF", "logical_keywords": "#ff00bb", "functions": "#3023DD", "upcase_b": "#3055BB","numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			 "nat": {"window": {"bg" : "#070304", "fg": "#AAAAAA", "insertbg": "#005500", "selectbg": "#001500", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A53300", "logical_keywords": "#2090F0", "functions": "#E0AF60", "upcase_b": "#BB5522","numbers": "#BB9900", "operators": "#f75f00", "special_chars": "#00A000", "quotes": "#00DCFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			 "lens": {"window": {"bg" : "#070304", "fg": "#AAAAAA", "insertbg": "#005500", "selectbg": "#001500", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#E4D8B4", "logical_keywords": "#2090F0", "functions": "#83B799", "upcase_b": "#BB5522","numbers": "#E86F68", "operators": "#DE7E44", "special_chars": "#6C566D", "quotes": "#E2CD6D", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			 "tea": {"window": {"bg" : "#070304", "fg": "#AAAAAA", "insertbg": "#005500", "selectbg": "#001500", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A53300", "logical_keywords": "#2090F0", "functions": "#83B799", "upcase_b": "#BB5522","numbers": "#E86F68", "operators": "#f75f00", "special_chars": "#00A000", "quotes": "#E2CD6D", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			"thorfinn": {"window": {"bg" : "#000522", "fg": "#dde2e3", "insertbg": "#6f8ea9", "selectbg": "#120512", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#6f8ea9", "logical_keywords": "#b37c57", "functions": "#60412b", "upcase_b": "#796878", "numbers": "#3f5e89", "operators": "#f75c57", "special_chars": "#9aacb8", "quotes": "#005577", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			"muffin" : {"window": {"bg" : "#CCCCCC", "fg": "#000000", "insertbg": "#111111", "selectbg": "#111111", "selectfg": "#FFFFFF", "widget_fg": "#000000", "select_widget": "#000000", "select_widget_fg": "#FFFFFF"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#00BABA", "functions": "#3023DD", "logical_keywords": "#ff00bb", "upcase_b": "#3055BB", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#74091D", "comments": "#111111", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			"toast" : {"window": {"bg" : "#000000", "fg": "#9F005F", "insertbg": "#FFFFFF", "selectbg": "#555555", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#f70000", "logical_keywords": "#ff00bb", "functions": "#3023DD", "upcase_b": "#3055BB", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "pair_bg": "#990000", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			"student" : {"bg" : "#222222", "fg": "#FFFFFF"}
			}

		self.theme = self.theme_options["tea"]

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

		self.banned_keysyms = ["Up", "Down", "Right", "Left", "Home", "End", "Num_Lock", "Pause", "Scroll_Lock", "Insert", "Next", "Prior", "Caps_Lock", 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'F25', 'F26', 'F27', 'F28', 'F29', 'F30', 'F31', 'F32', 'F33', 'F34', 'F35', 'F36', 'F37', 'F38', 'F39', 'F40', 'F41', 'F42', 'F43', 'F44', 'F45', 'F46', 'F47', 'F48', 'F49', 'F50', 'F51']

		self.command_input_history = []
		self.command_input_history_index = 0

		self.scroll_multiplier = 0

		self.line_count = None

		self.tab_offset = 0
		self.tab_lock = False

		self.selection_start_index = None
		self.queue = []
		self.found = []
		self.found_index = 0
		self.cursor_index = ["1", "0"]
		self.current_line = ""
		self.last_index = "0.0"
		self.text_len = 0
		
		self.highlighting = False #now its turned off by default # turned on by default because it finally works (still, fuck regex (less than before tho))
		self.command_highlighting = False
		
		self.split_mode = 0 # 0 means it's turned off / 1 is for vertically split text buffers / 2 is for horizontally split text buffers

		# self.txt.insert = False
		# self.txt.terminal_like_cursor = True
		# self.txt.insert_offtime = 0; self.txt.insert_ontime = 1

		self.loading = False
		self.fullscreen = False
		self.run = True
		self.sharpness = 1.35

		self.font_size = 11
		self.sfont_size = self.font_size - 2

		#configuring main window
		# self.title_bar = tkinter.Frame(bg="blue", relief='raised', bd=2)

		# self.wm_attributes("-type", "splash")
		self.resizable(True,True)
		self.tk.call("tk","scaling", self.sharpness)
		self.geometry(f"600x400")
		self.wm_minsize(20, 0)
		self.update_win()
		self.geometry(self.winfo_geometry())
		self.title(f"Nix: <None>")
		# self.wm_attributes("-type", "normal")

		self.file_handler = file_handler(self)
		self.video_handler = video_handler(self)
		self.filename = filedialog

		self.init()

	def init(self):
		""" a completely useless initialize function """
		# widget.cget("text")
		self.update_win()
		self.wm_attributes("-alpha", 1)
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
		self.temperature_label = tkinter.Label(text="("+self.get_rand_temperature()+")")
		self.line_no = tkinter.Label()
		self.fps_label = tkinter.Label()
		
		self.find_entry = tkinter.Entry()

		self.find_label = tkinter.Label()

		self.definition_label = tkinter.Label()

		#command line entry
		self.command_entry = tkinter.Text()

		#command output
		self.command_out = tkinter.Label()
		
		#right click pop-up menu
		self.right_click_menu = tkinter.Menu()
		self.right_click_menu.add_command(label="Copy            Control-C", font=self.smaller_font, command=self.copy)
		self.right_click_menu.add_command(label="Paste           Control-V", font=self.smaller_font, command=self.paste)
		self.right_click_menu.add_command(label="Cut             Control-X", font=self.smaller_font, command=self.cut)
		self.right_click_menu.add_command(label="Show definition Control-Q", font=self.smaller_font, command=self.test_function)
		# self.right_click_menu.add_separator()

		#menubar
		self.file_menubar_label = MENUBAR_LABEL(self, "file_menu")
		# self.file_separator_label = tkinter.Label(self, text="----" ,font=self.font, bg=self.theme["bg"], fg="#999999").place(x=0, y=15, height=2, anchor="nw")
		self.file_menubar_label.place(x=2, y=2, height=20, anchor="nw")

		self.settings_menubar_label = MENUBAR_LABEL(self, "settings_menu")
		# self.settings_separator_label = tkinter.Label(self, text="--------" ,font=self.font, bg=self.theme["bg"], fg="#999999").place(x=60, y=15, height=2, anchor="nw")
		self.settings_menubar_label.place(x=60, y=2, height=20, anchor="nw")


		#dropdown for menubar
		self.file_dropdown = tkinter.Menu() #declare dropdown
		self.file_dropdown.add_command(label="New file",command=self.file_handler.new_file) #add commands
		self.file_dropdown.add_command(label="Open file",command=self.file_handler.load_file)
		self.file_dropdown.add_command(label="Save file",command=self.file_handler.save_file)
		self.file_dropdown.add_command(label="Save file as",command=self.file_handler.save_file_as)

		self.txt = None
		self.file_handler.init(".~scratch")

		try:
			self.music_player = music_player(self)
		except Exception:
			pass

		self.command_entry.tag_configure("command_keywords", foreground=self.theme["highlighter"]["command_keywords"])

		#command binding
		# self.command_out.bind("<KeyPress>", lambda arg: self.txt.focus_set())
		self.command_out.bind("<Down>", lambda arg: self.txt.focus_set())

		self.command_entry.bind("<Return>", self.cmmand) #if you press enter in command line it executes the command and switches you back to text widget
		self.command_entry.bind("<Up>", self.command_history) # lets you scroll through commands you have already used
		self.command_entry.bind("<Down>", self.command_history)
		self.command_entry.bind("<Escape>", self.command_entry_unset)
		self.command_entry.bind("<Insert>", self.set_cursor_mode)
	
		self.find_entry.bind("<Return>", self.find)
		self.find_entry.bind("<Up>", self.scroll_through_found)
		self.find_entry.bind("<Down>", self.scroll_through_found)
		self.find_entry.bind("<Escape>", self.find_unplace)

		self.file_menubar_label.bind("<Right>", lambda arg: self.window_select("settings_menu"))
		self.file_menubar_label.bind("<Left>", lambda arg: self.window_select("text"))
		self.settings_menubar_label.bind("<Right>", lambda arg: self.window_select("text"))
		self.settings_menubar_label.bind("<Left>", lambda arg: self.window_select("file_menu"))
	
		# self.txt.bind("<Control-space>", self.command_entry_set)
		self.bindable_widgets = [self.file_menubar_label, self.settings_menubar_label, self.find_entry, self.command_entry, self.command_out]
		for widget in self.bindable_widgets:
			widget.bind("<Control-space>", self.command_entry_set)
			widget.bind("<F11>", self.set_fullscreen)
			widget.bind("<Alt-Right>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Left>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Up>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Down>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Shift-Right>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Left>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Up>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Down>", lambda arg: self.set_dimensions(arg, False))

		self.bind("<Control-Escape>", lambda arg: self.destroy())
		self.bind("<Control-w>", self.win_destroy)
		self.bind("<Control-Shift-W>", self.win_destroy)
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
		for key in self.theme["highlighter"].items():
			if (key[0][-2:] == "bg"): self.txt.tag_configure(key[0], background=key[1], foreground=self.theme["window"]["bg"])
			elif (key[0][-2:] == "_b"): self.txt.tag_configure(key[0][:-2], foreground=key[1], font=self.font_bold)
			else: self.txt.tag_configure(key[0], foreground=key[1])

	def theme_load(self):
		self.theme_make()
		self.configure(bg=self.theme["window"]["bg"])

		self.canvas.configure(bg=self.theme["window"]["bg"], bd=0, highlightthickness=0)

		self.txt.configure(font=self.font,bg = self.theme["window"]["bg"],fg=self.theme["window"]["fg"], undo=True, maxundo=0, spacing1=2,
		insertwidth=0, insertofftime=self.txt.insert_offtime, insertontime=self.txt.insert_ontime, insertbackground="#555",
		selectbackground=self.theme["window"]["selectbg"], selectforeground=self.theme["window"]["selectfg"], borderwidth=1,
		relief="flat", tabs=(f"{self.font.measure(' ' * 4)}"), wrap="word", exportselection=True,
		blockcursor=self.txt.block_cursor, highlightthickness=0, insertborderwidth=0)

		self.time_label.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.temperature_label.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.line_no.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.fps_label.configure(text="<0.0KHz>", fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])

		self.command_entry.configure(blockcursor=self.txt.block_cursor, font=self.smaller_font, bg=self.theme["window"]["bg"], fg="#00AAFF",
		insertwidth=1, insertofftime=0, relief="raised", highlightthickness=0, bd=1, insertbackground=self.theme["window"]["insertbg"],
		selectbackground=self.theme["window"]["selectbg"], highlightbackground="#FFFFFF")

		self.command_out.configure(font=self.smaller_font_bold, bg=self.theme["window"]["bg"], fg="#00df00")
		self.find_entry.configure(font=self.smaller_font_bold, bg=self.theme["window"]["bg"], fg="#00df00", insertbackground=self.theme["window"]["fg"], relief="flat", highlightthickness=0)
		self.find_label.configure(font=self.font, bg=self.theme["window"]["bg"], fg="#00df00")
		self.definition_label.configure(font=self.font, bg=self.theme["window"]["selectfg"], fg="#00df00")
		self.right_click_menu.configure(tearoff=0, font=self.smaller_font, bg=self.theme["window"]["bg"], fg="#ffffff")
		self.file_menubar_label.configure(text="File", font=self.widget_font, bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.settings_menubar_label.configure(text="Settings" ,font=self.widget_font, bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.file_dropdown.configure(font=self.widget_font, tearoff=False,fg="#FFFFFF", bg=self.theme["window"]["bg"], bd=0)

		for buffer_tab in self.file_handler.buffer_tab_list:
			buffer_tab.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"], highlightcolor=self.theme["window"]["widget_fg"])
			buffer_tab.menu.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])

		self.update_win()

	def reposition_widgets(self, arg=None):
		if (self.command_entry.winfo_viewable()): self.command_entry.place(x=-1, y=self.winfo_height(), width=self.winfo_width()+2, height=20, anchor="sw")
		if (self.command_out.winfo_viewable()): self.command_out.place(x=0, y=self.winfo_height(), width=self.winfo_width(), anchor="sw")
		self.time_label.place(x=self.temperature_label.winfo_x()-self.time_label.winfo_width(), y=2, height=20, anchor="nw")
		self.temperature_label.place(x=self.line_no.winfo_x()-self.temperature_label.winfo_width()-10, y=2, height=20, anchor="nw")
		self.line_no.place(x=self.winfo_width()-self.line_no.winfo_width()-10, y=2, height=20, anchor="nw")
		self.fps_label.place(x=self.time_label.winfo_x()-self.fps_label.winfo_width()-10, y=2, height=20, anchor="nw")

		if (self.split_mode == 0): self.txt.place(x=0,y=45, width=self.winfo_width(), height=self.winfo_height()-45, anchor="nw") # self.txt.change_coords([2, 45, self.winfo_width()-2, self.winfo_height()-50])
		elif (self.split_mode == 1): self.txt.place(x=2,y=45, width=self.winfo_width()//2-2, height=self.winfo_height()-50, anchor="nw"); self.txt_1.place(x=self.winfo_width()//2,y=45, width=self.winfo_width()//2-2, height=self.winfo_height()-50, anchor="nw")
		elif (self.split_mode == 2): self.txt.place(x=2,y=45, width=self.winfo_width()-2, height=self.winfo_height()//2-50, anchor="nw"); self.txt_1.place(x=2,y=self.winfo_height()//2, width=self.winfo_width()-2, height=self.winfo_height()//2, anchor="nw")

		self.canvas.create_line(0, 23, self.winfo_width(), 23, fill=self.theme["window"]["fg"], smooth=1)
		self.canvas.create_line(0, 44, self.winfo_width(), 44, fill=self.theme["window"]["fg"], smooth=1)


	def win_destroy(self, arg=None) -> str:
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

	def sort_index(self, index1, index2):
		if (int(index1.split(".")[1]) <= int(index2.split(".")[1])): return (index1, index2)
		else: return (index2, index1)
			
	def del_selection(self):
		try:
			self.selection_get()
		except Exception: # if no text is selected self.selection_get() will throw an error
			self.queue.clear()

		if (self.queue): self.queue[0].sort(); start_index = self.queue[0][0]; stop_index = self.queue[0][1]+1
		else: self.txt.delete(self.selection_start_index, "insert lineend"); return

		for line_no in range(start_index, stop_index):
			self.txt.delete(float(line_no), "insert lineend")

	def queue_make(self, arg=None):
		# There is a better solution for this, but I am lazy and this works, so why bother?
		if (arg): self.queue = []
		try:
			self.selection_get()
		except Exception: #if selection is empty self.selection_get throws an error
			self.selection_start_index = None
		
		if (not self.selection_start_index): self.selection_start_index = self.txt.index(tkinter.INSERT)

	def queue_get(self, arg=None):
		self.queue = [self.convert_line_index("int", self.selection_start_index), self.convert_line_index("int", self.txt.index("insert"))]
		self.queue.sort()
		return self.queue[0], self.queue[1] + 1

	def del_queue(self, arg=None):
		self.selection_start_index = None
		self.queue = []

	def move(self, arg=None):
		key = arg.keysym
		suffix = ["Line", "Char"]
		
		if (arg.state == CONTROL_KEYSYM or arg.state == 20):
			suffix = ["Para", "Word"]

		if (key == "Up"):
			self.txt.event_generate(f"<<Prev{suffix[0]}>>")
			self.queue = []
			self.txt.see(self.convert_line_index("float")-3)

		elif (key == "Down"):
			self.txt.event_generate(f"<<Next{suffix[0]}>>")
			self.queue = []
			self.txt.see(self.convert_line_index("float")+3)

		elif (key == "Left"):
			self.txt.event_generate(f"<<Prev{suffix[1]}>>")
			self.queue = []

		elif (key == "Right"):
			self.txt.event_generate(f"<<Next{suffix[1]}>>")
			self.queue = []

		self.selection_start_index = None


		if (self.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.command_out.place_forget()
		return "break"

	#text manipulation bindings
	def cut(self, arg=None):
		""" Control-X """
		self.txt.event_generate("<<Cut>>")
		return "break"

	def undo(self, arg=None):
		""" Control-Z """
		chunk_size = self.get_line_count()
		self.txt.event_generate("<<Undo>>")
		start_index = self.convert_line_index("int")
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	def redo(self, arg=None):
		""" Control-Y """
		chunk_size = self.get_line_count()
		self.txt.event_generate("<<Redo>>")
		start_index = self.convert_line_index("int")
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	def copy(self, arg=None):
		""" Control-C """
		self.txt.event_generate("<<Copy>>")
		return "break"

	def paste(self, arg=None):
		""" Control-V """
		to_paste = self.clipboard_get()

		if (self.selection_start_index): start_index = self.selection_start_index; self.del_selection()
		else: start_index = self.txt.index(tkinter.INSERT)
		stop_index = float(start_index)+len(to_paste.split("\n"))

		self.txt.insert(start_index, to_paste)
		self.highlight_chunk(start_index=start_index, stop_index=stop_index)

		self.txt.event_generate("<<SelectNone>>"); self.del_queue()
		return "break"

	def select_all(self, arg=None):
		""" Control-A """
		self.txt.event_generate("<<SelectAll>>")
		return "break"

		
	def home(self, arg=None):
		index = ""
		i = 0
		for i, char in enumerate(self.current_line, 0):
			if (not re.match(r"\s", char)): index = f"{self.cursor_index[0]}.{i}"; break
		
		if (self.txt.index(tkinter.INSERT) == index): self.txt.event_generate("<<LineStart>>")
		else: self.txt.mark_set(tkinter.INSERT, index)
		self.txt.event_generate("<<SelectNone>>"); self.del_queue()
		return "break"

	def home_select(self, arg=None):
		index = ""
		i = 0
		self.queue_make()
		for i, char in enumerate(self.current_line, 0):
			if (not re.match(r"\t", char)): index = f"{self.cursor_index[0]}.{i}"; break

		if (self.txt.index(tkinter.INSERT) == index):
			self.txt.event_generate("<<SelectLineStart>>")
		
		elif (self.txt.index(tkinter.INSERT) != index):
			self.txt.event_generate("<<SelectLineStart>>")
			[self.txt.event_generate("<<SelectNextChar>>") for i in range(i)]
		return "break"

	def end(self, arg=None):
		self.txt.event_generate("<<LineEnd>>")
		self.txt.event_generate("<<SelectNone>>"); self.del_queue()
		return "break"

	def end_select(self, arg=None):
		self.queue_make()
		self.txt.event_generate("<<SelectLineEnd>>")
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
			
		elif (self.txt.cursor_mode == 1): #RETARDED BLOCK PROVIDED BY TKINTER
			self.txt.block_cursor = True
			self.txt.terminal_like_cursor = False

		elif (self.txt.cursor_mode == 2): #NORMAL BLOCK
			self.txt.block_cursor = True
			self.txt.terminal_like_cursor = True
		
		else:
			print("congrats, you broke it")
			self.command_out_set("congrats, you broke it")
			self.txt.cursor_mode = 2
			self.txt.block_cursor = True
			self.txt.terminal_like_cursor = True

		self.txt.configure(blockcursor=self.txt.block_cursor)
		return "break"

	def change_case(self, arg=None):
		index_range = [self.selection_start_index, self.txt.index(tkinter.INSERT)]
		queue = self.queue; queue.sort()

		if (int(index_range[0].split(".")[1]) > int(index_range[1].split(".")[1])): #sort the list
			index_range.insert(0, index_range[1])
		
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
		index = self.sort_index(self.txt.index("insert"), self.selection_start_index)
		print(index)
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

		for line_no in range(start_index, stop_index):
			current_line = self.txt.get(float(line_no), "insert lineend+1c")
			for i, current_char in enumerate(current_line, 0):
				try:
					if (self.txt.highlighter.commment_regex.match(current_char+current_line[i+1])):
						if (re.search(r"\s", self.txt.get(f"{line_no}.{i}", f"{line_no}.{i+1+len(self.txt.highlighter.comment_sign)}"))):
							self.txt.delete(f"{line_no}.{i}", f"{line_no}.{i+1+len(self.txt.highlighter.comment_sign)}")
						else:
							self.txt.delete(f"{line_no}.{i}", f"{line_no}.{i+len(self.txt.highlighter.comment_sign)}")
						break

					elif (not self.txt.highlighter.whitespace_regex.match(current_char)):
						self.txt.insert(f"{line_no}.{i}", self.txt.highlighter.comment_sign+" ")
						break
				except IndexError:
					self.txt.insert(f"{line_no}.{i}", self.txt.highlighter.comment_sign+" ")
					break

		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break" # returning "break" prevents system/tkinter to call default bindings

		
	def unindent(self, arg=None):
		""" Checks if the first character in line is \t (tab) and deletes it accordingly """
		start_index, stop_index = self.queue_get()

		for line_no in range(start_index, stop_index):
			if (re.match(r"\t", self.txt.get(f"{line_no}.0", f"{line_no}.1"))):
				self.txt.delete(f"{line_no}.0", f"{line_no}.1")
		
		return "break"

	def indent(self, arg=None):
		""" Tab """
		start_index, stop_index = self.queue_get()
		index = 0
		if (start_index+1 == stop_index): index = self.cursor_index[1]

		for line_no in range(start_index, stop_index):
			self.txt.insert(f"{line_no}.{index}", "\t")

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
		
	def set_font_size(self, arg=None):
		""" Changes font size and reconfigures(updates) widgets accordingly """
		if (arg):
			if (arg.delta > 120 or arg.delta < -120): arg.delta=0 
			if (arg.keysym == "period" or arg.num == 4 or arg.delta > 0):
				self.txt.font_size += 1
				self.txt.sfont_size += 1
			elif (arg.keysym == "comma" or arg.num == 5 or arg.delta < 0):
				self.txt.font_size -= 1
				self.txt.sfont_size -= 1
			
			if (self.txt.font_size <= 0):
				self.txt.font_size = 1
			elif (self.txt.font_size >= 80):
				self.txt.font_size = 80

		self.font = font.Font(family=self.font_family[0], size=self.txt.font_size, weight=self.font_family[1])
		# self.smaller_font = font.Font(family="Ubuntu",size=self.txt.sfont_size, weight="bold")
		self.font_bold = font.Font(family=self.font_family[0], size=self.txt.font_size, weight="bold")
		self.txt.configure(font=self.font, tabs=(f"{self.font.measure(' ' * 4)}"))
		self.theme_make()
		self.command_out_set(f"font size: {self.txt.font_size}")
		return "break" # returning "break" prevents system/tkinter to call default bindings

	def find(self, arg=None, keyword=None):
		"""  """

		if (not keyword): keyword = self.find_entry.get()

		for index in self.found:
			self.txt.tag_remove("found_select_bg", index[0], index[1])
			self.txt.tag_remove("found_bg", index[0], index[1])

		self.found_index = 0
		self.found = []

		start = self.txt.index("1.0")
		end = self.txt.index("end")
		self.txt.mark_set("matchStart", start)
		self.txt.mark_set("matchEnd", start)
		self.txt.mark_set("searchLimit", end)

		count = tkinter.IntVar()
		while True:
			index = self.txt.search(keyword, "matchEnd", "searchLimit", count=count)
			if index == "": break
			if count.get() == 0: break # degenerate pattern which matches zero-lenght strings
			self.txt.mark_set("matchStart", index)
			self.txt.mark_set("matchEnd", f"{index}+{count.get()}c")
			self.found.append([index, self.txt.index(f"{index}+{count.get()}c")])
		
		for index in self.found:
			self.txt.tag_add("found_bg", index[0], index[1])
		
		self.scroll_through_found()

	def scroll_through_found(self, arg=None):
		result_count = len(self.found)
		offset = 0
		if (result_count == 0): self.command_out_set(f"found none"); return

		if (arg):
			self.command_out.place_forget()
			if (arg.keysym == "Up"):
				self.found_index -= 1
				offset = -5
				if (self.found_index < 0):
					self.found_index = result_count-1
					offset = 5

			elif (arg.keysym == "Down"):
				self.found_index += 1
				offset = 5
				if (self.found_index >= result_count):
					self.found_index = 0
					offset = -5

		for index in self.found:
			self.txt.tag_remove("found_select_bg", index[0], index[1])
			
		
		self.txt.mark_set(tkinter.INSERT, self.found[self.found_index][0])
		self.txt.see(float(self.found[self.found_index][0])+offset)
		self.txt.tag_add("found_select_bg", self.found[self.found_index][0], self.found[self.found_index][1])
		
		self.command_out_set(f"{self.found_index+1} out of {result_count} results : {self.found[self.found_index]}", focus=0)

	def find_place(self, arg=None, text=""):
		self.find_entry.place(x=0, y=self.winfo_height()-40, relwidth=0.5, height=20, anchor="nw")
		self.find_entry.insert("1", text)
		# self.find_label.place(relx=0., y=125, anchor="ne")
		self.find_entry.tkraise(); self.find_entry.focus_set()
	
	def find_unplace(self, arg=None):
		for index in self.found:
			self.txt.tag_remove("found_bg", index[0], index[1])
			self.txt.tag_remove("found_select_bg", index[0], index[1])
		
		self.find_entry.delete(0, "end")
		self.find_entry.place_forget()
		self.find_label.place_forget()
		self.txt.focus_set()
		self.found_index = 0
		self.found = []

	def scroll(self, arg, multiplier=1):
		""" scrolls through the text widget MouseWheel && Shift-MouseWheel for speedy scrolling """
		next_index = float(self.txt.index("insert"))
		if (arg.num == 5 or arg.delta < 0):
			self.txt.mark_set("insert", next_index+3*multiplier)

		elif (arg.num == 4 or arg.delta > 0):
			self.txt.mark_set("insert", next_index-3*multiplier)
		
		# hides widgets that could be in the way
		self.txt.focus_set()
		self.txt.see(tkinter.INSERT)
		self.command_out.place_forget()
		self.command_entry.place_forget()

		self.update_index()

	def show_definition(self, arg=None):
		self.definition_label.place(relx=0., y=125, anchor="ne")

	def popup(self, arg=None):
		""" gets x, y position of mouse click and places a menu accordingly """
		self.right_click_menu.tk_popup(arg.x_root+5, arg.y_root)
		
	def file_menu_popup(self, widget):
		""" places a dropdown menu accordingly to menubar option clicked """
		if (widget == "file_menu"): 
			self.file_dropdown.tk_popup(self.file_menubar_label.winfo_rootx(), self.file_menubar_label.winfo_rooty()+self.file_menubar_label.winfo_height())
		
		elif (widget == "settings_menu"):
			self.file_dropdown.tk_popup(self.settings_menubar_label.winfo_rootx(), self.settings_menubar_label.winfo_rooty()+self.settings_menubar_label.winfo_height())

	def command_entry_set(self, arg=None):
		""" Shows command entry widget """
		self.command_entry.place(x=-1, y=self.winfo_height(), width=self.winfo_width()+2, height=20, anchor="sw")
		self.command_out.place_forget()
		self.command_entry.tkraise(); self.command_entry.focus_set()
		return "break"

	def command_entry_unset(self, arg=None):
		""" hides command entry widget 'tis a kinda useless function"""
		self.command_entry.place_forget()
		self.txt.focus_set()
		return "break"

	def command_history(self, arg=None):
		""" scroll through used commands with Up and Down arrows(?) """
		self.command_entry.delete("1.0", "end")
		try:
			if (arg.keysym == "Up"):
				self.command_input_history_index += 1
			else:
				self.command_input_history_index -= 1
			
			if (self.command_input_history_index <= 0):
				self.command_input_history_index = len(self.command_input_history)+1

			elif (self.command_input_history_index > len(self.command_input_history)):
				self.command_input_history_index = len(self.command_input_history)

			last_command = self.command_input_history[-self.command_input_history_index]
			self.command_entry.insert("1.0", last_command)
			l=0
			for x in last_command:
				l += len(x)+1
			self.command_entry.mark_set(tkinter.INSERT, f"1.{l}")
			self.command_entry.see(tkinter.INSERT)


		except IndexError:
			self.command_input_history_index = 0
			self.command_entry.delete("1.0", "end")

		return "break"

	def command_out_set(self, arg=None, focus=True, anchor="sw", justify="l"):
		""" sets the text in command output """
		self.command_out.tkraise(); self.command_out.place(x=0, y=self.winfo_height(), width=self.winfo_width(), anchor="sw")
		self.command_out.configure(text=str(arg), justify=justify, anchor=anchor, wraplength=self.winfo_width())
		if (focus): self.txt.focus_set() # self.command_out.focus_set()


	def cmmand(self, arg):
		""" parses command(case insensitive) from command line and executes it"""
		self.command_input_history_index = 0
		command = self.command_entry.get("1.0", "end-1c").split()#turns command into a list of arguments
		
		if (not command): self.command_entry_unset(); return #if no input/argument were provided hide the command entry widget and break function
		
		#help command
		if (command[0] == "help"):
			try:
				self.command_out_set(f"{self.commands[command[1]]}")
			except IndexError:
				x = ""
				for item in list(self.commands.keys()):
					x += "\n"+item
				self.command_out_set(x)
				
		elif (command[0] == "test"):
			self.txt.event_generate("<<Return>>")

		elif (command[0] == "highlighting"):
			if (command[1] == "on"):
				self.command_out_set("highlighting on")
				self.highlight_chunk()
				self.highlighting = True
			elif (command[1] == "off"):
				self.unhighlight_chunk()
				self.command_out_set("highlighting off")
				self.highlighting = False

		#line/ line and column commands

		elif (re.match(r"[0-9]", command[0][0])):
			self.txt.mark_set(tkinter.INSERT, float(command[0]))
			self.txt.see(float(command[0])+2)
			self.command_out_set(f"moved to: {float(command[0])}")

		elif (re.match(r"^l[0-9]+$|^l[0-9]+.[0-9]+$|^lget$", command[0])):
			for i, pnum in enumerate(command[0][1:], 1):
				if (re.search("[0-9]", pnum)): 
					argument = command[0][i:]
					break
				
				elif (re.search("[a-zA-Z]", pnum)):
					argument = command[0][i:]
					break

			if (re.match(r"[0-9]", argument)):
				self.txt.mark_set(tkinter.INSERT, float(argument))
				self.txt.see(float(argument)+2)
				self.command_out_set(f"moved to: {float(argument)}")

			elif (re.match("get", argument)):
				self.command_out_set(f"total lines: {self.get_line_count()}")

		elif (command[0] == "find"):
			self.find_place(text=command[1])
			self.find(command[1])

		elif (command[0] == "lyrics"):
			def lyr():
				command1 = ""
				for word in command[1:]:
					command1 += "-"+word
				command1 = command1.split(",")
				url = f"http://www.songlyrics.com/{command1[0]}/{command1[1]}-lyrics/" #link to Stockholm's weather data
				html = requests.get(url).content #gets the html of the url
				x = BeautifulSoup(html, features="html.parser").find(id="songLyricsDiv").text
				self.command_out_set(x, anchor="c", justify="c")
			threading.Thread(target=lyr).start()

		elif (command[0] == "temp"):
			self.get_temperature()
			self.txt.focus_set()

		elif (command[0] == "split"):
			if (command[1] == "n"):
				self.txt_1.place_forget()
				self.split_mode = 0
				self.txt_1 = None

			elif (command[1] == "vertical" or command[1] == "v"):
				self.split_mode = 1
				try: self.txt_1 = self.file_handler.buffer_list[self.txt.buffer_index+1][0]
				except IndexError: self.txt_1 = self.file_handler.buffer_list[1][0]
				self.command_out_set("split vertically")

			elif (command[1] == "horizontal" or command[1] == "h"):
				self.split_mode = 2
				try: self.txt_1 = self.file_handler.buffer_list[self.txt.buffer_index+1][0]
				except IndexError: self.txt_1 = self.file_handler.buffer_list[1][0]
				self.command_out_set("split horizontally")

			self.reposition_widgets()

		elif (command[0] == "unsplit"):
			self.txt_1.place_forget()
			self.split_mode = 0
			self.txt_1 = None
			self.reposition_widgets()

		elif (command[0] == "quit" or command[0] == "q"):
			self.run = False
			self.quit()
			# self.destroy()

		elif (command[0] == "sharpness"):
			self.sharpness = command[1]
			self.tk.call("tk", "scaling", command[1])
			self.command_out_set(f"sharpness: {command[1]}")

		elif (command[0] == "alpha" or command[0] == "transparency"):
			if (command[1] == "default"): command[1] = 90
			self.wm_attributes("-alpha", int(command[1])/100)
			self.command_out_set(f"alpha: {command[1]}")

		elif (command[0] == "convert"):
			try:
				if (command[1][:2] == "0x"):
					decimal = int(command[1], 16)
				elif (command[1][:2] == "0b"):
					decimal = int(command[1], 2)
				else:
					decimal = int(command[1], 10)

				self.command_out_set(f"DECIMAL: {decimal}, HEXADECIMAL: {hex(decimal)}, BINARY: {bin(decimal)}")
			except ValueError:
				self.command_out_set("Error: wrong format; please, add prefix (0x | 0b)")

		elif (command[0] == "cap"):
			if (command[1] == "start"):
				self.process = self.video_handler.video_record_start(self)
			
			elif (command[1] == "stop"):
				self.video_handler.video_record_stop(self.process)
				self.command_out_set("screen capture terminated")
		
		elif (command[0] == "screenshot" or command[0] == "printscreen"):
			self.video_handler.screenshot(self)
		
		elif (command[0] == "resize"):
			self.update_win()
			self.geometry(f"{int(command[1])}x{int(command[2])}")
			
		elif (command[0] == "buffers"):
			if (not command[1:]):
				result = ""
				for val in self.file_handler.buffer_list[1:]:
					result += f"<{val[1].name}> "
				if (not result): result = "<None>"
				self.command_out_set("buffers: "+result)
			else:
				self.file_handler.load_buffer(command[1:])

		elif (command[0] == "save"):
			self.file_handler.save_file()
			self.loading = True
		
		elif (command[0] == "saveas"):
			self.file_handler.save_file_as(tmp=command[1])

		elif (command[0] == "open"):
			self.file_handler.load_file(filename="".join(command[1:]))

		elif (command[0] == "del" or command[0] == "rm"):
			self.file_handler.del_file(filename="".join(command[1:]))

		elif (command[0] == "reload"):
			self.file_handler.load_file(filename=self.file_handler.current_file.name)
			
		elif (command[0] == "play"):
			self.music_player.load_song(command[1:])

		elif (command[0] == "pause"):
			self.music_player.pause_song()

		elif (command[0] == "unpause"):
			self.music_player.pause_song(unpause=True)

		elif (command[0] == "stop"):
			self.music_player.stop_song()

		elif (command[0] == "sys"):
			self.txt.run_subprocess(argv=command[1:])

		elif (command[0] == "ls"):
			result = ""
			for i, file in enumerate(os.listdir(self.file_handler.current_dir), 0):
				# if (i % 3 == 0): result += f"{file}\n"
				# else: result += f"{file} | "
				result += file+"\n"
			self.command_out_set(f"{result}")
		
		elif (command[0] == "cd"):
			try:
				os.chdir(command[1])
				self.current_dir = os.getcwd()
				self.command_out_set(arg=f"current directory: {self.file_handler.current_dir}")
			except FileNotFoundError:
				self.command_out_set(arg=f"Error: File/Directory not found")
				
		elif (command[0] == "theme"):
			if (command[1]):
				self.unhighlight_chunk()
				self.theme = self.theme_options[command[1]]
				self.theme_load()
				self.highlight_chunk()
				self.command_out_set(f"theme set to: <{command[1]}>")
			else:
				result = ""
				for key in self.theme_options.keys():
					result += "<"+key+">\n"
				self.command_out_set(result)
		else:
			res = ""
			for c in command:
				res += c+" "
			self.command_out_set(f"Command <{res[:-1]}> not found")

		#append command to command history
		self.command_input_history.append(command)

		#sets focus back to text widget
		# self.txt.focus_set()
		self.txt.see(tkinter.INSERT)
		self.command_entry.delete("1.0", "end") #deletes command line input

		#set command history to newest index
		self.command_input_history_index = 0       
		self.command_entry.place_forget()


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
				self.command_out_set("temperature changed")
			except Exception: #dunno if it won't crash the app if there's no internet connection
				pass

		threading.Thread(target=temp).start()

	def get_time(self):
		""" gets time and parses to make it look the way I want it to """
		d_time = datetime.datetime.now().time()
		time = ""

		if (d_time.hour < 10):
			time += f"0{d_time.hour}:"
		else:
			time += f"{d_time.hour}:"

		if (d_time.minute < 10):
			time += f"0{d_time.minute}:"
		else:
			time += f"{d_time.minute}:"

		if (d_time.second < 10):	
			time += f"0{d_time.second}"
		else:
			time += f"{d_time.second}"

		
		if (d_time.minute % 10 == 0 and d_time.second == 10 and d_time.microsecond >= 51000 and d_time.microsecond <= 52000): #checks if it's time for updating the temperature
			self.get_temperature()

		return time #updates the time label/widget to show current time


	def update_index(self, arg=None):
		if (self.txt.index("insert") == self.selection_start_index): self.selection_start_index = None

		self.cursor_index = self.txt.index(tkinter.INSERT).split(".") # gets the cursor's position
		self.line_no.configure(text=f"[{self.txt.index(tkinter.INSERT)}]") #updates the line&column widget to show current cursor index/position
		if (self.selection_start_index):
			self.line_no.configure(text=f"[{self.selection_start_index}][{self.txt.index(tkinter.INSERT)}]")

		self.txt.highlighter.bracket_pair_make(self.txt.get("insert"))
		self.txt.highlighter.bracket_pair_highlight(self.cursor_index[0], self.current_line)

		self.current_line = self.txt.get(f"insert linestart", f"insert lineend+1c")
		
		if (arg): return "break"

	def update_buffer(self, arg=None):
		""" updates some of the widgets when a character is typed in """
		#and arg.keysym not in self.banned_keysyms
		if (self.file_handler.current_file_name and self.txt.change_index != self.txt.index("end")): #if statement to prevent an error because there is no file at the start of the app other && if a new character has been typed in put an asterisk to the title to show that the file hasn't been updated yet
			self.title(f"Nix: <*{self.txt.name}>")
			self.file_handler.buffer_tab.change_name(extra_char="*")
			self.txt.change_index = self.txt.index("end")

			if (self.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.txt.see(tkinter.INSERT)

			if (self.focus_displayof() != self.command_entry): #if the user is not using the command entry widget and a character has been typed into the text widget: hide the command enter widget
				self.command_entry.place_forget()

			if (self.focus_displayof() != self.command_out): #if the a character has been typed into the text widget: hide the command output widget
				self.command_out.place_forget()
				
			if (self.focus_displayof() != self.find_entry): #if the a character has been typed into the text widget: hide the command output widget
				self.find_unplace()

		self.update_index()

		if (self.highlighting): # if the highlighting option is on then turn on highlighting :D
			self.txt.highlighter.highlight(self.cursor_index[0], line=self.current_line)

		if (self.txt.terminal_like_cursor): #not so horrible anymore
			try: self.txt.configure(insertbackground=self.theme["highlighter"][self.txt.tag_names("insert")[-2]]) #Checks if there are any tags available 
			except Exception: self.txt.configure(insertbackground=self.theme["window"]["insertbg"])

			self.txt.tag_configure("cursor", foreground=self.theme["window"]["bg"])

	def update_win(self):
		""" updates the window whole window (all of it's widgets)"""
		self.update()
		self.update_idletasks()

	def main(self):
		""" reconfigures(updates) some of the widgets to have specific values and highlights the current_line"""
		t0 = time.time(); c = 0

		while (self.run):
			self.update_win()

			self.time_label.config(text=self.get_time())

			if (self.focus_displayof() == self.command_entry):
				self.txt.highlighter.command_highlight()

			# self.txt.tag_remove("cursor", "insert-1c linestart", "insert lineend+2c")
			self.txt.tag_remove("cursor", "1.0", "end")
			self.txt.tag_add("cursor", self.txt.index("insert"))
			
			c += 1

			if (int(time.time()-t0) >= 1): # I guess this is supposed to count elapsed cycles
				self.fps_label.configure(text=f"<{round(c/1000, 2)}KHz>")
				t0 = time.time()
				c = 0

			
	def keep_indent(self, arg=None):
		""" gets the amount of tabs in the last line and puts them at the start of a new one """
		#this functions gets called everytime Enter/Return has been pressed
		self.del_queue()
		offset = "\n"
		
		if (match := re.search(r"^\t+", self.current_line)):
			offset += match.group()

		# I am seeing a lot of horrible code in this project
		# magic with brackets
		if (re.match(r"[\:]", self.txt.get("insert-1c"))): 
			self.txt.insert(self.txt.index(tkinter.INSERT), offset+"\t")
		elif (re.match(r"[\{\[\(]", self.txt.get("insert-1c"))):
			if (re.match(r"[\}\]\)]", self.txt.get("insert"))):
				self.txt.insert(self.txt.index(tkinter.INSERT), offset+"\t"+offset)
				self.txt.mark_set(tkinter.INSERT, f"insert-{len(offset)}c")
			else:
				self.txt.insert(self.txt.index(tkinter.INSERT), offset+"\t")
		elif (re.match(r"[\{\[\(]", self.txt.get("insert"))):
			if (re.match(r"[\}\]\)]", self.txt.get("insert+1c"))):
				self.txt.insert(self.txt.index(tkinter.INSERT), offset)
				self.txt.mark_set("insert", "insert+1c")
				self.txt.insert(self.txt.index(tkinter.INSERT), offset+"\t"+offset)
				self.txt.mark_set(tkinter.INSERT, f"insert-{len(offset)}c")
			else:
				self.txt.insert(self.txt.index(tkinter.INSERT), offset)
				self.txt.mark_set(tkinter.INSERT, f"insert+{len(offset)+2}c")
		else:
			if (re.match(r"\t+\n", self.current_line)):
				self.txt.delete(f"{self.cursor_index[0]}.0", "insert") #removes extra tabs if the line is empty
			self.txt.insert(self.txt.index(tkinter.INSERT), offset)

		return "break"


	def highlight_chunk(self, arg=None, start_index=None, stop_index=None):
		if (not start_index): start_index = 1
		if (not stop_index): stop_index = self.get_line_count()+1 #+1 becuace for loops don't iterate over the last element or something in that sense
		self.convert_line_index("int", start_index)
		self.convert_line_index("int", stop_index)
		def highlight(text):
			# t0 = time.time() # timer gets current time in miliseconds
			if self.highlighting:
				[text.highlighter.highlight(i) for i in range(start_index, stop_index+1)] 
				# self.bracket_pair_make()
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

	def note_mode(self):
		# I wanna do some latex level with this piece of shit
		self.highlighting = False

	def retro_mode(self):
		# ehh... nah
		pass



main_win = win()

if __name__ == '__main__':
	main_win.after(0, main_win.main)
	main_win.mainloop()
	







