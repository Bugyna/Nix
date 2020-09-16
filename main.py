__author__ = "Bugy"
__license__ = "MIT"
__maintainer__ = "Bugy"
__email__ = ["matejbugy@gmail.com", "achjoj5@gmail.com"]
__status__ = "Production"

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

import lyricwikia
import requests
from bs4 import BeautifulSoup

import random
import threading

from highlighter import highlighter
from handlers import file_handler


# for i in tqdm.tqdm(range(10)):
#	sleep(0.01)



class win(file_handler):
	""" main object of Nix text editor"""
	def __init__(self, root, file=None):
		super().__init__(self, root)
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

		self.command_keywords = ["l", "lget", "highlighting", "q", "quit", "temp", "sharpness", "alpha", "save", "open", "find", "theme"]
		
		self.command_definition = {
			"l" : "-get: gets last line number || -[LINE_NUMBER(.CHARACTER)]: puts you to line number (eg. 120(by default starts at column 0 but you can specify the column like: 120.5)",
			"highlighting" : "-on: turns highlighting on -off: turns highlighting off"
		}

		self.root = root

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

		self.loading = False
		self.fullscreen = False
		self.run = True
		self.sharpness = 1.35

		self.Font_size = 11
		self.sFont_size = self.Font_size - 2

		#configuring main window
		# root.overrideredirect(True)
		# self.title_bar = tkinter.Frame(bg="blue", relief='raised', bd=2)

		root.resizable(True,True)
		root.tk.call("tk","scaling", self.sharpness)
		root.geometry(f"600x400")
		self.update_win()
		root.geometry(root.winfo_geometry())
		root.title(f"Nix: <None>")


		self.txt = tkinter.Text()
		self.filename = filedialog

		self.init()

	def init(self):
		""" a completely useless initialize function """
		
		self.update_win()
		root.wm_attributes("-alpha", 1)
			

		self.font_family = ["Consolas", "bold", "normal", "roman"]
		self.font = font.Font(family=self.font_family[0], size=self.Font_size, weight=self.font_family[1], slant=self.font_family[3])
		self.font_bold = font.Font(family=self.font_family[0], size=self.Font_size, weight="bold", slant=self.font_family[3]) 
		self.smaller_font = font.Font(family=self.font_family[0],size=self.sFont_size, weight=self.font_family[1])
		self.smaller_font_bold = font.Font(family=self.font_family[0],size=self.sFont_size, weight="bold")
		self.widget_font = font.Font(family=self.font_family[0], size=self.Font_size, weight=self.font_family[1])

		self.time_label = tkinter.Label()
		self.time_label.place(x=root.winfo_width()-250,y=5, anchor="nw")
		
		self.temperature_label = tkinter.Label(text="("+self.get_rand_temperature()+")")
		self.temperature_label.place(x=root.winfo_width()-200,y=5, anchor="nw")

		self.line_no = tkinter.Label()
		self.line_no.place(x=root.winfo_width()-100,y=10, anchor="nw")
		
		self.find_entry = tkinter.Entry()

		self.find_label = tkinter.Label()

		self.definition_label = tkinter.Label()

		#command line entry
		self.command_entry = tkinter.Text()

		#command output
		self.command_out = tkinter.Label()
		
		#right click pop-up menu
		self.right_click_menu = tkinter.Menu()
		self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
		self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
		self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
		self.right_click_menu.add_separator()

		#menubar
		self.file_menubar_label = tkinter.Label(root)
		# self.file_separator_label = tkinter.Label(root, text="----" ,font=self.font, bg=self.theme["bg"], fg="#999999").place(x=0, y=15, height=2, anchor="nw")
		self.file_menubar_label.bind("<Button-1>", 
			lambda event: self.file_menu_popup("file_menu"))
		self.file_menubar_label.place(x=0, y=5, height=20, anchor="nw")

		self.settings_menubar_label = tkinter.Label(root)
		# self.settings_separator_label = tkinter.Label(root, text="--------" ,font=self.font, bg=self.theme["bg"], fg="#999999").place(x=60, y=15, height=2, anchor="nw")
		self.settings_menubar_label.bind("<Button-1>",
			lambda event: self.file_menu_popup("settings_menu"))
		self.settings_menubar_label.place(x=60, y=5, height=20, anchor="nw")


		#dropdown for menubar
		self.file_dropdown = tkinter.Menu() #declare dropdown
		self.file_dropdown.add_command(label="New file",command=self.new_file) #add commands
		self.file_dropdown.add_command(label="Open file",command=self.load_file)
		self.file_dropdown.add_command(label="Save file",command=self.save_file)
		self.file_dropdown.add_command(label="Save file as",command=self.save_file_as)

		# not anymore #tags for highlighting
		#sick fucking colors #A500FF;
		self.command_entry.tag_configure("command_keywords", foreground=self.theme["highlighter"]["command_keywords"])

		#command binding
		self.command_entry.bind("<Return>", self.cmmand) #if you press enter in command line it executes the command and switches you back to text widget
		self.command_entry.bind("<Up>", self.command_history) # lets you scroll through commands you have already used
		self.command_entry.bind("<Down>", self.command_history)
		self.command_entry.bind("<Escape>", self.command_entry_unset)
		self.command_entry.bind("<Insert>", self.set_cursor_mode)
	
		self.txt.bind("<Control-period>", self.set_font_size)
		self.txt.bind("<Control-comma>", self.set_font_size)
		self.txt.bind("<Control-MouseWheel>", self.set_font_size)
		self.txt.bind("<Control-Button-4>", self.set_font_size)
		self.txt.bind("<Control-Button-5>", self.set_font_size)

		self.txt.bind("<Up>", self.move)
		self.txt.bind("<Down>", self.move)
		self.txt.bind("<Left>", self.move)
		self.txt.bind("<Right>", self.move)
		self.txt.bind("<Control-Up>", self.move)
		self.txt.bind("<Control-Down>", self.move)
		self.txt.bind("<Control-Left>", self.move)
		self.txt.bind("<Control-Right>", self.move)

		self.txt.bind("<MouseWheel>", self.scroll)
		self.txt.bind("<Button-4>", self.scroll)
		self.txt.bind("<Button-5>", self.scroll)
		self.txt.bind("<Shift-MouseWheel>", lambda arg: self.scroll(arg, multiplier=3))
		self.txt.bind("<Shift-Button-4>", lambda arg: self.scroll(arg, multiplier=3))
		self.txt.bind("<Shift-Button-5>", lambda arg: self.scroll(arg, multiplier=3))
		self.txt.bind("<Button-3>", self.popup) #right click pop-up window

		self.txt.bind("<Return>", self.keep_indent)
		self.txt.bind("<Control-slash>", self.comment_line) #self.comment_line)

		self.txt.bind("<Control-S>", self.save_file)
		self.txt.bind("<Control-s>", self.save_file)
		self.txt.bind("<Control-Shift-S>", self.save_file_as)
		self.txt.bind("<Control-Shift-s>", self.save_file_as)
		self.txt.bind("<Control-N>", self.new_file)
		self.txt.bind("<Control-n>", self.new_file)
		self.txt.bind("<Control-F>", self.find_place)
		self.txt.bind("<Control-f>", self.find_place)
		self.txt.bind("<Control-V>", self.paste)
		self.txt.bind("<Control-v>", self.paste)

		self.txt.bind("<Control-Z>", self.undo)
		self.txt.bind("<Control-z>", self.undo)
		self.txt.bind("<Control-Y>", self.redo)
		self.txt.bind("<Control-y>", self.redo)
		self.txt.bind("<Control-A>", self.select_all)
		self.txt.bind("<Control-a>", self.select_all)
		self.txt.bind("<Control-L>", lambda arg: self.change_case("lower"))
		self.txt.bind("<Control-l>", lambda arg: self.change_case("lower"))
		self.txt.bind("<Control-Shift-L>", lambda arg: self.change_case("upper"))
		self.txt.bind("<Control-Shift-l>", lambda arg: self.change_case("upper"))
		self.txt.bind("<Tab>", self.indent)

		self.txt.bind("<Shift-Up>", self.queue_make)
		self.txt.bind("<Shift-Down>", self.queue_make)
		self.txt.bind("<Shift-Left>", self.queue_make)
		self.txt.bind("<Shift-Right>", self.queue_make)
		self.txt.bind("<Shift-Return>", lambda arg: subprocess.call("./open.sh"))

		self.txt.bind("<Control-Q>", self.test_function)
		self.txt.bind("<Control-q>", self.test_function)
		# self.txt.bind("<Shift_L>", self.Qq)

		self.txt.bind("<Insert>", self.set_cursor_mode)
		self.txt.bind("<Home>", self.home)
		self.txt.bind("<Shift-Home>", self.home_select)

	
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

		self.txt.bind("<Control-space>", self.command_entry_set)
		self.bindable_widgets = [self.txt, self.file_menubar_label, self.settings_menubar_label, self.find_entry, self.command_entry]
		for widget in self.bindable_widgets:
			widget.bind("<F11>", self.set_fullscreen)
			widget.bind("<Alt-Right>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Left>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Up>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Down>", lambda arg: self.set_dimensions(arg, True))
			widget.bind("<Alt-Shift-Right>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Left>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Up>", lambda arg: self.set_dimensions(arg, False))
			widget.bind("<Alt-Shift-Down>", lambda arg: self.set_dimensions(arg, False))

		root.bind("<Control-Escape>", lambda arg: root.destroy())
		root.bind("<Control-Shift-W>", lambda arg: root.destroy())
		root.bind("<Configure>", self.reposition_widgets) #repositions the text widget to be placed correctly


		# self.a=""
		# self.loading_label_background = tkinter.Label(root, bg="#999999", fg="#FFFFFF")
		# self.loading_label_background.place(relx=0.52,rely=0.965, relwidth=0.205 ,relheight=0.015)
		# self.loading_label = tkinter.Label(root, text="", bg=self.theme["bg"], fg="#FFFFFF")
		# self.loading_label.place(relx=0.52,rely=0.965, relheight=0.015)

		
		self.theme_load()
		self.update_buffer()

		try:
			self.load_file(filename=sys.argv[1])
		except IndexError:
			pass

	def test_function(self, arg=None):		
		# sw = tkinter.Tk()
		# x = tkinter.Label(sw)
		# x.pack()
		# self.definition_label.place(x=0, y=100)
		# f = f"self.definition_label.configure(text={root.selection_get()}.__doc__)"
		f = f"self.command_O(arg={root.selection_get()}.__doc__)"
		try:
			exec(f)
		except Exception:
			self.command_O(arg="None")
		return "break"

	def theme_load(self):
		for key in self.theme["highlighter"].items():
			if (key[0][-2:] == "bg"): self.txt.tag_configure(key[0], background=key[1])
			else: self.txt.tag_configure(key[0], foreground=key[1])
		self.txt.tag_configure("test", foreground=self.theme["window"]["bg"])
		root.config(bg=self.theme["window"]["bg"])
		self.txt.configure(font=self.font,bg = self.theme["window"]["bg"],fg=self.theme["window"]["fg"], undo=True, maxundo=0, spacing1=2,
			 insertwidth=0, insertofftime=0, insertontime=1, insertbackground=self.theme["window"]["insertbg"],
			 selectbackground=self.theme["window"]["selectbg"], selectforeground=self.theme["window"]["selectfg"], borderwidth=0,
			 relief="ridge", tabs=(f"{self.font.measure(' ' * 4)}"), wrap="word", exportselection=True,
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
		self.file_menubar_label.configure(text="File" ,font=self.widget_font, bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.settings_menubar_label.configure(text="Settings" ,font=self.widget_font, bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.file_dropdown.configure(font=self.widget_font, tearoff=False,fg="#FFFFFF", bg=self.theme["window"]["bg"], bd=0)
		self.highlighter = highlighter(self, root); self.set_highlighter()


	def reposition_widgets(self, arg=None):
		if (self.command_entry.winfo_viewable()): self.command_entry.place(x=-1, y=root.winfo_height()+1, width=root.winfo_width()+2, height=22, anchor="sw")
		self.txt.place(x=0,y=25,relwidth=1, height=root.winfo_height()-25, anchor="nw")
		self.time_label.place(x=self.temperature_label.winfo_x()-self.time_label.winfo_width(),y=5, anchor="nw")
		self.temperature_label.place(x=self.line_no.winfo_x()-self.temperature_label.winfo_width()-10,y=5, anchor="nw")
		self.line_no.place(x=root.winfo_width()-self.line_no.winfo_width()-10,y=5, anchor="nw")

	def get_line_count(self):
		""" returns total amount of lines in opened text """
		self.info = self.txt.get("1.0", "end-1c")
		return sum(1 for line in self.info.split("\n"))

	def set_highlighter(self):
		""" sets the highlighter accordingly to the current file extension """
		if (self.current_file_name):
			arg = os.path.basename(self.current_file.name).split(".")[1]
		else:
			arg = "NaN"

		if (arg in self.highlighter.supported_languagues):
			self.highlighting = True
			self.highlighter.set_languague(arg)
		else:
			self.highlighting = False


	def queue_make(self, arg=None):
		self.queue = []
		try:
			root.selection_get()
		except Exception:
			self.selection_start_index = None
		
		# print(root.selection_get())
		if (not self.selection_start_index): self.selection_start_index = self.txt.index(tkinter.INSERT)
		
		try:
			start_index = int(float(self.selection_start_index))
			if (arg.keysym == "Down"): stop_index = int(float(self.cursor_index[0]))+1
			elif (arg.keysym == "Up"): stop_index = int(float(self.cursor_index[0]))-1
			self.queue.append([start_index, stop_index])
			print(self.queue)
		except Exception as e:
			pass


	def move(self, arg=None):
		key = arg.keysym
		suffix = ["Line", "Char"]
		
		if (arg.state == 20):
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

		if (root.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])

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
		to_paste = root.clipboard_get()
		start_index = float(self.txt.index(tkinter.INSERT))
		stop_index = start_index+len(to_paste.split("\n"))
		self.txt.insert(start_index, to_paste)
		self.highlight_chunk(start_index=int(start_index), stop_index=int(stop_index))
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
			root.selection_get()
		except Exception: # if no text is selected root.selection_get() will throw an error
			self.queue.clear()

		if (self.queue): self.queue[0].sort(); start_index = self.queue[0][0]; stop_index = self.queue[0][1]+1
		else: start_index = int(self.cursor_index[0]); stop_index = int(self.cursor_index[0])+1

		for line_no in range(start_index, stop_index):
			current_line = self.txt.get(float(line_no), self.highlighter.get_line_lenght(line_no))
			for i, current_char in enumerate(current_line, 0):
				if (self.highlighter.commment_regex.match(current_char)):

					if (re.match(r"\s", self.txt.get(f"{line_no}.{i+len(self.highlighter.comment_sign)}"))):
						self.txt.delete(f"{line_no}.{i}", f"{line_no}.{i+1+len(self.highlighter.comment_sign)}")
					else:
						self.txt.delete(f"{line_no}.{i}", f"{line_no}.{i+len(self.highlighter.comment_sign)}")
					break

				elif (self.highlighter.abc_regex.match(current_char)):
					self.txt.insert(f"{line_no}.{i}", self.highlighter.comment_sign+" ")
					break

		self.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break" # returning "break" prevents system/tkinter to call default bindings

		
	def unindent(self, arg=None):
		""" Checks if the first character in line is \t (tab) and deletes it accordingly """
		try:
			root.selection_get()
		except Exception: # if no text is selected root.selection_get() will throw an error
			self.queue.clear()

		if (self.queue): self.queue[0].sort(); start_index = self.queue[0][0]; stop_index = self.queue[0][1]+1
		else: start_index = int(self.cursor_index[0]); stop_index = int(self.cursor_index[0])+1

		for line_no in range(start_index, stop_index):
			if (re.match(r"\t", self.txt.get(f"{line_no}.0", f"{line_no}.1"))):
				self.txt.delete(f"{line_no}.0", f"{line_no}.1")

	def indent(self, arg=None):
		""" Tab """
		try:
			root.selection_get()
		except Exception: # if no text is selected root.selection_get() will throw an error
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
		root.attributes("-fullscreen", self.fullscreen)

		return "break"

	def set_dimensions(self, arg=None, expand=None): # I do understand that this is a terrible, hideous thing but I couldn't come up with a better solution
		""" changes window size accordingly to keys pressed Alt-Curses """
		key = arg.keysym
		if (expand):
			margin = 20
			if (key == "Right"):
				root.geometry(f"{root.winfo_width()+margin}x{root.winfo_height()}")
			if (key == "Left"):
				root.geometry(f"{root.winfo_width()+margin}x{root.winfo_height()}+{root.winfo_rootx()-margin}+{root.winfo_rooty()-24}")
			if (key == "Up"):
				root.geometry(f"{root.winfo_width()}x{root.winfo_height()+margin}+{root.winfo_rootx()}+{root.winfo_rooty()-margin-24}")
			if (key == "Down"):
				root.geometry(f"{root.winfo_width()}x{root.winfo_height()+margin}")

		elif (not expand):
			margin = -20
			if (key == "Right"):
				root.geometry(f"{root.winfo_width()+margin}x{root.winfo_height()}+{root.winfo_rootx()-margin}+{root.winfo_rooty()-24}")
			if (key == "Left"):
				root.geometry(f"{root.winfo_width()+margin}x{root.winfo_height()}+{root.winfo_rootx()}+{root.winfo_rooty()-24}")
			if (key == "Up"):
				root.geometry(f"{root.winfo_width()}x{root.winfo_height()+margin}+{root.winfo_rootx()}+{root.winfo_rooty()-24}")
			if (key == "Down"):
				root.geometry(f"{root.winfo_width()}x{root.winfo_height()+margin}+{root.winfo_rootx()}+{root.winfo_rooty()-margin-24}")
				
		return "break"	
		
	def set_font_size(self, arg):
		""" Changes font size and reconfigures(updates) widgets accordingly """
		if (arg.delta > 120 or arg.delta < 120): arg.delta=0 
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
			if count.get() == 0: break # degenerate pattern which matches zero-length strings
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
		self.find_entry.place(x=0, y=root.winfo_height()-40, relwidth=0.5, height=20, anchor="nw")
		self.find_entry.insert("1", text)
		# self.find_label.place(relx=0., y=125, anchor="ne")
		self.find_entry.focus_set()
	
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
			self.file_dropdown.tk_popup(root.winfo_rootx(), root.winfo_rooty()+25)
		
		elif (widget == "settings_menu"):
			self.file_dropdown.tk_popup(root.winfo_rootx()+63, root.winfo_rooty()+25)

	def command_entry_set(self, arg=None):
		""" Shows command entry widget """
		self.command_entry.place(x=-1, y=root.winfo_height()+1, width=root.winfo_width()+2, height=22, anchor="sw")
		self.command_out.place_forget()
		self.command_entry.focus_set()

	def command_entry_unset(self, arg=None):
		""" hides command entry widget 'tis a kinda useless function"""
		self.command_entry.place_forget()
		self.txt.focus_set()

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
				if (command[1] != None):
					self.help_win(command[1])
			except IndexError:
				self.help_win()
				
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
			print(command)
			command1 = ""
			for word in command[1:]:
				command1 += " "+word
			command1 = command1.split(",")
			print(command1)
			lyrics = lyricwikia.get_lyrics(command1[0], command1[1])
			self.command_O(lyrics)

		elif (command[0] == "temp"):
			self.temperature_label.configure(text=self.get_temperature())
			self.command_O("temperature changed")

		elif (command[0] == "quit" or command[0] == "q"):
			self.run = False

		elif (command[0] == "sharpness"):
			self.sharpness = command[1]
			root.tk.call("tk", "scaling", command[1])
			self.command_O(f"sharpness: {command[1]}")

		elif (command[0] == "alpha" or command[0] == "transparency"):
			if (command[1] == "default"): command[1] = 90
			root.wm_attributes("-alpha", int(command[1])/100)
			self.command_O(f"alpha: {command[1]}")

		elif (command[0] == "resize"):
			self.update_win()
			root.geometry(f"{int(command[1])}x{int(command[2])}")

		elif (command[0] == "save"):
			self.save_file()
			self.loading = True

		elif (command[0] == "open"):
			self.load_file(filename=command[1])
			#self.command_O(f"file saved")
			
		elif (command[0] == "ls"):
			x = ""
			for i, file in enumerate(os.listdir(self.current_dir), 0):
				if (i % 3 == 0): x += f"{file}\n"
				else: x += f"{file} | "
			self.command_O(f"{x}")
			# self.command_O(f"{os.listdir(self.current_dir)}")
		
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
		try: 
			url = "https://www.bbc.com/weather/2673730" #link to Stockholm's weather data
			html = requests.get(url).content #gets the html of the url
			return "("+BeautifulSoup(html, features="html.parser").find("span", class_="wr-value--temperature--c").text+"C)" #returns the scraped temperature
		except Exception: #dunno if it won't crash the app if there's no internet connection
			pass

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
			self.temperature_label.configure(text=self.get_temperature())
			self.command_O("temperature changed")

		return time


	def update_buffer(self):
		""" updates some of the widgets when a character is typed in """
		if (self.current_file_name): root.title(f"Nix: <*{os.path.basename(self.current_file_name)}>") #if statement to prevent an error because there is no file at the start of the app other && if a new character has been typed in put an asterisk to the title to show that the file hasn't been updated yet
		# len(self.content) != len(self.txt.get("1.0", "end-1c")) and
		
		
		if (root.focus_displayof() != self.command_entry): #if the user is not using the command entry widget and a character has been typed into the text widget: hide the command enter widget
			self.command_entry.place_forget()

		if (root.focus_displayof() != self.command_out): #if the a character has been typed into the text widget: hide the command output widget
			self.command_out.place_forget() 
		
		if (root.focus_displayof() != self.find_entry): #if the a character has been typed into the text widget: hide the command output widget
			self.find_unplace()


	def update_win(self):
		""" updates the window whole window (all of it's widgets)"""
		try:
			root.update()
			root.update_idletasks()
		except Exception: #when exiting window it throws an error because root wasn't properly destroyed
			self.run = False
			root.quit()


	def main(self):
		""" reconfigures(updates) some of the widgets to have specific values and highlights the current_line"""
		#basically the main function
		self.txt.mark_set(tkinter.INSERT, "1.0")
		while (self.run):
			self.update_win()
			if (root.focus_displayof() == self.txt): self.file_menubar_label.configure(bg=self.theme["window"]["bg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"])
			
			self.cursor_index = self.txt.index(tkinter.INSERT).split(".") # gets the cursor's position
			self.current_line = self.txt.get(float(self.cursor_index[0]), self.highlighter.get_line_lenght(int(self.cursor_index[0])))+"\n"
			self.time_label.config(text=self.get_time()) #updates the time label/widget to show current time
			self.line_no.configure(text=f"[{self.txt.index(tkinter.INSERT)}]") #updates the line&column widget to show current cursor index/position

			if (self.selection_start_index): self.line_no.configure(text=f"[{self.selection_start_index}][{self.txt.index(tkinter.INSERT)}]")

			if (self.highlighting): # if the highlighting option is on then turn on highlighting :D
				self.highlighter.highlight(self.cursor_index[0], line=self.current_line) #highlight function

			if (len(self.content) != len(self.txt.get("1.0", "end-1c"))): #if a character has been typed into the text widget call the udpate buffer function
				self.update_buffer()

			if (root.focus_displayof() == self.command_entry):
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
		#this functions gets called everytime Enter/Return has been pressed or rather everytime a \n (newline) character has been found
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
		if (not stop_index): stop_index = self.get_line_count()+1
		if (type(start_index) == str): start_index = float(start_index) #fuck
		if (type(stop_index) == str): stop_index = float(stop_index) #this
		if (type(start_index) == float): start_index = int(start_index)	#shit
		if (type(stop_index) == float): stop_index = int(stop_index) #am out
		if self.highlighting:
			for i in range(start_index, stop_index): #+1 because the last line doesn't get highlighted
				self.highlighter.highlight(i)

	def unhighlight_chunk(self, arg=None, start_index=None, stop_index=None):
		if (not start_index): start_index = 1
		if (not stop_index): stop_index = self.get_line_count()+1
		for i in range(start_index, stop_index): #+1 because the last line doesn't get highlighted
			self.highlighter.unhighlight(i)

	def note_mode(self):
		self.highlighting = False

	def retro_mode(self):
		pass



root = tkinter.Tk()
main_win = win(root)


if __name__ == '__main__':
	main_win.main()
	root.quit()
	
