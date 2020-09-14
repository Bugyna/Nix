import os
import tkinter
from time import time

class file_handler(object):
	""" File opening and closing yes"""
	def __init__(self, parent, root):
		self. supported_filetypes = ["TXT files", "*.txt *.py *.c *.cpp *.cc  *.html *.htm"]
		self.current_file = None
		self.current_file_name = None
		self.content = ""
		self.root = root
		self.parent = parent
		
	def new_file(self, name=""):
		i = 0
		name = f"{os.getcwd()}/untitled_{i}.txt"
		while (os.path.isfile(name)):
			i += 1
			name = f"{os.getcwd()}/untitled_{i}.txt"

		self.current_file_name = name
		self.current_file = open(self.current_file_name, "w+")
		self.parent.txt.delete("1.0", "end")
		self.root.title(f"Nix: <{os.path.basename(self.current_file.name)}>")
		
		self.parent.set_highlighter()

	def save_file(self, arg = None):
		""" saves current text into opened file """
		self.content = str(self.parent.txt.get("1.0", "end-1c"))
		
		
		if (self.current_file_name):
			self.current_file = open(self.current_file_name, "w")
			self.current_file.write(self.content)
			
			self.parent.set_highlighter()

			self.current_file.close()
			self.root.title(f"Nix: <{os.path.basename(self.current_file_name)}>")
			self.parent.command_O(f"total of {self.parent.get_line_count()} lines saved")
			
		elif (not self.current_file_name):
			self.new_file()
			self.save_file()


	def save_file_as(self, arg=None):
		""" saves current text into a new file """
		if (self.current_file_name != None):
			try:
				tmp = self.parent.filename.asksaveasfilename(initialdir=f'{os.getcwd()}', title="Save file as", defaultextension=".txt" ,filetypes=(self.supported_filetypes, ("all files","*.*")))
			except TypeError: #throws an error when closing the menu without choosing anything
				pass
			os.rename(self.current_file_name, tmp)
			self.current_file_name = tmp
		else:
			self.current_file_name = self.parent.filename.asksaveasfilename(initialdir=f'{os.getcwd()}', title="Save file as", defaultextension=".txt" ,filetypes=(self.supported_filetypes, ("all files","*.*")))


		self.root.title(f"Nix: <{os.path.basename(self.current_file_name)}>")
		self.save_file()
		self.parent.unhighlight_chunk()
		self.parent.highlight_chunk()

	def load_file(self, filename=None):
		""" opens a file and loads it's content into the text widget """

		if (filename): #if the filename arguments is given: set the current filename to be the argument (pretty self explanatory)
			self.current_file_name = filename
		
		elif (filename == None): #if the filename argument is not provided open a file menu to provide a filename
			try:
				self.current_file_name = self.parent.filename.askopenfilename(initialdir=f"{os.getcwd()}/", title="Select file", filetypes=(self.supported_filetypes, ("all files","*.*")))
			except TypeError: #throws an error when closing the menu without choosing anything
				pass
			
		try:
			self.current_file = open(self.current_file_name, "r+") #opens the file
			self.parent.set_highlighter() #takes the file extension and passes it to the set_highlighter function to highlight the file accordingly
		except Exception as e:
			self.parent.command_O(e)
			return


		self.root.title(f"Nix: <{os.path.basename(self.current_file.name)}>") #sets the title of the window to the current filename
		self.parent.txt.delete("1.0", "end-1c") #deletes the buffer so there's not any extra text

		self.parent.content = self.current_file.read() #self.content is the variable storing all of the files text
		self.current_file.close() #closes current file

		t0 = time() # timer| gets current time in miliseconds
		self.parent.txt.insert("1.0", self.content) #puts all of the file's text in the text widget
		self.parent.txt.mark_set(tkinter.INSERT, "1.0") #puts the cursor at the start of the file
		self.parent.txt.see(tkinter.INSERT) #puts the cursor at the start of the file

		
		self.parent.highlight_chunk() #highlights the text in the text widget
		t1 = time() # timer| gets current time in miliseconds
		elapsed_time = round(t1-t0, 3) #elapsed time
		self.parent.command_O(f"total lines: {self.parent.get_line_count()};	loaded in: {elapsed_time} seconds") #puts the time it took to load and highlight the text in the command output widget
							
							
class launcher:
	def __init__(self):
		pass