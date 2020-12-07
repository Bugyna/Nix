import subprocess
import threading
import tkinter
import datetime
import time
import os

from tkinter import font

from highlighter import highlighter

class BUFFER_TAB(tkinter.Label):
	def __init__(self, name: str, parent):
		super().__init__(parent)
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)

		self.buffer_index = len(self.parent.file_handler.buffer_list)
		self.configure(text=" "+os.path.basename(self.name))
		self.configure(text=" "+os.path.basename(self.name), font=self.parent.widget_font, 
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
		self.menu.add_command(label="Close", command=lambda: self.parent.file_handler.del_buffer(buffer_name=self.full_name))

		self.hover_info = tkinter.Label(self.parent)
		self.hover_info.configure(text=self.name, font=self.parent.widget_font, fg="#FFFFFF", bg=self.parent.theme["window"]["bg"], bd=1)

		# self.hover_info.place(x=self.winfo_rootx(), y=self.winfo_rooty()+self.winfo_height())
		# self.hover_info.pack()
		# self.destroy_label = tkinter.Label(self, text="X"); self.destroy_label.place(relx=1, y=0, width=10, height=10, anchor="ne")
		# self.destroy_label.bind("<Button-1>", lambda arg: self.parent.file_handler.del_buffer(buffer_name=self.name))

		self.bind("<Button-1>", self.load_buffer)
		# self.bind("<Enter>", lambda arg: self.hover_info.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height()), print("aa"))
		self.bind("<Enter>", lambda arg: self.parent.command_O(self.full_name))
		# self.bind("<Leave>", lambda arg: self.hover_info.place_forget())
		self.bind("<Button-3>", lambda arg: self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty()+self.winfo_height()))
		# self.bind("<FocusIn>", lambda arg: self.parent.file_handler.load_buffer(buffer_name=self.name))

	def reposition(self, last_buffer_tab=None):
		if (not last_buffer_tab or self.buffer_index == 1):
			self.place(x=0, y=24, height=18)
		else:
			self.place(x=last_buffer_tab.winfo_x()+last_buffer_tab.winfo_width()+3, y=24, height=18)

	def change_name(self, new_name: str=None, extra_char: str = ""):
		if (new_name): self.full_name = new_name; self.name = os.path.basename(new_name)
		self.configure(text=extra_char+os.path.basename(self.full_name))

	def load_buffer(self, arg=None):
		self.focus_set()
		self.parent.file_handler.load_buffer(buffer_name=self.full_name)


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


