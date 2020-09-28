import os
import tkinter
from time import time

from widgets import BUFFER_TAB, TEXT

class file_handler(object):
	""" File opening and closing yes"""
	def __init__(self, parent):
		self. supported_filetypes = ["TXT files", "*.txt *.py *.c *.cpp *.cc  *.html *.htm"]
		self.current_dir = os.getcwd()
		self.current_file = None
		self.current_file_name = None
		self.current_buffer = ""
		self.buffers = {}
		self.parent = parent

	def init(self):
		self.current_buffer = "<~NONE>"
		self.buffers[self.current_buffer] = TEXT(self.parent)

	def new_buffer(self, buffer_name: str):
		try: self.buffers[buffer_name]; return # Checks for existing buffers
		except KeyError: pass
		self.parent.txt.place_forget()
		self.current_buffer = buffer_name
		self.buffers[buffer_name] = TEXT(self.parent)
		self.parent.txt = self.buffers[buffer_name]
		self.parent.buffer_tabs.append(BUFFER_TAB(buffer_name, self.parent))
		self.parent.theme_load()

	def del_buffer(self, buffer_name: str=None):
		last_buffer = None
		for buffer in self.parent.buffer_tabs:
			if (buffer.name == buffer_name): self.parent.buffer_tabs[buffer.index].place_forget(); self.parent.buffer_tabs.pop(buffer.index); break
			last_buffer = buffer
			
		self.buffers.pop(buffer_name)
		self.current_buffer = last_buffer.name
		self.load_buffer(last_buffer.name)

	def load_buffer(self, buffer_name: str):
		self.parent.txt.place_forget()
		self.current_buffer = buffer_name; self.parent.txt = self.buffers[buffer_name]
		self.parent.txt.place(x=0,y=40,relwidth=1, height=self.parent.winfo_height()-25, anchor="nw")

	def new_file(self, name: str=""):
		i = 0
		name = f"{self.current_dir}/untitled_{i}.txt"
		while (os.path.isfile(name)):
			i += 1
			name = f"{self.current_dir}/untitled_{i}.txt"

		self.current_file_name = name
		self.current_file = open(self.current_file_name, "w+")
		print(self.current_file.name)
		self.new_buffer(os.path.basename(self.current_file.name))
		self.parent.txt.delete("1.0", "end")
		self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{os.path.basename(self.current_file.name)}>")
		
		self.parent.set_highlighter()

	def save_file(self, arg = None):
		""" saves current text into opened file """
		self.buffer = str(self.parent.txt.get("1.0", "end-1c"))
		
		
		if (self.current_file_name):
			self.current_file = open(self.current_file_name, "w")
			self.current_file.write(self.buffer)
			
			self.parent.set_highlighter()

			self.current_file.close()
			self.current_dir = os.path.dirname(self.current_file.name)
			self.parent.title(f"Nix: <{os.path.basename(self.current_file_name)}>")
			self.parent.command_O(f"total of {self.parent.get_line_count()} lines saved")
			
		elif (not self.current_file_name):
			self.new_file()
			self.save_file()


	def save_file_as(self, arg=None, tmp=None):
		""" saves current text into a new file """
		if (self.current_file_name):
			if (not tmp):
				try:
					tmp = self.parent.filename.asksaveasfilename(initialdir=f'{self.current_dir}', title="Save file as", defaultextension=".txt" ,filetypes=(self.supported_filetypes, ("all files","*.*")))
				except TypeError: #throws an error when closing the menu without choosing anything
					pass
		else:
			self.current_file_name = self.parent.filename.asksaveasfilename(initialdir=f'{self.current_dir}', title="Save file as", defaultextension=".txt" ,filetypes=(self.supported_filetypes, ("all files","*.*")))

		os.rename(self.current_file.name, tmp)
		self.current_file_name = tmp

		self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{os.path.basename(self.current_file_name)}>")
		self.save_file()
		self.parent.unhighlight_chunk()
		self.parent.highlight_chunk()

	def load_file(self, filename=None):
		""" opens a file and loads it's content into the text widget """

		if (filename): #if the filename arguments is given: set the current filename to be the argument (pretty self explanatory)
			self.current_file_name = f"{self.current_dir}/{filename}"
		
		elif (filename == None): #if the filename argument is not provided open a file menu to provide a filename
			try:
				self.current_file_name = self.parent.filename.askopenfilename(initialdir=f"{self.current_dir}/", title="Select file", filetypes=(self.supported_filetypes, ("all files","*.*")))
			except TypeError: #throws an error when closing the menu without choosing anything
				pass
			
		try:
			self.current_file = open(self.current_file_name, "r+") #opens the file
			self.parent.set_highlighter() #takes the file extension and passes it to the set_highlighter function to highlight the file accordingly
		except Exception as e:
			self.parent.command_O(e)
			return

		self.new_buffer(os.path.basename(self.current_file.name))
		self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{os.path.basename(self.current_file.name)}>") #sets the title of the window to the current filename
		self.parent.txt.delete("1.0", "end-1c") #deletes the buffer so there's not any extra text

		t0 = time() # timer| gets current time in miliseconds
		self.parent.txt.insert("1.0", self.current_file.read()) #puts all of the file's text in the text widget
		self.parent.txt.mark_set(tkinter.INSERT, "1.0") #puts the cursor at the start of the file
		self.parent.txt.see(tkinter.INSERT) #puts the cursor at the start of the file
		self.current_file.close() #closes current file
		
		self.parent.highlight_chunk() #highlights the text in the text widget
		t1 = time() # timer| gets current time in miliseconds
		elapsed_time = round(t1-t0, 3) #elapsed time
		print(t1-t0)
		self.parent.command_O(f"total lines: {self.parent.get_line_count()};	loaded in: {elapsed_time} seconds") #puts the time it took to load and highlight the text in the command output widget
							
							
class launcher:
	def __init__(self):
		pass