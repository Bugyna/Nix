import tkinter
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

import math

import re
import json

import subprocess

import requests
try: from bs4 import BeautifulSoup # usually don't get imported when running as root
except Exception: pass
	
import random
import threading
import sys
import pytz
from importlib import reload as importlib_reload

try: import psutil # usually don't get imported when running as root
except Exception: pass

from highlighter import *
from command_parser import *
from util import *

from inspect import isclass

WINDOW_MARGIN = 0
if (platform == "Windows"):
	import ctypes
	ctypes.windll.shcore.SetProcessDpiAwareness(True)
elif (platform == "Linux"):
	WINDOW_MARGIN = 24 # weird GTK fuckery

CRLF="\r\n"
LF="\n"

class WIN(tkinter.Tk):
	# """
	# this whole project is very weird and I made a lot of pretty bad decisions,
	# but ultimately it's working (at least a bit on Linux anyways) 
	# It lags a lot on macOS and Windows, because tkinter sucks with a lot of text
	# (especially with long lines) and can't process it very well, which makes it lag
	# also making a text editor in Python is a very questionable idea on it's own
	# it also isn't really optimized in any way at all
	# summary: this editor sucks, but I can use it better than other editors so I don't care
	# if you use mainly C, C++ check out 4coder (it's going to become free as of 1.7.2021),
	# it's a really cool editor
	# """
	def __init__(self, file=None):
		super().__init__()

		self.conf = {
			"theme": "spacey",
			"tab_size": 4,
			"orientate": "down",
			"backup_files": 0,
			"underline_pairs": 0,
			"font_size": 12,
			"smaller_font_size": 11,
			"command_entry_font_size": 11,
			"find_entry_font_size": 12,
			"command_out_font_size": 11,
			"suggest_widget_font_size": 11,
			"start_width": 80,
			"start_height": 32,
			"show_buffer_tab": 1,
			"line_end": LF,
			"suggest": 1,
			"font": "Consolas",
			"default_find_mode": "?",
			"username": "",
			"default_split_mode": "vertical",
			"keybinds_file": "keybinds_conf.json",
			"themes_file": "theme_conf.json",
			"show_speed": False,
			"show_temperature": True,
			"show_time": True,
			"show_line_no": True,
			"show_keypress": True,
			"show_buffer_name": True,
			"highlight_line": False,
			"cursor_style": 2,
			"allow_external_modules": 1,
			"allow_notifications": 1,
			"alpha": 100,
			"percentage_pos_func": self.get_abs_percentage_pos,
			"buffer_border_style": "ridge",
			"command_entry_border_style": "ridge",
			"command_out_border_style": "ridge",
			"find_border_style": "ridge",
			"suggest_widget_border_style" : "ridge",
			"supress_keybind_warning": 1,
			"find_on_key": 1,
			"timezone": "GMT-8",
		}

		self.split_mode_options = {
			"nosplit": self.nosplit,
			"v": self.split_vertical,
			"vertical": self.split_vertical,
			"h": self.split_horizontal,
			"horizontal": self.split_horizontal,
		}

		self.theme_options = load_themes(f'{SOURCE_PATH}/{self.conf["themes_file"]}')

		self.load_conf()

		self.widgets = []

		self.found = []
		self.found_index = 0

		self.fullscreen = False
		self.split_mode = "nosplit"

		self.subprocesses = []

		self.command_history = []
		
		self.run = True

		self.font_set()

		#configuring main window
		# self.wm_attributes("-type", "splash")
		self.resizable(True,True)
		# self.geometry(f"{self.font.measure(' ')*self.conf['start_width']}x{self.font.metrics('linespace')*self.conf['start_height']}")
		self.wm_minsize(20, 0)
		self.geometry("1080x720")
		self.update_win()

		# self.geometry(f"{self.winfo_width()}x{self.winfo_height()}+{self.winfo_x()+self.winfo_width()//2}+{(self.winfo_screenheight()-self.winfo_height())//2}") #CENTERING MAGIC #PROLLY DOESN'T WORK THOUGH

		# try: self.iconbitmap("icon.ico")
		# except Exception as e: print(e)
		try: self.tk.call('wm', 'iconphoto', self._w, tkinter.PhotoImage(file=f"{os.path.dirname(os.path.abspath(__file__))}/icon.png"))
		except Exception as e: print(e)

		self.canvas = tkinter.Canvas()
		self.buffer_tab_frame = tkinter.Frame(self)
		self.buffer_frame = tkinter.Frame(self)
		self.buffer_render_list = []
		self.buffer_render_index = 0

		self.buffer_tab_render_list = []
		# self.file_handler.buffer_tab.buffer_index or self.buffer.buffer_index is the index for this


		self.parser = PARSER(self)

		self.file_handler = FILE_HANDLER(self)
		# self.video_handler = VIDEO_HANDLER(self)
		# self.music_player = MUSIC_PLAYER(self)
		self.update_win()

		self.l = tkinter.Text(font=self.font, spacing1=0)
		for i in range(1000):
			self.l.insert("insert", f"{i}\n")
		self.l.place(x=-1, y=20, w=0, h=1000)
		self.time_label = tkinter.Label()
		self.time_label_value = tkinter.StringVar()
		self.time_label_value.set("0:0:0")
		self.temperature_label = tkinter.Label(text=self.get_rand_temperature())
		self.line_no = tkinter.Label()
		self.fps_label = tkinter.Label()
		self.key_label = tkinter.Label()
		self.buffer_name_label = tkinter.Label()

		self.buffer = None #file_handler.init functions uses this txt variable so if it's not declared before running the function it's going to break 
		self.file_handler.init(".scratch") #see handlers.py/FILE_HANDLER
		# self.curs = tkinter.Label(self.buffer, bg=self.theme["window"]["fg"])
		# self.buffer is only meant to be a pointer to the focused text buffer
		# this pointer points to buffer_render_list which is a list of pointers pointing to
		# text buffers stored in the file_handler.buffer_list
		
		# self.test_label = tkinter.Label(text="test")
		# self.buffer.window_create("1.0", window=self.test_label, stretch=1)
		# print(self.buffer.dlineinfo("1.0"))

		# see widgets.py
		self.find_entry = FIND_ENTRY(self)
		self.command_entry = COMMAND_ENTRY(self)
		self.command_out = COMMAND_OUT(self)
		self.suggest_widget = SUGGEST_WIDGET(self)
		self.suggest_widget.configure_self()
		self.prompt = BOX(self)

		self.load_modules()

		self.canvas.configure(bd=0, highlightthickness=0)
		self.buffer_tab_frame.configure(relief="ridge", borderwidth=0, highlightthickness=0)
		self.buffer_frame.configure(relief="flat", borderwidth=0, highlightthickness=0)

		self.time_label.configure(fill=None, anchor="w", justify="left")
		self.temperature_label.configure(fill=None, anchor="w")
		self.line_no.configure(fill=None, anchor="w", justify="left")
		self.fps_label.configure(fill=None, anchor="w", justify="left")
		self.key_label.configure(fill=None, anchor="w", justify="left")
		self.buffer_name_label.configure(fill=None, anchor="w", justify="left")

		self.command_entry.configure_self()
		self.find_entry.configure_self()
		self.command_out.configure_self()
		self.alpha_set(self.conf["alpha"])

		bind_keys_from_conf(self)

		self.reposition_widgets()
		self.theme_load()
		self.update_buffer()
		self.update_win()
		# self.command_out.unplace() # weird fucking bug making the output widget appear for basically no reason

		if (len(sys.argv) > 1): [self.file_handler.load_file(filename=os.path.abspath(arg)) for arg in sys.argv[1:]]; self.file_handler.load_buffer(buffer_index=1)

	def load_conf(self):
		# this is gross, but it works
		try: file = open(f"{SOURCE_PATH}/conf", "r"); conf = file.read(); file.close()
		except Exception: return

		for index, line in enumerate(conf.split("\n"), 1):
			if (line and line[0] != "#"): # checks if line isn't empty and if doesn't start with "#" signifying a comment
				line = line.split("=") # split the line into two sections
				line[0] = line[0].strip() # strip the spaces
				line[1] = line[1].strip()
				
				try: self.conf[line[0]] = globals()[line[1]]; continue # try if the second section is a global object
				except KeyError: pass
				
				try: self.conf[line[0]] = getattr(self, line[1]); continue # try if the second section is a object in this class
				except Exception: pass
				
				try:
					if (line[1][0] != "\""): self.conf[line[0]] = int(line[1]) # checks if the second section starts with a double quote (a string) and if it doesn't it signifies an integer
					else: self.conf[line[0]] = line[1].strip("\"") # otherwise it's a string (so we strip the excessive double quotes)
				except Exception as e: print(f"Error while loading conf file line: {index} \nErorr: {e}")

		self.theme = self.theme_options[self.conf["theme"]] # sets the theme
		self.alpha_set(self.conf["alpha"]) # sets the alpha
		self.conf["timezone"] = pytz.timezone("Etc/"+self.conf["timezone"])
		
		try: self.theme_load() # HACK: tries to load the theme, but the theme_load function errors at startup because the needed object aren't completely initialized
		except Exception: pass

	def add_module(self, name, _class):
		_class = _class(self)
		if (hasattr(_class, "importable") and getattr(_class, "importable")):
			setattr(self, name, _class)
			if (hasattr(_class, "type") and _class.type == "widget"):
				self.widgets.append(_class)

		else:
			del _class

	def load_modules(self, dir=None, reload=False):
		# who the fuck made python modules so stupid
		# java levels of abstraction
		if (not self.conf["allow_external_modules"]): return
		if (not dir): dir = f"{SOURCE_PATH}/modules" # if the dir is not specified we want to take the path of the source file
		else: dir = os.path.dirname(dir) if (not os.path.isdir(dir)) else dir # if the dir is specified we want to check if it's an actual directory and if it's a file we just use the path to the file
		print("Loading modules from: ", dir)
		if (not os.path.isdir(dir)): print("no modules directory"); return

		for file in os.listdir(dir): # iterate through the files in the modules directory
			if (os.path.isdir(file)): # recursively loads modules from subdirectories in the modules directory
				self.load_modules(dir=os.path.abspath(f"{dir}/{file}"))
				
			if (file[-3:] == ".py"):
				file = file[:-3] # take the (.py) extension out of the file name
				modules = __import__(f"modules.{file}") # import the "module" from the modules directory
				module = modules.__dict__[file] # get the exact file we're looking for
				if (reload): importlib_reload(module) # reload the module

				for attr in module.__dict__.keys(): # iterate through the attributes of the imported file
					c = getattr(module, attr) # get the attribute from the file
					if (isclass(c)): # check if there's a class declared in the file
						self.add_module(attr, c) # if it's a class we add it to self under the filename

				del modules # delete the reduntant stuff

	def reload_modules(self, dir=None):
		self.load_modules(dir, reload=True)
		
	def theme_make(self):
		for buffer in self.buffer_render_list: # because fuck effieciency, right?
			if (type(buffer) != TEXT): return # if the buffer isn't a text buffer we don't want to set these
			for item in self.theme["highlighter"].items(): # iterate through the theme
				if (type(item[1]) == str):
					if (item[0][-2:] == "bg"): # if the name ends with bg we want to create a tag that uses the color specified as a background color
						buffer.tag_configure(item[0], background=item[1], foreground=self.theme["window"]["bg"], font=buffer.font)
						buffer.tag_configure(item[0][:-3], foreground=item[1], font=buffer.font) # but we create a tag with the specified color as the foreground color
						
						self.command_out.tag_configure(item[0], background=item[1], foreground=self.theme["window"]["bg"], font=self.command_out.font) # do the same for the other text widgets
						self.command_out.tag_configure(item[0][:-3], foreground=item[1], font=self.command_out.font)
						self.suggest_widget.tag_configure(item[0][:-3], foreground=item[1], font=self.suggest_widget.font)
						
					elif (item[0][-2:] == "_b"): # bold
						buffer.tag_configure(item[0][:-2], foreground=item[1], font=buffer.font_bold)
						self.command_out.tag_configure(item[0][:-2], foreground=item[1], font=self.command_out.font_bold)
						self.suggest_widget.tag_configure(item[0][:-2], foreground=item[1], font=self.suggest_widget.font_bold)
						
					else: # normal tag
						buffer.tag_configure(item[0], foreground=item[1], font=buffer.font) # , borderwidth=2, relief="groove", bgstipple="gray75"
						self.command_out.tag_configure(item[0], foreground=item[1], font=self.command_out.font)
						self.suggest_widget.tag_configure(item[0], foreground=item[1], font=self.suggest_widget.font)
				else:
					try:
						item[1]["font"] = self.buffer.font
						item[1]["bold"]
						item[1]["font"] = self.buffer.font_bold
						item[1].pop("bold")
						 
					except KeyError: pass
					buffer.tag_configure(item[0], **item[1])
					item[1].pop("font")
					self.command_out.tag_configure(item[0], **item[1], font=self.command_out.font)
					self.suggest_widget.tag_configure(item[0], **item[1], font=self.suggest_widget.font)

		self.command_entry.tag_configure("command_keywords", foreground=self.theme["highlighter"]["command_keywords"])
		self.buffer.tag_raise("cursor")

	def theme_set(self, theme=None):
		if (type(theme) == list): theme = theme[-1] #failsave switch when selecting multiple themes through the command_out widget
		self.theme = self.theme_options[theme]
		self.theme_load() # load the theme
		self.highlight_chunk() # highlight with new theme

	def theme_load(self):
		self.theme_make() # create the tags used in text buffers

		# configure a whole lot of widgets
		self.configure(bg=self.theme["window"]["bg"], cursor=None)

		self.canvas.configure(bg=self.theme["window"]["bg"])
		self.buffer_tab_frame.configure(bg=self.theme["window"]["bg"])
		self.buffer_frame.configure(bg=self.theme["window"]["bg"])

		self.time_label.configure(font=self.widget_font, textvariable=self.time_label_value, bg = self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"])
		self.temperature_label.configure(font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.line_no.configure(font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.fps_label.configure(font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.key_label.configure(font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])
		self.buffer_name_label.configure(text=self.buffer.name, font=self.widget_font, bg = self.theme["window"]["bg"],fg=self.theme["window"]["widget_fg"])

		self.command_entry.configure_self()
		self.find_entry.configure_self()
		self.command_out.configure_self()
		self.suggest_widget.configure_self()
		self.prompt.configure_self()

		for buffer in self.buffer_render_list:
			buffer.configure_self()

		if (self.conf["show_buffer_tab"]):
			[buffer_tab.configure_self() for buffer_tab in self.file_handler.buffer_tab_list]
				
	
			if (self.file_handler.buffer_tab): self.file_handler.buffer_tab.focus_highlight()

		for widget in self.widgets:
			widget.configure_self()
		
		self.update_win()

	def font_set(self, arg=None, family=None):
		if (not family): family=self.conf["font"]
		self.font_family = [family, "normal", "bold", "roman"]

		self.font = font.Font(family=self.font_family[0], size=self.conf["font_size"], weight=self.font_family[1], slant=self.font_family[3])
		self.font_bold = font.Font(family=self.font_family[0], size=self.conf["font_size"], weight="bold", slant=self.font_family[3]) 
		self.smaller_font = font.Font(family=self.font_family[0],size=self.conf["smaller_font_size"], weight=self.font_family[1])
		self.smaller_font_bold = font.Font(family=self.font_family[0],size=self.conf["smaller_font_size"], weight="bold")
		self.widget_font = font.Font(family=self.font_family[0], size=self.conf["smaller_font_size"], weight=self.font_family[2])

		#lazy workaround
		try: self.theme_load() # fails on startup
		except Exception: pass

	def font_set_all(self, arg=None, size=None):
		self.conf["font_size"] = size
		self.conf["smaller_font_size"] = size - 2
		self.font_set()
		self.command_out.font_size = size
		self.command_out.smaller_font_size = size - 2
		self.command_out.font_size_set()

		self.find_entry.font_size = size
		self.find_entry.smaller_font_size = size - 2
		self.find_entry.font_size_set()
		
		self.command_entry.font_size = size
		self.command_entry.smaller_font_size = size - 2
		self.command_entry.font_size_set()
		self.file_handler.buffer_tab.font = self.widget_font
		self.file_handler.buffer_tab.configure_self()
		
		for b in self.file_handler.buffer_list:
			b[1].font = self.widget_font
			
			b[0].font_size = size
			b[0].smaller_font_size = size - 2
			b[0].font_size_set()

		for b in self.file_handler.buffer_tab_list:
			b.font = self.widget_font

		for widget in self.widgets:
			widget.font = self.widget_font
			widget.font_size = self.conf["smaller_font_size"]
			widget.configure_self()

		try: self.theme_load()
		except Exception: pass

	def get_color_from_theme(self, color, arg="foreground"):
		""" """
		res = None
		theme=self.theme["highlighter"]
		try:
			if (type(theme[color]) == dict):
				if (type(arg) == str):
					res = theme[color][arg]
					
				elif (type(arg) == list):
					for a in arg:
						res.append(theme[color][a])
						
			elif (type(theme[color]) == str):
				res = theme[color]
						
		except KeyError as e: print("error in get_color_from_theme: ", e); self.error(f"{e}")

		return res

	def alpha_set(self, arg=None):
		self.wm_attributes("-alpha", arg/100)

	def reposition_widgets(self, arg=None):
		btf_bd = self.buffer_tab_frame["bd"]+1 # border width
		fs = self.widget_font.metrics("linespace") # font height
		buffer_tab_y = fs//1.5+4
		txt_y = fs*2
		win_width = self.winfo_width()
		win_height = self.winfo_height()

		if (self.conf["show_buffer_tab"] and len(self.file_handler.buffer_list) > 0): # checks if we can show the buffer tabs in the config and if there are any buffers opened except the scratch buffer
			# x = self.file_handler.buffer_tab.winfo_x()
			# w = self.file_handler.buffer_tab.winfo_width()
			# if (x >= win_width or x + w >= win_width): 
				# self.buffer_tab_frame.place(x=-x, y=buffer_tab_y+btf_bd, width=win_width+x, height=fs+btf_bd+4, anchor="nw")
			# else:
			self.buffer_tab_frame.place(x=0, y=buffer_tab_y+btf_bd, width=win_width, height=fs+btf_bd+4, anchor="nw")
				
			self.buffer_frame.place(x=0, y=txt_y+btf_bd, relwidth=1, height=win_height-txt_y-btf_bd, anchor="nw")

			
		else:
			self.buffer_frame.place(x=0, y=buffer_tab_y, relwidth=1, height=win_height-buffer_tab_y, anchor="nw")	
	
		if (self.command_entry.winfo_viewable()): self.command_entry_place()
		if (self.command_out.winfo_viewable()): self.command_out_set(resize=True)
		if (self.find_entry.winfo_viewable()): self.find_place(resize=True)
		if (self.suggest_widget.winfo_viewable()): self.suggest(resize=True)
		if (self.prompt.winfo_viewable()): self.prompt.place_self()
		
		if (self.conf["show_time"]): self.time_label.place(x=self.temperature_label.winfo_x(), y=0, height=buffer_tab_y, anchor="ne")
		if (self.conf["show_temperature"]): self.temperature_label.place(x=self.line_no.winfo_x()-10, y=0, height=buffer_tab_y, anchor="ne")
		if (self.conf["show_line_no"]): self.line_no.place(x=self.winfo_width()-self.line_no.winfo_width()-10, y=0, height=buffer_tab_y, anchor="nw")
		if (self.conf["show_speed"]): self.fps_label.place(x=self.time_label.winfo_x()-10, y=0, height=buffer_tab_y, anchor="ne")
		if (self.conf["show_keypress"]): self.key_label.place(x=0, y=0, height=buffer_tab_y, anchor="nw")
		if (self.conf["show_buffer_name"]): self.buffer_name_label.place(x=self.buffer_frame.winfo_width()//2+self.buffer_name_label.winfo_width()//2, y=0, height=buffer_tab_y, anchor="ne")

		x = self.file_handler.buffer_tab.winfo_x()
		w = self.file_handler.buffer_tab.winfo_width()
		for buffer_tab in self.file_handler.buffer_tab_list:
			if (x >= win_width or x + w >= win_width):
				if (buffer_tab.buffer_index >= self.buffer.buffer_index):
					buffer_tab.reposition()
				else:
					buffer_tab.unplace()
			else:
				buffer_tab.reposition()

		for widget in self.widgets:
			widget.place_self()

		self.split_mode_options[self.split_mode]()

	def flashy_loading_bar(self, arg=None):
		def a():
			x = ""
			r = 100
			for i in range(r):
				time.sleep(0.2)
				x = "["+chr(9608)*i+"."*(r-i)+"]"
				self.notify(x, justify="center")

		threading.Thread(target=a, daemon=True).start()

	def split(self, arg=None):
		self.split_mode = self.conf["default_split_mode"]

		try:
			self.buffer_render_index += 1
			self.file_handler.load_buffer(buffer_index=self.buffer.buffer_index+1)
		except IndexError: pass
		self.reposition_widgets()

	def nosplit(self, arg=None):
		self.buffer_render_list[self.buffer_render_index].place(x=0, y=0, relwidth=1, relheight=1)

	def split_vertical(self, arg=None):
		w = round(1/len(self.buffer_render_list), 3)
		for i, buffer in enumerate(self.buffer_render_list, 0):
			buffer.place(relx=w*i, y=0, relwidth=w, relheight=1)

	def split_horizontal(self, arg=None):
		h = round(1/len(self.buffer_render_list), 3)
		for i, buffer in enumerate(self.buffer_render_list, 0):
			buffer.place(x=0, rely=h*i, relwidth=1, relheight=h)

	def win_destroy(self, arg=None) -> str:
		# self.file_handler.closing_sequence()
		self.run = False
		self.quit()
		return "break"

	def set_fullscreen(self, arg=None):
		""" set the window to be fullscreen F11 """
		self.fullscreen = not self.fullscreen
		self.attributes("-fullscreen", self.fullscreen)

		return "break"

	def win_minimize(self, arg=None):
		self.wm_state("iconic")

		return "break"

	def set_dimensions(self, arg=None, expand=True): # I do understand that this is a terrible, hideous thing but I couldn't come up with a better solution
		""" changes window size accordingly to keys pressed Alt-Curses """
		key = arg.keysym
		x, y = self.winfo_x(), self.winfo_y()
		if (expand):
			margin = 20
			if (key == "Right"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{x}+{y-WINDOW_MARGIN}")
			elif (key == "Left"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{x-margin}+{y-WINDOW_MARGIN}")
			elif (key == "Up"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{x}+{y-WINDOW_MARGIN-margin}")
			elif (key == "Down"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{x}+{y-WINDOW_MARGIN}")

		elif (not expand):
			margin = -20
			if (key == "Right"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{x-margin}+{y-WINDOW_MARGIN}")
			if (key == "Left"):
				self.geometry(f"{self.winfo_width()+margin}x{self.winfo_height()}+{x}+{y-WINDOW_MARGIN}")
			if (key == "Up"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{x}+{y-WINDOW_MARGIN}")
			if (key == "Down"):
				self.geometry(f"{self.winfo_width()}x{self.winfo_height()+margin}+{x}+{y-margin-WINDOW_MARGIN}")
		
		return "break"	

	def win_expand(self, arg=None):
		self.set_dimensions(arg)
		return "break"

	def win_shrink(self, arg=None):
		self.set_dimensions(arg, expand=False)
		return "break"

	def suggest(self, arg=None, resize=False):
		token = self.buffer.current_token.strip()
		
		if (not resize):
			if (re.match(r"[a-zA-Z_]+([0-9])*", token)):
				self.suggest_widget.delete("1.0", "end")
				
				longest_line = 0
				ret = ""
				
				for m in self.buffer.highlighter.vars + self.buffer.lexer.vars:
					if (re.match(token, m)):
						self.suggest_widget.insert("insert", m+"\n")
						if (len(m) > longest_line): longest_line = len(m)
						
				for m in self.buffer.highlighter.funcs + self.buffer.lexer.functions:
					if (re.match(token, m)):
						self.suggest_widget.insert("insert", m+"\n")
						self.suggest_widget.tag_add("functions", "insert -1l linestart", "insert -1l lineend")
						if (len(m) > longest_line): longest_line = len(m)
	
				for m in self.buffer.highlighter.keywords + self.buffer.highlighter.logical_keywords + self.buffer.highlighter.numerical_keywords:
					if (re.match(token, m)):
						self.suggest_widget.insert("insert", m+"\n")
						self.suggest_widget.tag_add("keywords", "insert -1l linestart", "insert -1l lineend")
						if (len(m) > longest_line): longest_line = len(m)

				self.suggest_widget.delete("end-1c")
				self.suggest_widget.mark_set("insert", "1.0")
				c = list(self.buffer.bbox("insert"))
				out_len = len(self.suggest_widget.get("1.0", "end").split("\n"))
				
				if (out_len <= 0):
					self.buffer.mode_set(mode="normal", force=True)
					self.buffer.focus_set()
					return
				
				self.buffer.mode_set(mode="suggest", force=True)
				self.suggest_widget.tkraise()
			
				if (out_len >= 15):
					h = 15*self.buffer.font.metrics("linespace")
				else:
					h = out_len*self.buffer.font.metrics("linespace")
	
				if (c[1]+h > self.winfo_height()): c[1] = self.winfo_height() - h - 100
				self.suggest_widget.place(x=c[0]+30, y=c[1], width=longest_line*self.buffer.font_size, height=h, anchor="nw")

			elif (len(self.suggest_widget.get("1.0", "end-2c").split("\n")) > 1):
				c = list(self.buffer.bbox("insert"))
				self.suggest_widget.place(x=c[0]+30, y=c[1])

		self.buffer.focus_set()

	def nt_place(self, arg=None): # why nt???
		self.command_out.change_ex(self.command_out.file_explorer)
		arg, tags = self.file_handler.highlight_ls()
		self.command_out_set(arg=arg, tags=tags, append_history=False)

	def popup(self, arg=None):
		""" gets x, y position of mouse click and places a menu accordingly """
		self.right_click_menu.tk_popup(arg.x_root+5, arg.y_root)

	def command_entry_place(self, arg=None):
		""" Shows command entry widget """
		h = self.command_entry.font.metrics("linespace") + (self.command_entry["pady"]+self.command_entry["bd"])*2
		y = self.buffer_frame.winfo_height()
			
		# if (self.command_entry["relief"] == "flat"): x = self.buffer["bd"]; w = self.buffer["bd"]; y -= self.buffer["bd"]
		# else: x = 0; w = 0
		# if (self.command_entry["relief"] == "flat"): y -= self.buffer["bd"]
		x = 0; w = 0
		
		if (self.conf["orientate"] == "down"): self.command_entry.place(x=x, y=y-h, width=self.buffer_frame.winfo_width()-w*2, height=h, anchor="nw")
		elif (self.conf["orientate"] == "up"): self.command_entry.place(x=-1, y=0, width=self.buffer_frame.winfo_width()-w, height=h, anchor="nw")
		
		self.command_out.place_forget()
		self.command_entry.tkraise(); self.command_entry.focus_set()
		
		return "break"

	def find_place(self, arg=None, text=None, resize=False):
		if (not resize):
			self.find_entry.start_index = self.buffer.index("insert")
			self.find_entry.find_mode_set(text=text)
			self.find_entry.tkraise(); self.find_entry.focus_set()

		h = self.find_entry.font.metrics("linespace") + (self.find_entry["pady"]+self.find_entry["bd"])*2
		
		# if (self.find_entry["relief"] == "flat"): x = self.buffer["bd"]; w = self.buffer["bd"]
		# else: x = 0; w = 0
		x = 0; w = 0
		
		self.find_entry.place(x=x, y=self.buffer_frame.winfo_height()-h-40, width=self.buffer_frame.winfo_width()-w*2, height=h, anchor="nw")

		return "break"

	def find_place_with_token(self, arg=None):
		self.find_place(text=self.buffer.current_token)

		return "break"

	def command_out_set(self, arg=None, tags=None, resize=False, focus=False, justify="left", append_history=True):
		# honestly this is a really shitty function, but it works somehow, so you shouldn't question it, if you poke around with it it's most probably going to break
		""" sets the text in command output """
		if (resize and self.command_out.arg == None):
			return
			
		elif (not resize):
			
			if (focus):
				if (self.focus_get() == self.buffer): self.buffer.focus_set()
				elif (self.focus_get() == self.find_entry): pass
			else:
				self.command_out.focus_set()
				if (append_history and arg): self.command_out.append_history(arg)

			self.command_out.stdout(arg=arg, tags=tags, justify=justify)

		lines = len(self.command_out.arg.split("\n"))
		font_size = (self.command_out.font.metrics("linespace")+self.command_out.cget("spacing3"))

		if (lines < 10):
			h = font_size*lines
		else:
			h = font_size*((self.winfo_height()//2)/font_size)

		# y = self.buffer_frame.winfo_height()
		# if (self.command_out["relief"] == "flat"): x = self.buffer["bd"]; w = self.buffer["bd"]; y -= self.buffer["bd"]
		# else: x = 0; w = 0; h += (self.command_out["bd"])
		if (self.command_out["relief"] != "flat"): h += (self.command_out["bd"])
		x = 0; w = 0; 

		self.command_out.tkraise()
		if (self.conf["orientate"] == "down"): self.command_out.place(x=x, y=self.buffer_frame.winfo_height(), width=self.buffer_frame.winfo_width()-w*2, height=h, anchor="sw")
		elif (self.conf["orientate"] == "up"): self.command_out.place(x=x, y=0, width=self.buffer_frame.winfo_width()-w*2, height=h, anchor="nw")
		
		return "break"

	def notify(self, arg=None, tags=None, justify="left"):
		# one hack after another
		self.command_out["state"] = "normal"
		self.command_out_set(arg=arg, tags=tags, focus=True, justify=justify, append_history=False)
		if (not self.conf["allow_notifications"]): self.command_out.unplace() # HACK
		self.command_out["state"] = "disabled"

	def error(self, arg=None, tags=None, justify="left"):
		tags = [["1.0", "1.6", "error"], tags] if tags else [["1.0", "1.6", "error"]]
		self.notify("Error: "+arg, tags, justify)

	def show_last_output(self, arg=None): 
		self.command_out_set(arg=None, tags=None)
		return "break"

	def cmmand(self, arg):
		# gets input from the command_entry widget, checks if there's any actual input or if it's an empty string
		# if it's not an empty string it sends it to the parser class and if it's a valid command defined in the "commands" dictionary
		# and if it's defined it runs the function related to that name
		""" """
		
		command = self.command_entry.get("1.0", "end-1c").split() #turns command into a list of arguments
		in_quote = False
		delimeter_start = 0
		
		for i in range(len(command)): # wonky path correction
			if (re.search(r"\\", command[i])):
				command[i] = command[i].replace("\\", " ")

			elif (len(re.findall(r"\"|'", command[i])) % 2 != 0):
				in_quote = not in_quote
				if (in_quote): delimeter_start = i
				else:
					sub = command[delimeter_start:i+1]
					del command[delimeter_start:i+1]
					command.insert(delimeter_start, " ".join(sub))
					command[delimeter_start] = command[delimeter_start].strip("\"'")
		
		if (not command): self.command_entry.unplace(); return #if no input/argument were provided hide the command entry widget and break function
		if (command != self.command_entry.input_history[-1]): self.command_entry.input_history.append(command)
		self.parser.parse_argument(command)

		#sets focus back to text widget
		self.buffer.see("insert")
		self.command_entry.delete("1.0", "end") #deletes command line input

		#set command history to newest index
		self.command_entry.input_history_index = 0
		self.command_entry.unplace()

	def buffer_unplace(self, arg=None):
		""" I have no idea why this is a separate function """
		try:
			for buffer in self.buffer_render_list:
				buffer.unplace()
		except Exception: pass

	def unplace_all_except_buffer(self, arg=None):
		self.command_entry.unplace()
		self.find_entry.unplace()
		self.command_out.unplace()

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
		self.temperature_label.configure(text=self.get_rand_temperature())
		# """ scrapes the current temperature of Stockholm """
		# def temp():
			# try:
				# url = "https://www.bbc.com/weather/2673730" #link to Stockholm's weather data
				# html = requests.get(url).content #gets the html of the url
				# x = "("+BeautifulSoup(html, features="html.parser").find("span", class_="wr-value--temperature--c").text+"C)" # looks for the temperature value and puts it in a string "([value and degree sign]C)"
				# self.temperature_label.configure(text=x)
			# except Exception: #dunno if it won't crash the app if there's no internet connection
				# self.temperature_label.configure(text=self.get_rand_temperature())

		# threading.Thread(target=temp, daemon=True).start()

	def get_time(self):
		""" gets time and parses to make it look the way I want it to """

		# d_time = datetime.datetime.now().time()
		# curr_time = time.localtime()
		time = datetime.datetime.now(self.conf["timezone"])
		d_time = time.strftime("%H:%M:%S")
		if (self.time_label_value.get().split(":")[2] == time.second): return # checks if it's still the same second as the last time the function was executed, not very efficient, but still more efficient than running a bunch of string formatting every few miliseconds
	
		if (time.minute == "00" and time.second == "10"): #checks if it's time for updating the temperature
			self.get_temperature()

		self.time_label_value.set(d_time)# return time #updates the time label/widget to show current time

	def get_abs_percentage_pos(self):
		return math.ceil(self.buffer.current_char_abs_pos*100/self.buffer.total_chars) # m(a)eth

	def get_line_relative_percentage_pos(self):
		return math.ceil(int(self.buffer.cursor_index[0])*100/self.buffer.total_lines) # this gotta be slow as shit

	def update_index(self, arg=None):
		# called upon every keypress
		if (self.buffer.index("insert") == self.buffer.sel_start): self.buffer.sel_start = None

		self.buffer.cursor_index = self.buffer.index("insert").split(".") # gets the cursor's position and makes it into a list [line, column]
		self.buffer.current_char_abs_pos = len(self.buffer.get("1.0", "insert"))
		
		# p = self.get_line_relative_percentage_pos()
		# p = self.get_abs_percentage_pos()
		p = self.conf["percentage_pos_func"]()
		self.line_no.configure(text=f"[{self.buffer.index('insert')}] {p}%") #updates the line&column widget to show current cursor index/position

		if (self.buffer.sel_start): # show selection index on the top of the window if a selection is active
			self.line_no.configure(text=f"[{self.buffer.index('sel.first')}][{self.buffer.index('sel.last')}] {p}%")

		self.buffer.highlighter.bracket_pair_make(self.buffer.get("insert")) # highlights matching brackets

		self.buffer.current_line = self.buffer.get(f"insert linestart", f"insert lineend+1c") #+1c so the line includes the newline character
		self.buffer.current_token = self.buffer.get("insert wordstart", "insert wordend")
		
		if (re.match(r"^\s+", self.buffer.current_token) and len(self.buffer.current_token) <= 1):
		# if (len(self.buffer.current_token) < 1):
			# self.buffer.current_token = self.buffer.get("insert -1c wordstart", "insert -1c wordend")
			self.buffer.current_token = self.buffer.get("insert wordstart -1c wordstart", "insert wordstart -1c wordend")
			# self.buffer.current_token = self.buffer.current_token.strip("\n")

		# elif (re.match(r"(.)+\s+$", self.buffer.current_token) and len(self.buffer.current_token) <= 1):
			# self.buffer.current_token = self.buffer.get("insert wordstart -1c wordstart", "insert wordstart -1c")
			# self.buffer.current_token = self.buffer.current_token.strip("\n")
			
		elif (self.buffer.current_token[0] == "\n"):
			self.buffer.current_token = self.buffer.get("insert wordstart +1c", "insert wordend")

		# elif (self.buffer.current_token == "\n"):
			# self.buffer.current_token = self.buffer.get("insert wordstart -1c wordstart", "insert wordstart -1c wordend")

			# if (len(self.buffer.current_token) <= 1): self.buffer.current_token = ""

		# print("token: ", self.buffer.current_token, self.buffer.index("insert wordstart"), self.buffer.index("insert wordend"))

		if (self.conf["highlight_line"]): self.buffer.tag_remove("whitespace_bg", "1.0", "end"); self.buffer.tag_add("whitespace_bg", "insert linestart", "insert lineend")
		self.buffer.see("insert")

		# mark_name = self.buffer.mark_names()[-1]
		# if (mark_name[:2] == "tk"):
			# coords = self.buffer.bbox(mark_name)
			# print(coords)
			
		# custom cursor thingy
		# coords = self.buffer.bbox("insert")
			# a = tkinter.Label(self.buffer)
			# a.place(x=coords[0], y=coords[1]-2, w=1, h=self.buffer.font.metrics("linespace"))
		# self.curs.place(x=coords[0]-2, y=coords[1]-2, w=1, h=self.buffer.font.metrics("linespace"))
		# self.curs.place(x=coords[0]-2, y=coords[1]+self.buffer.font.metrics("linespace")-2, w=self.buffer.font_size-3, h=1)
		# threading.Thread(target=t, args=(self.buffer.cursor_index[0],), deamon=True).start()
		# self.l.see(float(self.buffer.cursor_index[0])+20)
		if (arg): return "break"

	def update_buffer(self, arg=None):
		""" updates some of the widgets when a key is released """
		# called upon every keyrelease
		if (arg): # shows the characters that were released (eg. Control: D), but it can't handle more than one character (eg. Control: b-w)
			# print(chr(arg.state), chr(arg.keysym_num))
			if (re.match("Control|Alt|Shift", arg.keysym)): return # ignore keyrelease of Control Alt Shift etc.
			# text = re.sub("\|*Mod2", "", re.search("state=[a-zA-Z0-9\|]+", f"{arg}").group()[6:]) # magic with regex to show the keys you pressed in a nicer format
			# if (text): self.key_label["text"] = f"[{arg.state}: {arg.keysym}]"
			# else: self.key_label["text"] = f"[{arg.keysym}]"
			# self.key_label["text"] = f"[{arg.state}|{arg.keysym}]"
			self.key_label["text"] = f"[{arg.state}|{arg.keysym}]"
			if (arg.keysym in ("Up", "Down", "Left", "Right")): return # ends function if it was triggered by arrow keys (as they have different functions to handle them)
		
		self.update_index()
		# if (self.buffer.total_chars != len(self.buffer.get("1.0", "end"))): # checks if any changes have been made to the text
		if (self.buffer.edit_modified()):
			self.buffer.state_set(add="*")
			if (self.buffer.type != "temp" and self.buffer.file_start_time != os.stat(self.buffer.full_name).st_mtime):
				self.buffer.state_set(add="!")
			else:
				self.buffer.state_set(pop="!")
			
			self.buffer.total_chars = self.buffer.current_char_abs_pos+len(self.buffer.get("insert", "end"))
			# self.buffer.lexer.lex() # lex text for variables, functions, structures and class etc.
			self.buffer.typing_index_set() # Alt-Shift-M: sets your cursor to the position you were last typing in
			self.buffer.highlighter.highlight(self.buffer.cursor_index[0], self.buffer.current_line) # highlight current line

			# if the following widgets are not focused they are hidden
			if (self.focus_displayof() != self.command_entry):
				self.command_entry.place_forget()
			if (self.focus_displayof() != self.command_out):
				self.command_out.place_forget()

			if (self.conf["suggest"]): self.buffer.highlighter.suggest(self.buffer.cursor_index[0], self.buffer.current_line)
		
		self.update_win()


	def update_win(self):
		""" updates the window whole window (all of it's widgets) """
		self.update()
		self.update_idletasks()

	def main(self):
		""" reconfigures(updates) some of the widgets to have specific values and highlights the current_line"""
		self.buffer.focus_set()
		t0 = time.time(); self.c = 0
		counter = 0
		def a(counter=0): # some annoying notifications
			while (self.run):
				time.sleep(1)
				self.get_time()
				counter += 1
				if (counter == 1650):
					self.notify("POSTURE CHECK! You've been programming for half an hour now. Consider stretching for a bit")
				elif (counter == 3600):
					self.notify("You've been programming for an hour now. Consider taking a break")
					counter = 0
			# time.sleep(1650)
			# try:
			# self.notify("POSTURE CHECK! You've been programming for half an hour now. Consider stretching for a bit")
				# notify2.init("Nix")
				# notify2.Notification("POSTURE CHECK", "You've been programming for half an hour now. Consider stretching for a bit").show()
			# except Exception:
			# 	self.commmand_out_set("Consider downloading the notify2 module"); return
			# time.sleep(1650)
			# try:
			# self.notify("You've been programming for an hour now. Consider taking a break")
			# 	notify2.init("Nix")
			# 	notify2.Notification("BREAK TIME", "You've been programming for an hour now. Consider taking a break").show()
			# except Exception:
			# 	self.commmand_out_set("Consider downloading the notify2 module"); return
			# a()
			# self.after(0, self.get_time())

		# def b():
			# while (self.run):
				# time.sleep(1)
				# self.get_time()
				# self.fps_label.configure(text=f"<{round(self.c/1000, 2)}KHz>")
				# self.c = 0

		threading.Thread(target=a, daemon=True).start()
		# threading.Thread(target=b, daemon=True).start()
		
		# while (self.run):
			# self.update_win()
			# self.get_time()

			# if (int(time.time()-t0) >= 1): # updates the processor frequency value every second
				# def a():
					# self.fps_label.configure(text=f"<{round(psutil.cpu_freq().current/100*psutil.cpu_percent(), 2)}MHz> <{psutil.sensors_temperatures()['coretemp'][0].current}>")
				# threading.Thread(target=a, daemon=True).start()
				# t0 = time.time()

	def highlight_chunk(self, arg=None, start_index=None, stop_index=None):
		for buffer in self.buffer_render_list:
			if (not start_index): start_index = 1
			if (not stop_index): stop_index = buffer.get_line_count()
			buffer.convert_line_index("int", start_index)
			buffer.convert_line_index("int", stop_index)
			def highlight(text):
				for i in range(start_index, stop_index+1):
					text.highlighter.highlight(i)
					text.highlighter.lex_line(i)
			threading.Thread(target=highlight, args=(buffer, ), daemon=True).start()
		
	def unhighlight_chunk(self, arg=None, start_index=None, stop_index=None):
		for buffer in self.buffer_render_list:
			if (not start_index): start_index = 1
			if (not stop_index): stop_index = buffer.get_line_count()
			buffer.convert_line_index("int", start_index)
			buffer.convert_line_index("int", stop_index)
			def unhighlight():
				[buffer.highlighter.unhighlight(i) for i in range(start_index, stop_index+1)]
			threading.Thread(target=unhighlight, args=(buffer, ), daemon=True).start()


if __name__ == "__main__":
	win = WIN()
	win.after(0, win.main)
	win.mainloop()
	print("thank you for using Nix")



