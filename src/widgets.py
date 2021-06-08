import subprocess
import threading
import datetime
import tkinter
import time
import json
import os
import re
import platform
platform = platform.system()

from tkinter import font, PhotoImage
try: from PIL import ImageTk, Image
except Exception: pass

from highlighter import *

if (platform == "Windows"):
	ctypes.windll.shcore.SetProcessDpiAwareness(True)
	CONTROL_KEYSYM = 262156
	WINDOW_MARGIN = 0
	LINE_END = "\r\n"
else:
	CONTROL_KEYSYM = None
	WINDOW_MARGIN = 24
	LINE_END = "\n"

def bind_keys_from_config(widget, filename=f"{os.path.dirname(__file__)}/keybinds_conf.json"):
	keybinds = json.load(open(filename, "r"))
	widget_name = type(widget).__name__
	for val in keybinds[widget_name]["parent"].items():
		widget.bind(val[0], getattr(widget.parent, val[1]))
	for val in keybinds[widget_name]["self"].items():
		widget.bind(val[0], getattr(widget, val[1]))

class BUFFER_TAB(tkinter.Label):
	def __init__(self, name: str, parent):
		super().__init__(parent.buffer_tab_frame)
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)

		self.buffer_index = len(self.parent.file_handler.buffer_list)
		self.parent.file_handler.buffer_tab_index = self.buffer_index

		self["text"] = f" {self.name} "

		self.font = self.parent.widget_font
		self.update()
		
		if (self.buffer_index > 1):
			self.reposition(self.parent.file_handler.buffer_list[self.buffer_index-1][1])
		elif (self.buffer_index == 1):
			self.reposition()

		self.menu = tkinter.Menu(self.parent)
		self.menu.configure(font=self.font, tearoff=False, fg="#FFFFFF", bg=self.parent.theme["window"]["bg"], bd=0)
		self.menu.add_command(label="Close", command=lambda: self.parent.file_handler.close_buffer(buffer_name=self.full_name))

		self.bind("<Button-1>", self.load_buffer)
		# self.bind("<Enter>", lambda arg: self.hover_info.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height()), print("aa"))
		self.bind("<Enter>", lambda arg: self.parent.notify(self.full_name))
		# self.bind("<Leave>", lambda arg: self.hover_info.place_forget())
		self.bind("<Button-3>", lambda arg: self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty()+self.winfo_height()))
		# self.bind("<FocusIn>", lambda arg: self.parent.file_handler.load_buffer(buffer_name=self.name))

	def configure_self(self, arg=None):
		self.configure(text=f"{self['text']}", font=self.font, 
		 bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["widget_fg"],
		 highlightcolor=self.parent.theme["window"]["widget_fg"])
		
		self.menu.configure(font=self.font, tearoff=False,fg="#FFFFFF",
		 bg=self.parent.theme["window"]["bg"], bd=0)
		# self.hover_info.configure(text=self.full_name, font=self.font, fg="#FFFFFF", bg=self.parent.theme["window"]["bg"], bd=1)

	def reposition(self, last_buffer_tab=None):
		self.pack(fill="both", side="left")
		self.tkraise()

	def unplace(self):
		self.pack_forget()

	def change_name(self, new_name: str=None, extra_char: str = ""):
		if (new_name): self.full_name = new_name; self.name = os.path.basename(new_name)
		self.configure(text=extra_char+self.name+" ")

	def load_buffer(self, arg=None):
		
		self.parent.file_handler.load_buffer(buffer_name=self.full_name)

	def focus_highlight(self):
		self.configure(bg=self.parent.theme["window"]["widget_fg"], fg=self.parent.theme["window"]["bg"])


