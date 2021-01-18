import subprocess
import threading
import datetime
import tkinter
import time
import os
import re

from tkinter import font, PhotoImage
from PIL import ImageTk, Image

from highlighter import highlighter


class BUFFER_TAB(tkinter.Label):
	def __init__(self, name: str, parent):
		super().__init__(parent)
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)

		self.buffer_index = len(self.parent.file_handler.buffer_list)
		self.configure(text=" "+self.name, font=self.parent.widget_font, 
		 bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["widget_fg"],
		 highlightcolor=self.parent.theme["window"]["widget_fg"])

		self.parent.file_handler.buffer_tab_index = self.buffer_index
		# self.configure(command=lambda: self.parent.file_handler.load_buffer(buffer_name=self.name)) # if I ever wanna go back to the button widget
		
		if (self.buffer_index > 1):
			self.reposition(self.parent.file_handler.buffer_list[self.buffer_index-1][1])
		elif (self.buffer_index == 1):
			self.reposition()

		self.menu = tkinter.Menu(self.parent)
		self.menu.configure(font=self.parent.widget_font, tearoff=False,fg="#FFFFFF", bg=self.parent.theme["window"]["bg"], bd=0)
		self.menu.add_command(label="Close", command=lambda: self.parent.file_handler.close_buffer(buffer_name=self.full_name))

		self.hover_info = tkinter.Label(self.parent)
		self.hover_info.configure(text=self.full_name, font=self.parent.widget_font, fg="#FFFFFF", bg=self.parent.theme["window"]["bg"], bd=1)

		# self.hover_info.place(x=self.winfo_rootx(), y=self.winfo_rooty()+self.winfo_height())
		# self.hover_info.pack()
		# self.destroy_label = tkinter.Label(self, text="X"); self.destroy_label.place(relx=1, y=0, width=10, height=10, anchor="ne")
		# self.destroy_label.bind("<Button-1>", lambda arg: self.parent.file_handler.close_buffer(buffer_name=self.name))

		self.bind("<Button-1>", self.load_buffer)
		# self.bind("<Enter>", lambda arg: self.hover_info.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height()), print("aa"))
		self.bind("<Enter>", lambda arg: self.parent.command_out_set(self.full_name))
		# self.bind("<Leave>", lambda arg: self.hover_info.place_forget())
		self.bind("<Button-3>", lambda arg: self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty()+self.winfo_height()))
		# self.bind("<FocusIn>", lambda arg: self.parent.file_handler.load_buffer(buffer_name=self.name))

	def reposition(self, last_buffer_tab=None):
		if (self.buffer_index == 1):
			self.place(x=0, y=25, height=18)
		else:
			self.place(x=last_buffer_tab.winfo_x()+last_buffer_tab.winfo_width()+3, y=25, height=18)

	def change_name(self, new_name: str=None, extra_char: str = ""):
		if (new_name): self.full_name = new_name; self.name = os.path.basename(new_name)
		self.configure(text=extra_char+self.name)

	def load_buffer(self, arg=None):
		self.focus_set()
		self.parent.file_handler.load_buffer(buffer_name=self.full_name)

	def focus_highlight(self):
		self.configure(bg=self.parent.theme["window"]["widget_fg"], fg=self.parent.theme["window"]["bg"])