class TEXT(tkinter.Text):
	def __init__(self, parent, name):
		super().__init__(parent)
		print("name: ", name)
		self.parent = parent
		self.full_name = name
		self.name = os.path.basename(name)
		self.buffer_index = len(self.parent.file_handler.buffer_list)
		
		self.highlighter = highlighter(self.parent, self)
		self.set_highlighter()

		self.font_size = 11
		self.sfont_size = self.font_size - 2
		
		self.block_cursor = False
		self.terminal_like_cursor = True
		self.insert_offtime = 0; self.insert_ontime = 1

		self.text_len = ""

		self.bind("<KeyRelease>", self.parent.update_buffer)

		self.bind("<Control-period>", self.parent.set_font_size)
		self.bind("<Control-comma>", self.parent.set_font_size)
		self.bind("<Control-MouseWheel>", self.parent.set_font_size)
		self.bind("<Control-Button-4>", self.parent.set_font_size)
		self.bind("<Control-Button-5>", self.parent.set_font_size)

		self.bind("<F2>", lambda arg: self.insert("insert", self.get_time()))

		self.bind("<Button-1>", self.parent.update_index)
		self.bind("<B1-Motion>", self.parent.update_index)

		self.bind("<Prior>", self.parent.del_queue)
		self.bind("<Next>", self.parent.del_queue)
		self.bind("<Up>", self.parent.move)
		self.bind("<Down>", self.parent.move)
		self.bind("<Left>", self.parent.move)
		self.bind("<Right>", self.parent.move)
		self.bind("<Control-Up>", self.parent.move)
		self.bind("<Control-Down>", self.parent.move)
		self.bind("<Control-Left>", self.parent.move)
		self.bind("<Control-Right>", self.parent.move)

		self.bind("<MouseWheel>", self.parent.scroll)
		self.bind("<Button-4>", self.parent.scroll)
		self.bind("<Button-5>", self.parent.scroll)
		self.bind("<Shift-MouseWheel>", lambda arg: self.parent.scroll(arg, multiplier=3))
		self.bind("<Shift-Button-4>", lambda arg: self.parent.scroll(arg, multiplier=3))
		self.bind("<Shift-Button-5>", lambda arg: self.parent.scroll(arg, multiplier=3))
		self.bind("<Button-3>", self.parent.popup) #right click pop-up window

		self.bind("<Return>", self.parent.keep_indent)
		self.bind("<Control-slash>", self.parent.comment_line) #self.comment_line)

		self.bind("<Control-S>", self.parent.file_handler.save_file)
		self.bind("<Control-s>", self.parent.file_handler.save_file)
		self.bind("<Control-Shift-S>", self.parent.file_handler.save_file_as)
		self.bind("<Control-Shift-s>", self.parent.file_handler.save_file_as)
		self.bind("<Control-N>", self.parent.file_handler.new_file)
		self.bind("<Control-n>", self.parent.file_handler.new_file)
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
		self.bind("<Control-L>", lambda arg: self.parent.change_case("lower"))
		self.bind("<Control-l>", lambda arg: self.parent.change_case("lower"))
		self.bind("<Control-Shift-L>", lambda arg: self.parent.change_case("upper"))
		self.bind("<Control-Shift-l>", lambda arg: self.parent.change_case("upper"))

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

		self.bind("<Shift-Up>", self.parent.queue_make)
		self.bind("<Shift-Down>", self.parent.queue_make)
		self.bind("<Shift-Left>", self.parent.queue_make)
		self.bind("<Shift-Right>", self.parent.queue_make)
		# self.bind("<Shift-Return>", lambda arg: subprocess.call("./open.sh"))

		self.bind("<Control-Q>", self.parent.test_function)
		self.bind("<Control-q>", self.parent.test_function)
		# self.bind("<Shift_L>", self.parent.Qq)

		self.bind("<Insert>", self.parent.set_cursor_mode)
		self.bind("<Home>", self.parent.home)
		self.bind("<Shift-Home>", self.parent.home_select)
		self.bind("<End>", self.parent.end)
		self.bind("<Shift-End>", self.parent.end_select)

		self.bind("<Shift-Return>", lambda arg: self.run_subprocess(argv=["make"]))

		self.bind("<Control-space>", self.parent.command_entry_set)
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

		# self.bind("<FocusIn>", self.test)

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
			arg = os.path.basename(self.parent.file_handler.current_file_name).split(".")[-1]
		except Exception:
			arg = "NaN"

		if (arg in self.highlighter.supported_languagues):
			self.parent.highlighting = True
			self.highlighter.set_languague(arg)
		else:
			self.parent.highlighting = False

	def switch_buffer(self, arg=None, next = True):
		if (next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index+1

		elif (not next):
			buffer_tab_index = self.parent.file_handler.buffer_tab_index-1

		if (buffer_tab_index >= len(self.parent.file_handler.buffer_list)):
			buffer_tab_index = 1

		elif (buffer_tab_index < 1):
			buffer_tab_index = len(self.parent.file_handler.buffer_list)-1
			
		buffer_name = self.parent.file_handler.buffer_list[buffer_tab_index][0].full_name
		
		self.parent.file_handler.load_buffer(buffer_name=buffer_name)

		return "break"

	def run_subprocess(self, argv):
		def run():
			process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			out = process.stdout.read().decode("UTF-8")

			self.parent.command_O(out, focus=False)
			print(out)
			
		threading.Thread(target=run).start()
		return "break"

class GRAPHICAL_BUFFER: # FORESHADOWING
	def __init__(self):
		pass