class BUFFER(tkinter.Frame):
	def __init__(self, parent, name):
		super().__init__(parent)
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)
		self.buffer_index = len(self.parent.file_handler.buffer_list)

		self.font_size = 11
		self.smaller_font_size = self.font_size - 2
		self.font_weight = "normal"
		self.font = self.parent.font
		self.font_bold = self.parent.font_bold

		self.bind("<Control-N>", self.parent.file_handler.new_file)
		self.bind("<Control-n>", self.parent.file_handler.new_file)
		self.bind("<Control-B>L", self.parent.file_handler.load_file)
		self.bind("<Control-b>l", self.parent.file_handler.load_file)
		self.bind("<Control-B>W", lambda arg: self.parent.file_handler.close_buffer(arg, self.full_name))
		self.bind("<Control-b>w", lambda arg: self.parent.file_handler.close_buffer(arg, self.full_name))
		self.bind("<Control-w>", self.parent.win_destroy)
		self.bind("<Control-W>", self.parent.win_destroy)
		self.bind("<Control-B><Delete>", lambda arg: self.parent.file_handler.del_file(arg, self.full_name))
		self.bind("<Control-b><Delete>", lambda arg: self.parent.file_handler.del_file(arg, self.full_name))
		self.bind("<Control-E>", lambda arg: self.parent.command_out_set("\n".join(self.parent.command_out.out[-1:])))
		self.bind("<Control-e>", lambda arg: self.parent.command_out_set("\n".join(self.parent.command_out.out[-1:])))

		self.bind("<Control-Tab>", self.switch_buffer_next)
		try: #linux bindings that throw errors on windows
			self.bind("<Control-Shift-ISO_Left_Tab>", self.switch_buffer_prev)
			self.parent.command_entry.bind("<KP_Enter>", self.parent.cmmand)
		except Exception:
			self.bind("<Control-Shift-Tab>", self.switch_buffer_prev)

		self.bind("<Control-space>", self.parent.command_entry_place)
		self.bind("<Control-Alt-space>", lambda arg: self.parent.command_out_set(resize=True))
		self.bind("<Alt-Right>", self.parent.win_expand)
		self.bind("<Alt-Left>", self.parent.win_expand)
		self.bind("<Alt-Up>", self.parent.win_expand)
		self.bind("<Alt-Down>", self.parent.win_expand)
		self.bind("<Alt-Shift-Right>", self.parent.win_shrink)
		self.bind("<Alt-Shift-Left>", self.parent.win_shrink)
		self.bind("<Alt-Shift-Up>", self.parent.win_shrink)
		self.bind("<Alt-Shift-Down>", self.parent.win_shrink)

		self.bind("<F1>", lambda arg: self.bell())
		self.bind("<F2>", lambda arg: self.insert("insert", self.get_time()))
		self.bind("<F3>", lambda arg: self.parent.video_handler.screenshot())
		self.bind("<F11>", self.parent.set_fullscreen)

	def configure_self(self):
		self.configure(bg = self.parent.theme["window"]["bg"], relief="flat", highlightthickness=0, cursor="pirate")

	def change_name(self, name):
		self.full_name = name
		self.name = os.path.basename(name)

	def switch_buffer(self, arg=None, next = True) -> str:
		if (next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index+1

		elif (not next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index-1

		if (buffer_tab_index >= len(self.parent.file_handler.buffer_list)):
			buffer_tab_index = 1

		elif (buffer_tab_index < 1):
			buffer_tab_index = len(self.parent.file_handler.buffer_list)-1
		
		self.parent.file_handler.load_buffer(buffer_index=buffer_tab_index)
		self.parent.notify(f"buffer [{self.parent.txt.name}] was loaded", tags=[["1.7", "1.8", "logical_keywords"], ["1.8", f"1.{8+len(self.parent.txt.name)}"], [f"1.{8+len(self.parent.txt.name)}", f"1.{9+len(self.parent.txt.name)}", "logical_keywords"]])

		return "break"

	def switch_buffer_prev(self, arg=None):
		self.switch_buffer(next=False)
		return "break"

	def switch_buffer_next(self, arg=None):
		self.switch_buffer()
		return "break"

class GRAPHICAL_BUFFER(BUFFER):
	def __init__(self, parent, name):
		super().__init__(parent, name)
		self.orig_img = None
		self.img = None
		self.picture_place()

		self.bind("<Control-period>", lambda arg: self.picture_resize(zoom=True))
		self.bind("<Control-comma>", lambda arg: self.picture_resize(zoom=False))

	def picture_place(self, arg=None):
		if (not self.orig_img):
			self.orig_img = Image.open(self.full_name)
			self.orig_img_size = [self.orig_img.size[0], self.orig_img.size[1]]
			self.orig_img = self.orig_img.resize(self.orig_img_size, Image.ANTIALIAS)
			
			self.img_size = [self.orig_img.size[0], self.orig_img.size[1]]
		
		self.img = self.orig_img.resize(self.img_size, Image.ANTIALIAS)
			
		self.img_resized = ImageTk.PhotoImage(self.img)
		self.img_label = tkinter.Label(self, image=self.img_resized)
		self.img_label.image = self.img_resized
		
		self.img_label.place(x=0, y=0, width=self.parent.winfo_width(), height=self.parent.winfo_height())
		self.img_label.configure(bg = self.parent.theme["window"]["bg"], relief="flat", highlightthickness=0, cursor="pirate")
		
		self.bind("<Configure>", self.picture_place)

	def picture_resize(self, arg=None, zoom=True):
		if (zoom): self.img_size[0] += 10; self.img_size[1] += 10;
		else: self.img_size[0] -= 10; self.img_size[1] -= 10;

		self.picture_place()

class DEFAULT_TEXT_BUFFER(tkinter.Text):
	def __init__(self, parent, name):
		super().__init__(parent.text_buffer_frame)

		self["padx"] = 2
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)
		self.buffer_index = len(self.parent.file_handler.buffer_list)

		self.font_size = 11
		self.smaller_font_size = self.font_size - 2
		self.font_weight = "normal"
		self.font = self.parent.font
		self.font_bold = self.parent.font_bold
		
		self.block_cursor = True
		self.terminal_like_cursor = True
		self.cursor_mode = 1

		self.blink = False
		self.insert_offtime = 0; self.insert_ontime = 1

		self.tag_configure("overstrike", overstrike=True)
		self.tag_configure("underline", underline=True)
		self.tag_configure("left", justify="left")
		self.tag_configure("center", justify="center")
		self.tag_configure("right", justify="right")
		self.tag_configure("error_bg", background="#990088") # for now it's here

		self.bind("<Control-period>", self.font_size_set)
		self.bind("<Control-comma>", self.font_size_set)
		self.bind("<Control-MouseWheel>", self.font_size_set)
		self.bind("<Control-Button-4>", self.font_size_set)
		self.bind("<Control-Button-5>", self.font_size_set)
		
		self.bind("<Insert>", self.cursor_mode_set)

		self.bind("<Control-space>", self.parent.command_entry_place)
		self.bind("<Control-Alt-space>", lambda arg: self.parent.command_out_set(resize=True))
		self.bind("<Alt-Right>", self.parent.win_expand)
		self.bind("<Alt-Left>", self.parent.win_expand)
		self.bind("<Alt-Up>", self.parent.win_expand)
		self.bind("<Alt-Down>", self.parent.win_expand)
		self.bind("<Alt-Shift-Right>", self.parent.win_shrink)
		self.bind("<Alt-Shift-Left>", self.parent.win_shrink)
		self.bind("<Alt-Shift-Up>", self.parent.win_shrink)
		self.bind("<Alt-Shift-Down>", self.parent.win_shrink)

		self.bind("<F1>", lambda arg: self.bell())
		self.bind("<F2>", lambda arg: self.insert("insert", self.get_time()))
		self.bind("<F3>", lambda arg: self.parent.video_handler.screenshot())
		self.bind("<F11>", self.parent.set_fullscreen)

	def remove_all_tags(self, index1, index2):
		self.tag_remove("overstrike", index1, index2)
		self.tag_remove("underline", index1, index2)
		self.tag_remove("left", index1, index2)
		self.tag_remove("center", index1, index2)
		self.tag_remove("right", index1, index2)

	def unplace(self, arg=None):
		""" hides command entry widget 'tis a kinda useless function"""
		self.place_forget()
		self.parent.txt.focus_set()
		return "break"

	def font_size_set(self, arg=None):
		""" Changes font size and reconfigures widget accordingly """
		if (arg):
			if (arg.delta > 120 or arg.delta < -120): arg.delta=0 
			
			if (arg.keysym == "period" or arg.num == 4 or arg.delta > 0):
				self.font_size += 1
			elif (arg.keysym == "comma" or arg.num == 5 or arg.delta < 0):
				self.font_size -= 1
	
			if (self.font_size <= 0):
				self.font_size = 1
			elif (self.font_size >= 150):
				self.font_size = 150

		self.font = font.Font(family=self.parent.font_family[0], size=self.font_size, weight=self.font_weight)
		self.font_bold = font.Font(family=self.parent.font_family[0], size=self.font_size, weight="bold")

		self.configure(font=self.font, tabs=(f"{self.font.measure(' ' * self.parent.tab_size)}"))
		self.see("insert")
		self.parent.theme_make()
		return "break"

	def cursor_highlight(self):
		pass

	def line_highlight(self):
		pass

	def terminal_highlight(self):
		try: self.configure(insertbackground=self.parent.theme["highlighter"][self.tag_names("insert")[-2]]) #Checks if there are any tags available on current character and if so it sets the cursor color to that tag 
		except Exception: self.configure(insertbackground=self.parent.theme["window"]["insertbg"])
		self.tag_configure("cursor", foreground=self.parent.theme["window"]["bg"])

	def normal_highlight(self):
		self.configure(insertbackground=self.parent.theme["window"]["insertbg"])
		self.tag_configure("cursor", foreground=self.parent.theme["window"]["bg"])

	def cursor_mode_set(self, arg=None):
		""" Insert """
		self["insertwidth"] = 0
		self["insertbackground"] = self.parent.theme["window"]["insertbg"]
		self.cursor_mode += 1
		if (self.cursor_mode >= 3):
			self.cursor_mode = 0
			
		if (self.cursor_mode == 0): #LINE
			self.block_cursor = False
			self.cursor_highlight = self.line_highlight
			self.tag_delete("cursor")
			self["insertwidth"] = 1
			
		elif (self.cursor_mode == 1): #NORMAL BLOCK
			self.block_cursor = True
			self.cursor_highlight = self.normal_highlight

		elif (self.cursor_mode == 2): #TERMINAL-LIKE BLOCK
			self.block_cursor = True
			self.cursor_highlight = self.terminal_highlight
		
		else:
			self.cursor_mode = 2
			self.block_cursor = True
			self.cursor_highlight = self.normal_highlight

		self.cursor_highlight()
		self.tag_add("cursor", "insert")
		self["blockcursor"] = self.block_cursor
		return "break"

	def cursor_xy_get(self, arg=None):
		return self.parent.txt.bbox('insert')[:2]

	def cursor_coords_get(self, arg=None):
		return self.parent.txt.bbox('insert')

class COMMAND_ENTRY(DEFAULT_TEXT_BUFFER):
	def __init__(self, parent, name="COMMAND_ENTRY"):
		super().__init__(parent, name)

		self.font_size = 9
		self.smaller_font_size = self.font_size - 2
		self.font_weight = "normal"
		self.font = self.parent.smaller_font
		self.font_bold = self.parent.smaller_font_bold
		
		self.input_history = [""]
		self.input_history_index = 0		

		self.bind("<Return>", self.parent.cmmand) #if you press enter in command line it executes the command and switches you back to text widget
		self.bind("<Shift-Return>", self.insert_newline)
		self.bind("<KP_Enter>", self.parent.cmmand) #if you press enter in command line it executes the command and switches you back to text widget
		self.bind("<Shift-KP_Enter>", self.insert_newline)
		self.bind("<Up>", self.history) # lets you scroll through commands you have already used
		self.bind("<Down>", self.history)
		self.bind("<Escape>", self.unplace)
		self.bind("<KeyRelease>", self.on_key)

	def configure_self(self, arg=None):
		self.font_size_set()
		self.configure(font=self.font, bg = self.parent.theme["window"]["bg"], fg=self.parent.theme["highlighter"]["logical_keywords"], undo=True, maxundo=0,
		 insertborderwidth=0, insertwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, borderwidth=2, relief="ridge", tabs=(f"{self.font.measure(' ' * self.parent.tab_size)}"), wrap="word", exportselection=True,
		 blockcursor=self.block_cursor, highlightthickness=0, cursor="xterm")

	def on_key(self, arg=None) -> None:
		self.parent.txt.highlighter.command_highlight()
		self.see("insert")

	def insert_newline(self, arg=None) -> str:
		self.insert("insert", "\n")
		return "break"

	def history(self, arg=None):
		""" scroll through used commands with Up and Down arrows(?) """
		self.delete("1.0", "end")
		try:
			if (arg.keysym == "Up"):
				self.input_history_index += 1
			else:
				self.input_history_index -= 1
			
			if (self.input_history_index <= 0):
				self.input_history_index = len(self.input_history)+1

			elif (self.input_history_index > len(self.input_history)):
				self.input_history_index = len(self.input_history)

			last_command = self.input_history[-self.input_history_index]
			self.insert("1.0", last_command)
			self.mark_set("insert", f"insert lineend")
			
		except IndexError:
			self.input_history_index = 0
			self.delete("1.0", "end")

		return "break"	

class FIND_ENTRY(DEFAULT_TEXT_BUFFER):
	def __init__(self, parent, name="FIND_ENTRY"):
		super().__init__(parent, name)
		
		self.font_size = 9
		self.smaller_font_size = self.font_size - 2
		self.font_weight = "bold"
		self.font = self.parent.smaller_font_bold
		self.font_bold = self.parent.smaller_font_bold

		self.find_history = []
		self.find_history_index = 0
		self.found = []
		self.found_index = 0

		self.mode = "<search>"

		self.bind("<Return>", self.find)
		self.bind("<KP_Enter>", self.find)
		self.bind("<Up>", self.scroll_through_found)
		self.bind("<Down>", self.scroll_through_found)
		self.bind("<Shift-Up>", self.scroll_through_find_history)
		self.bind("<Shift-Down>", self.scroll_through_find_history)
		self.bind("<Escape>", self.unplace)

		self.bind("<Control-R>", self.mode_change)
		self.bind("<Control-r>", self.mode_change)
		self.bind("<Control-F>", self.mode_change)
		self.bind("<Control-f>", self.mode_change)
		self.bind("<Control-A>R", self.replace_all)
		self.bind("<Control-a>r", self.replace_all)

		self.bind("<Control-Shift-Z>", self.parent.undo)
		self.bind("<Control-Shift-z>", self.parent.undo)
		self.bind("<Control-Shift-Y>", self.parent.redo)
		self.bind("<Control-Shift-y>", self.parent.redo)
		
		self.bind("<Configure>", self.parent.find_place)

	def configure_self(self, arg=None) -> None:
		self.font_size_set()
		self.configure(font=self.font,bg = self.parent.theme["window"]["bg"], fg=self.parent.theme["highlighter"]["upcase_b"], undo=True, maxundo=0,
		 spacing1=0, insertborderwidth=0, insertwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, borderwidth=1, relief="flat", tabs=(f"{self.font.measure(' ' * self.parent.tab_size)}"), wrap="none", exportselection=True,
		 blockcursor=self.block_cursor, highlightthickness=0, cursor="xterm")

	def mode_change(self, arg=None):
		self.delete("1.0", "end")
		if (self.mode == "<search>"):
			self.replace_mode_set()

		elif (self.mode == "<replace>"):
			self.find_mode_set()
			
		self.parent.command_out_set(f"{self.mode}")
		

		return "break"

	def find_mode_set(self, arg=None):
		self.mode = "<search>"
		if (self.get("1.0") not in ["?", "/"]): self.insert("1.0", "?")
		self.bind("<Return>", self.find)
		self.bind("<KP_Enter>", self.find)
		self.unbind("<Control-Z>")
		self.unbind("<Control-z>")
		
	def replace_mode_set(self, arg=None):
		self.mode = "<replace>"
		self.bind("<Return>", self.replace)
		self.bind("<KP_Enter>", self.replace)
		self.bind("<Control-Z>", self.parent.undo)
		self.bind("<Control-z>", self.parent.undo)

	def find_match(self, keyword, start="match_end", end="end", regexp=False, count=None):
		if (count == None):
			count = tkinter.IntVar()
		index = self.parent.txt.search(keyword, start, end, regexp=regexp, count=count)
		if (index == ""): return None
		if (count.get()) == 0: return None # degenerate pattern which matches zero-lenght strings
		return [ index, self.parent.txt.index(f"{index}+{count.get()}c") ]

	def find(self, arg=None, keyword=None, regexp=None):
		"""  """
		if (not regexp):
			if (regexp := self.get("1.0", "1.1") == "?"):
				self.regexp = False
			elif (regexp := self.get("1.0", "1.1") == "/"):
				self.regexp = True
			else:
				self.regexp = False
				keyword = self.get("1.0", "end-1c")
			
		if (not keyword): keyword = self.get("1.1", "end-1c")

		self.find_history.append(self.get("1.0", "end-1c"))

		for index in self.found:
			self.parent.txt.tag_remove("found_select_bg", index[0], index[1])
			self.parent.txt.tag_remove("found_bg", index[0], index[1])

		self.found_index = 0
		self.found = []
		self.find_query = keyword
		
		self.parent.txt.mark_set("match_end", "1.0")

		count = tkinter.IntVar()
		while True:
			if (index := self.find_match(keyword, start="match_end", end="end", regexp=self.regexp, count=count)):
				self.parent.txt.mark_set("match_end", index[1])
				self.found.append(index)
			else: break
		
		for index in self.found:
			self.parent.txt.tag_add("found_bg", index[0], index[1])

		self.parent.txt.mark_unset("match_end")
		self.scroll_through_found()
		return "break"

	def replace(self, arg=None):
		result_count = len(self.found)
		match = self.parent.txt.get(self.found[self.found_index][0], self.found[self.found_index][1])
		self.parent.command_out_set(f"{self.found_index+1} out of {result_count} results : {self.found[self.found_index]} match: {match} {self.mode}")
				
		start, end = self.found[self.found_index][0], self.found[self.found_index][1]
		self.parent.txt.delete(start, end)
		self.parent.txt.insert(start, self.get("1.0", "end-1c"))
		# self.parent.highlight_chunk(start_index=start, stop_index=end)
		self.parent.txt.highlighter.highlight(line_no=self.parent.txt.convert_line_index("int", start))
		f = self.found.pop(self.found_index)
		
		# fixes offset in line caused by replacing previous matches in line
		# I just hope it doesn't create any additional bugs, cuz I am too lazy to test ;) too bad
		if (match := self.find_match(keyword=self.find_query, start=f"{f[0]} wordstart", end=f"{f[0]} lineend", regexp=self.regexp)):
			self.found[self.found_index] = match

		self.scroll_through_found()

		return "break"

	def replace_all(self, arg=None):
		if (self.mode == "<replace>"):
			for i in range(len(self.found)):
				self.replace(arg)

			return "break"

	def scroll_through_found(self, arg=None):
		result_count = len(self.found)
		offset = 0
		if (result_count == 0): self.parent.command_out_set(f"found none"); return "break"

		if (arg):
			self.parent.command_out.place_forget()
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
			self.parent.txt.tag_remove("sel", index[0], index[1])
			self.parent.txt.tag_remove("underline", index[0], index[1])
		
		self.parent.txt.mark_set("insert", self.found[self.found_index][1])
		self.parent.txt.mark_set(self.parent.txt.mark_names()[-1], self.found[self.found_index][0])
		self.parent.txt.see(float(self.found[self.found_index][0])+offset)
		self.parent.txt.tag_add("sel", self.found[self.found_index][0], self.found[self.found_index][1])
		self.parent.txt.tag_add("underline", self.found[self.found_index][0], self.found[self.found_index][1])
		
		match = self.parent.txt.get(self.found[self.found_index][0], self.found[self.found_index][1])		
		self.parent.command_out_set(f"{self.found_index+1} out of {result_count} results : {self.found[self.found_index]} match: {match} {self.mode}")
		
		return "break"

	def scroll_through_find_history(self, arg=None):
		self.delete("1.0", "end")
		try:
			if (arg.keysym == "Up"):
				self.find_history_index += 1
			else:
				self.find_history_index -= 1
			
			if (self.find_history_index <= 0):
				self.find_history_index = len(self.find_history)+1

			elif (self.find_history_index > len(self.find_history)):
				self.find_history_index = len(self.find_history)

			last_input = self.find_history[-self.find_history_index]
			self.insert("1.0", last_input)

			self.mark_set("insert", f"1.0 lineend")
			self.see("insert")
			
		except IndexError:
			self.find_history_index = 0
			self.delete("1.0", "end")

		return "break"

	def unplace(self, arg=None):
		self.parent.txt.tag_remove("found_bg", "1.0", "end")
		self.parent.txt.tag_remove("underline", "1.0", "end")
		
		self.delete("1.0", "end")
		self.place_forget()
		self.parent.txt.focus_set()
		self.found_index = 0
		self.found = []
	

class COMMAND_OUT(DEFAULT_TEXT_BUFFER):
	#DUNNO who tf wrote this, but they were a complete piece of shit ......................................
	def __init__(self, parent, name="COMMAND_OUT"):
		super().__init__(parent, name)

		self.font_bold = self.parent.font_bold
		self.font = self.parent.smaller_font_bold
		self.font_size = 9
		self.font_weight = "bold"

		self.arg = ""
		self.modified_arg = ""

		self.tags = []
		self.selected_lines = []
		self.out = []

		self.input = ""
		self.input_label = tkinter.Label(self)
		self.input_label.configure(bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"])
		self.input_label.pack()

		self.bind("<KeyPress>", self.add_input)
		self.bind("<Down>", self.scroll)
		self.bind("<Up>", self.scroll)
		self.bind("<Prior>", self.scroll)
		self.bind("<Next>", self.scroll)
		
		self.bind("<Escape>", self.unplace)
		# self.bind("<Control-w>", self.parent.win_destroy)
		# self.bind("<Control-W>", self.parent.win_destroy)
		self.bind("<Control-b>w", self.unplace)
		self.bind("<Control-B>W", self.unplace)
		self.bind("<Button-1>", lambda arg: self.focus_set())

		self.bind("<Control_L>", self.add_selection)
		self.bind("<Return>", self.use_selection)
		self.bind("<Shift-Return>", lambda arg: self.use_selection())
		self.bind("<KP_Enter>", self.use_selection)
		self.bind("<Shift-KP_Enter>", lambda arg: self.use_selection())

	def configure_self(self, arg=None):
		self.font_size_set()
		self.configure(font=font.Font(family=self.parent.font_family[0], size=self.font_size,
		 weight=self.font_weight), bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 spacing3=5, cursor="left_ptr", relief="ridge", borderwidth=2, highlightthickness=0, wrap="word") # cursor="trek"

	def add_input(self, arg):
		if (arg.keysym == "BackSpace"):
			self.input = self.input[:-1]

		elif (arg.keysym == "space"):
			self.input += " "
			
		else:
			self.input += arg.char

		self.modified_stdout(self.arg, self.tags)
		self.show_input()

	def show_input(self):
		self.input_label.configure(text=self.input)

		if (self.input == ""): self.input_label.forget(); return
		self.input_label.pack()

		self.modified_arg = []

		self.mark_set("match_end", "1.0")
		
		count = tkinter.IntVar()
		while (True):
			index = self.search(self.input, "match_end", "end", count=count)
			if (index == ""): break
			if (count.get()) == 0: break
			self.mark_set("match_end", index+" lineend")
			self.modified_arg.append(self.get(index+" linestart", index+" lineend"))

		self.mark_unset("match_end")
		result, tags = self.parent.file_handler.highlight_ls(self.modified_arg)
		self.modified_stdout(result, tags)

	def unplace(self, arg=None):
		self.parent.txt.focus_set()
		self.place_forget()

	def scroll(self, arg):
		key = arg.keysym
		self["state"] = "normal"
		
		if (key == "Up"):
			self.mark_set("insert", "insert linestart-1c")
			self.see("insert")

		elif (key == "Down"):
			self.mark_set("insert", "insert lineend+1c")
			self.see("insert")

		elif (key == "Prior"):
			self.mark_set("insert", "1.0")
			self.see("insert")

		elif (key == "Next"):
			self.mark_set("insert", "end linestart")
			self.see("insert")

		self.tag_remove("command_out_insert_bg", "1.0", "end")
		self.tag_add("command_out_insert_bg", "insert linestart", "insert lineend")
		self["state"] = "disabled"

		return "break"
		
	def stdout(self, arg=None, tags=None, justify="left"):
		if (not arg): arg = self.arg
		if (not tags): tags = self.tags
		self["state"] = "normal"
		self.input = ""
		
		self.show_input()
		del self.tags[:]
		
		self.arg = arg
		if (len(arg.split("\n")) >= 2 and arg != self.out[-1:]): self.out.append(arg) # I can't compare arg and self.out[-1], because it throws an error, but this is fine apparently
		self.delete("1.0", "end")
		self.insert("1.0", self.arg)
		self.mark_set("insert", "1.0")
		self.tag_add(justify, "1.0", "end")

		if (tags):
			self.tags = tags
			for tag in tags:
				if tag[2:]: self.tag_add(tag[2], tag[0], tag[1])
				else: self.tag_add("keywords", tag[0], tag[1])

			else: [self.tag_add("keywords", tag[0], tag[1]) for tag in tags]

		self["state"] = "disabled"

	def modified_stdout(self, arg=None, tags=None, justify="left"):
		self.configure(state="normal")
		self.delete("1.0", "end")
		self.insert("1.0", arg)
		self.mark_set("insert", "1.0")
		self.tag_add(justify, "1.0", "end")

		if (tags):
			for tag in tags:
				if tag[2:]: self.tag_add(tag[2], tag[0], tag[1])
				else: self.tag_add("keywords", tag[0], tag[1])

			else: [self.tag_add("keywords", tag[0], tag[1]) for tag in tags]

		self.tag_add("command_out_insert_bg", "insert linestart", "insert lineend")

		self.configure(state="disabled")

	def change_ex(self, new_ex):
		self.ex = new_ex

	def add_selection(self, arg=None):
		if (arg):
			self.tag_add("command_out_select_bg", "insert linestart", "insert lineend")
			for i, line in enumerate(self.selected_lines, 0):
				if (line == self.get("insert linestart", "insert lineend")):
					self.selected_lines.pop(i)
					self.tag_remove("command_out_select_bg", "insert linestart", "insert lineend")
					return "break"
			
		self.selected_lines.append(self.get("insert linestart", "insert lineend"))

		return "break"
			
	def use_selection(self, arg=None):
		if (arg): self.add_selection()
		self.ex(self.selected_lines)
		self.input = ""
		self.show_input()
		del self.selected_lines[:]

		return "break"

	def open_line(self, arg=None):
		num_results = []
		for line in arg:
			if (re.search(r"line [0-9]+", line)):
				match = re.search(r"line [0-9]+", line).group()[5:]
			elif (re.search(r"[0-9]+", line)):
				match = re.search(r"[0-9]+", line)

			if (match):
				index = self.parent.txt.convert_line_index("float", match)
				self.parent.txt.mark_set("insert", index)
				self.parent.txt.see("insert")
		
		return "break"
		
	def file_explorer(self, arg=None):
		for line in arg:
			line = f"{self.parent.file_handler.current_dir}/{line}"
			line.replace(" ", r"\ ")
			if (os.path.isfile(line)):
				self.parent.file_handler.load_file(filename=line)
			elif (os.path.isdir(line)):
				self.parent.file_handler.current_dir = os.path.normpath(line)
				self.parent.file_handler.ls()
			
		return "break"

	def buffer_load(self, arg=None):
		arg=arg[0]
		self.parent.file_handler.load_buffer(buffer_name=arg)
		self.unplace()

	def task_set(self, arg=None):
		# how the fuck am I supposed to handle the index bullshit???
		pass

class SUGGEST_WIDGET(DEFAULT_TEXT_BUFFER):
	def __init__(self, parent, name="SUGGEST_WIDGET"):
		super().__init__(parent, name)
		self.insert("1.0", "COMPLETELY ARBITARY TEXT")

	def suggest(self, arg=None) -> None:
		coords = self.parent.txt.bbox("insert")
		self.place(x=coords[0]+coords[3], y=coords[1]+50, width=100, height=100)
		self.tkraise()

	def unplace(self, arg=None) -> None:
		self.place_forget()
		self.delete("1.0", "end")

class TEXT(DEFAULT_TEXT_BUFFER):
	def __init__(self, parent, name):
		super().__init__(parent, name)
		
		self.make_argv = ""
		self.highlighter = highlighter(self.parent, self)
		self.set_highlighter()
		self.cursor_highlight = self.normal_highlight

		self.clipboard_register = ""
		self.sel_start = None
		self.moving_index = "1.0" # I should be using the inbuilt tkinter text marks, but that would've probably fucked up other things I am too lazy to fix
		self.typing_index = "1.0"
		self.cursor_index = ["1", "0"]
		self.queue = []
		self.current_line = ""

		# self.text_len = ""
		self.change_index = ""
		self["wrap"] = "none"

		bind_keys_from_config(self)

	def configure_self(self, arg=None) -> None:
		self.font_size_set()
		self.configure(font=self.font, bg = self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"], undo=True, maxundo=0,
		 spacing1=0, insertborderwidth=0, insertwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, borderwidth=2, relief="ridge", tabs=(f"{self.font.measure(' ' * self.parent.tab_size)}"), wrap=self["wrap"], exportselection=True,
		 blockcursor=self.block_cursor, highlightthickness=0, cursor="xterm")

	def configure_wrap(self, arg=None) -> None:
		if (self["wrap"] == "none"):
			self["wrap"] = "word"
		else:
			self["wrap"] = "none"

		self.see("insert")

	def convert_to_lf(self):
		self.replace_x_with_y("\r", "", True)

	def convert_to_crlf(self):
		self.convert_to_lf()
		self.replace_x_with_y("\n", "\r\n", True)

	def convert_line_index(self, type: str, index=None):
		""" gets the cursor's position """
		if (not index): index = self.cursor_index[0]
		if (type == "int"): return int(float(index))
		elif (type == "float"): return float(index)

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
		self.sel_start = None
		self.mark_unset(self.mark_names()[-1])
		self.tag_remove("sel", "1.0", "end")

	def queue_get(self, arg=None):
		self.queue = [self.convert_line_index("int", self.sel_start), self.convert_line_index("int", self.index("insert"))]
		self.queue.sort()
		return self.queue[0], self.queue[1] + 1

	def moving(func): #something something event queue something
		def wrapped_func(self, *args, **kwargs):
			self.tag_remove("cursor", "1.0", "end")
			func(self, *args, **kwargs)
			self.tag_add("cursor", "insert")
			self.cursor_highlight()
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
			self.event_generate(f"<<{prefix}Prev{suffix[0]}>>")
			self.see(self.convert_line_index("float")-5)

		elif (key == "Down"):
			self.event_generate(f"<<{prefix}Next{suffix[0]}>>")
			self.see(self.convert_line_index("float")+5)

		elif (key == "Left"):
			self.event_generate(f"<<{prefix}Prev{suffix[1]}>>")

		elif (key == "Right"):
			self.event_generate(f"<<{prefix}Next{suffix[1]}>>")

		if (prefix == ""): self.sel_start = None; del self.queue[:]
		else: self.sel_start = self.index(self.mark_names()[-1])
		self.parent.update_index()
		# if (self.focus_displayof() == self): self.file_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.settings_menubar_label.configure(bg=self.theme["window"]["bg"], fg=self.theme["window"]["widget_fg"]); self.command_out.place_forget()

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
		self.event_generate("<<Cut>>")
		return "break"
		
	@moving
	def undo(self, arg=None):
		""" Control-Z """
		chunk_size = self.get_line_count()
		self.event_generate("<<Undo>>")
		start_index = self.convert_line_index("int")
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.parent.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	@moving
	def redo(self, arg=None):
		""" Control-Y """
		chunk_size = self.get_line_count()
		self.event_generate("<<Redo>>")
		start_index = self.convert_line_index("int")
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.parent.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	@moving
	def copy(self, arg=None):
		""" Control-C """
		self.event_generate("<<Copy>>")
		return "break"

	@moving
	def paste(self, arg=None):
		""" Control-V """
		to_paste = self.clipboard_get()
		start_index = self.convert_line_index("int", self.index("insert"))
		self.insert("insert", to_paste)
		self.parent.highlight_chunk(start_index=start_index, stop_index=self.convert_line_index("int", self.index("insert")))

		self.event_generate("<<SelectNone>>")
		return "break"

	def select_all(self, arg=None):
		""" Control-A """
		self.event_generate("<<SelectAll>>")
		return "break"

	@moving
	def home(self, arg=None):
		""" Home """
		index = ""
		i = 0
		for i, char in enumerate(self.current_line, 0):
			if (not re.match(r"\s", char)): index = f"{self.cursor_index[0]}.{i}"; break
		
		if (self.index("insert") == index): self.event_generate("<<LineStart>>")
		else: self.mark_set("insert", index)
		self.event_generate("<<SelectNone>>")
		return "break"

	@moving
	def home_select(self, arg=None):
		""" Shift-Home """
		index = ""
		i = 0
		for i, char in enumerate(self.current_line, 0):
			if (not re.match(r"\t", char)): index = f"{self.cursor_index[0]}.{i}"; break

		if (self.index("insert") == index):
			self.event_generate("<<SelectLineStart>>")
		
		elif (self.index("insert") != index):
			self.event_generate("<<SelectLineStart>>")
			[self.event_generate("<<SelectNextChar>>") for i in range(i)]
		return "break"

	@moving
	def end(self, arg=None):
		self.event_generate("<<LineEnd>>")
		self.event_generate("<<SelectNone>>")
		return "break"

	@moving
	def end_select(self, arg=None):
		self.event_generate("<<SelectLineEnd>>")
		return "break"

	@moving
	def mouse_left(self, arg=None):
		self.mark_set("insert", "current")
		self.del_selection()
		self.parent.update_buffer()
		return "break"

	def mouse_left_motion(self, arg=None):
		if (not self.sel_start):
			self.sel_start = self.index("insert")
		self.mark_set("insert", "current")
		self.parent.update_buffer()

	def change_case(self, arg=None):
		self.sel_start = self.index(self.mark_names()[-1])
		index_range = [self.sel_start, self.index("insert")]

		index_range = self.inline_index_sort(*index_range)
		
		if (arg.state == 20): # without shift
			text = self.get(index_range[0], index_range[1])
			self.delete(index_range[0], index_range[1])
			text = text.lower()
			self.insert(index_range[0], text)

		elif (arg.state == 21): # shift
			text = self.get(index_range[0], index_range[1])
			self.delete(index_range[0], index_range[1])
			text = text.upper()
			self.insert(index_range[0], text)

		self.parent.highlight_chunk(start_index=float(index_range[0]), stop_index=float(index_range[1]))

		del index_range
		del text
		return "break"

	def char_enclose(self, arg=None) -> str:
		self.sel_start = self.index(self.mark_names()[-1])
		index = self.inline_index_sort(self.index("insert"), self.sel_start)

		if (arg.keysym == "parenleft"): c1 = "("; c2 = ")"
		elif (arg.keysym == "bracketleft"): c1 = "["; c2 = "]"
		elif (arg.keysym == "braceleft"): c1 = "{"; c2 = "}"
		elif (arg.keysym == "apostrophe" or arg.keysym == "quotedbl"): c1 = "\""; c2 = "\""
		self.insert(index[1], c2)
		self.insert(index[0], c1)

		return "break"

	def comment_line(self, arg=None) -> str:
		""" I wish I knew what the fuck is going on in here I am depressed """
		
		start_index, stop_index = self.queue_get()

		comment_len = len(self.highlighter.comment_sign)

		for line_no in range(start_index, stop_index):
			current_line = self.get(float(line_no), f"{line_no}.0 lineend+1c")
			for i, current_char in enumerate(current_line, 0):
				if (self.highlighter.commment_regex.match(current_char+current_line[i+1:i+1+comment_len])):
					if (self.get(f"{line_no}.{i+comment_len}", f"{line_no}.{i+1+comment_len}") == " "):
						self.delete(f"{line_no}.{i}", f"{line_no}.{i+1+comment_len}")
					else:
						self.delete(f"{line_no}.{i}", f"{line_no}.{i+comment_len}")
					break

				elif (not re.match("\s", current_char)):
					self.insert(f"{line_no}.{i}", self.highlighter.comment_sign+" ")
					break

		self.parent.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break" # returning "break" prevents system/tkinter to call default bindings

	def indent(self, arg=None):
		""" Tab """
		start_index, stop_index = self.queue_get()
		index = 0
		if (start_index+1 == stop_index): index = self.cursor_index[1]

		for line_no in range(start_index, stop_index):
			self.insert(f"{line_no}.{index}", "\t")

		return "break"
		
	def unindent(self, arg=None):
		""" Checks if the first character in line is \t (tab) and deletes it accordingly """
		start_index, stop_index = self.queue_get()

		for line_no in range(start_index, stop_index):
			if (re.match(r"\t", self.get(f"{line_no}.0", f"{line_no}.1"))):
				self.delete(f"{line_no}.0", f"{line_no}.1")
		
		return "break"

	@moving
	def scroll(self, arg, multiplier=1):
		""" scrolls through the text widget MouseWheel && Shift-MouseWheel for speedy scrolling """
		if (arg.num == 5 or arg.delta < 0):
			self.mark_set("insert", f"{int(self.cursor_index[0])+3*multiplier}.{self.cursor_index[1]}")
	
		elif (arg.num == 4 or arg.delta > 0):
			self.mark_set("insert", f"{int(self.cursor_index[0])-3*multiplier}.{self.cursor_index[1]}")
		
		# hides widgets that could be in the way
		self.focus_set()
		self.see("insert")
		
		self.del_selection()
		self.parent.update_index()

	@moving
	def scroll_fast(self, arg=None):
		self.scroll(arg, 3)

	@moving	
	def keep_indent(self, arg=None):
		""" gets the amount of tabs in the last line and puts them at the start of a new one """
		#this functions gets called everytime Enter/Return has been pressed
		self.see(self.convert_line_index("float")+3)
		offset = LINE_END
		
		if (match := re.search(r"^\t+", self.current_line)):
			offset += match.group()

		# I am seeing a lot of horrible code in this project
		# sometimes I look back at my code and wonder if I am insane
		# magic with brackets
		# basically automatic indenting
		if (re.match(r"[\:]", self.get("insert-1c"))): 
			self.insert(self.index("insert"), offset+"\t")
			
		elif (re.match(r"[\{\[\(]", self.get("insert-1c"))):
			if (re.match(r"[\}\]\)]", self.get("insert"))):
				self.insert(self.index("insert"), offset+"\t"+offset)
				self.mark_set("insert", f"insert-{len(offset)}c")
			else:
				self.insert(self.index("insert"), offset+"\t")
				
		elif (re.match(r"[\{\[\(]", self.get("insert"))):
			if (re.match(r"[\}\]\)]", self.get("insert+1c"))):
				self.insert(self.index("insert"), offset)
				self.mark_set("insert", "insert+1c")
				self.insert(self.index("insert"), offset+"\t"+offset)
				self.mark_set("insert", f"insert-{len(offset)}c")
			else:
				self.insert(self.index("insert"), offset)
				self.mark_set("insert", f"insert+{len(offset)+2}c")
		
		else:
			if (re.match(r"\t+(\n|\r\n)", self.current_line)):
				self.delete(f"{self.cursor_index[0]}.0", "insert") #removes extra tabs if the line is empty
			self.insert(self.index("insert"), offset)
		
		return "break"

	def get_line_count(self, arg=None):
		""" returns total amount of lines in opened text """
		return sum(1 for line in self.get("1.0", "end").split("\n"))

	def get_word_count(self, arg=None):
		t = self.get("1.0", "end-1c")
		return [len(t.split(" ")), len(t)/5]

	def get_selection_count(self, arg=None):
		self.parent.notify(f"len: {len(self.selection_get())}")
		return "break"

	def change_name(self, name) -> None:
		self.full_name = name
		self.name = os.path.basename(name)

	def empty_break(self, arg=None):
		return "break"

	def delete_selection_start_index(self, arg=None) -> None:
		""" This has to be a function and I hate it """
		self.sel_start = None
		self.parent.update_index()

	def get_time(self, arg=None) -> None:
		date = datetime.date.today()
		day_name = datetime.date.today().strftime("%A")
		return f"{self.highlighter.comment_sign} ~\t[ {day_name} ] [ {self.parent.get_time()} ] [ {date} ] "

	def replace_x_with_y(self, x, y, arg=None, regexp=False) -> None: #replace spaces with tabs for example
		self.mark_set("match_end", "1.0")
		
		count = tkinter.IntVar()
		while True:
			index = self.search(x, "match_end", "end", regexp=regexp, count=count)
			if (index == ""): break
			if (count.get()) == 0: break # degenerate pattern which matches zero-lenght strings
			self.mark_set("match_end", self.index(f"{index}+{count.get()}c"))
			self.delete(index, "match_end")
			self.insert(index, y)
		self.mark_unset("match_end")

	def buffer_clipboard_set(self, arg=None, text=None):
		if (arg and not text):
			text = self.get(self.sel_start, self.index("insert"))
		self.buffer_clipboard = text
		
		if (arg): return "break"

	def buffer_clipboard_paste(self, arg=None):
		self.insert("insert", self.buffer_clipboard)
		if (arg): return "break"

	def delete_prev_word(self, arg=None):
		self.delete("insert-1c wordstart", "insert-1c wordend")
		if (arg): return "break"

	def delete_next_word(self, arg=None):
		self.delete("insert wordstart", "insert wordend")
		if (arg): return "break"

	def delete_line(self, arg=None):
		self.delete("insert linestart", "insert lineend")
		if (arg): return "break"

	def moving_index_set(self, arg=None, index="insert"):
		self.moving_index = self.index(index)
		if (arg): return "break"

	def typing_index_set(self, arg=None, index="insert"):
		index = self.index(index)
		self.typing_index = index
		if (arg): return "break"

	def jump_to_moving_index(self, arg=None):
		tmp_index = self.index("insert")
		self.mark_set("insert", self.moving_index)
		self.see(self.moving_index)
		self.moving_index = tmp_index
		
		if (arg): return "break"

	def jump_to_typing_index(self, arg=None):
		tmp_index = self.index("insert")
		self.mark_set("insert", self.typing_index)
		self.see(self.typing_index)
		self.typing_index = tmp_index
		
		if (arg): return "break"

	def jump_to_scope_start(self, arg=None):
		if (arg): return "break"

	def jump_to_scope_end(self, arg=None):
		if (arg): return "break"

	def selection_index_swap(self, arg=None):
		swp_index = self.index("insert")
		self.mark_set("insert", self.sel_start)
		self.mark_set(self.mark_names()[-1], swp_index)
		self.sel_start = swp_index
		self.see("insert")
		
		if (arg): return "break"

	def split_args(self, arg=None):
		pass

	def move_to_scope_start(self, arg=None):
		pass

	def move_to_scope_end(self, arg=None):
		pass

	def set_highlighter(self) -> None:
		""" sets the highlighter accordingly to the current file extension """
		try: arg = self.name.split(".")[-1]
		except Exception: arg = "NaN"

		self.parent.highlighting = True
		self.highlighter.set_languague(arg)

	def unplace(self):
		self.place_forget()

	def switch_buffer(self, arg=None, next = True) -> str:
		# if (self.parent.split_mode != 0):
			# return "break"
			
		if (next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index+1

		elif (not next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index-1

		if (buffer_tab_index >= len(self.parent.file_handler.buffer_list)):
			buffer_tab_index = 1

		elif (buffer_tab_index < 1):
			buffer_tab_index = len(self.parent.file_handler.buffer_list)-1
		
		self.parent.file_handler.load_buffer(buffer_index=buffer_tab_index)

		return "break"

	def switch_buffer_prev(self, arg=None):
		self.switch_buffer(next=False)
		return "break"

	def switch_buffer_next(self, arg=None):
		self.switch_buffer()
		return "break"

	def list_buffer(self, arg=None):
		self.parent.file_handler.list_buffer()
		return "break"

	def run_subprocess(self, argv=None, make=False) -> str:
		if (make):
			argv = self.make_argv.split(" ")
			self.parent.command_out.change_ex(self.parent.command_out.open_line)
		
		def run():
			process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			out = process.stdout.read().decode("UTF-8")

			self.parent.command_out_set(out)
			print(out)
			
		threading.Thread(target=run, daemon=True).start()
		return "break"

	def run_make(self, arg=None):
		return self.run_subprocess(make=True)