class MENUBAR_LABEL(tkinter.Label):
	def __init__(self, parent, name):
		super().__init__(parent)
		self.parent = parent
		self.name = name

		self.bind("<Button-1>", lambda event: self.parent.file_menu_popup(self.name))
		self.bind("<Return>", lambda arg: self.parent.file_menu_popup(self.name))
		self.bind("<Alt_L>", lambda arg: self.parent.window_select("text", arg))
		self.bind("<Alt_R>", lambda arg: self.parent.window_select("text", arg))
		self.bind("<Escape>", lambda arg: self.parent.window_select("text", arg))


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
		self.bind("<Control-B><BackSpace>", lambda arg: self.parent.file_handler.del_file(arg, self.full_name))
		self.bind("<Control-b><BackSpace>", lambda arg: self.parent.file_handler.del_file(arg, self.full_name))

		self.bind("<Control-O>", lambda arg: self.parent.command_out_set(resize=True))
		self.bind("<Control-o>", lambda arg: self.parent.command_out_set(resize=True))
		
		self.bind("<Control-Tab>", self.switch_buffer)
		try: #linux bindings that throw errors on windows
			self.bind("<Control-Shift-ISO_Left_Tab>", lambda arg: self.switch_buffer(next=False))
		except Exception:
			self.bind("<Control-Shift-Tab>", lambda arg: self.switch_buffer(next=False))


		self.bind("<Control-space>", self.parent.command_entry_set)
		self.bind("<Control-Alt-space>", lambda arg: self.parent.command_out_set(resize=True))
		self.bind("<F11>", self.parent.set_fullscreen)
		self.bind("<Alt-Right>", lambda arg: self.parent.set_dimensions(arg, True))
		self.bind("<Alt-Left>", lambda arg: self.parent.set_dimensions(arg, True))
		self.bind("<Alt-Up>", lambda arg: self.parent.set_dimensions(arg, True))
		self.bind("<Alt-Down>", lambda arg: self.parent.set_dimensions(arg, True))
		self.bind("<Alt-Shift-Right>", lambda arg: self.parent.set_dimensions(arg, False))
		self.bind("<Alt-Shift-Left>", lambda arg: self.parent.set_dimensions(arg, False))
		self.bind("<Alt-Shift-Up>", lambda arg: self.parent.set_dimensions(arg, False))
		self.bind("<Alt-Shift-Down>", lambda arg: self.parent.set_dimensions(arg, False))

		self.bind("<Control-Alt_L>", lambda arg: self.parent.window_select("file_menu"))
		self.bind("<Control-Alt_R>", lambda arg: self.parent.window_select("file_menu"))

		self.bind("<F1>", lambda arg: self.bell())
		self.bind("<F2>", lambda arg: self.insert("insert", self.get_time()))
		self.bind("<F3>", lambda arg: self.parent.video_handler.screenshot())

	def configure_self(self):
		self.configure(bg = self.parent.theme["window"]["bg"], relief="flat", highlightthickness=0, cursor="pirate")

	def change_name(self, name):
		self.full_name = name
		self.name = os.path.basename(name)

	def switch_buffer(self, arg=None, next = True):
		if (next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index+1

		elif (not next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index-1

		if (buffer_tab_index >= len(self.parent.file_handler.buffer_list)):
			buffer_tab_index = 1

		elif (buffer_tab_index < 1):
			buffer_tab_index = len(self.parent.file_handler.buffer_list)-1
		
		self.parent.file_handler.load_buffer(buffer_index=buffer_tab_index)
		self.parent.command_out_set(f"buffer [{self.parent.txt.name}] was loaded")

		return "break"

class GRAPHICAL_BUFFER(BUFFER):
	def __init__(self, parent, name):
		super().__init__(parent, name)
		self.img = None
		self.picture_place()

		self.bind("<Control-period>", lambda arg: self.picture_resize(zoom=True))
		self.bind("<Control-comma>", lambda arg: self.picture_resize(zoom=False))

	def picture_place(self, arg=None):
		if (not self.img):
			self.img = Image.open(self.full_name)
			self.img_size = [self.img.size[0], self.img.size[1]]
		# if (self.parent.winfo_width() <= img.size[0] and self.parent.winfo_height() <= img.size[1]):
			# self.img_size = self.parent.winfo_width(), self.parent.winfo_height()
		self.img = self.img.resize(self.img_size, Image.ANTIALIAS)
			
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

class CHAT_BUFFER(BUFFER):
	def __init__(self, parent, name):
		super().__init__(self, parent, name)
		

class FIND_ENTRY(tkinter.Text):
	def __init__(self, parent):
		super().__init__(parent)

class COMMAND_OUT(tkinter.Text):
	def __init__(self, parent, name):
		super().__init__(parent)
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)

		self.arg = ""
		self.tags = []
		self.selected_lines = []

		self.font = self.parent.smaller_font_bold
		self.font_size = 9
		self.font_weight = "bold"

		# self.bind("<Key>", lambda arg: "break")
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

		self.bind("<Control-comma>", lambda arg: self.parent.set_font_size(arg, self))
		self.bind("<Control-period>", lambda arg: self.parent.set_font_size(arg, self))

		self.bind("<Control_L>", self.add_selection)
		self.bind("<Return>", self.use_selection)
		self.bind("<Shift-Return>", lambda arg: self.use_selection())

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
		
	def stdout(self, arg=None, tags=None):
		self.configure(state="normal")
		# print(arg)
		self.arg = ""
		self.arg = arg
		self.delete("1.0", "end")
		self.insert("1.0", self.arg)
		self.mark_set("insert", "1.0")

		if (tags):
			self.tags = []
			self.tags.append(tags)
			[self.tag_add("keywords", tag[0], tag[1]) for tag in tags]

		self.configure(state="disabled")

	def empty_function(self, arg=None):
		pass

	def change_ex(self, new_ex):
		self.ex = new_ex

	def ex(self, arg=None):
		pass

	def add_selection(self, arg=None):
		if (arg):
			self.tag_add("command_out_select_bg", "insert linestart", "insert lineend")
			for i, line in enumerate(self.selected_lines, 0):
				if (line == self.get("insert linestart", "insert lineend")):
					print("oh shit it working")
					self.selected_lines.pop(i)
					self.tag_remove("command_out_select_bg", "insert linestart", "insert lineend")
					return "break"
			
		self.selected_lines.append(self.get("insert linestart", "insert lineend"))

		return "break"
			
	def use_selection(self, arg=None):
		if (arg): self.add_selection()
		self.ex(self.selected_lines)
		del self.selected_lines[:]

		return "break"

	def open_line(self, arg=None):
		num_results = []
		for line in arg:
			if (re.search(r"line [0-9]+", line)):
				match = re.search(r"line [0-9]+", line).group()[5:]
			else:
				match = re.search(r"[0-9]+", line)

			if (match):
				index = self.parent.convert_line_index("float", match)
				self.parent.txt.mark_set("insert", index)
				self.parent.txt.see("insert")
		
		return "break"
		
	def file_explorer(self, arg=None):
		for line in arg:
			line = f"{self.parent.file_handler.current_dir}/{line}"
			print(line)
			if (os.path.isfile(line)):
				self.parent.file_handler.load_file(filename=line)
			elif (os.path.isdir(line)):
				self.parent.file_handler.current_dir = os.path.normpath(line)
				self.parent.file_handler.ls()
			
		return "break"


class TEXT(tkinter.Text):
	def __init__(self, parent, name):
		super().__init__(parent)
		
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)
		self.buffer_index = len(self.parent.file_handler.buffer_list)
		
		self.make_argv = ""

		self.highlighter = highlighter(self.parent, self)
		self.set_highlighter()

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

		# self.text_len = ""
		self.change_index = ""


		self.bind("<KeyRelease>", self.parent.update_buffer)
		self.bind("<KeyRelease-BackSpace>", self.delete_selection_start_index)

		self.bind("<Control-period>", self.parent.set_font_size)
		self.bind("<Control-comma>", self.parent.set_font_size)
		self.bind("<Control-MouseWheel>", self.parent.set_font_size)
		self.bind("<Control-Button-4>", self.parent.set_font_size)
		self.bind("<Control-Button-5>", self.parent.set_font_size)

		self.bind("<Button-1>", self.parent.update_buffer)
		self.bind("<B1-Motion>", self.parent.update_index)
		
		self.bind("<Up>", self.parent.move)
		self.bind("<Down>", self.parent.move)
		self.bind("<Left>", self.parent.move)
		self.bind("<Right>", self.parent.move)
		self.bind("<Control-Up>", self.parent.move)
		self.bind("<Control-Down>", self.parent.move)
		self.bind("<Control-Left>", self.parent.move)
		self.bind("<Control-Right>", self.parent.move)

		# self.bind("<Shift-Up>", self.parent.queue_make)
		# self.bind("<Shift-Down>", self.parent.queue_make)
		# self.bind("<Shift-Left>", self.parent.queue_make)
		# self.bind("<Shift-Right>", self.parent.queue_make)

		self.bind("<Shift-Up>", lambda arg: self.parent.move(arg, prefix="Select"))
		self.bind("<Shift-Down>", lambda arg: self.parent.move(arg, prefix="Select"))
		self.bind("<Shift-Left>", lambda arg: self.parent.move(arg, prefix="Select"))
		self.bind("<Shift-Right>", lambda arg: self.parent.move(arg, prefix="Select"))

		self.bind("<MouseWheel>", self.parent.scroll)
		self.bind("<Button-4>", self.parent.scroll)
		self.bind("<Button-5>", self.parent.scroll)
		self.bind("<Shift-MouseWheel>", lambda arg: self.parent.scroll(arg, multiplier=3))
		self.bind("<Shift-Button-4>", lambda arg: self.parent.scroll(arg, multiplier=3))
		self.bind("<Shift-Button-5>", lambda arg: self.parent.scroll(arg, multiplier=3))
		self.bind("<Button-3>", self.parent.popup) #right click pop-up window

		self.bind("<Return>", self.parent.keep_indent)
		self.bind("<Control-slash>", self.parent.comment_line) #self.comment_line)

		self.bind("<Control-quotedbl>", self.parent.char_enclose)		#"
		# self.bind("<Control-apostrophe>", self.parent.char_enclose)		#'
		self.bind("<Control-parenleft>", self.parent.char_enclose) 		#( 
		self.bind("<Control-bracketleft>", self.parent.char_enclose) 	#[
		self.bind("<Control-braceleft>", self.parent.char_enclose) 		#{


		self.bind("<Control-S>", self.parent.file_handler.save_file)
		self.bind("<Control-s>", self.parent.file_handler.save_file)
		self.bind("<Control-Shift-S>", self.parent.file_handler.save_file_as)
		self.bind("<Control-Shift-s>", self.parent.file_handler.save_file_as)
		self.bind("<Control-N>", self.parent.file_handler.new_file)
		self.bind("<Control-n>", self.parent.file_handler.new_file)
		self.bind("<Control-B>L", self.parent.file_handler.load_file)
		self.bind("<Control-b>l", self.parent.file_handler.load_file)
		self.bind("<Control-B>W", lambda arg: self.parent.file_handler.close_buffer(arg, self.full_name))
		self.bind("<Control-b>w", lambda arg: self.parent.file_handler.close_buffer(arg, self.full_name))
		self.bind("<Control-w>", self.parent.win_destroy)
		self.bind("<Control-W>", self.parent.win_destroy)
		self.bind("<Control-B><BackSpace>", lambda arg: self.parent.file_handler.del_file(arg, self.full_name))
		self.bind("<Control-b><BackSpace>", lambda arg: self.parent.file_handler.del_file(arg, self.full_name))

		self.bind("<Control-O>", lambda arg: self.parent.command_out_set(resize=True))
		self.bind("<Control-o>", lambda arg: self.parent.command_out_set(resize=True))

		self.bind("<Control-F>", self.parent.find_place)
		self.bind("<Control-f>", self.parent.find_place)
		self.bind("<Control-V>", self.parent.paste)
		self.bind("<Control-v>", self.parent.paste)

		self.bind("<Control-Z>", self.parent.undo)
		self.bind("<Control-z>", self.parent.undo)
		self.bind("<Control-Y>", self.parent.redo)
		self.bind("<Control-y>", self.parent.redo)
		self.bind("<Control-A>", self.parent.select_all)
		self.bind("<Control-a>", self.parent.select_all)
		self.bind("<Control-L>", self.parent.change_case)
		self.bind("<Control-l>", self.parent.change_case)
		self.bind("<Control-Shift-L>", self.parent.change_case)
		self.bind("<Control-Shift-l>", self.parent.change_case)

		self.bind("<Control-K>", self.parent.get_selection_count)
		self.bind("<Control-k>", self.parent.get_selection_count)

		self.bind("<Tab>", self.parent.indent)
		self.bind("<Control-Tab>", self.switch_buffer)
		try: #linux bindings that throw errors on windows
			self.bind("<Shift-ISO_Left_Tab>", self.parent.unindent)
			self.bind("<Control-Shift-ISO_Left_Tab>", lambda arg: self.switch_buffer(next=False))
			self.parent.command_entry.bind("<KP_Enter>", self.parent.cmmand)
		except Exception:
			self.bind("<Shift-Tab>", self.parent.unindent)
			self.bind("<Control-Shift-Tab>", lambda arg: self.switch_buffer(next=False))

		# self.bind("<Control-Q>", self.parent.test_function)
		# self.bind("<Control-q>", self.parent.test_function)
		self.bind("<Control-Q>", lambda arg: self.highlighter.suggest(self.parent.cursor_index[0], self.parent.current_line))
		self.bind("<Control-q>", lambda arg: self.highlighter.suggest(self.parent.cursor_index[0], self.parent.current_line))

		self.bind("<Insert>", self.parent.set_cursor_mode)
		self.bind("<Home>", self.parent.home)
		self.bind("<Shift-Home>", self.parent.home_select)
		self.bind("<End>", self.parent.end)
		self.bind("<Shift-End>", self.parent.end_select)

		self.bind("<Shift-Return>", lambda arg: self.run_subprocess(make=True))

		self.bind("<Control-space>", self.parent.command_entry_set)
		self.bind("<Control-Alt-space>", lambda arg: self.parent.command_out_set(resize=True))
		self.bind("<F11>", self.parent.set_fullscreen)
		self.bind("<Alt-Right>", lambda arg: self.parent.set_dimensions(arg, True))
		self.bind("<Alt-Left>", lambda arg: self.parent.set_dimensions(arg, True))
		self.bind("<Alt-Up>", lambda arg: self.parent.set_dimensions(arg, True))
		self.bind("<Alt-Down>", lambda arg: self.parent.set_dimensions(arg, True))
		self.bind("<Alt-Shift-Right>", lambda arg: self.parent.set_dimensions(arg, False))
		self.bind("<Alt-Shift-Left>", lambda arg: self.parent.set_dimensions(arg, False))
		self.bind("<Alt-Shift-Up>", lambda arg: self.parent.set_dimensions(arg, False))
		self.bind("<Alt-Shift-Down>", lambda arg: self.parent.set_dimensions(arg, False))

		self.bind("<Control-Alt_L>", lambda arg: self.parent.window_select("file_menu"))
		self.bind("<Control-Alt_R>", lambda arg: self.parent.window_select("file_menu"))

		self.bind("<F1>", lambda arg: self.bell())
		self.bind("<F2>", lambda arg: self.insert("insert", self.get_time()))
		self.bind("<F3>", lambda arg: self.parent.video_handler.screenshot())

		# self.bind("<FocusIn>", self.test)

	def configure_self(self):
		self.configure(font=self.font,bg = self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"], undo=True, maxundo=0,
		 spacing1=0, insertborderwidth=0, insertwidth=0, insertofftime=self.insert_offtime, insertontime=self.insert_ontime, insertunfocussed="hollow",
		 insertbackground=self.parent.theme["window"]["insertbg"], inactiveselectbackground=self.parent.theme["window"]["selectbg"],
		 selectbackground=self.parent.theme["window"]["selectbg"], selectforeground=self.parent.theme["window"]["selectfg"],
		 selectborderwidth=0, borderwidth=1, relief="flat", tabs=(f"{self.font.measure(' ' * 4)}"), wrap="word", exportselection=True,
		 blockcursor=self.block_cursor, highlightthickness=0, cursor="pirate")

	def change_name(self, name):
		self.full_name = name
		self.name = os.path.basename(name)

	def delete_selection_start_index(self, arg=None):
		""" This has to be a function and I hate it """
		self.parent.selection_start_index = None
		self.parent.update_index()


	def get_time(self, arg=None):
		date = datetime.date.today()
		day_name = datetime.date.today().strftime("%A")
		return f"~\t[ {day_name} ] [ {self.parent.get_time()} ] [ {date} ] "


	def change_coords(self, coords: list):
		self.coords = coords
		self.place(x=coords[0], y=coords[1], width=coords[2], height=coords[3], anchor="nw")


	def set_highlighter(self):
		""" sets the highlighter accordingly to the current file extension """
		try:
			arg = self.name.split(".")[-1]
			print(arg)
		except Exception:
			arg = "NaN"

		if (arg == "py" or arg == "pyw"): self.make_argv = f"python3 {self.name}"
		elif (arg == "c" or arg == "h" or arg == "cc" or arg == "hh" or arg == "cpp" or arg == "hpp"): self.make_argv = "make"
		elif (arg == "html"): self.make_argv = f"firefox {self.full_name}"
		print(self.make_argv)

		self.parent.highlighting = True
		self.highlighter.set_languague(arg)


	def switch_buffer(self, arg=None, next = True):
		if (next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index+1

		elif (not next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index-1

		if (buffer_tab_index >= len(self.parent.file_handler.buffer_list)):
			buffer_tab_index = 1

		elif (buffer_tab_index < 1):
			buffer_tab_index = len(self.parent.file_handler.buffer_list)-1
		
		self.parent.file_handler.load_buffer(buffer_index=buffer_tab_index)
		self.parent.command_out_set(f"buffer [{self.parent.txt.name}] was loaded")

		return "break"


	def run_subprocess(self, argv=None, make=False):
		if (make):
			argv = self.make_argv.split(" ")
			self.parent.command_out.change_ex(self.parent.command_out.open_line)
		print(argv)
		def run():
			process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			out = process.stdout.read().decode("UTF-8")

			self.parent.command_out_set(out, focus=False)
			print(out)
			
		threading.Thread(target=run).start()
		return "break"



















