import random
import tkinter
import asyncio
from tkinter import ttk
from tkinter import font
import re
import threading
import os, sys
import tqdm
from time import sleep, time
from tkinter import filedialog
from functools import partial

from highlighter import python_highlighter, C_highlighter

# keywords = [
# 	'False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in',
# 	 'raise', 'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for',
# 	  'lambda', 'try', 'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del',
# 	   'global', 'not', 'with', 'async', 'elif', 'if', 'or', 'yield', "self"
# 	   ]

# keywords = [
# 		'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
# 		 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof',
# 		  'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while',
# 		   "int", "char", "bool"
#    ]

# sumn = ['self']
# var_types = ['int', 'float', 'string', 'str', 'list']
# other_chars = ["$","#","@","&","|","^","_","\\",r"\\",r"\[\]",r"[\\]"]
# all_key = [keywords, other_chars]
# all_key = list(chain.from_iterable(all_key))
#print(all_key)

#print(chr(9619))

for i in tqdm.tqdm(range(10)):
   sleep(0.01)




class win():
	def __init__(self, root, file=None):
		#self.background_color = "#000000"
		#self.foreground_color = "#9F005F"
		self.theme_options = {
			"cake": {"bg" : "#000000", "fg": "#999999", "insertbg": "#CCCCCC", "selectbg": "#CCCCCC", "keywords": "other_chars", "functions": "modules", "numbers": "var_types", "special_chars": "special_chars", "quotes": "quotes", "comments": "comments"},
			"muffin" : {"bg" : "#CCCCCC", "fg": "#9F005F", "insertbg": "#111111", "selectbg": "#111111", "keywords": "other_chars", "functions": "modules", "numbers": "var_types", "special_chars": "special_chars", "quotes": "quotes", "comments": "comments"},
			"toast" : {"bg" : "#000000", "fg": "#9F005F", "insertbg": "#CCCCCC", "selectbg": "#CCCCCC", "keywords": "var_types", "functions": "modules", "numbers": "var_types", "special_chars": "special_chars", "quotes": "quotes", "comments": "comments"},
			"student" : {"bg" : "#222222", "fg": "#FFFFFF"}
			}
		self.theme = self.theme_options["cake"]
		print(self.theme)

		self.command_definition = {
			"l" : "-get: gets last line number || -[LINE_NUMBER(.CHARACTER)]: puts you to line number (eg. 120(by default starts at column 0 but you can specify the column like: 120.5)",
			"highlighting" : "-on: turns highlighting on -off: turns highlighting off"
		}

		self.command_input_history = []
		self.command_input_history_index = 0

		self.current_file = None #open(f"{os.getcwd()}/untitled.txt", "w+") #stores path to currently opened file
		self.current_file_name = None
		self.content = ""

		self.scroll_multiplier = 0

		self.line_count = None
		self.last_index = 1

		self.tab_offset = 0
		self.tab_lock = False
		
		self.highlighter = None
		self.highlighting = False #now its turned off by default # turned on by default because it finally works (still, fuck regex)
		self.command_highlighting = False


		self.loading = False
		self.fullscreen = False
		self.run = True


		#configuring main window
		#root.overrideredirect(True)
		root.resizable(True,True)
		root.geometry("600x400")
		#root.minsize(width=200, height=200)
		#self.title_bar = tkinter.Frame(bg="blue", relief='raised', bd=2)
		root.title(f"N Editor: <None>") #{os.path.basename(self.current_file.name)}
		#root.overrideredirect(True)
		#prints all fonts you have installed
		#fonts = list(font.families())
		#for item in fonts:
		#    print(item)

		#configuring fonts
		# self.font = font.Font(family="Px437 IBM CGA", size=9, weight="bold")
		# self.smaller_font = font.Font(family="Px437 IBM CGA", size=7, weight="bold")
		self.init()

	def init(self):
		""" a completely useless initialize function """
		
		self.update_win()
		
		root.config(bg=self.theme["bg"])
		root.wm_attributes("-alpha", 0.9)
			
		self.Font_size = 11
		self.sFont_size = self.Font_size - 2
		self.font = font.Font(family="Ubuntu", size=self.Font_size, weight="normal")
		self.smaller_font = font.Font(family="Ubuntu",size=self.sFont_size, weight="normal")

		#filediaolog pretty much self-explanatory
		self.filename = filedialog

		# self.canvas = tkinter.Canvas(bg=self.theme["bg"])
		# self.canvas.create_line(3, 23, 38, 23, dash=(6, 3), fill="#CCCCCC")
		# self.canvas.place(x=0, y=0, relwidth=1, relheight=1)

		#text widget configuration
		self.txt = tkinter.Text()

		self.txt.configure(font=self.font,bg = self.theme["bg"],fg=self.theme["fg"], undo=True, spacing1=2,
			insertwidth=0, insertofftime=0, insertontime=1, insertbackground=self.theme["insertbg"], selectbackground=self.theme["selectbg"],
			borderwidth=0, relief="ridge", tabs=(f"{(self.Font_size/2-1)*4}"), wrap="word", blockcursor=True, highlightthickness=0, insertborderwidth=0)

		# self.txt.place(x=0,y=25,relwidth=0.9975, relheight=0.9475, anchor="nw", bordermode="outside") "#A2000A"
		
		#scrollbar configuration
		# self.scrollb = tkinter.Scrollbar(root, command=self.txt.yview, relief="flat") #self.scrollb.grid(row=0,column=2,sticky="nsew")
		# self.scrollb.place(relx=0.985, rely=0.0, relwidth=0.15, relheight=.95)
		# self.txt['yscrollcommand'] = self.scrollb.set

		#line and column number label
		self.line_no = tkinter.Label(text="aaa",fill=None ,justify=tkinter.RIGHT, font=self.font,bg = self.theme["bg"],fg="#999999") #self.line_no.grid(row=1,column=2)
		self.line_no.place(relx=0.85, y=20, height=15, anchor="sw")
		
		
		#command line entry
		self.command_entry = tkinter.Entry(text="aa", justify=tkinter.LEFT, font=self.font,
		bg = self.theme["bg"],fg="#555555", insertwidth=0, insertofftime=0, insertbackground="#CCCCCC", relief="flat")
		#self.command_entry.grid(row=1,column=0,ipady=3);
		# self.command_entry.place(x=0.0,rely=0.99, relwidth=0.25, height=15, anchor="sw")


		#command output
		self.command_out = tkinter.Label(font=self.smaller_font, text="biog bruh", bg=self.theme["bg"], fg="#00df00",
		 justify=tkinter.CENTER, anchor="w")
		# self.command_out.place(relx=0.28,rely=0.99, relwidth=0.25, height=15, anchor="sw")

		#progressbar
		#self.progress_bar = p_bar(root) #.grid(row=1,column=1)8
		#self.style=ttk.Style()
		#self.style.theme_use("clam")
		#self.style.configure("color.Horizontal.TProgressbar", foreground="white", background="white")
		#self.progress_bar = ttk.Progressbar(orient=tkinter.HORIZONTAL, style="color.Horizontal.TProgressbar",
		# length=100, mode='determinate')
		#self.progress_bar.place(relx=0.35,rely=0.975,relwidth=0.3,relheight=0.025)

		#right click pop-up menu
		self.right_click_menu = tkinter.Menu(tearoff=0, font=self.smaller_font, bg=self.theme["bg"], fg="#ffffff")
		self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
		self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
		self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
		self.right_click_menu.add_separator()

		#menubar
		#self.menubar = tkinter.Menu(root, font=self.font, bg="black") #declare menubar
		#self.menubar.configure(font=self.font, bg="black") #configure font and background

		#self.menubar_button = tkinter.Button(root, text="File" ,font=self.font, bg=self.background_color, fg=self.foreground_color, command=self.popup).place(relx=0,rely=0,relwidth=0.05)

		self.file_menubar_label = tkinter.Label(root, text="File" ,font=self.font, bg=self.theme["bg"], fg="#999999")
		# self.file_separator_label = tkinter.Label(root, text="----" ,font=self.font, bg=self.theme["bg"], fg="#999999").place(x=0, y=15, height=2, anchor="nw")
		self.file_menubar_label.bind("<Button-1>", 
			lambda event: self.file_menu_popup("file_menu"))
		self.file_menubar_label.place(x=0, y=5, height=15, anchor="nw")

		self.settings_menubar_label = tkinter.Label(root, text="Settings" ,font=self.font, bg=self.theme["bg"], fg="#999999")
		# self.settings_separator_label = tkinter.Label(root, text="--------" ,font=self.font, bg=self.theme["bg"], fg="#999999").place(x=60, y=15, height=2, anchor="nw")
		self.settings_menubar_label.bind("<Button-1>",
			lambda event: self.file_menu_popup("settings_menu"))
		self.settings_menubar_label.place(x=60, y=5, height=15, anchor="nw")


		#dropdown for menubar
		self.file_dropdown = tkinter.Menu(font=self.font, tearoff=False,fg="#FFFFFF", bg=self.theme["bg"]) #declare dropdown
		self.file_dropdown.add_command(label="New file",command=self.new_file) #add commands
		self.file_dropdown.add_command(label="Open file",command=self.load_file)
		self.file_dropdown.add_command(label="Save file",command=self.save_file)
		self.file_dropdown.add_command(label="Save file as",command=self.save_file_as)
		#self.menubar.add_cascade(label="File",menu=self.file_dropdown) #add dropdown to menubar
		#self.file_dropdown.add_separator()
		#self.file_dropdown.add_command(label="EXIT")

		#root.config(menu=self.menubar)#adds menubar to main window

		#tags for highlighting
		self.txt.tag_configure("sumn", foreground="#74091D")
		self.txt.tag_configure("special_chars",foreground="#ff00bb")
		self.txt.tag_configure("var_types",foreground="#01cdfe")
		self.txt.tag_configure("operators",foreground="#05ffa1")
		self.txt.tag_configure("keywords", foreground="#ff5500")
		self.txt.tag_configure("quotes", foreground="#f75f00")
		self.txt.tag_configure("default", foreground="#302387")
		self.txt.tag_configure("modules", foreground="#B71DDE")
		self.txt.tag_configure("other_chars", foreground="#302387")
		self.txt.tag_configure("comments", foreground="#333333")
		self.txt.tag_configure("tabs", background="#444444")
		self.txt.tag_configure("command_keywords", background="#FFFFFF")

		#command binding
		self.line_no.bind("<Button-3>", self.detach_widget)
		self.command_entry.bind("<Return>", self.cmmand) #if you press enter in command line it executes the command and switches you back to text widget
		self.command_entry.bind("<Up>", self.command_history) # lets you scroll through commands you have already used
		self.command_entry.bind("<Down>", self.command_history)
		self.command_entry.bind("<Escape>", self.command_entry_unset)
		self.command_out.bind("<Return>", lambda arg: self.txt.focus_set())
		self.txt.unbind("<MouseWheel>")
		self.txt.unbind("<Button-4>")
		self.txt.unbind("<Button-5>")
		self.txt.bind("<MouseWheel>", self.scroll)
		self.txt.bind("<Button-4>", self.scroll)
		self.txt.bind("<Button-5>", self.scroll)
		self.txt.bind("<Alt-MouseWheel>", lambda arg: self.scroll(arg, multiplier=3))
		self.txt.bind("<Alt-Button-4>", lambda arg: self.scroll(arg, multiplier=3))
		self.txt.bind("<Alt-Button-5>", lambda arg: self.scroll(arg, multiplier=3))
		self.txt.bind("<Button-3>", self.popup) #right click pop-up window
		self.txt.bind("<Control-s>", self.save_file)
		self.txt.bind("<Control-S>", self.save_file)
		self.txt.bind("<Return>", self.set_tab_lock)
		try:
			self.txt.bind("<Shift-ISO_Left_Tab>", self.unindent)
		except Exception:
			self.txt.bind("<Shift-Tab>", self.unindent)
		root.bind("<Control-space>", self.command_entry_set)
		root.bind("<F11>", self.set_fullscreen)
		root.bind("<Alt-Right>", self.set_dimensions)
		root.bind("<Alt-Left>", self.set_dimensions)
		root.bind("<Alt-Up>", self.set_dimensions)
		root.bind("<Alt-Down>", self.set_dimensions)
		#self.txt.bind("<Tab>", self.cmmand)
		#self.txt.bind("<Control_L><k>", self.cmmand)

		#self.checked = [] #checked lines (for syntax highlighting optimization not yet added)
		#self.keys = [] #no idea 



		self.a=""
		if self.current_file_name:
			self.load_file()


		self.loading_label_background = tkinter.Label(root, bg="#999999", fg="#FFFFFF")
		# self.loading_label_background.place(relx=0.52,rely=0.965, relwidth=0.205 ,relheight=0.015)
		self.loading_label = tkinter.Label(root, text="", bg=self.theme["bg"], fg="#FFFFFF")
		# self.loading_label.place(relx=0.52,rely=0.965, relheight=0.015)
	
		try:
			self.load_file(filename=sys.argv[1])
		except IndexError:
			pass


	def set_highlighter(self, arg):
		print(arg)
		self.highlighting = True
		if (arg == "py"):
			self.highlighter = python_highlighter(self.txt, self.theme)
		elif (arg == "c"):
			self.highlighter = C_highlighter(self.txt, self.theme)
		else:
			self.highlighting = False
			self.highlighter = None

	def set_tab_lock(self, arg):
		self.tab_lock = False

	def loading_widg(self):
		self.a += chr(9608)
		if len(self.a) < 11:
			print(len(self.a))
			sleep(0.1)
			self.loading_label.configure(text=self.a)
		
		else:
			print("aa")
			self.loading = False
			self.a = ""
			sleep(0.1)
			self.loading_label.configure(text=self.a)

	def get_line_count(self):
		""" returns total amount of lines in opened text """
		self.info = self.txt.get("1.0", "end-1c")
		return sum(1 for line in self.info.split("\n"))
		# return len(self.content)


	def error_win(self, e):
		""" set up error window """
		error_win = tkinter.Tk("aaa")
		error_win.configure(bg="#000000", bd=2)
		#error_win.geometry("600x200")
		error_win.title(f"Error Window")
		error_label = tkinter.Label(error_win, text=f"Error: {e}", justify=tkinter.CENTER, bg="#000000", fg="#ffffff"); error_label.pack()
		error_button = tkinter.Button(error_win, text="OK", command=error_win.destroy, bg="#000000", fg="#ffffff"); error_button.pack()
		#error_label.place(relx=0.0, rely=0.10, relwidth=1, relheight=0.20)
		#error_button.place(relx=0.25, rely=0.25, relwidth=0.35, relheight=0.26)

	def help_win(self, command=None):
		""" set up help window """
		help_win = tkinter.Tk("aaa")
		help_win.configure(bg="#000000")
		help_win.title(f"Help Window")
		if (command == None):
			help_label = tkinter.Label(help_win, text=f"Commands: \n l -options: get || [ LINE_NUMBER(.CHARACTER) ] (eg. 120 or 120.5)  \n highlighting -options: on || off \n", bg="#000000", fg="#ffffff", justify=tkinter.LEFT).pack()
		elif (command != None):
			help_label = tkinter.Label(help_win, text=f"{command}: {self.command_definition[command]}", bg="#000000", fg="#ffffff", justify=tkinter.LEFT).pack()
		#-puts you to line number (eg. 120(by default starts at column 0 but you can specify the column like: 120.5)

	#binded functions

	def detach_widget(self, arg):
		pass
		# self.widget_window = tkinter.Tk()
		# self.widget_window.geometry("100x50")
		# self.widget_window.configure(bg=self.theme["bg"])
		# self.line_no = tkinter.Label(self.widget_window)
		# self.line_no.configure(bg=self.theme["bg"], fg=self.theme["fg"])
		# self.line_no.place(width=100, height=50)

	def set_fullscreen(self, arg):
		self.fullscreen = not self.fullscreen
		root.attributes("-fullscreen", self.fullscreen)

	def set_dimensions(self, arg):
		key = arg.keysym
		margin = 20
		if (key == "Right"):
			root.geometry(f"{root.winfo_width()+margin}x{root.winfo_height()}")
		if (key == "Left"):
			root.geometry(f"{root.winfo_width()-margin}x{root.winfo_height()}")
		if (key == "Up"):
			root.geometry(f"{root.winfo_width()}x{root.winfo_height()-margin}")
		if (key == "Down"):
			root.geometry(f"{root.winfo_width()}x{root.winfo_height()+margin}")

	def popup(self, arg):
		""" gets x, y position of mouse click """
		self.right_click_menu.tk_popup(arg.x_root+5, arg.y_root)
		# self.right_click_menu.grab_release()
		
	def file_menu_popup(self, widget):
		if (widget == "file_menu"): 
			self.file_dropdown.tk_popup(root.winfo_rootx(), root.winfo_rooty()+25)
		
		elif (widget == "settings_menu"):
			self.file_dropdown.tk_popup(root.winfo_rootx()+63, root.winfo_rooty()+25)

	def command_entry_set(self, arg):
		self.command_entry.place(x=0,rely=0.99975, relwidth=0.9975, height=20, anchor="sw")
		self.command_entry.focus_set()

	def command_entry_unset(self, arg):
		self.command_entry.place_forget()
		self.txt.focus_set()

	def command_history(self, arg):
		""" scroll through used commands with Up and Down arrows(?) """
		self.command_entry.delete(0, "end")
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
			self.command_entry.insert(0, last_command)

			#print(self.command_input_history_index)

		except IndexError:
			#print(self.command_input_history_index)
			self.command_input_history_index = 0
			self.command_entry.delete(0, "end")

	def command_O(self, arg):
		""" sets the text in command output"""
		#(I have no idea why past me made this into a function when it doesn't really have to be a function)
		self.command_out.place(relx=0.1,rely=0.99975, relwidth=1, height=20, anchor="sw")
		self.command_out.configure(text=str(arg))
		self.command_out.focus_set()


	def cmmand(self, arg):
		""" parses command(case insensitive) from command line and executes it"""
		self.command_input_history_index = 0
		command = self.command_entry.get().lower().split()#turns command into a list and turns it all into lowercase chars

		#help command
		if (command[0] == "help"):
			try:
				if (command[1] != None):
					self.help_win(command[1])
			except IndexError:
				self.help_win()

		#highlighting command
		elif (command[0] == "highlighting"):
			#print("aaa")
			if (command[1] == "on"):
				self.command_O("highlighting on")
				self.highlight_all()
				self.highlighting = True
			elif (command[1] == "off"):
				self.unhighlight_all()
				self.command_O("highlighting off")
				self.highlighting = False

		#line/ line and column commands

		elif (re.match(r"[0-9]", command[0][0])):
			self.txt.mark_set("insert", float(command[0]))
			self.txt.see(float(command[0]))
			self.command_O(f"moved to: {float(command[0])}")

		elif (command[0][0] == "l"):
			print(command[0][0])
			for i, pnum in enumerate(command[0][1:], 1):
				print(pnum)
				if (re.search("[0-9]", pnum)): 
					argument = command[0][i:]
					break
				
				elif (re.search("[a-zA-Z]", pnum)):
					argument = command[0][i:]
					break

			if (re.match("[0-9]", argument)):
				self.txt.mark_set("insert", float(argument))
				self.txt.see("insert")
				self.command_O(f"moved to: {float(argument)}")

			elif (re.match("get", argument)):
				self.command_O(f"total lines: {self.get_line_count()}")


		elif (command[0] == "quit"):
			self.run = False

		elif (command[0] == "save"):
			self.save_file()
			self.loading = True

		elif (command[0] == "open"):
			self.load_file(filename=command[1])
			#self.command_O(f"file saved")
		
		elif (command[0] == "theme"):
			try:
				self.theme = self.theme_options[command[1]]
				self.init()
			except IndexError:
				p = "themes:"
				for x in list(self.theme_options.keys()):
					p += " "+x
				self.command_O(p)


		#append command to command history
		self.command_input_history.append(command)

		#sets focus back to text widget
		self.txt.focus_set()
		self.command_entry.delete(0, "end") #deletes command line input

		#set command history to newest index
		self.command_input_history_index = 0       
		self.command_entry.place_forget()


	def scroll(self, arg, multiplier=1):

		next_index = float(self.txt.index("insert"))
		if (arg.num == 5 or arg.delta < 0):
			self.txt.mark_set("insert", next_index+3*multiplier)

		elif (arg.num == 4 or arg.delta > 0):
			self.txt.mark_set("insert", next_index-3*multiplier)
	
		

	#menubar functions
	def new_file(self, name="untitled.txt"):
		try:
			self.current_file_name = f"{os.getcwd()}/{name}"
			self.current_file = open(self.current_file_name, "w+")
			root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
			
			self.set_highlighter(os.path.basename(self.current_file.name).split(".")[1])

		except Exception as e:
			self.current_file.close()
			self.error_win(e)

	def save_file(self, arg = None):
		""" saves current text into opened file """
		content = str(self.txt.get("1.0", "end-1c"))
		
		# try:
		#     self.current_file = open(f"{os.getcwd()}/untitled.txt", "w+")
		#     root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
		# except:
		#     pass
		
		try:
			self.current_file = open(self.current_file_name, "w")
			self.current_file.write(content)
			
			self.set_highlighter(os.path.basename(self.current_file.name).split(".")[1])

			self.current_file.close()
			self.command_O(f"total of {self.get_line_count()} lines saved")
		except TypeError:
			self.new_file()
			self.save_file()
			# self.error_win(f"{e}\n aka you probably didn't open any file yet")

	def save_file_as(self):
		""" saves current text into a new file """
		if (self.current_file_name != None):
			tmp = self.filename.asksaveasfilename(initialdir=f'{os.getcwd()}', title="Select file", defaultextension=".txt" ,filetypes=(["TXT files", "*.txt *.py *.c"],("all files","*.*")))
			os.rename(self.current_file_name, tmp)
			self.current_file_name = tmp
		else:
			self.current_file_name = self.filename.asksaveasfilename(initialdir=f'{os.getcwd()}', title="Select file", defaultextension=".txt" ,filetypes=(["TXT files", "*.txt *.py *.c"],("all files","*.*")))

		root.title(f"N Editor: <{os.path.basename(self.current_file_name)}>")
		self.save_file()

	def load_file(self, filename=None):
		""" opens a file and loads it's content into the text widget """
		if (filename):
			self.current_file_name = filename
		
		elif (filename == None):
			self.current_file_name = self.filename.askopenfilename(initialdir=f"{os.getcwd()}/", title="Select file", filetypes=(["TXT files", "*.txt *.py *.c"],("all files","*.*")))
		
		try:
			self.current_file = open(self.current_file_name, "r+")

			self.set_highlighter(os.path.basename(self.current_file.name).split(".")[1])

			# self.content = self.current_file.readlines()
			root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
			self.txt.delete("1.0", "end-1c")

			self.content = self.current_file.read()
			# print(len(self.content)/2)

			self.txt.insert("1.0", self.content)
			# for i in range(10):
			# 	print(offset, offset1)
			# 	self.txt.insert("end", self.content[offset:offset1])
			# 	offset += int(len(self.content)/10)
			# 	offset1 += int(len(self.content)/10)
			# for line in self.content[0]:
			# 	self.txt.insert("end", line)
			t0 = time()
			self.txt.mark_set("insert", "1.0")
			self.txt.see("insert")
			self.current_file.close()
			self.command_O(f"total lines: {self.get_line_count()}")
			# del content
			self.highlight_all()
			t1 = time()
			print(t1-t0)
		except Exception as e:
			self.new_file(name=self.current_file_name)
			self.save_file()

	def update_buffer(self):
		for line in self.content[self.get_line_count():self.get_line_count()+1]:
			self.txt.insert("end", line)

	def update_win(self):
		""" updates window """
		try:
			root.update()
			root.update_idletasks()
		except Exception: #when exiting window it throws an error because root wasn't properly destroyed
			root.quit()
			quit()

	def update_text(self, x=''):
		""" updates the text and sets current position of the insert cursor"""
		#basically the main function
		#counter = 0
		while self.run:
			self.update_win()
			self.txt.see("insert")

			# print(root.winfo_pointerx())
			# if random.randint(1, 10) == 4:
			self.cursor_index = self.txt.index(tkinter.INSERT).split(".") # gets the cursor's position
			# if (self.last_index != self.cursor_index[0] and self.get_line_count() < len(self.content)-1):
			# 	print(self.get_line_count(), len(self.content))
			# 	self.last_index = int(self.cursor_index[0])
			# 	self.update_buffer()
			self.txt.place(x=0,y=25,relwidth=1, height=root.winfo_height()-25, anchor="nw")
			# print(self.txt.index(tkinter.INSERT))
			#self.txt.after(0, self.update_line_numbers)
			# self.line_no.configure(text=f"l:{self.cursor_index[0]} c:{self.cursor_index[1]}") # sets the cursor position into line number label
			self.line_no.configure(text=f"[{self.txt.index(tkinter.INSERT)}]")
			# if (self.loading):
			#     threading.Thread(target=self.loading_widg, args=()).start()

			if (root.focus_displayof() != self.command_entry):
				self.command_entry.place_forget()

			if (root.focus_displayof() != self.command_out):
				self.command_out.place_forget() 

			if (self.command_highlighting):
				self.command_highlight()

			if (self.highlighting): # if the highlighting option is on then turn on highlighting :D
				self.highlighter.highlight(self.cursor_index[0], line=self.txt.get(self.cursor_index[0]+".0", "end"))
				# self.highlight_chunk()
				if (not self.tab_lock):
					if (self.txt.get(f"{self.cursor_index[0]}.{int(self.cursor_index[1])-1}") == "\n"):
						self.txt.insert(self.txt.index("insert"), self.keep_indent())
						self.tab_lock = True

	def unindent(self, arg=None):
		if (re.match(r"\t", self.txt.get(f"{self.cursor_index[0]}.0"))):
			self.txt.delete(f"{self.cursor_index[0]}.0", f"{self.cursor_index[0]}.1")
			
	def keep_indent(self):
		# tab_offset = 0
		offset_string = ""
		for current_char in self.txt.get(f"{int(self.cursor_index[0])-1}.0", "end"):
			if (re.match(r"[\t]",  current_char)):
				offset_string += "\t"
			elif (re.match(r"[\/\#]", current_char)):
				pass
			else:
				break
				
			# else:
			# 	if (re.match(r"[\:]", line[-3])):
			# 		offset_string += "\t"
			# 	break
		
		return offset_string


	def command_highlight(self):
		pass

	# def highlight_chunk(self):
	# 	if self.highlighting:
	# 		for i in range(int(self.cursor_index[0])-30, int(self.cursor_index[0])+30):
	# 			self.highlighter.highlight(str(i))

	def highlight_all(self):
		if self.highlighting:
			for i in range(1, self.get_line_count()):
				self.highlighter.highlight(str(i))

	def unhighlight_all(self):
		for i in range(1, self.get_line_count()+1):
			self.highlighter.unhighlight(str(i))

	def note_mode(self):
		self.highlighting = False

	def retro_mode(self):
		pass



root = tkinter.Tk()
main_win = win(root)


if __name__ == '__main__':
	main_win.update_text()
	