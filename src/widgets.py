import subprocess
import threading
import datetime
import tkinter
import time
import os
import re

from tkinter import font, PhotoImage
try: from PIL import ImageTk, Image
except Exception: pass

from highlighter import *

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
		self.bind("<Enter>", lambda arg: self.parent.command_out_set(self.full_name))
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
		self.pack(side="left")
		self.tkraise()

	def change_name(self, new_name: str=None, extra_char: str = ""):
		if (new_name): self.full_name = new_name; self.name = os.path.basename(new_name)
		self.configure(text=extra_char+self.name+" ")

	def load_buffer(self, arg=None):
		self.focus_set()
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
		self.parent.command_out_set(f"buffer [{self.parent.txt.name}] was loaded", tags=[["1.7", "1.8", "logical_keywords"], ["1.8", f"1.{8+len(self.parent.txt.name)}"], [f"1.{8+len(self.parent.txt.name)}", f"1.{9+len(self.parent.txt.name)}", "logical_keywords"]])

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
		
		self.block_cursor = True
		self.terminal_like_cursor = True
		self.cursor_mode = 2

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

	def cursor_mode_set(self, arg=None):
		""" Insert """
		# don't ask
		
		self.configure(insertwidth=1)
		
		# self.txt.cursor_mode -= -1 if self.txt.cursor_mode < 2 else 2 #I fucking hate this :DDD
		self.cursor_mode += 1
		if (self.cursor_mode >= 3):
			self.cursor_mode = 0
			
		if (self.cursor_mode == 0): #LINE
			# self.txt.tag_delete("cursor")
			self.block_cursor = False
			self.terminal_like_cursor = False
			
		elif (self.cursor_mode == 1): #
			self.block_cursor = True
			self.terminal_like_cursor = False

		elif (self.cursor_mode == 2): #NORMAL BLOCK
			self.block_cursor = True
			self.terminal_like_cursor = True
		
		else:
			self.cursor_mode = 2
			self.block_cursor = True
			self.terminal_like_cursor = True

		self.configure(blockcursor=self.block_cursor)
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
		 selectborderwidth=0, borderwidth=1, relief="raised", tabs=(f"{self.font.measure(' ' * self.parent.tab_size)}"), wrap="word", exportselection=True,
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
			
		self.parent.command_out_set(f"{self.mode}", focus=False)

		return "break"

	def find_mode_set(self, arg=None):
		self.mode = "<search>"
		if (self.get("1.0") not in ["?", "/"]): self.insert("1.0", "?")
		self.bind("<Return>", self.find)
		self.unbind("<Control-Z>")
		self.unbind("<Control-z>")
		
	def replace_mode_set(self, arg=None):
		self.mode = "<replace>"
		self.bind("<Return>", self.replace)
		self.bind("<Control-Z>", self.parent.undo)
		self.bind("<Control-z>", self.parent.undo)

	def find_match(self, keyword, start="match_end", end="end", regexp=False, count=None):
		if (count == None):
			count = tkinter.IntVar()
		index = self.parent.txt.search(keyword, start, end, regexp=regexp, count=count)
		if (index == ""): return None
		if (count.get()) == 0: return None # degenerate pattern which matches zero-lenght strings
		return [ index, self.parent.txt.index(f"{index}+{count.get()}c") ]

	def find(self, arg=None, keyword=None):
		"""  """
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
		self.parent.command_out_set(f"{self.found_index+1} out of {result_count} results : {self.found[self.found_index]} match: {match} {self.mode}", focus=False)
		start, end = self.found[self.found_index][0], self.found[self.found_index][1]
		self.parent.txt.delete(start, end)
		self.parent.txt.insert(start, self.get("1.0", "end-1c"))
		# self.parent.highlight_chunk(start_index=start, stop_index=end)
		self.parent.txt.highlighter.highlight(line_no=self.parent.convert_line_index("int", start))
		f = self.found.pop(self.found_index)
		
		# fixes offset in line caused by replacing previous matches in line
		# I just hope it doesn't create any additional bugs, cuz I am too lazy to test ;) too bad
		if (match := self.find_match(keyword=self.find_query, start=f"{f[0]} wordend", end=f"{f[0]} lineend", regexp=self.regexp)):
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
		if (result_count == 0): self.parent.command_out_set(f"found none", focus=False); return "break"

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
		self.parent.command_out_set(f"{self.found_index+1} out of {result_count} results : {self.found[self.found_index]} match: {match} {self.mode}", focus=False)

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
		for index in self.found:
			self.parent.txt.tag_remove("found_bg", index[0], index[1])
			self.parent.txt.tag_remove("underline", index[0], index[1])
		
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

	def configure_self(self, arg=None):
		self.font_size_set()
		self.configure(font=font.Font(family=self.parent.font_family[0], size=self.font_size,
		 weight=self.font_weight), bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 spacing3=5, cursor="left_ptr", highlightthickness=0, wrap="word") # cursor="trek"

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
		self.configure(state="normal")
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
		self.configure(state="disabled")

		return "break"
		
	def stdout(self, arg=None, tags=None, justify="left"):
		self.configure(state="normal")
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

		self.configure(state="disabled")

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
				index = self.parent.convert_line_index("float", match)
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

		self.clipboard_register = ""
		self.moving_index = "1.0" # I should be using the inbuilt tkinter text marks, but that would've probably fucked up other things I am too lazy to fix
		self.typing_index = "1.0"

		# self.text_len = ""
		self.change_index = ""
		self["wrap"] = "none"

		self.bind("<KeyRelease>", self.parent.update_buffer)
		# self.bind("<KeyRelease><BackSpace>", self.delete_selection_start_index)

		self.bind("<Button-1>", self.parent.mouse_left)
		self.bind("<B1-Motion>", self.parent.mouse_left_motion)
		# self.bind("<Motion>", lambda arg: self.mark_set("insert", "current"))
		
		self.bind("<Up>", self.parent.move_standard)
		self.bind("<Down>", self.parent.move_standard)
		self.bind("<Left>", self.parent.move_standard)
		self.bind("<Right>", self.parent.move_standard)
		
		self.bind("<Control-Up>", self.parent.move_jump)
		self.bind("<Control-Down>", self.parent.move_jump)
		self.bind("<Control-Left>", self.parent.move_jump)
		self.bind("<Control-Right>", self.parent.move_jump)

		self.bind("<Shift-Up>", self.parent.move_select)
		self.bind("<Shift-Down>", self.parent.move_select)
		self.bind("<Shift-Left>", self.parent.move_select)
		self.bind("<Shift-Right>", self.parent.move_select)

		self.bind("<Control-Shift-Up>", self.parent.move_jump_select)
		self.bind("<Control-Shift-Down>", self.parent.move_jump_select)
		self.bind("<Control-Shift-Left>", self.parent.move_jump_select)
		self.bind("<Control-Shift-Right>", self.parent.move_jump_select)
		
		self.bind("<Home>", self.parent.home)
		self.bind("<Shift-Home>", self.parent.home_select)
		self.bind("<End>", self.parent.end)
		self.bind("<Shift-End>", self.parent.end_select)

		self.bind("<Shift-Return>", lambda arg: self.run_subprocess(make=True))

		self.bind("<MouseWheel>", self.parent.scroll)
		self.bind("<Button-4>", self.parent.scroll)
		self.bind("<Button-5>", self.parent.scroll)
		self.bind("<Shift-MouseWheel>", lambda arg: self.parent.scroll(arg, multiplier=3))
		self.bind("<Shift-Button-4>", lambda arg: self.parent.scroll(arg, multiplier=3))
		self.bind("<Shift-Button-5>", lambda arg: self.parent.scroll(arg, multiplier=3))
		# self.bind("<Button-3>", self.parent.popup) #right click pop-up window

		self.bind("<Return>", self.parent.keep_indent)
		self.bind("<Control-slash>", self.parent.comment_line)

		self.bind("<Control-S>", self.parent.file_handler.save_file)
		self.bind("<Control-s>", self.parent.file_handler.save_file)
		self.bind("<Control-Shift-S>", self.parent.file_handler.save_file_as)
		self.bind("<Control-Shift-s>", self.parent.file_handler.save_file_as)
		self.bind("<Control-N>", self.parent.file_handler.new_file)
		self.bind("<Control-n>", self.parent.file_handler.new_file)
		self.bind("<Control-O>", self.parent.file_handler.load_file)
		self.bind("<Control-o>", self.parent.file_handler.load_file)

		self.bind("<Control-B>", self.empty_break)
		self.bind("<Control-b>", self.empty_break)
		self.bind("<Control-B>L", self.parent.file_handler.load_file)
		self.bind("<Control-b>l", self.parent.file_handler.load_file)
		self.bind("<Control-B>W", lambda arg: self.parent.file_handler.close_buffer(arg, self.full_name))
		self.bind("<Control-b>w", lambda arg: self.parent.file_handler.close_buffer(arg, self.full_name))
		self.bind("<Control-w>", self.parent.win_destroy)
		self.bind("<Control-W>", self.parent.win_destroy)
		self.bind("<Control-B><Delete>", lambda arg: self.parent.file_handler.del_file(arg, self.full_name))
		self.bind("<Control-b><Delete>", lambda arg: self.parent.file_handler.del_file(arg, self.full_name))
		self.bind("<Control-B>S", self.parent.file_handler.load_scratch)
		self.bind("<Control-b>s", self.parent.file_handler.load_scratch)

		# lol this is gross
		self.bind("<Control-E>", lambda arg: self.parent.command_out_set("\n".join(self.parent.command_out.out[-1:])))
		self.bind("<Control-e>", lambda arg: self.parent.command_out_set("\n".join(self.parent.command_out.out[-1:])))

		# self.bind("<Control-T>", self.parent.task_handler.show_tasks)
		# self.bind("<Control-t>", self.parent.task_handler.show_tasks)
	
		self.bind("<Control-F>", self.parent.find_place)
		self.bind("<Control-f>", self.parent.find_place)
		self.bind("<Control-G>", self.parent.nt_place)
		self.bind("<Control-g>", self.parent.nt_place)

		self.bind("<Control-Z>", self.parent.undo)
		self.bind("<Control-z>", self.parent.undo)
		self.bind("<Control-Y>", self.parent.redo)
		self.bind("<Control-y>", self.parent.redo)
		self.bind("<Control-A>", self.parent.select_all)
		self.bind("<Control-a>", self.parent.select_all)

		self.bind("<Control-K>", self.parent.get_selection_count)
		self.bind("<Control-k>", self.parent.get_selection_count)

		self.bind("<Tab>", self.parent.indent)
		self.bind("<Control-Tab>", self.switch_buffer_next)
		try: #linux bindings that throw errors on windows
			self.bind("<Shift-ISO_Left_Tab>", self.parent.unindent)
			self.bind("<Control-Shift-ISO_Left_Tab>", self.switch_buffer_prev)
			self.parent.command_entry.bind("<KP_Enter>", self.parent.cmmand)
		except Exception:
			self.bind("<Shift-Tab>", self.parent.unindent)
			self.bind("<Control-Shift-Tab>", self.switch_buffer_prev)

		self.bind("<Control-B><KeyPress><Left>", self.switch_buffer_prev)
		self.bind("<Control-b><KeyPress><Left>", self.switch_buffer_prev)
		self.bind("<Control-B><KeyPress><Right>", self.switch_buffer_next)
		self.bind("<Control-b><KeyPress><Right>", self.switch_buffer_next)

		self.bind("<Control-Q>", self.configure_wrap)
		self.bind("<Control-q>", self.configure_wrap)

		# text inserstion and deletion
		self.bind("<Control-L>", self.parent.change_case)
		self.bind("<Control-l>", self.parent.change_case)
		self.bind("<Control-Shift-L>", self.parent.change_case)
		self.bind("<Control-Shift-l>", self.parent.change_case)
		self.bind("<Control-B>C", self.buffer_clipboard_set)
		self.bind("<Control-b>c", self.buffer_clipboard_set)
		self.bind("<Control-B>V", self.buffer_clipboard_paste)
		self.bind("<Control-b>v", self.buffer_clipboard_paste)
		self.bind("<Control-V>", self.parent.paste)
		self.bind("<Control-v>", self.parent.paste)
		self.bind("<Control-quotedbl>", self.parent.char_enclose)		#"
		# self.bind("<Control-apostrophe>", self.parent.char_enclose)		#'
		self.bind("<Control-parenleft>", self.parent.char_enclose) 		#( 
		self.bind("<Control-bracketleft>", self.parent.char_enclose) 	#[
		self.bind("<Control-braceleft>", self.parent.char_enclose) 		#{
		self.bind("<Control-BackSpace>", self.delete_prev_word)
		self.bind("<Control-Delete>", self.delete_next_word)
		self.bind("<Control-Shift-BackSpace>", self.delete_line)
		self.bind("<Control-Shift-Delete>", self.delete_line)

		# moving around with marks and stuff
		self.bind("<Alt-S>", self.selection_index_swap)
		self.bind("<Alt-s>", self.selection_index_swap)

		self.bind("<Alt-Shift-M>", self.moving_index_set)
		self.bind("<Alt-Shift-m>", self.moving_index_set)
		self.bind("<Alt-M>", self.jump_to_moving_index)
		self.bind("<Alt-m>", self.jump_to_moving_index)
		self.bind("<Alt-N>", self.jump_to_typing_index)
		self.bind("<Alt-n>", self.jump_to_typing_index)
		self.bind("<Alt-B>", self.jump_to_scope_start)
		self.bind("<Alt-b>", self.jump_to_scope_start)
		self.bind("<Alt-Shift-B>", self.jump_to_scope_end)
		self.bind("<Alt-Shift-b>", self.jump_to_scope_end)

		self.bind("<FocusIn>", lambda arg: self.parent.theme_load())

	def configure_self(self, arg=None) -> None:
		self.font_size_set()
		self.configure(font=self.font, bg = self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"], undo=True, maxundo=0,
		 spacing1=0, insertborderwidth=0, insertwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, borderwidth=1, relief="flat", tabs=(f"{self.font.measure(' ' * self.parent.tab_size)}"), wrap=self["wrap"], exportselection=True,
		 blockcursor=self.block_cursor, highlightthickness=0, cursor="xterm")

	def configure_wrap(self, arg=None) -> None:
		if (self["wrap"] == "none"):
			self["wrap"] = "word"
		else:
			self["wrap"] = "none"

		self.see("insert")

	def change_name(self, name) -> None:
		self.full_name = name
		self.name = os.path.basename(name)

	def empty_break(self, arg=None):
		return "break"

	def delete_selection_start_index(self, arg=None) -> None:
		""" This has to be a function and I hate it """
		self.parent.selection_start_index = None
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
			text = self.get(self.parent.selection_start_index, self.index("insert"))
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
		self.mark_set("insert", self.parent.selection_start_index)
		self.mark_set(self.mark_names()[-1], swp_index)
		self.parent.selection_start_index = swp_index
		self.see("insert")
		
		if (arg): return "break"

	def set_highlighter(self) -> None:
		""" sets the highlighter accordingly to the current file extension """
		try: arg = self.name.split(".")[-1]
		except Exception: arg = "NaN"

		self.parent.highlighting = True
		self.highlighter.set_languague(arg)

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
		self.parent.command_out_set(f"buffer [{self.parent.txt.name}] was loaded", tags=[["1.7", "1.8", "logical_keywords"], ["1.8", f"1.{8+len(self.parent.txt.name)}"], [f"1.{8+len(self.parent.txt.name)}", f"1.{9+len(self.parent.txt.name)}", "logical_keywords"]])

		return "break"

	def switch_buffer_prev(self, arg=None):
		self.switch_buffer(next=False)
		return "break"

	def switch_buffer_next(self, arg=None):
		self.switch_buffer()
		return "break"

	def run_subprocess(self, argv=None, make=False) -> str:
		if (make):
			argv = self.make_argv.split(" ")
			self.parent.command_out.change_ex(self.parent.command_out.open_line)
		
		def run():
			process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			out = process.stdout.read().decode("UTF-8")

			self.parent.command_out_set(out, focus=False)
			print(out)
			
		threading.Thread(target=run, daemon=True).start()
		return "break"

