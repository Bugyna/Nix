import tkinter
import os

class BUFFER_TAB(tkinter.Label):
	def __init__(self, name: str, parent):
		super().__init__(parent)
		self.parent = parent
		self.name = name
		self.index = len(self.parent.file_handler.buffers)
		self.configure(text=os.path.basename(self.name), font=self.parent.widget_font, 
		bg="#111111", fg=self.parent.theme["window"]["widget_fg"],
		 highlightcolor=self.parent.theme["window"]["widget_fg"])
		# self.configure(command=lambda: self.parent.file_handler.load_buffer(buffer_name=self.name))
		
		if (self.index > 1):
			self.reposition(list(self.parent.file_handler.buffers.values())[self.index-1][1])
		elif (self.index == 1):
			self.reposition()

		self.menu = tkinter.Menu(self.parent)
		self.menu.configure(font=self.parent.widget_font, tearoff=False,fg="#FFFFFF", bg=self.parent.theme["window"]["bg"], bd=0)
		self.menu.add_command(label="Close", command=lambda: self.parent.file_handler.del_buffer(buffer_name=self.name))

		self.hover_info = tkinter.Label(self.parent)
		self.hover_info.configure(text=self.name, font=self.parent.widget_font, fg="#FFFFFF", bg=self.parent.theme["window"]["bg"], bd=1)
		# self.hover_info.place(x=self.winfo_rootx(), y=self.winfo_rooty()+self.winfo_height())
		# self.hover_info.pack()
		# self.destroy_label = tkinter.Label(self, text="X"); self.destroy_label.place(relx=1, y=0, width=10, height=10, anchor="ne")
		# self.destroy_label.bind("<Button-1>", lambda arg: self.parent.file_handler.del_buffer(buffer_name=self.name))

		self.bind("<Button-1>", self.load_buffer)
		# self.bind("<Enter>", lambda arg: self.hover_info.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height()), print("aa"))
		self.bind("<Enter>", lambda arg: self.parent.command_O(self.name))
		# self.bind("<Leave>", lambda arg: self.hover_info.place_forget())
		self.bind("<Button-3>", lambda arg: self.menu.tk_popup(self.winfo_rootx(), self.winfo_rooty()+self.winfo_height()))
		# self.bind("<FocusIn>", lambda arg: self.parent.file_handler.load_buffer(buffer_name=self.name))

	def reposition(self, last_buffer_tab=None):
		if (not last_buffer_tab or self.index == 1):
			self.place(x=0, y=24, height=18)
		else:
			self.place(x=last_buffer_tab.winfo_x()+last_buffer_tab.winfo_width()+3, y=24, height=18)

	def change_name(self, new_name: str):
		self.name = new_name
		self.configure(text="~"+os.path.basename(new_name))

	def load_buffer(self, arg=None):
		self.focus_set()
		self.parent.file_handler.load_buffer(buffer_name=self.name)
		self.parent.file_handler.buffer_tab_index = self.index


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
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

		self.bind("<KeyRelease>", self.parent.update_buffer)
		self.bind("(", self.parent.bracket_pair_make)
		self.bind(")", self.parent.bracket_pair_make)
		self.bind("[", self.parent.bracket_pair_make)
		self.bind("]", self.parent.bracket_pair_make)
		self.bind("{", self.parent.bracket_pair_make)
		self.bind("}", self.parent.bracket_pair_make)
		self.bind("<KeyRelease>-<Delete>", self.parent.bracket_pair_make)
		# self.bind("<Delete>", self.parent.bracket_pair_make)
		# self.bind("<Backspace>", self.parent.bracket_pair_make)

		self.bind("<Control-period>", self.parent.set_font_size)
		self.bind("<Control-comma>", self.parent.set_font_size)
		self.bind("<Control-MouseWheel>", self.parent.set_font_size)
		self.bind("<Control-Button-4>", self.parent.set_font_size)
		self.bind("<Control-Button-5>", self.parent.set_font_size)

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
		self.bind("<Tab>", self.parent.indent)
		try: #linux bindings that throw errors on windows
			self.bind("<Shift-ISO_Left_Tab>", self.parent.unindent)
			self.parent.command_entry.bind("<KP_Enter>", self.parent.cmmand)
		except Exception:
			self.bind("<Shift-Tab>", self.parent.unindent)


		self.bind("<Control-Tab>", self.switch_buffer)
		self.bind("<Control-Shift-ISO_Left_Tab>", lambda arg: self.switch_buffer(next=False))

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

		# self.bind("<KeyPress>", lambda arg: self.parent.update_buffer())
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

	def switch_buffer(self, arg=None, next = True):
		if (next): buffer_tab_index = self.parent.file_handler.buffer_tab_index+1
		elif (not next): buffer_tab_index = self.parent.file_handler.buffer_tab_index-1
		if (buffer_tab_index >= len(self.parent.file_handler.buffers)): buffer_tab_index = 1
		elif (buffer_tab_index < 1): buffer_tab_index = len(self.parent.file_handler.buffers)-1
		buffer_name = list(self.parent.file_handler.buffers.values())[buffer_tab_index][1].name
		print(buffer_name, buffer_tab_index)
		self.parent.file_handler.load_buffer(buffer_name=buffer_name)

		return "break"