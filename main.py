__author__ = "Bugy"
__license__ = "MIT"
__maintainer__ = "Bugy"
__email__ = ["matejbugy@gmail.com", "achjoj5@gmail.com"]
__status__ = "Production"
"""bugajma20"""

x = 55555555555
xx = 0x5000000000
xxx = 0b100000000


import tkinter
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

import re
import inspect

import subprocess
import os, sys
from datetime import datetime
from time import sleep, time, localtime, strftime

# import lyricwikia
import requests
from bs4 import BeautifulSoup

import random
import threading

from highlighter import highlighter
from handlers import file_handler

try:
	import platform, ctypes

	if int(platform.release()) >= 8:
		ctypes.windll.shcore.SetProcessDpiAwareness(True)

	CONTROL_KEYSYM = 262156
except Exception:
	CONTROL_KEYSYM = None


class win(tkinter.Tk):
	""" main object of Nix text editor"""
	def __init__(self, file=None):
		super().__init__()
		self.theme_options = {
			"cake": {"window": {"bg" : "#000000", "fg": "#AAAAAA", "insertbg": "#AAAAAA", "selectbg": "#555555", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A500FF", "logical_keywords": "#ff00bb", "functions": "#3023DD", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			"timelord": {"window": {"bg" : "#000099", "fg": "#AAAAAA", "insertbg": "#FFFFFF", "selectbg": "#555555", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#A500FF", "logical_keywords": "#ff00bb", "functions": "#3023DD", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},


			"muffin" : {"window": {"bg" : "#CCCCCC", "fg": "#000000", "insertbg": "#111111", "selectbg": "#111111", "selectfg": "#FFFFFF", "widget_fg": "#000000", "select_widget": "#000000", "select_widget_fg": "#FFFFFF"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#00BABA", "functions": "#3023DD", "logical_keywords": "#ff00bb", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#74091D", "comments": "#111111", "command_keywords": "#FFFFFF", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			"toast" : {"window": {"bg" : "#000000", "fg": "#9F005F", "insertbg": "#FFFFFF", "selectbg": "#555555", "selectfg": "#AAAAAA", "widget_fg": "#AAAAAA", "select_widget": "#FFFFFF", "select_widget_fg": "#000000"},
			 "highlighter": {"whitespace": "#111111", "keywords": "#f70000", "logical_keywords": "#ff00bb", "functions": "#3023DD", "numbers": "#FF0000", "operators": "#f75f00", "special_chars": "#ff00bb", "quotes": "#00FDFD", "comments": "#555555", "command_keywords": "#FFFFFF", "found_bg": "#145226", "found_select_bg": "#FFFFFF"}},

			"student" : {"bg" : "#222222", "fg": "#FFFFFF"}
			}
		self.theme = self.theme_options["cake"]

		self.command_keywords = ["l", "lget", "highlighting", "q", "quit", "temp", "sharpness", "alpha", "convert", "save", "saveas", "open", "find", "theme"]
		self.commands = {
			"lget":"gets total amount of lines", "l":"use: l[number|number.number] :: puts your cursor on line[number]",
			"q":"quits", "quit":"quits", "temp":"updates temperature", "alpha": "use: alpha [number] \n sets how see through your window is \n 0 is completely transparent :: 100 is completely opaque",
			"convert": "use: convert [number] (decimal|hex|binary) \n converts [number] into decimal, hex and binary", "save":"saves your current file",
			"saveas":"use: saveas [name] :: saves your current file as [name]", "open":"use:  open [name] :: opens file with name[name]", "theme": "use: theme [themename] :: sets theme"
			}
		
		

		

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
		
		self.highlighting = False #now its turned off by default # turned on by default because it finally works (still, fuck regex (less than before tho))
		self.command_highlighting = False
		
		self.insert = False
		self.trippy = True
		self.insert_offtime = 0; self.insert_ontime = 1

		self.loading = False
		self.fullscreen = False
		self.run = True
		self.sharpness = 1.35

		self.Font_size = 11
		self.sFont_size = self.Font_size - 2

		#configuring main window
		# self.overrideredirect(True)
		# self.title_bar = tkinter.Frame(bg="blue", relief='raised', bd=2)

		self.resizable(True,True)
		self.tk.call("tk","scaling", self.sharpness)
		self.geometry(f"600x400")
		self.wm_minsize(20, 20)
		self.update_win()
		self.geometry(self.winfo_geometry())
		self.title(f"Nix: <None>")

		self.filename = filedialog
		self.file_handler = file_handler(self)
		self.file_handler.init()
		self.txt = self.file_handler.buffers[self.file_handler.current_buffer]
		self.canvas = tkinter.Canvas(bg=self.theme["window"]["bg"], bd=0, relief="flat", highlightthickness=0)

		self.init()

	def init(self):
		""" a completely useless initialize function """
		# widget.cget("text")
		self.update_win()
		self.wm_attributes("-alpha", 1)
		# self.canvas.create_line(0, 20, 2000, 20, fill="#FFFFFF", smooth=1)
		self.canvas.place(x=0, y=0, width=self.winfo_width(), height=41)
		# self.canvas.create_line(0, 40, 2000, 40, fill="#FFFFFF", smooth=1)

		self.font_family = ["Consolas", "bold", "normal", "roman"]
		self.font = font.Font(family=self.font_family[0], size=self.Font_size, weight=self.font_family[1], slant=self.font_family[3])
		self.font_bold = font.Font(family=self.font_family[0], size=self.Font_size, weight="bold", slant=self.font_family[3]) 
		self.smaller_font = font.Font(family=self.font_family[0],size=self.sFont_size, weight=self.font_family[1])
		self.smaller_font_bold = font.Font(family=self.font_family[0],size=self.sFont_size, weight="bold")
		self.widget_font = font.Font(family=self.font_family[0], size=self.Font_size, weight=self.font_family[1])

		self.time_label = tkinter.Label()
		self.temperature_label = tkinter.Label(text="("+self.get_rand_temperature()+")")
		self.line_no = tkinter.Label()
		
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
		self.file_menubar_label = tkinter.Label(self)
		# self.file_separator_label = tkinter.Label(self, text="----" ,font=self.font, bg=self.theme["bg"], fg="#999999").place(x=0, y=15, height=2, anchor="nw")
		self.file_menubar_label.bind("<Button-1>", 
			lambda event: self.file_menu_popup("file_menu"))
		self.file_menubar_label.place(x=0, y=0, height=20, anchor="nw")

		self.settings_menubar_label = tkinter.Label(self)
		# self.settings_separator_label = tkinter.Label(self, text="--------" ,font=self.font, bg=self.theme["bg"], fg="#999999").place(x=60, y=15, height=2, anchor="nw")
		self.settings_menubar_label.bind("<Button-1>",
			lambda event: self.file_menu_popup("settings_menu"))
		self.settings_menubar_label.place(x=60, y=0, height=20, anchor="nw")


		#dropdown for menubar
		self.file_dropdown = tkinter.Menu() #declare dropdown
		self.file_dropdown.add_command(label="New file",command=self.file_handler.new_file) #add commands
		self.file_dropdown.add_command(label="Open file",command=self.file_handler.load_file)
		self.file_dropdown.add_command(label="Save file",command=self.file_handler.save_file)
		self.file_dropdown.add_command(label="Save file as",command=self.file_handler.save_file_as)

		self.buffer_tabs = []

		# not anymore #tags for highlighting
		#sick fucking colors #A500FF;
		self.command_entry.tag_configure("command_keywords", foreground=self.theme["highlighter"]["command_keywords"])

		#command binding
		self.command_entry.bind("<Return>", self.cmmand) #if you press enter in command line it executes the command and switches you back to text widget
		self.command_entry.bind("<Up>", self.command_history) # lets you scroll through commands you have already used
		self.command_entry.bind("<Down>", self.command_history)
		self.command_entry.bind("<Escape>", self.command_entry_unset)
		self.command_entry.bind("<Insert>", self.set_cursor_mode)
	
		self.find_entry.bind("<Return>", self.find)
		self.find_entry.bind("<Up>", self.scroll_through_found)
		self.find_entry.bind("<Down>", self.scroll_through_found)
		self.find_entry.bind("<Escape>", self.find_unplace)


		try: #linux bindings that throw errors on windows
			self.txt.bind("<Shift-ISO_Left_Tab>", self.unindent)
			self.command_entry.bind("<KP_Enter>", self.cmmand)
		except Exception:
			self.txt.bind("<Shift-Tab>", self.unindent)


		self.txt.bind("<Control-Tab>", lambda arg: self.window_select("file_menu"))
		self.file_menubar_label.bind("<Return>", lambda arg: self.file_menu_popup("file_menu"))
		self.file_menubar_label.bind("<Control-Tab>", lambda arg: self.window_select("settings_menu"))
		self.file_menubar_label.bind("<Right>", lambda arg: self.window_select("settings_menu"))
		self.file_menubar_label.bind("<Left>", lambda arg: self.window_select("text"))
		self.settings_menubar_label.bind("<Return>", lambda arg: self.file_menu_popup("settings_menu"))
		self.settings_menubar_label.bind("<Control-Tab>", lambda arg: self.window_select("text"))
		self.settings_menubar_label.bind("<Right>", lambda arg: self.window_select("text"))
		self.settings_menubar_label.bind("<Left>", lambda arg: self.window_select("file_menu"))
	
		# self.txt.bind("<Control-space>", self.command_entry_set)
		self.bindable_widgets = [self.file_menubar_label, self.settings_menubar_label, self.find_entry, self.command_entry]
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
		self.bind("<Control-Shift-W>", lambda arg: self.destroy())
		self.bind("<Configure>", self.reposition_widgets) #repositions the text widget to be placed correctly


		# self.a=""
		# self.loading_label_background = tkinter.Label(self, bg="#999999", fg="#FFFFFF")
		# self.loading_label_background.place(relx=0.52,rely=0.965, relwidth=0.205 ,relheight=0.015)
		# self.loading_label = tkinter.Label(self, text="", bg=self.theme["bg"], fg="#FFFFFF")
		# self.loading_label.place(relx=0.52,rely=0.965, relheight=0.015)

		
		self.theme_load()
		self.update_buffer()

		try:
			self.file_handler.load_file(filename=sys.argv[1])
		except IndexError:
			pass

	def test_function(self, arg=None):		
		# sw = tkinter.Tk()
		# x = tkinter.Label(sw)
		# x.pack()
		# self.definition_label.place(x=0, y=100)
		# f = f"self.definition_label.configure(text={self.selection_get()}.__doc__)"
		f = f"self.command_O(arg={self.selection_get()}.__doc__)"
		try:
			exec(f)
		except Exception:
			self.command_O(arg="None")
		return "break"

	def theme_load(self):
		for key in self.theme["highlighter"].items():
			if (key[0][-2:] == "bg"): self.txt.tag_configure(key[0], background=key[1])
			else: self.txt.tag_configure(key[0], foreground=key[1])
		self.configure(bg=self.theme["window"]["bg"])

		self.txt.tag_configure("test", foreground=self.theme["window"]["bg"])
		self.txt.configure(font=self.font,bg = self.theme["window"]["bg"],fg=self.theme["window"]["fg"], undo=True, maxundo=0, spacing1=2,
			 insertwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertbackground=self.theme["window"]["insertbg"],
			 selectbackground=self.theme["window"]["selectbg"], selectforeground=self.theme["window"]["selectfg"], borderwidth=0,
			 relief="ridge", tabs=(f"{self.font.measure(' ' * 4)}"), wrap="none", exportselection=True,
			 blockcursor=self.insert, highlightthickness=0, insertborderwidth=0)

		self.time_label.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font,bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.temperature_label.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font,bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.line_no.configure(fill=None, anchor="w", justify=tkinter.LEFT, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])

		self.command_entry.configure(blockcursor=self.insert, font=self.font, bg=self.theme["window"]["bg"], fg="#00AAFF",
			 insertwidth=1, insertofftime=0, relief="raised", highlightthickness=0, bd=1, insertbackground=self.theme["window"]["insertbg"],
			 selectbackground=self.theme["window"]["selectbg"], highlightbackground="#FFFFFF")

		self.command_out.configure(font=self.smaller_font, bg=self.theme["window"]["bg"], fg="#00df00")
		self.find_entry.configure(font=self.smaller_font_bold, bg="#555555", fg="#00df00", insertbackground=self.theme["window"]["fg"], relief="flat", highlightthickness=0)
		self.find_label.configure(font=self.font, bg=self.theme["window"]["bg"], fg="#00df00")
		self.definition_label.configure(font=self.font, bg=self.theme["window"]["selectfg"], fg="#00df00")
		self.right_click_menu.configure(tearoff=0, font=self.smaller_font, bg=self.theme["window"]["bg"], fg="#ffffff")
		self.file_menubar_label.configure(text="File", font=self.widget_font, bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.settings_menubar_label.configure(text="Settings" ,font=self.widget_font, bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.file_dropdown.configure(font=self.widget_font, tearoff=False,fg="#FFFFFF", bg=self.theme["window"]["bg"], bd=0)
		self.highlighter = highlighter(self); self.set_highlighter()
		self.update_win()


	def reposition_widgets(self, arg=None):
		if (self.command_entry.winfo_viewable()): self.command_entry.place(x=-1, y=self.winfo_height()+1, width=self.winfo_width()+2, height=22, anchor="sw")
		self.txt.place(x=0,y=40,relwidth=1, height=self.winfo_height()-25, anchor="nw")
		self.time_label.place(x=self.temperature_label.winfo_x()-self.time_label.winfo_width(), y=0, height=20, anchor="nw")
		self.temperature_label.place(x=self.line_no.winfo_x()-self.temperature_label.winfo_width()-10, y=0, height=20, anchor="nw")
		self.line_no.place(x=self.winfo_width()-self.line_no.winfo_width()-10, y=0, height=20, anchor="nw")

	def get_line_count(self):
		""" returns total amount of lines in opened text """
		self.info = self.txt.get("1.0", "end-1c")
		return sum(1 for line in self.info.split("\n"))

	def set_highlighter(self):
		""" sets the highlighter accordingly to the current file extension """
		if (self.file_handler.current_file):
			arg = os.path.basename(self.file_handler.current_file.name).split(".")[1]
		else:
			arg = "NaN"

		if (arg in self.highlighter.supported_languagues):
			self.highlighting = True
			self.highlighter.set_languague(arg)
		else:
			self.highlighting = False
			
	def del_selection(self):
		try:
			self.selection_get()
		except Exception: # if no text is selected self.selection_get() will throw an error
			self.queue.clear()

		if (self.queue): self.queue[0].sort(); start_index = self.queue[0][0]; stop_index = self.queue[0][1]+1
		else: self.txt.delete(self.selection_start_index, self.highlighter.get_line_lenght(int(self.cursor_index[0]))); return

		for line_no in range(start_index, stop_index):
			self.txt.delete(float(line_no), self.highlighter.get_line_lenght(line_no))

	def queue_make(self, arg=None):
		self.queue = []
		try:
			self.selection_get()
		except Exception: #if selection is empty self.selection_get throws an error
			self.selection_start_index = None
		
		if (not self.selection_start_index): self.selection_start_index = self.txt.index(tkinter.INSERT)

		try:
			start_index = int(float(self.selection_start_index))
			if (arg.keysym == "Down"): stop_index = int(float(self.cursor_index[0]))+1
			elif (arg.keysym == "Up"): stop_index = int(float(self.cursor_index[0]))-1
			self.queue.append([start_index, stop_index])
		except Exception:
			pass

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
			self.selection_start_index = None
		elif (key == "Down"):
			self.txt.event_generate(f"<<Next{suffix[0]}>>")
			self.queue = []
			self.selection_start_index = None
		elif (key == "Left"):
			self.txt.event_generate(f"<<Prev{suffix[1]}>>")
			self.queue = []
			self.selection_start_index = None
		elif (key == "Right"):
			self.txt.event_generate(f"<<Next{suffix[1]}>>")
			self.queue = []
			self.selection_start_index = None

		if (self.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.command_out.place_forget()
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
		start_index = int(self.cursor_index[0])
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	def redo(self, arg=None):
		""" Control-Y """
		chunk_size = self.get_line_count()
		self.txt.event_generate("<<Redo>>")
		start_index = int(self.cursor_index[0])
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
		if (self.trippy): self.trippy = False; self.insert = False; self.txt.tag_delete("test")
		elif (not self.insert): self.insert = True; self.txt.tag_configure("test", foreground=self.theme["window"]["bg"])
		elif (self.insert): self.trippy = True; self.txt.configure(insertwidth=0); self.insert = False

		self.txt.configure(blockcursor=self.insert)
		self.command_entry.configure(blockcursor=self.insert)
		return "break"

	def change_case(self, arg):
		index_range = [self.selection_start_index, self.txt.index(tkinter.INSERT)]
		queue = self.queue; queue.sort()

		if (int(index_range[0].split(".")[1]) > int(index_range[1].split(".")[1])): #sort the list
			index_range.insert(0, index_range[1])
		
		if (arg == "lower"):
			text = self.txt.get(index_range[0], index_range[1])
			self.txt.delete(index_range[0], index_range[1])
			text = text.lower()
			self.txt.insert(index_range[0], text)

		elif (arg == "upper"):
			text = self.txt.get(index_range[0], index_range[1])
			self.txt.delete(index_range[0], index_range[1])
			text = text.upper()
			self.txt.insert(index_range[0], text)

		self.highlight_chunk(start_index=float(index_range[0]), stop_index=float(index_range[1]))

		del index_range
		del text
		return "break"

	def comment_line(self, arg=None):
		""" I wish I knew what the fuck is going on in here I am depressed """
		try:
			self.selection_get()
		except Exception: # if no text is selected self.selection_get() will throw an error
			self.queue.clear()

		if (self.queue): self.queue[0].sort(); start_index = self.queue[0][0]; stop_index = self.queue[0][1]+1
		else: start_index = int(self.cursor_index[0]); stop_index = int(self.cursor_index[0])+1

		for line_no in range(start_index, stop_index):
			current_line = self.txt.get(float(line_no), self.highlighter.get_line_lenght(line_no))
			for i, current_char in enumerate(current_line, 0):
				try:
					if (self.highlighter.commment_regex.match(current_char+current_line[i+1])):
						if (re.search(r"\s", self.txt.get(f"{line_no}.{i}", f"{line_no}.{i+1+len(self.highlighter.comment_sign)}"))):
							self.txt.delete(f"{line_no}.{i}", f"{line_no}.{i+1+len(self.highlighter.comment_sign)}")
						else:
							self.txt.delete(f"{line_no}.{i}", f"{line_no}.{i+len(self.highlighter.comment_sign)}")
						break

					elif (self.highlighter.abc_regex.match(current_char)):
						self.txt.insert(f"{line_no}.{i}", self.highlighter.comment_sign+" ")
						break
				except IndexError:
					self.txt.insert(f"{line_no}.{i}", self.highlighter.comment_sign+" ")
					break

		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break" # returning "break" prevents system/tkinter to call default bindings

		
	def unindent(self, arg=None):
		""" Checks if the first character in line is \t (tab) and deletes it accordingly """
		try:
			self.selection_get()
		except Exception: # if no text is selected self.selection_get() will throw an error
			self.queue.clear()

		if (self.queue): self.queue[0].sort(); start_index = self.queue[0][0]; stop_index = self.queue[0][1]+1
		else: start_index = int(self.cursor_index[0]); stop_index = int(self.cursor_index[0])+1

		for line_no in range(start_index, stop_index):
			if (re.match(r"\t", self.txt.get(f"{line_no}.0", f"{line_no}.1"))):
				self.txt.delete(f"{line_no}.0", f"{line_no}.1")
		
		return "break"

	def indent(self, arg=None):
		""" Tab """
		try:
			self.selection_get()
		except Exception: # if no text is selected self.selection_get() will throw an error
			self.queue.clear()
		if (self.queue): self.queue[0].sort(); start_index = self.queue[0][0]; stop_index = self.queue[0][1]+1; index = 0
		else: start_index = int(self.cursor_index[0]); stop_index = int(self.cursor_index[0])+1; index = self.cursor_index[1]

		for line_no in range(start_index, stop_index):
			self.txt.insert(f"{line_no}.{index}", "\t")

		return "break"
		

	def detach_widget(self, arg):
		pass
		# self.widget_window = tkinter.Tk()
		# self.widget_window.geometry("100x50")
		# self.widget_window.configure(bg=self.theme["bg"])
		# self.line_no = tkinter.Label(self.widget_window)
		# self.line_no.configure(bg=self.theme["bg"], fg=self.theme["fg"])
		# self.line_no.place(width=100, height=50)

	#window operation bindings
	def window_select(self, widget="", arg=None,):
		if (widget == "file_menu"): self.file_menubar_label.focus_set(); self.file_menubar_label.configure(bg=self.theme["window"]["select_widget"], fg=self.theme["window"]["select_widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		elif (widget == "settings_menu"): self.settings_menubar_label.focus_set(); self.settings_menubar_label.configure(bg=self.theme["window"]["select_widget"], fg=self.theme["window"]["select_widget_fg"]); self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		elif (widget == "text"): self.txt.focus_set(); self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])

		return "break"

	def set_fullscreen(self, arg=None):
		""" set the window to be fullscreen F11 """
		self.fullscreen = not self.fullscreen
		self.attributes("-fullscreen", self.fullscreen)

		return "break"

	def set_dimensions(self, arg=None, expand=None): # I do understand that this is a terrible, hideous thing but I couldn't come up with a better solution
		""" changes window size accordingly to keys pressed Alt-Curses """
		key = arg.keysym
		if (expand):
			margin = 20
			if (key == "Right"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}")
			if (key == "Left"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{self.winfo_x()-margin}+{self.winfo_y()}")
			if (key == "Up"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{self.winfo_x()}+{self.winfo_y()-margin}")
			if (key == "Down"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}")

		elif (not expand):
			margin = -20
			if (key == "Right"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{self.winfo_x()-margin}+{self.winfo_y()}")
			if (key == "Left"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{self.winfo_x()}+{self.winfo_y()}")
			if (key == "Up"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{self.winfo_x()}+{self.winfo_y()}")
			if (key == "Down"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{self.winfo_x()}+{self.winfo_y()-margin}")
				
		return "break"	
		
	def set_font_size(self, arg):
		""" Changes font size and reconfigures(updates) widgets accordingly """
		print(arg)
		if (arg.delta > 120 or arg.delta < -120): arg.delta=0 
		if (arg.keysym == "period" or arg.num == 4 or arg.delta > 0):
			self.Font_size += 1
			self.sFont_size += 1
		elif (arg.keysym == "comma" or arg.num == 5 or arg.delta < 0):
			self.Font_size -= 1
			self.sFont_size -= 1
		
		if self.Font_size <= 0:
			self.Font_size = 1
		elif self.Font_size >= 30:
			self.Font_size = 30

		self.font = font.Font(family=self.font_family[0], size=self.Font_size, weight=self.font_family[1])
		self.smaller_font = font.Font(family="Ubuntu",size=self.sFont_size, weight="bold")
		self.txt.configure(font=self.font, tabs=(f"{self.font.measure(' ' * 4)}"))
		self.command_out.configure(text=f"font size: {self.Font_size}")
		self.command_O(f"font size: {self.Font_size}")
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
			self.txt.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
			self.found.append([index, self.txt.index(f"{index}+{count.get()}c")])
		
		for index in self.found:
			self.txt.tag_add("found_bg", index[0], index[1])
		
		self.scroll_through_found()

	def scroll_through_found(self, arg=None):
		result_count = len(self.found)
		offset = 0
		if (result_count == 0): self.command_O(f"found none"); return

		if (arg):
			self.command_out.place_forget()
			if (arg.keysym == "Up"):
				self.found_index -= 1
				offset = -3
				if (self.found_index < 0):
					self.found_index = result_count-1
					offset = 3

			elif (arg.keysym == "Down"):
				self.found_index += 1
				offset = 3
				if (self.found_index >= result_count):
					self.found_index = 0
					offset = -3

		for index in self.found:
			self.txt.tag_remove("found_select_bg", index[0], index[1])
			
		self.txt.see(float(self.found[self.found_index][0])+offset)
		# self.find_label.configure(text=f" {self.found_index+1} out of {result_count} results : {self.found[self.found_index]}")
		self.find_label.configure(text=f" {result_count} found")
		self.command_O(f"{self.found_index+1} out of {result_count} results : {self.found[self.found_index]}")
		self.txt.tag_add("found_select_bg", self.found[self.found_index][0], self.found[self.found_index][1])
		self.txt.mark_set(tkinter.INSERT, self.found[self.found_index][0])


	def find_place(self, arg=None, text=""):
		self.find_entry.place(x=0, y=self.winfo_height()-40, relwidth=0.5, height=20, anchor="nw")
		self.find_entry.insert("1", text)
		# self.find_label.place(relx=0., y=125, anchor="ne")
		self.find_entry.tkraise(); self.find_entry.focus_set()
	
	def find_unplace(self, arg=None):
		for index in self.found:
			self.txt.tag_remove("found_bg", index[0], index[1])
			self.txt.tag_remove("found_select_bg", index[0], index[1])
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
		self.command_entry.place(x=-1, y=self.winfo_height()+1, width=self.winfo_width()+2, height=22, anchor="sw")
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
			# self.command_entry.see(f"1.{len(last_command)}")
			self.command_entry.mark_set(tkinter.INSERT, f"1.{l}")
			self.command_entry.see(tkinter.INSERT)

			#print(self.command_input_history_index)

		except IndexError:
			#print(self.command_input_history_index)
			self.command_input_history_index = 0
			self.command_entry.delete("1.0", "end")

		return "break"

	def command_O(self, arg):
		""" sets the text in command output """
		#(I have no idea why past me made this into a function when it doesn't really have to be a function)
		self.command_out.place(relx=0, rely=0.99975, relwidth=1, anchor="sw")
		self.command_out.configure(text=str(arg), anchor="c")


	def cmmand(self, arg):
		""" parses command(case insensitive) from command line and executes it"""
		self.command_input_history_index = 0
		command = self.command_entry.get("1.0", "end-1c").split()#turns command into a list of arguments
		
		if (not command): self.command_entry_unset(); return #if no input/argument were provided hide the command entry widget and break function
		
		#help command
		if (command[0] == "help"):
			try:
				self.command_O(f"{self.commands[command[1]]}")
			except IndexError:
				x = ""
				for item in self.command_keywords:
					x += "\n"+item
				self.command_O(x)
				
		elif (command[0] == "test"):
			self.txt.event_generate("<<Return>>")
		#highlighting command
		elif (command[0] == "highlighting"):
			#print("aaa")
			if (command[1] == "on"):
				self.command_O("highlighting on")
				self.highlight_chunk()
				self.highlighting = True
			elif (command[1] == "off"):
				self.unhighlight_chunk()
				self.command_O("highlighting off")
				self.highlighting = False

		#line/ line and column commands

		elif (re.match(r"[0-9]", command[0][0])):
			self.txt.mark_set(tkinter.INSERT, float(command[0]))
			self.txt.see(float(command[0])+2)
			self.command_O(f"moved to: {float(command[0])}")

		elif (re.match(r"^l[0-9]+$|^lget$", command[0])):
			for i, pnum in enumerate(command[0][1:], 1):
				print(pnum)
				if (re.search("[0-9]", pnum)): 
					argument = command[0][i:]
					break
				
				elif (re.search("[a-zA-Z]", pnum)):
					argument = command[0][i:]
					break

			if (re.match(r"[0-9]", argument)):
				self.txt.mark_set(tkinter.INSERT, float(argument))
				self.txt.see(float(argument)+2)
				self.command_O(f"moved to: {float(argument)}")

			elif (re.match("get", argument)):
				self.command_O(f"total lines: {self.get_line_count()}")

		elif (command[0] == "find"):
			self.find_place(text=command[1])
			self.find(command[1])

		elif (command[0] == "lyrics"):
			command1 = ""
			for word in command[1:]:
				command1 += " "+word
			command1 = command1.split(",")
			lyrics = lyricwikia.get_lyrics(command1[0], command1[1])
			self.command_O(lyrics)

		elif (command[0] == "temp"):
			self.temperature_label.configure(text=self.get_temperature())
			self.command_O("temperature changed")

		elif (command[0] == "quit" or command[0] == "q"):
			self.run = False

		elif (command[0] == "sharpness"):
			self.sharpness = command[1]
			self.tk.call("tk", "scaling", command[1])
			self.command_O(f"sharpness: {command[1]}")

		elif (command[0] == "alpha" or command[0] == "transparency"):
			if (command[1] == "default"): command[1] = 90
			self.wm_attributes("-alpha", int(command[1])/100)
			self.command_O(f"alpha: {command[1]}")

		elif (command[0] == "convert"):
			try:
				if (command[1][:2] == "0x"):
					decimal = int(command[1], 16)
				elif (command[1][:2] == "0b"):
					decimal = int(command[1], 2)
				else:
					decimal = int(command[1], 10)

				self.command_O(f"DECIMAL: {decimal}, HEXADECIMAL: {hex(decimal)}, BINARY: {bin(decimal)}")
			except ValueError:
				self.command_O("Error: wrong format; please, add prefix (0x | 0b)")
		
		elif (command[0] == "resize"):
			self.update_win()
			self.geometry(f"{int(command[1])}x{int(command[2])}")

		elif (command[0] == "save"):
			self.file_handler.save_file()
			self.loading = True
		
		elif (command[0] == "saveas"):
			self.file_handler.save_file_as(tmp=command[1])

		elif (command[0] == "open"):
			self.file_handler.load_file(filename=command[1])

		elif (command[0] == "reload"):
			self.file_handler.load_file(filename=self.file_handler.current_file.name)
			
		elif (command[0] == "ls"):
			x = ""
			for i, file in enumerate(os.listdir(self.file_handler.current_dir), 0):
				if (i % 3 == 0): x += f"{file}\n"
				else: x += f"{file} | "
			self.command_O(f"{x}")
		
		elif (command[0] == "cd"):
			try:
				os.chdir(command[1])
				self.current_dir = os.getcwd()
				self.command_O(arg=f"current directory: {self.file_handler.current_dir}")
			except FileNotFoundError:
				self.command_O(arg=f"Error: File/Directory not found")
				
		elif (command[0] == "theme"):
			try:
				self.unhighlight_chunk()
				self.theme = self.theme_options[command[1]]
				self.theme_load()
				self.highlight_chunk()
			except IndexError:
				result = "themes:"
				for key in self.theme_options.keys():
					result += "  "+key
				self.command_O(result)
		else:
			self.command_O(f"Command {command} not found")


		#append command to command history
		self.command_input_history.append(command)

		#sets focus back to text widget
		self.txt.focus_set()
		self.txt.see(tkinter.INSERT)
		self.command_entry.delete("1.0", "end") #deletes command line input

		#set command history to newest index
		self.command_input_history_index = 0       
		self.command_entry.place_forget()	


	def get_rand_temperature(self):
		""" generates a random temperature depending on the current month """
		month = datetime.now().date().month
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
				self.temperature_label.configure(text="("+BeautifulSoup(html, features="html.parser").find("span", class_="wr-value--temperature--c").text+"C)") #returns the scraped temperature
			except Exception: #dunno if it won't crash the app if there's no internet connection
				pass

		threading.Thread(target=temp).start()

	def get_time(self):
		""" gets time and parses to make it look the way I want it to """
		d_time = datetime.now().time()
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
			self.command_O("temperature changed")

		self.time_label.config(text=time) #updates the time label/widget to show current time


	def update_buffer(self, arg=None):
		""" updates some of the widgets when a character is typed in """
		if (self.file_handler.current_file_name): self.title(f"Nix: <*{os.path.basename(self.file_handler.current_file_name)}>") #if statement to prevent an error because there is no file at the start of the app other && if a new character has been typed in put an asterisk to the title to show that the file hasn't been updated yet
		# len(self.content) != len(self.txt.get("1.0", "end-1c")) and
		# self.file_handler.buffers[self.file_handler.current_buffer] = self.txt.get("1.0", "end")

		if (self.focus_displayof() != self.command_entry): #if the user is not using the command entry widget and a character has been typed into the text widget: hide the command enter widget
			self.command_entry.place_forget()

		if (self.focus_displayof() != self.command_out): #if the a character has been typed into the text widget: hide the command output widget
			self.command_out.place_forget() 
		
		if (self.focus_displayof() != self.find_entry): #if the a character has been typed into the text widget: hide the command output widget
			self.find_unplace()


	def update_win(self):
		""" updates the window whole window (all of it's widgets)"""
		try:
			self.update()
			self.update_idletasks()
		except Exception: #when exiting window it throws an error because self wasn't properly destroyed
			self.run = False
			self.quit()


	def main(self):
		""" reconfigures(updates) some of the widgets to have specific values and highlights the current_line"""
		self.txt.mark_set(tkinter.INSERT, "1.0")
		while (True):
			self.update_win()
			if (self.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"])
			# print(self.buffer_tabs)
			self.cursor_index = self.txt.index(tkinter.INSERT).split(".") # gets the cursor's position
			self.current_line = self.txt.get(float(self.cursor_index[0]), self.highlighter.get_line_lenght(int(self.cursor_index[0])))+"\n"

			self.line_no.configure(text=f"[{self.txt.index(tkinter.INSERT)}]") #updates the line&column widget to show current cursor index/position
			if (self.selection_start_index): self.line_no.configure(text=f"[{self.selection_start_index}][{self.txt.index(tkinter.INSERT)}]")

			self.get_time()

			if (self.highlighting): # if the highlighting option is on then turn on highlighting :D
				self.highlighter.highlight(self.cursor_index[0], line=self.current_line) #highlight function

			# if (len(self.file_handler.buffers[self.file_handler.current_buffer]) != len(self.txt.get("1.0", "end-1c")) and self.focus_displayof() == self.txt): #if a character has been typed into the text widget call the udpate buffer function
			# self.update_buffer()

			if (self.focus_displayof() == self.command_entry):
				self.highlighter.command_highlight()

			if (self.trippy):
				try:
					# print(self.txt.get(self.txt.index(tkinter.INSERT)), "x")
					if (re.match(r"\n", self.txt.get(self.txt.index(tkinter.INSERT)))): self.txt.tag_configure("test", background=self.theme["window"]["bg"]); self.txt.configure(blockcursor=True)
					else: self.txt.tag_configure("test", background=self.theme["highlighter"][self.txt.tag_names(self.txt.index(tkinter.INSERT))[0]], foreground=self.theme["window"]["bg"]); self.txt.configure(blockcursor=self.insert)
				except Exception:
					self.txt.tag_configure("test", background=self.theme["window"]["fg"], foreground=self.theme["window"]["bg"])
			
			self.txt.tag_remove("test", "1.0", "end")
			self.txt.tag_add("test", self.txt.index(tkinter.INSERT))

			
	def keep_indent(self, arg=None):
		""" gets the amount of tabs in the last line and puts them at the start of a new one """
		#this functions gets called everytime Enter/Return has been pressed
		self.del_queue()
		for offset, current_char in enumerate(self.current_line, 0):
			if (not re.match(r"\t",  current_char) or self.highlighter.commment_regex.match(current_char)):
				break

		try:
			if (re.match(r"[\:\{\[]", self.current_line[int(self.cursor_index[1])-1])): offset += 1
		except IndexError:
			pass

		self.txt.insert(self.txt.index(tkinter.INSERT), "\n")
		[self.txt.insert(self.txt.index(tkinter.INSERT), "\t") for i in range(offset)]#insert the tabs at the start of the line
		return "break"

	def highlight_chunk(self, arg=None, start_index=None, stop_index=None):
		if (not start_index): start_index = 1
		if (not stop_index): stop_index = self.get_line_count()+1 #+1 because the last line doesn't get highlighted
		if (type(start_index) == str): start_index = float(start_index) #fuck
		if (type(stop_index) == str): stop_index = float(stop_index) #this
		if (type(start_index) == float): start_index = int(start_index)	#shit
		if (type(stop_index) == float): stop_index = int(stop_index) #am out
		def highlight():
			t0 = time() # timer| gets current time in miliseconds
			if self.highlighting: [self.highlighter.highlight(i) for i in range(start_index, stop_index)]
			t1 = time() # timer| gets current time in miliseconds
			print(t1-t0)
		threading.Thread(target=highlight).start()
		

	def unhighlight_chunk(self, arg=None, start_index=None, stop_index=None):
		if (not start_index): start_index = 1
		if (not stop_index): stop_index = self.get_line_count()+1 #+1 because the last line doesn't get highlighted
		def unhighlight():
			[self.highlighter.unhighlight(i) for i in range(start_index, stop_index)]

		threading.Thread(target=unhighlight).start()

	def note_mode(self):
		self.highlighting = False

	def retro_mode(self):
		pass



main_win = win()

if __name__ == '__main__':
	main_win.after(0, main_win.main)
	main_win.mainloop()
	
