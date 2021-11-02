import subprocess
import threading
import datetime
import tkinter
import time
import os
import re
import platform
platform = platform.system()

from tkinter import font, PhotoImage
try: from PIL import ImageTk, Image
except Exception: pass

from util import *
from highlighter import *


class BUFFER_TAB(tkinter.Label):
	def __init__(self, name: str, parent, render=True):
		super().__init__(parent.buffer_tab_frame)
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)
		self.render = render

		self.buffer_index = len(self.parent.file_handler.buffer_list)
		self.parent.file_handler.buffer_tab_index = self.buffer_index

		self["text"] = f" {self.name} "

		self.font = self.parent.widget_font
		self.update()
		
		# self.reposition()

		self.menu = tkinter.Menu(self.parent)
		self.menu.add_command(label="Close", command=lambda: self.parent.file_handler.close_buffer(buffer_name=self.full_name))

		self.bind("<Button-1>", self.load_buffer)
		# self.bind("<Enter>", lambda arg: self.hover_info.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height()), print("aa"))
		self.bind("<Enter>", lambda arg: self.parent.notify(self.full_name))
		# self.bind("<Leave>", lambda arg: self.hover_info.place_forget())
		self.bind("<Button-3>", lambda arg: self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty()+self.winfo_height()))
		# self.bind("<FocusIn>", lambda arg: self.parent.file_handler.load_buffer(buffer_name=self.name))

		self.configure_self()


	def configure_self(self, arg=None):
		self.font = self.parent.widget_font
		self.configure(text=f"{self['text']}", font=self.font,
		 bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["widget_fg"],
		 highlightcolor=self.parent.theme["window"]["widget_fg"])
		
		self.menu.configure(font=self.font, tearoff=False,fg="#FFFFFF",
		 bg=self.parent.theme["window"]["bg"], bd=0)
		# self.hover_info.configure(text=self.full_name, font=self.font, fg="#FFFFFF", bg=self.parent.theme["window"]["bg"], bd=1)

	def reposition(self, last_buffer_tab=None):
		if (self.render):
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
		self.configure(bg=self.parent.theme["window"]["bg"], relief=self.parent.conf["buffer_border_style"],
		 highlightthickness=0, cursor="pirate"
		)

	def change_name(self, name):
		self.full_name = name
		self.name = os.path.basename(name)

	def switch_buffer(self, arg=None, next = True) -> str:
		if (next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index+1

		elif (not next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index-1

		if (buffer_tab_index >= len(self.parent.file_handler.buffer_list)):
			buffer_tab_index = 0

		elif (buffer_tab_index < 0):
			buffer_tab_index = len(self.parent.file_handler.buffer_list)-1
		
		self.parent.file_handler.load_buffer(buffer_index=buffer_tab_index)
		self.parent.notify(f"buffer [{self.parent.buffer.name}] was loaded", tags=[["1.7", "1.8", "logical_keywords"], ["1.8", f"1.{8+len(self.parent.buffer.name)}"], [f"1.{8+len(self.parent.buffer.name)}", f"1.{9+len(self.parent.buffer.name)}", "logical_keywords"]])

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
		self.img_label.configure(bg = self.parent.theme["window"]["bg"], relief=self.parent.conf["buffer_border_style"], highlightthickness=0, cursor="pirate")
		
		self.bind("<Configure>", self.picture_place)


	def picture_resize(self, arg=None, zoom=True):
		if (zoom): self.img_size[0] += 10; self.img_size[1] += 10;
		else: self.img_size[0] -= 10; self.img_size[1] -= 10;

		self.picture_place()



class BOX(tkinter.Frame):
	def __init__(self, parent, name=None):
		super().__init__(parent.buffer_frame)
		self.parent = parent
		self.name = name
		self.options = []
		self.current_option = 0
		
		self.title = tkinter.Label(self)
		self.title.pack()
		self.set_title("TITLE")
		self.add_option("yes", lambda arg: print("yes"))
		self.add_option("no", lambda arg: print("no"))
	
		self.font = self.parent.widget_font
		
		self.update()
		self.configure_self()
		bind_keys_from_conf(self)

	
	def configure_self(self):
		self.font = self.parent.widget_font
		self.configure(bg=self.parent.theme["window"]["bg"],
			 highlightcolor=self.parent.theme["window"]["widget_fg"], relief="groove", bd=2)
			
		for p in self.winfo_children():
			p.configure(bg=self.parent.theme["window"]["bg"],
			 highlightcolor=self.parent.theme["window"]["widget_fg"])

			try: p["fg"] = self.parent.theme["window"]["fg"]
			except tkinter._tkinter.TclError: pass

	
	def place_self(self):
		x = self.parent.winfo_width()//2-100
		y = self.parent.winfo_height()//2-100
		self.place(x=x, y=y, width=200)

	
	def unplace(self, arg=None):
		self.place_forget()
		self.parent.buffer.focus_self()
		del self.options[:]

	
	def set_title(self, text=None):
		self.title["text"] = text

	
	def add_option(self, text, func_ptr, type="button"):
		if (type == "button"):
			ptr = PROMPT_OPTION(self.parent, self, len(self.options))
			ptr.set_text(text)
			ptr.set_execute(func_ptr)
			ptr.pack(expand=True, fill="x", side="left")
			ptr.focus_set()
			self.options.append(ptr)

	
	def focus_option(self, arg=None, next=True):
		if (len(self.options) <= 1): return
		if (next):
			if (self.current_option+1 < len(self.options)):
				self.options[self.current_option+1].focus_self()
			else:
				self.options[0].focus_self()

		else:
			if (self.current_option-1 >= 0):
				self.options[self.current_option-1].focus_self()
			else:
				self.options[len(self.options)-1].focus_self()

	def focus_option_next(self, arg=None):
		self.focus_option(arg)

	
	def focus_option_prev(self, arg=None):
		self.focus_option(arg, next=False)
			


class PROMPT_OPTION(tkinter.Label):
	def __init__(self, parent, render_parent, position):
		super().__init__(render_parent)
		self.parent = parent
		self.render_parent = render_parent
		self.position = position
		self.configure_self()
		self.focus_set()

		bind_keys_from_conf(self)

	def focus_self(self, arg=None):
		self.focus_set()
		self.render_parent.current_option = self.position

	def configure_self(self, arg=None):
		self.configure(bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"],
			 highlightcolor=self.parent.theme["window"]["widget_fg"])


	def unplace(self, arg=None):
		self.render_parent.unplace()


	def execute(self, arg=None):
		pass


	def set_execute(self, func_ptr, arg=None):
		# self.execute = func_ptr
		def func(*args, **kwargs):
			func_ptr(args)
			self.unplace()

		self.execute = func
		bind_keys_from_conf(self)


	def highlight(self, arg=None):
		self["bg"] = self.parent.theme["window"]["fg"]
		self["fg"] = self.parent.theme["window"]["bg"]
	
	def set_text(self, text):
		self["text"] = text



class DEFAULT_TEXT_BUFFER(tkinter.Text):
	def __init__(self, parent, name, type="normal"):
		# types: normal, readonly, temp
		super().__init__(parent.buffer_frame)
		if (type == "readonly"): self["state"] = "disabled"

		self.parent = parent
		self.type = type
		self.mode = "normal"

		self.full_name = name
		self.name = os.path.basename(name) if type != "temp" else name
		self.buffer_index = len(self.parent.file_handler.buffer_list)

		self.font_size = self.parent.conf["font_size"]
		self.smaller_font_size = self.font_size - 2
		self.font_weight = "normal"
		self.font = self.parent.font
		self.font_bold = self.parent.font_bold
		
		self.tag_configure("cursor")
		self.cursor_mode_set()

		self.blink = False
		self.insert_offtime = 0; self.insert_ontime = 1

		self.command_history = []

		self.tag_configure("overstrike", overstrike=True)
		self.tag_configure("underline", underline=True)
		self.tag_configure("left", justify="left")
		self.tag_configure("center", justify="center")
		self.tag_configure("right", justify="right")
		self.tag_configure("error_bg", background="#990088") # for now it's here
		
		bind_keys_from_conf(self)

	def remove_all_tags(self, index1, index2):
		self.tag_remove("overstrike", index1, index2)
		self.tag_remove("underline", index1, index2)
		self.tag_remove("left", index1, index2)
		self.tag_remove("center", index1, index2)
		self.tag_remove("right", index1, index2)

	def unplace(self, arg=None):
		""" hides command entry widget 'tis a kinda useless function"""
		self.place_forget()
		self.parent.buffer.focus_set()
		return "break"
	
	def focus_self(self, arg=None):
		self.focus_set()

	def empty_func(self, arg=None):
		return

	def empty_break(self, arg=None):
		return "break"

	def call_last_command(self, arg=None):
		if (self.parent.command_history):
			print("calling: ", self.parent.command_history[-1])
			self.parent.command_history[-1][0](self, self.parent.command_history[-1][1:])
			print("called: ", self.parent.command_history[-1])
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

		self.configure(font=self.font, tabs=(f"{self.font.measure(' ' * self.parent.conf['tab_size'])}"))
		self.see("insert")
		self.parent.theme_make()
		return "break"

	def cursor_highlight(self):
		pass

	def terminal_highlight(self):
		try: #Checks if there are any tags available on current character and if so it sets the cursor color to that tag 
			self["insertbackground"] = self.parent.theme["highlighter"][self.tag_names("insert")[-2]]
		except Exception:
			self["insertbackground"] = self.parent.theme["window"]["insertbg"]

	def normal_highlight(self):
		pass

	def cursor_mode_set(self, arg=None):
		""" Insert """
		self["insertwidth"] = 0
		self["insertbackground"] = self.parent.theme["window"]["insertbg"]
		
		if (arg):
			self.parent.conf["cursor_style"] += 1
		
		if (self.parent.conf["cursor_style"] >= 3):
			self.parent.conf["cursor_style"] = 0
			
		if (self.parent.conf["cursor_style"] == 0): #LINE
			self.block_cursor = False
			self.cursor_highlight = self.normal_highlight
			self.tag_delete("cursor")
			self.tag_configure("cursor")
			self["insertwidth"] = 1
			
		elif (self.parent.conf["cursor_style"] == 1): #NORMAL BLOCK
			self["insertbackground"] = self.parent.theme["window"]["insertbg"]
			self.tag_configure("cursor", foreground=self.parent.theme["window"]["bg"])
			self.block_cursor = True
			self.cursor_highlight = self.normal_highlight

		elif (self.parent.conf["cursor_style"] >= 2): #TERMINAL-LIKE BLOCK
			self.tag_configure("cursor", foreground=self.parent.theme["window"]["bg"])
			self.block_cursor = True
			self.cursor_highlight = self.terminal_highlight

		self["blockcursor"] = self.block_cursor
		self.tag_raise("cursor")
		self.cursor_highlight()
		self.tag_add("cursor", "insert")
		return "break"

	def cursor_xy_get(self, arg=None):
		return self.parent.buffer.bbox('insert')[:2]

	def cursor_coords_get(self, arg=None):
		return self.parent.buffer.bbox('insert')

	def insert_time(self, arg=None):
		self.insert("insert", self.get_time())

	def convert_line_index(self, type: str, index=None):
		""" gets the cursor's position """
		if (not index): index = self.cursor_index[0]
		if (type == "int"): return int(float(index))
		elif (type == "float"): return float(index)

	def get_line_index(self, index=None):
		if (not index): index = self.cursor_index[0]
		return int(float(index))

	def get_column_index(self, index=None):
		if (not index): index = self.cursor_index[1]
		return int(float(index))

	def index_sort(self, index1, index2):
		if (self.compare(index1, "<=", index2)): return (index1, index2)
		else: return (index2, index1)
		
	def multiline_index_sort(self, index1, index2):
		self.queue = [self.convert_line_index("int", index1), self.convert_line_index("int", index2)]
		self.queue.sort()
		return self.queue[0], self.queue[1] + 1

	def sameline_check(self, index1, index2):
		return self.compare(index1, "==", index2)
			
	def del_selection(self):
		self.sel_start = None
		self.mark_unset(self.mark_names()[-1])
		self.tag_remove("sel", "1.0", "end")

	def queue_get(self, arg=None):
		self.queue = [self.convert_line_index("int", self.index("sel.first")), self.convert_line_index("int", self.index("sel.last"))]
		self.queue.sort()
		return self.queue[0], self.queue[1] + 1

	def change_case(self, arg=None, case=None):
		index_range = [self.index("sel.first"), self.index("sel.last")]

		index_range = self.index_sort(*index_range)
		
		if (case == "lowercase"):
			text = self.get(index_range[0], index_range[1])
			self.delete(index_range[0], index_range[1])
			text = text.lower()
			self.insert(index_range[0], text)

		else:
			text = self.get(index_range[0], index_range[1])
			self.delete(index_range[0], index_range[1])
			text = text.upper()
			self.insert(index_range[0], text)

		self.parent.highlight_chunk(start_index=float(index_range[0]), stop_index=float(index_range[1]))

		del index_range
		del text
		return "break"

	def change_case_to_lowercase(self, arg=None):
		self.change_case(case="lowercase")
		
	def change_case_to_uppercase(self, arg=None):
		self.change_case(case="uppercase")

	def char_enclose(self, arg=None) -> str:
		self.sel_start = self.index(self.mark_names()[-1])
		index = self.index_sort(self.index("insert"), self.sel_start)

		if (arg.keysym == "parenleft"): c1 = "("; c2 = ")"
		elif (arg.keysym == "bracketleft"): c1 = "["; c2 = "]"
		elif (arg.keysym == "braceleft"): c1 = "{"; c2 = "}"
		elif (arg.keysym == "apostrophe" or arg.keysym == "quotedbl"): c1 = "\""; c2 = "\""
		self.insert(index[1], c2)
		self.insert(index[0], c1)
		self.mark_set("insert", f"insert -1{len(c2)}") # sets the insert cursor back the length of the string we're enclosing with

		return "break"

	def delete_prev_word(self, arg=None):
		self.delete("insert-1c wordstart", "insert-1c wordend")
		if (arg): return "break"

	def delete_next_word(self, arg=None):
		self.delete("insert wordstart", "insert wordend")
		if (arg): return "break"

	def delete_line(self, arg=None):
		self.delete("insert linestart", "insert lineend+1c")
		if (arg): return "break"

	def delete_line_before_cursor_tab_sensitive(self, arg=None):
		line = self.get("insert linestart", "insert")
		offset = 0
		for c in line:
			if (c == "\t"): offset += 1
			else: break

		if (re.match(r"^(\t)+$", line)): offset = 0
		
		self.delete(f"insert linestart +{offset}c", "insert")

		return "break"

	def delete_line_before_cursor(self, arg=None):
		self.delete("insert linestart", "insert")
		return "break"

	def delete_line_after_cursor(self, arg=None):
		self.delete("insert", "insert lineend")
		return "break"

class COMMAND_ENTRY(DEFAULT_TEXT_BUFFER):
	def __init__(self, parent, name="COMMAND_ENTRY"):
		super().__init__(parent, name)

		self.font_size = self.parent.conf["command_entry_font_size"]
		self.smaller_font_size = self.font_size - 2
		self.font_weight = "normal"
		self.font = self.parent.smaller_font
		self.font_bold = self.parent.smaller_font_bold
		
		self.input_history = [""]
		self.input_history_index = 0
		
		bind_keys_from_conf(self)

	def configure_self(self, arg=None):
		self.font_size_set()
		self.configure(font=self.font, bg = self.parent.theme["window"]["bg"], fg=self.parent.theme["highlighter"]["logical_keywords"], undo=True, maxundo=0,
		 insertborderwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, borderwidth=2, relief=self.parent.conf["command_entry_border_style"], tabs=(f"{self.font.measure(' ' * self.parent.conf['tab_size'])}"), wrap="char", exportselection=True,
		 blockcursor=self.block_cursor, highlightthickness=0, cursor="xterm")

		if (self["relief"] == "flat"): self["bd"] = 0
		else: self["bd"] = 2
		
	def on_key(self, arg=None) -> None:
		self.parent.buffer.highlighter.command_highlight()
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
		
		self.font_size = self.parent.conf["find_entry_font_size"]
		self.smaller_font_size = self.font_size - 2
		self.font_weight = "bold"
		self.font = self.parent.smaller_font_bold
		self.font_bold = self.parent.smaller_font_bold

		self.start_index = None

		self.find_history = []
		self.find_history_index = 0
		self.found = {}
		self.found_index = 0
		
		self.mode = "find"
		bind_keys_from_conf(self)

	def configure_self(self, arg=None) -> None:
		self.font_size_set()
		self.configure(font=self.font,bg = self.parent.theme["window"]["bg"], fg=self.parent.get_color_from_theme("upcase"), undo=True, maxundo=0,
		 spacing1=0, insertborderwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, borderwidth=2, relief=self.parent.conf["find_border_style"], tabs=(f"{self.font.measure(' ' * self.parent.conf['tab_size'])}"), wrap="none", exportselection=True,
		 blockcursor=self.block_cursor, highlightthickness=0, cursor="xterm")

		if (self["relief"] == "flat"): self["bd"] = 0
		else: self["bd"] = 2

	def mode_change(self, arg=None):
		self.delete("1.0", "end")
		if (self.mode == "find"):
			self.replace_mode_set()

		elif (self.mode == "replace"):
			self.find_mode_set()

		bind_keys_from_conf(self)	
		self.parent.notify(f"{self.mode}")

		return "break"


	def find_mode_set(self, arg=None, text=None):
		self.mode = "find"
		if (self.get("1.0") not in ["?", "/"]): self.insert("1.0", self.parent.conf["default_find_mode"])
		if (text): self.insert("end-1c", text)
		

	def replace_mode_set(self, arg=None):
		self.mode = "replace"


	def find_match(self, keyword, buffer=None, start="match_end", end="end", regexp=False, count=None):
		if (not count):
			count = tkinter.IntVar()

		if (not buffer):
			buffer = self.parent.buffer
			
		index = buffer.search(keyword, start, end, regexp=regexp, count=count)
		if (index == ""): return None
		if (count.get()) == 0: return None # degenerate pattern which matches zero-lenght strings
		return [ index, buffer.index(f"{index}+{count.get()}c") ]


	def find(self, arg=None, keyword=None, regexp=None):
		"""  """
		if (arg.keysym in ("Up", "Down", "Left", "Right")): return # ends function if it was triggered by arrow keys (as they have different functions to handle them)
		
		if (not regexp):
			if (regexp := self.get("1.0", "1.1") == "?"):
				self.regexp = False
			elif (regexp := self.get("1.0", "1.1") == "/"):
				self.regexp = True
			else:
				if (self.parent.conf["default_find_mode"] == "?"): self.regexp = False
				else: self.regexp = True
				keyword = self.get("1.0", "end-1c")
			
		if (not keyword): keyword = self.get("1.1", "end-1c")

		self.remove_tags()
		self.deselect_match()

		if (not self.parent.conf["find_on_key"]):
			self.append_history()
			self.found_index = 0

		self.found = {}
		for buffer in self.parent.buffer_render_list:
			self.found[buffer.full_name] = []
			
		self.find_query = keyword

		count = tkinter.IntVar()
		for buffer in self.parent.buffer_render_list:
			buffer.mark_set("match_end", "1.0")
			while True:
				if (index := self.find_match(keyword, buffer=buffer, start="match_end", end="end", regexp=self.regexp, count=count)):
					buffer.mark_set("match_end", index[1])
					buffer.tag_add("found", index[0], index[1])
					self.found[buffer.full_name].append(index)
				else: break

			buffer.mark_unset("match_end")

		self.scroll_through_found()
		return "break"

	def replace(self, arg=None):
		result_count = len(self.found[self.parent.buffer.full_name])
		match = self.parent.buffer.get(self.found[self.parent.buffer.full_name][self.found_index][0], self.found[self.parent.buffer.full_name][self.found_index][1])
		self.parent.notify(f"{self.found_index+1} out of {result_count} results : {self.found[self.parent.buffer.full_name][self.found_index]} match: {match} {self.mode}")
				
		start, end = self.found[self.parent.buffer.full_name][self.found_index][0], self.found[self.parent.buffer.full_name][self.found_index][1]
		self.parent.buffer.delete(start, end)
		self.parent.buffer.insert(start, self.get("1.0", "end-1c"))

		f = self.found[self.parent.buffer.full_name].pop(self.found_index)

		# fixes offset in line caused by replacing previous matches in line
		# I just hope it doesn't create any additional bugs, cuz I am too lazy to test ;) too bad
		if (match := self.find_match(keyword=self.find_query, start=f"{f[0]} wordstart", end=f"{f[0]} lineend-1c", regexp=self.regexp)):
			self.found[self.parent.buffer.full_name][self.found_index] = match

		self.parent.buffer.highlighter.highlight(line_no=self.parent.buffer.convert_line_index("int", start))
		self.scroll_through_found()

		return "break"

	def replace_all(self, arg=None):
		for i in range(len(self.found[self.parent.buffer.full_name])):
			self.replace(arg)

		return "break"

	def scroll_through_found(self, arg=None):
		result_count = len(self.found[self.parent.buffer.full_name])
		offset = 0
		if (result_count == 0): self.parent.notify(f"found none"); return "break"

		# self.parent.buffer.tag_remove("sel", self.found[self.found_index][0], self.found[self.found_index][1])
		# self.parent.buffer.tag_remove("underline", self.found[self.found_index][0], self.found[self.found_index][1])
		self.deselect_match()

		if (arg):
			if (arg.keysym == "Up"):
				self.found_index -= 1
				offset = -5
				if (self.found_index < 0):
					if (len(self.parent.buffer_render_list) > 1):
						self.parent.buffer.switch_buffer_next()
						result_count = len(self.found[self.parent.buffer.full_name])
						self.focus_set()
						self.found_index = result_count-1
						
					else:
						self.found_index = result_count-1
						
					offset = 5

			elif (arg.keysym == "Down"):
				self.found_index += 1
				offset = 5
				if (self.found_index >= result_count):
					if (len(self.parent.buffer_render_list) > 1):
						self.parent.buffer.switch_buffer_next()
						result_count = len(self.found[self.parent.buffer.full_name])
						self.found_index = 0
						
					else:
						self.found_index = 0
					offset = -5

		self.select_match(offset)
		self.move_to_find_index(unplace=False)

		self.parent.buffer.mark_set("insert", self.found[self.parent.buffer.full_name][self.found_index][1])
		self.parent.buffer.mark_set(self.parent.buffer.mark_names()[-1], self.found[self.parent.buffer.full_name][self.found_index][0])
		self.parent.buffer.tag_add("sel", self.found[self.parent.buffer.full_name][self.found_index][0], self.found[self.parent.buffer.full_name][self.found_index][1])
		self.parent.buffer.see(float(self.found[self.parent.buffer.full_name][self.found_index][0])+offset)
		self.parent.buffer.tag_add("sel", self.found[self.parent.buffer.full_name][self.found_index][0], self.found[self.parent.buffer.full_name][self.found_index][1])
		self.parent.buffer.tag_add("underline", self.found[self.parent.buffer.full_name][self.found_index][0], self.found[self.parent.buffer.full_name][self.found_index][1])
		self.parent.buffer.see("insert")

		self.parent.notify(f"{self.found_index+1} out of {result_count} results : {self.found[self.parent.buffer.full_name][self.found_index]} match: {self.find_query} {self.mode}")
		
		return "break"

	def append_history(self, arg=None, keyword=None):
		if (not keyword): keyword = self.get("1.0", "end-1c")
		if (not self.find_history or self.find_history[-1] != keyword): self.find_history.append(keyword);
		self.find_history_index = len(self.find_history)

	def scroll_through_find_history(self, arg=None):
		self.delete("1.0", "end")

		if (arg.keysym == "Up"):
			self.find_history_index -= 1
		else:
			self.find_history_index += 1
		
		if (self.find_history_index < 0):
			self.find_history_index = 0

		elif (self.find_history_index >= len(self.find_history)):
			self.find_history_index = len(self.find_history)-1

		last_input = self.find_history[self.find_history_index]
		self.insert("1.0", last_input)

		self.mark_set("insert", f"insert lineend")
		self.see("insert")

		return "break"


	def deselect_match(self):
		try:
			if (not self.found[self.parent.buffer.full_name] or not self.found[self.parent.buffer.full_name][self.found_index][0]): return
		except KeyError: return
		
		self.parent.buffer.tag_remove("sel",
			self.found[self.parent.buffer.full_name][self.found_index][0],
			self.found[self.parent.buffer.full_name][self.found_index][1]
		)
		
		self.parent.buffer.tag_remove("underline",
			self.found[self.parent.buffer.full_name][self.found_index][0],
			self.found[self.parent.buffer.full_name][self.found_index][1]	
		)
		
		self.parent.buffer.mark_unset(self.parent.buffer.mark_names()[-1])

	def select_match(self, offset=0):
		if (self.parent.buffer.full_name not in self.found): return
		self.parent.buffer.see(f"{self.found[self.parent.buffer.full_name][self.found_index][0]}+{offset}l")
		self.parent.buffer.tag_add("sel",
			self.found[self.parent.buffer.full_name][self.found_index][0],
			self.found[self.parent.buffer.full_name][self.found_index][1]
		)
		
		self.parent.buffer.tag_add("underline",
			self.found[self.parent.buffer.full_name][self.found_index][0],
			self.found[self.parent.buffer.full_name][self.found_index][1]
		)

	def remove_tags(self):
		for buffer in self.parent.buffer_render_list:
			try: [buffer.tag_remove("found", index[0], index[1]) for index in self.found[buffer.full_name]] # list comprehension go brr
			except KeyError: pass

	def move_to_find_index(self, arg=None, unplace=True):
		if (not self.found or self.parent.buffer.full_name not in self.found or not self.found[self.parent.buffer.full_name]):
			self.move_to_start_index()
			return

		self.parent.buffer.mark_set("insert", self.found[self.parent.buffer.full_name][self.found_index][1])
		self.parent.buffer.mark_set(self.parent.buffer.mark_names()[-1], self.found[self.parent.buffer.full_name][self.found_index][0])
		self.parent.buffer.tag_add("sel", 
			self.found[self.parent.buffer.full_name][self.found_index][0],
			self.found[self.parent.buffer.full_name][self.found_index][1])
		
		self.parent.buffer.see("insert")
		
		if (unplace): self.unplace()
		return "break"

	def move_to_start_index(self, arg=None, unplace=True):
		self.parent.buffer.mark_set("insert", self.start_index)
		
		if (self.found and self.parent.buffer.full_name in self.found and self.found[self.parent.buffer.full_name]):
			self.parent.buffer.tag_remove("sel",
				self.found[self.parent.buffer.full_name][self.found_index][0],
				self.found[self.parent.buffer.full_name][self.found_index][1])
		
		self.parent.buffer.see("insert")
		if (unplace): self.unplace()
		return "break"

	def unplace(self, arg=None):
		# self.parent.buffer.tag_remove("found_bg", "1.0", "end")
		# self.parent.buffer.tag_remove("underline", "1.0", "end")
		if (self.found and self.parent.buffer.full_name in self.found and self.found[self.parent.buffer.full_name]):
			self.parent.buffer.tag_remove("underline",
			 self.found[self.parent.buffer.full_name][self.found_index][0],
			 self.found[self.parent.buffer.full_name][self.found_index][1]
			)
		
			self.remove_tags()
			self.append_history()

		
		self.delete("1.0", "end")
		self.place_forget()
		self.parent.buffer.focus_set()
		self.found_index = 0
		self.found = {}
		self.start_index = None
	

class COMMAND_OUT(DEFAULT_TEXT_BUFFER):
	#DUNNO who tf wrote this, but they were a complete piece of shit ......................................
	def __init__(self, parent, name="COMMAND_OUT"):
		super().__init__(parent, name)

		self.font_bold = self.parent.font_bold
		self.font = self.parent.smaller_font_bold
		self.font_size = self.parent.conf["command_out_font_size"]
		self.font_weight = "bold"

		self.arg = ""
		self.modified_arg = ""

		self.tags = []
		self.selected_lines = []
		self.out = []

		self.input = ""
		self.input_label = tkinter.Label(self)
		self.input_label.pack()

		bind_keys_from_conf(self)

	def configure_self(self, arg=None):
		self.font_size_set()
		self.configure(font=self.font, bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"],
		 insertborderwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, exportselection=True, blockcursor=self.block_cursor,
		 spacing3=5, cursor="left_ptr", relief=self.parent.conf["command_out_border_style"], borderwidth=2, highlightthickness=0, wrap="word") # cursor="trek"

		if (self["relief"] == "flat"): self["bd"] = 0
		else: self["bd"] = 2
		
		self.input_label.configure(font=font.Font(family=self.parent.font_family[0], size=self.font_size,
		 weight=self.font_weight), bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"],
		 cursor="left_ptr", relief="flat", borderwidth=0, highlightthickness=0)


	def copy(self, arg=None):
		self.event_generate("<<Copy>>")
		return "break"

	def copy_line(self, arg=None):
		self.parent.clipboard_clear()
		self.parent.clipboard_append(self.get("insert linestart", "insert lineend"))
		self.parent.update()
		return "break"
	
	def add_input(self, arg):
		self["state"] = "normal"
		if (arg.keysym in ("Up", "Down", "Left", "Right")): return # ends function if it was triggered by arrow keys (as they have different functions to handle them)
		
		if (arg.keysym == "BackSpace"):
			if (not self.input): return "break"
			self.input = self.input[:-1]
			
		else:
			self.input += arg.char
			if (not self.input): return "break"

		self.modified_stdout(self.arg, self.tags) # fallback
		self.show_input()

		return "break"

	def show_input(self):
		# what is going on?????????????? ~	[ Sunday ] [ around 1am ] [ 2021-07-18 ] 
		# still trying to make a sense of this ~	[ Sunday ] [ 02:18:55 ] [ 2021-07-18 ] 
		self.input_label.configure(text=self.input)
		if (self.input == ""): self.input_label.forget(); return
		self.input_label.pack()

		self.modified_arg = []

		self.mark_set("match_end", "1.0")
		count = tkinter.IntVar()
		while (True):
			# index = self.search(parse_path(self.input), "match_end", "end", count=count, nocase=True, regexp=True, exact=False)
			index = self.search(self.input, "match_end", "end", count=count, nocase=True)
			if (index == ""): break
			if (count.get()) == 0: break
			self.mark_set("match_end", index+" lineend")
			self.modified_arg.append(self.get(index+" linestart", index+" lineend"))
		self.mark_unset("match_end")
		
		# result, tags = self.parent.file_handler.highlight_ls(self.modified_arg)
		# self.modified_stdout(result, tags)
		self.modified_stdout("\n".join(self.modified_arg))

	def unplace(self, arg=None):
		self.parent.buffer.focus_set()
		self.place_forget()

	def scroll(self, arg):
		key = arg.keysym

		if (key == "Prior"):
			self.mark_set("insert", "1.0")
			self.see("insert")

		elif (key == "Next"):
			self.mark_set("insert", "end linestart")
			self.see("insert")

		# self.tag_remove("command_out_insert_bg", "1.0", "end")
		# self.tag_add("command_out_insert_bg", "insert linestart", "insert lineend")

		return "break"

	def append_history(self, arg):
		if (self.out and arg != self.out[-1]): self.out.append(arg)
		
	def stdout(self, arg=None, tags=None, justify="left"):
		self["state"] = "normal"
		if (not arg):
			if (self.out): arg = self.out[-1]
			else: arg = self.arg
			tags = self.tags
		# else:
			# self.append_history(arg)
		
		self.input = ""
		self.show_input()
		
		del self.tags[:]
		
		self.arg = arg
		self.delete("1.0", "end")
		self.insert("1.0", self.arg)
		self.mark_set("insert", "1.0")
		self.tag_add(justify, "1.0", "end")

		if (tags):
			self.tags = tags
			
			for tag in self.tags:
				if (tag[2:]): self.tag_add(tag[2], tag[0], tag[1])
				else: self.tag_add("keywords", tag[0], tag[1])

			else: [self.tag_add("keywords", tag[0], tag[1]) for tag in tags]

	def modified_stdout(self, arg=None, tags=None, justify="left"):
		self["state"] = "normal"
		self.delete("1.0", "end")
		self.insert("1.0", arg)
		self.tag_add(justify, "1.0", "end")
		self.mark_set("insert", "1.0")

		if (tags):
			for tag in tags:
				if tag[2:]: self.tag_add(tag[2], tag[0], tag[1])
				else: self.tag_add("keywords", tag[0], tag[1])

			else: [self.tag_add("keywords", tag[0], tag[1]) for tag in tags]

	def change_ex(self, new_ex):
		self.ex = new_ex

	def add_selection(self, arg=None):
		if (arg):
			self.tag_add("command_out_select", "insert linestart", "insert lineend")
			for i, line in enumerate(self.selected_lines, 0):
				if (line == self.get("insert linestart", "insert lineend")):
					self.selected_lines.pop(i)
					self.tag_remove("command_out_select", "insert linestart", "insert lineend")
					return "break"
			
		self.selected_lines.append(self.get("insert linestart", "insert lineend"))

		return "break"
			
	def use_selection(self, arg=None):
		if (arg): self.add_selection()
		self.ex(self.selected_lines)
		self.show_input()
		del self.selected_lines[:]

		return "break"

	def open_line(self, arg=None):
		num_results = []
		line = arg[-1]
		
		if (re.search(r"line [0-9]+", line)):
			match = re.search(r"line [0-9]+", line).group()[5:]
		elif (re.search(r"[0-9]+", line)):
			match = re.search(r"[0-9]+", line)

		if (match):
			index = self.parent.buffer.convert_line_index("float", match)
			self.parent.buffer.mark_set("insert", index)
			self.parent.buffer.see("insert")
		
		return "break"
		
	def file_explorer(self, arg=None):
		for line in arg:
			line = f"{self.parent.file_handler.current_dir}/{line}"
			line.replace(" ", r"\ ")
			if (os.path.isfile(line)):
				self.parent.file_handler.load_file(filename=line)
			elif (os.path.isdir(line)):
				self.parent.file_handler.current_dir = os.path.normpath(line)
				self.parent.nt_place()
			
		return "break"

	def buffer_load(self, arg=None):
		arg=arg[-1]
		print(arg)
		self.parent.file_handler.load_buffer(buffer_name=arg)
		self.unplace()

class SUGGEST_WIDGET(DEFAULT_TEXT_BUFFER):
	def __init__(self, parent, name="SUGGEST_WIDGET"):
		super().__init__(parent, name)
		self.insert("1.0", "COMPLETELY ARBITARY TEXT")
		self.font_bold = self.parent.font_bold
		self.font = self.parent.smaller_font_bold
		self.font_size = self.parent.conf["suggest_widget_font_size"]

	def configure_self(self, arg=None):
		# self.configure(bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"])
		self.configure(font=self.font, bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"],
		 insertborderwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="solid",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, exportselection=True, blockcursor=self.block_cursor,
		 spacing3=0, cursor="left_ptr", relief=self.parent.conf["suggest_widget_border_style"], borderwidth=2, highlightthickness=0, wrap="word") # cursor="trek"

	def move(self, arg=None, up=None):
		if (up):
			self.mark_set("insert", "insert -1l")
		elif (not up):
			self.mark_set("insert", "insert +1l")
		self.see("insert")

		return "break"

	def move_up(self, arg=None):
		return self.move(arg, up=True)
	
	def move_down(self, arg=None):
		return self.move(arg, up=False)

	def write(self, arg=None):		
		self.parent.buffer.insert("insert", self.get("insert linestart", "insert lineend")[len(self.parent.buffer.current_token):])
		self.unplace()
		return "break"

	def suggest(self, arg=None) -> None:
		coords = self.parent.buffer.bbox("insert")
		self.place(x=coords[0]+coords[3], y=coords[1]+50, width=100, height=100)
		self.tkraise()

		return "break"

	def unplace(self, arg=None):
		self.delete("1.0", "end")
		self.place_forget()
		self.parent.buffer.focus_set()
		self.parent.buffer.mode_set("suggest")

		# return "break"

class PROMPT(BOX):
	def __init__(self, parent, name=None):
		super().__init__(parent, name)

	def configure_self(self):
		pass

	def place_self(self):
		self.place(relx=0.5, rely=0.5, width=200, height=200)

	def unplace(self):
		self.place_forget()


class TEXT(DEFAULT_TEXT_BUFFER):
	def __init__(self, parent, name, type="normal"):
		super().__init__(parent, name, type)

		self.make_argv = ""
		self.highlighter = highlighter(self.parent, self)
		self.set_highlighter()

		try: self.file_start_time = os.stat(self.full_name).st_mtime
		except FileNotFoundError: self.file_start_time = 0

		self.mode = None

		self.clipboard_register = ""
		self.sel_start = None
		# self.moving_index = "1.0" # I should be using the inbuilt tkinter text marks, but that would've probably fucked up other things I am too lazy to fix
		# self.typing_index = "1.0"
		self.cursor_index = ["1", "0"]
		self.queue = []
		self.current_line = ""
		self.current_token = ""
		self.total_lines = 1

		self.state = []

		self.total_chars = 1
		self.current_char_abs_pos = 0
		self["wrap"] = "none"

		self.mark_set("moving", "1.0")
		self.mark_set("typing", "1.0")

		# I should be using the inbuilt tkinter text marks, but that would've probably fucked up other things I am too lazy to fix
		# self.marks = {
			# "moving" : "1.0",
			# "typing" : "1.0",
		# }

		bind_keys_from_conf(self)

	def configure_self(self, arg=None) -> None:
		self.font_size_set()
		self.configure(font=self.font, bg = self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"], undo=True, maxundo=0,
		 spacing1=0, insertborderwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, borderwidth=2, relief=self.parent.conf["buffer_border_style"], tabs=(f"{self.font.measure(' ' * self.parent.conf['tab_size'])}"), wrap=self["wrap"], exportselection=True,
		 blockcursor=self.block_cursor, highlightthickness=0, cursor="xterm")

		if (self["relief"] == "flat"): self["bd"] = 0
		else: self["bd"] = 2

	def toggle_line_wrap(self, arg=None) -> None:
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

	def state_set(self, add=None, pop=None):
		if (type(add) == str): add = [add]
		if (type(pop) == str): pop = [pop]
		
		if (add): [self.state.append(state) for state in add if state not in self.state]
		if (pop): [self.state.pop(self.state.index(state)) for state in pop if state in self.state]
			# print("buffer state: ", self.state)
			# print("pop: ", pop)
			# for state in pop:
				# print("state: ", state)
				# try:
					# index = self.state.index(state)
					# print("popping", self.state.pop(index))
				# except ValueError: pass

		if (self.state): name = "".join(self.state)+self.name+" "
		else: name = " "+"".join(self.state)+self.name+" "
		self.parent.buffer_name_label["text"] = self.parent.file_handler.buffer_tab["text"] = name

	def moving(func):
		def wrapped_func(self, *args, **kwargs):
			self.tag_remove("cursor", "1.0", "end")
			ret = func(self, *args, **kwargs)
			self.tag_add("cursor", "insert")
			self.cursor_highlight()
			return ret

		return wrapped_func

	def mode_set(self, arg=None, mode=None, force=False):
		if (not force and self.mode == mode): self.mode = None
		else: self.mode = mode
		bind_keys_from_conf(self)

	def set_vim_mode(self, arg=None):
		self.mode_set(mode="vim_mode")
		print("mode: ", self.mode)

	def bind_key_with_all_mod(self, key, func_ptr):
		# what even is this
		mods = ["Control-Shift", "Control", "Shift", ""]
		if (type(func_ptr) == list):
			for i in range(len(mods)):
				if (mods[i] == ""): self.bind(f"{key}", func_ptr[i])
				else: self.bind(f"<{mods[i]}-{key}>", func_ptr[i])
		else:
			for i in range(len(mods)):
				if (mods[i] == ""): self.bind(f"{key}", func_ptr)
				else: self.bind(f"<{mods[i]}-{key}>", func_ptr)

	def unbind_key_with_all_mod(self, key):
		mods = ["Control-Shift", "Control", "Shift", ""]
		for i in range(len(mods)):
			if (mods[i] == ""): self.unbind(f"{key}")
			else: self.unbind(f"<{mods[i]}-{key}>")

	def bind_key_with_control_shift(self, key, func_ptr):
		self.bind(f"<Control-Shift-{key}>", func_ptr)

	def unbind_key_with_control_shift(self, key):
		self.unbind(f"<Control-Shift-{key}>")

	def bind_key_with_control(self, key, func_ptr):
		self.bind(f"<Control-{key}>", func_ptr)

	def unbind_key_with_control(self, key):
		self.unbind(f"<Control-{key}>")

	def bind_key_with_shift(self, key, func_ptr):
		self.bind(f"<Shift-{key}>", func_ptr)

	def unbind_key_with_shift(self, key):
		self.unbind(f"<Shift-{key}>")

	@moving
	def move(self, arg=None, mod=[], key=None):
		if (not key): key = arg.keysym
		
		suffix = ["Line", "Char"]
		prefix = ""
		# if (not mod): mod = [m for m in arg.state.split("|")]
		
		if ("control" in mod):
			suffix = ["Para", "Word"]

		if ("shift" in mod):
			prefix = "Select"

		if (key == "Up"):
			self.move_up(prefix=prefix, suffix=suffix[0])

		elif (key == "Down"):
			self.move_down(prefix=prefix, suffix=suffix[0])

		elif (key == "Left"):
			self.move_left(prefix=prefix, suffix=suffix[1])

		elif (key == "Right"):
			self.move_right(prefix=prefix, suffix=suffix[1])

		if (prefix == ""): self.sel_start = None; del self.queue[:]
		else: self.sel_start = self.index(self.mark_names()[-1])
		self.parent.update_index()

		return "break"

	def move_up(self, arg=None, prefix="", suffix="Line"):
		self.event_generate(f"<<{prefix}Prev{suffix}>>")
		self.see("insert -5l")
		return "break"
			
	def move_down(self, arg=None, prefix="", suffix="Line"):
		self.event_generate(f"<<{prefix}Next{suffix}>>")
		self.see("insert +5l")
		return "break"
		
	def move_left(self, arg=None, prefix="", suffix="Char"):
		self.event_generate(f"<<{prefix}Prev{suffix}>>")
		self.see("insert -5l")
		return "break"
		
	def move_right(self, arg=None, prefix="", suffix="Char"):
		self.event_generate(f"<<{prefix}Next{suffix}>>")
		self.see("insert +5l")
		return "break"

	def move_standard(self, arg=None, key=None):
		self.move(arg, key=key)
		return "break"

	def move_jump(self, arg=None, key=None):
		self.move(arg, ["control"], key=key)
		return "break"

	def move_select(self, arg=None, key=None):
		self.move(arg, ["shift"], key=key)
		return "break"

	def move_jump_select(self, arg=None, key=None):
		self.move(arg, ["control", "shift"], key=key)
		return "break"

	#text manipulation bindings
	@moving
	@add_command_to_history
	def cut(self, arg=None):
		""" Control-X """
		self.event_generate("<<Cut>>")
		return "break"
		
	@moving
	@add_command_to_history
	def undo(self, arg=None):
		""" Control-Z """
		chunk_size = self.get_line_count()
		self.event_generate("<<Undo>>")
		start_index = self.convert_line_index("int")
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.parent.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	@moving
	@add_command_to_history
	def redo(self, arg=None):
		""" Control-Y """
		chunk_size = self.get_line_count()
		self.event_generate("<<Redo>>")
		start_index = self.convert_line_index("int")
		stop_index = start_index + abs(chunk_size - self.get_line_count())
		self.parent.highlight_chunk(start_index=start_index, stop_index=stop_index)
		return "break"

	@moving
	@add_command_to_history
	def copy(self, arg=None):
		""" Control-C """
		self.event_generate("<<Copy>>")
		return "break"

	@moving
	@add_command_to_history
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

	@moving
	def mouse_left_motion(self, arg=None):
		if (not self.sel_start):
			self.sel_start = self.index("current")
		self.mark_set("current", "insert")
		self.parent.update_buffer()

	def todo_set(self, arg=None, text=None):
		# smort
		if (self.current_line[0] == "["):
			if (self.current_line[1] == "]"): self.insert("insert linestart+1c", " ")
			self.delete("insert linestart+1c")
			
			if (self.current_line[1] == " "):
				self.insert("insert linestart+1c", "X")
			else:
				self.insert("insert linestart+1c", " ")
	
		else:
			self.insert("insert linestart", "[ ] ")

		self.parent.update_index()
		if (self.current_line[3] != " "): self.insert("insert linestart+3c", " ")
		if (text): self.insert("insert linestart+3c", text)

		return "break"

	def move_line(self, arg=None, up=True, line_offset=1):
		# l = self.dump("insert linestart", "insert lineend+1c", tag="tag")
		# print(l)

		sel_mark_name = self.mark_names()[-1]
		start, stop = self.queue_get()
		stop -= 1

		f_index = self.index("insert")
		fs_index = self.index(sel_mark_name)

		if (up): offset = f"-{line_offset}l"
		else: offset = f"+{line_offset}l"

		text = self.get(f"{start}.0 linestart", f"{stop}.0 lineend+1c")
		self.delete(f"{start}.0 linestart", f"{stop}.0 lineend+1c")
		self.insert(f"{start}.0 linestart"+offset, text)
		self.parent.highlight_chunk(start_index=start-line_offset, stop_index=stop+line_offset)
		
		self.mark_set("insert", f_index+offset)
		self.mark_set(sel_mark_name, fs_index+offset)
		self.tag_add("sel", *self.index_sort("insert", sel_mark_name))
		
		self.parent.update_index()

		return "break"


	def move_line_down(self, arg=None):
		return self.move_line(arg, up=False)
		

	def move_line_up(self, arg=None):
		return self.move_line(arg, up=True)

	@add_command_to_history
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
			self.mark_set("insert", f"insert +{3*multiplier}l")
			self.see("insert +3l")
	
		elif (arg.num == 4 or arg.delta > 0):
			self.mark_set("insert", f"insert -{3*multiplier}l")
			self.see("insert -3l")
		
		# hides widgets that could be in the way
		self.focus_set()
		
		self.del_selection()
		self.parent.update_index()

		return "break"

	@moving
	def scroll_fast(self, arg=None):
		self.scroll(arg, 3)

	@moving
	def keep_indent(self, arg=None):
		""" gets the amount of tabs in the last line and puts them at the start of a new one """
		#this functions gets called everytime Enter/Return has been pressed
		self.see("insert +3l")
		
		tab_offset = self.parent.conf["line_end"]
		column_index = self.get_column_index()
		
		if (match := re.search(r"^\t+", self.current_line)):
			tab_offset += match.group()
			if (len(tab_offset) > column_index):
				tab_offset = tab_offset[:column_index+1]

		# I am seeing a lot of horrible code in this project
		# sometimes I look back at my code and wonder if I am insane
		# magic with brackets
		# basically automatic indenting
		if (re.match(r"[\:]", self.get("insert-1c"))): 
			offset = tab_offset
			self.insert("insert", offset+"\t")
			
		elif (re.match(r"[\{\[\(]", self.get("insert-1c"))):
			if (re.match(r"[\}\]\)]", self.get("insert"))):
				offset = tab_offset+"\t"+tab_offset
				self.insert(self.index("insert"), offset)
				self.mark_set("insert", f"insert-{len(tab_offset)}c")
			else:
				offset = tab_offset
				self.insert(self.index("insert"), offset+"\t")
				
		elif (re.match(r"[\{\[\(]", self.get("insert"))):
			if (re.match(r"[\}\]\)]", self.get("insert+1c"))):
				offset = tab_offset
				self.insert(self.index("insert"), offset)
				self.mark_set("insert", "insert+1c")
				offset = tab_offset+"\t"+tab_offset
				self.insert(self.index("insert"), offset)
				self.mark_set("insert", f"insert-{len(tab_offset)}c")
			else:
				offset = tab_offset
				self.insert(self.index("insert"), offset)
				self.mark_set("insert", f"insert+{len(tab_offset)+2}c")
		
		else:
			if (re.match(r"\t+(\n|\r\n)", self.current_line)):
				self.delete("insert linestart", "insert lineend") #removes extra tabs if the line is empty
				
			offset = tab_offset # if this line gets removed it fucks up
			self.insert("insert", offset)

		self.total_lines += len(re.findall("\n", offset))
		self.lexer.lex() # lex text for variables, functions, structures and class etc.
		
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

	def delete_selection_start_index(self, arg=None) -> None:
		""" This has to be a function and I hate it """
		self.sel_start = None
		self.parent.update_index()

	def get_time(self, arg=None) -> None:
		date = datetime.date.today()
		day_name = datetime.date.today().strftime("%A")
		return f"{self.highlighter.comment_sign} ~\t[ {day_name} ] [ {self.parent.time_label_value.get()} ] [ {date} ] "

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

	def copy_token(self, arg=None):
		self.parent.clipboard_clear()
		self.parent.clipboard_append(self.current_token)
		self.parent.update()
		
		return "break"

	def moving_index_set(self, arg=None, index="insert"):
		# self.moving_index = self.index(index)
		self.mark_set("moving", self.index(index))
		if (arg): return "break"

	def typing_index_set(self, arg=None, index="insert"):
		self.mark_set("typing", self.index(index))
		# index = self.index(index)
		# self.typing_index = index
		if (arg): return "break"

	def jump_to_moving_index(self, arg=None):
		tmp_index = self.index("insert")
		# self.mark_set("insert", self.moving_index)
		# self.see(self.moving_index)
		# self.moving_index = tmp_index

		self.mark_set("insert", "moving")
		self.see("moving")
		self.mark_set("moving", tmp_index)
		
		if (arg): return "break"

	def jump_to_typing_index(self, arg=None):
		tmp_index = self.index("insert")
		# self.mark_set("insert", self.typing_index)
		# self.see(self.typing_index)
		# self.typing_index = tmp_index

		self.mark_set("insert", "typing")
		self.see("typing")
		self.mark_set("typing", tmp_index)
		
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
		# self.pack_forget()
		self.place_forget()

	def switch_buffer(self, arg=None, next = True) -> str:
		# if (self.parent.split_mode != 0):
			# return "break"

		if (self.parent.split_mode == "nosplit" and len(self.parent.file_handler.buffer_list) > 1):
			if (next):
				buffer_tab_index = self.parent.file_handler.buffer_tab_index+1
	
			elif (not next):
				buffer_tab_index = self.parent.file_handler.buffer_tab_index-1
	
			if (buffer_tab_index >= len(self.parent.file_handler.buffer_list)):
				buffer_tab_index = 0
	
			elif (buffer_tab_index < 0):
				buffer_tab_index = len(self.parent.file_handler.buffer_list)-1
			
			self.parent.file_handler.load_buffer(buffer_index=buffer_tab_index)
		else:
			if (next):
				self.parent.buffer_render_index = self.parent.buffer_render_index+1
	
			elif (not next):
				self.parent.buffer_render_index = self.parent.buffer_render_index-1
	
			if (self.parent.buffer_render_index >= len(self.parent.buffer_render_list)):
				self.parent.buffer_render_index = 0
	
			elif (self.parent.buffer_render_index < 0):
				self.parent.buffer_render_index = len(self.parent.buffer_render_list)-1

			self.parent.buffer = self.parent.buffer_render_list[self.parent.buffer_render_index]
			if (self.parent.focus_get() == self): self.parent.buffer.focus_set()
			self.parent.file_handler.set_current_file(buffer_name=self.parent.buffer.full_name)
			self.parent.reposition_widgets()

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
			argv = self.make_argv
			self.parent.command_out.change_ex(self.parent.command_out.open_line)
			
		def run():
			process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			self.parent.subprocesses.append(process)
			index = len(self.parent.subprocesses)-1

			while (True):
				if (process.poll() is not None): break
				out = process.stdout.read().decode("UTF-8")
				out += process.stderr.read().decode("UTF-8")

				self.parent.command_out_set(out)
				print(out)
				self.parent.subprocesses.pop(index)
			
		threading.Thread(target=run, daemon=True).start()
		return "break"

	def run_make(self, arg=None):
		return self.run_subprocess(make=True)

		
