import os
import time
import tkinter
import threading
import subprocess
from pygame import mixer

from widgets import BUFFER_TAB, TEXT

class file_handler(object):
	""" File opening and closing yes"""
	def __init__(self, parent):
		self.supported_filetypes = ["TXT files", "*.txt *.py *.c *.cpp *.cc *.html *.htm *.css"]
		self.current_dir = os.getcwd()
		self.current_file = None
		self.current_file_name = None
		self.current_buffer = ""
		self.buffers = {}
		self.buffer_tab_index = None
		self.parent = parent

	def init(self):
		self.current_buffer = "<~NONE>"
		self.buffers[self.current_buffer] = TEXT(self.parent)

	def rename_buffer(self, buffer_name: str, new_buffer_name: str):
		for buffer in self.parent.buffer_tabs:
			if (buffer_name == buffer.name): buffer.change_name(new_buffer_name); break

		self.buffers[new_buffer_name] = self.buffers.pop(buffer_name)
		self.current_buffer = new_buffer_name


	def new_buffer(self, buffer_name: str):
		try: self.buffers[buffer_name]; return # Checks for existing buffers
		except KeyError: pass
		self.parent.txt.place_forget()
		self.current_file_name = self.current_buffer = buffer_name
		self.buffers[buffer_name] = [TEXT(self.parent), BUFFER_TAB(buffer_name, self.parent)]
		self.buffer_tab_index = self.buffers[self.current_buffer][1].index
		self.parent.txt = self.buffers[buffer_name][0]
		self.parent.theme_load()
		self.parent.title(f"Nix: <{os.path.basename(self.current_buffer)}>")

	def del_buffer(self, buffer_name: str=None):
		self.buffers[buffer_name][1].place_forget()
		self.buffers.pop(buffer_name)

		last_buffer_tab = None
		for buffer in list(self.buffers.values())[1:]:
			buffer[1].reposition(last_buffer_tab)
			last_buffer_tab = buffer[1]

	def load_buffer(self, buffer_name: str):
		self.parent.txt.place_forget()
		self.current_file_name = self.current_buffer = buffer_name; self.parent.highlighter.txt = self.parent.txt = self.buffers[buffer_name][0]
		self.buffer_tab_index = self.buffers[self.current_buffer][1].index
		self.current_dir = os.path.dirname(self.current_file_name)
		self.parent.txt.place(x=0,y=40,relwidth=1, height=self.parent.winfo_height()-25, anchor="nw")
		self.parent.title(f"Nix: <{os.path.basename(self.current_buffer)}>")

	def del_file(self, filename:str=""):
		if (not filename): filename=self.current_file_name
		if (os.path.isfile(filename)): os.remove(filename); self.parent.command_O(f"File ({filename}) was deleted")
		else: self.parent.command_O(f"File ({filename}) does not exist")

	def new_file(self, name: str=""):
		if (not name):
			i = 0
			name = f"{self.current_dir}/untitled_{i}.txt"
			while (os.path.isfile(name)):
				i += 1
				name = f"{self.current_dir}/untitled_{i}.txt"

		self.current_file_name = name
		self.current_file = open(self.current_file_name, "w+")
		print(self.current_file.name)
		self.new_buffer(self.current_file.name)
		self.parent.txt.delete("1.0", "end")
		# self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{os.path.basename(self.current_file.name)}>")
		
		self.parent.set_highlighter()

	def save_file(self, arg = None):
		""" saves current text into opened file """
		self.buffer = str(self.parent.txt.get("1.0", "end-1c"))
		
		if (self.current_file_name):
			self.current_file = open(self.current_file_name, "w")
			self.current_file.write(self.parent.txt.get("1.0", "end"))
			
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
		self.rename_buffer(self.current_buffer, tmp)

		self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{os.path.basename(self.current_file_name)}>")
		self.save_file()
		self.parent.unhighlight_chunk()
		self.parent.highlight_chunk()

	def load_file(self, filename=None):
		""" opens a file and loads it's content into the text widget """

		if (filename): #if the filename arguments is given: set the current filename to be the argument (pretty self explanatory)
			if (os.path.dirname(filename)): self.current_file_name = f"{filename}"
			else: self.current_file_name = f"{self.current_dir}/{filename}"
		
		elif (filename == None): #if the filename argument is not provided open a file menu to provide a filename
			try:
				self.current_file_name = self.parent.filename.askopenfilename(initialdir=f"{self.current_dir}/", title="Select file", filetypes=(self.supported_filetypes, ("all files","*.*")))
			except TypeError: #throws an error when closing the menu without choosing anything
				pass
			
		try:
			self.current_file = open(self.current_file_name, "r+") #opens the file
			self.parent.set_highlighter() #takes the file extension and passes it to the set_highlighter function to highlight the file accordingly
		except Exception as e:
			self.new_file(filename)
			self.parent.command_O("new file")
			return

		self.new_buffer(self.current_file.name)
		self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{os.path.basename(self.current_file.name)}>") #sets the title of the window to the current filename
		self.parent.txt.delete("1.0", "end-1c") #deletes the buffer so there's not any extra text

		t0 = time.time() # timer| gets current time in miliseconds
		self.parent.txt.insert("1.0", self.current_file.read()) #puts all of the file's text in the text widget
		self.parent.text_len = len(self.parent.txt.get("1.0", "end"))
		self.parent.txt.mark_set(tkinter.INSERT, "1.0") #puts the cursor at the start of the file
		self.parent.txt.see(tkinter.INSERT) #puts the cursor at the start of the file
		self.current_file.close() #closes current file
		
		self.parent.highlight_chunk() #highlights the text in the text widget
		t1 = time.time() # timer| gets current time in miliseconds
		elapsed_time = round(t1-t0, 3) #elapsed time
		print(t1-t0)
		self.parent.command_O(f"total lines: {self.parent.get_line_count()};	loaded in: {elapsed_time} seconds") #puts the time it took to load and highlight the text in the command output widget

class music_player:
	def __init__(self, parent):
		self.parent = parent
		self.volume = 1
		self.paused = False
		mixer.init()
		mixer.music.set_volume(self.volume)
		
	def load_song(self, name: str):
		try:
			mixer.music.load(*name)
			mixer.music.play()
		except Exception as e:
			print(e)
			self.parent.command_O("invalid file")
		
	def play_song(self, time: int = 0):
		mixer.music.play(start=time)
		
	def pause_song(self, unpause=False):
		if (not self.paused):
			self.paused = True
			mixer.music.pause()
		elif (self.paused or unpause):
			self.paused = False
			mixer.music.unpause()
		
	def stop_song(self):
		mixer.music.stop()
		
	def queue(self):
		pass


def video_record_start(parent):
	""" if you wanna record some video of your code (probably on works on linux (and you have to have ffmpeg installed"""
	pos = f":1.0+{parent.winfo_rootx()},{parent.winfo_rooty()}"
	videosize = f"{parent.winfo_width()}x{parent.winfo_height()}"
	path = parent.file_handler.current_dir
	filename = str(int(time.time())) + ".mkv"

	args = [
		["-f", "x11grab"],
		["-framerate", "120"],
		["-video_size", videosize],
		["-i", pos],
		["-vcodec", "libx264"],
		["-qscale", "0"]
	]

	print(args)
	command = f"cd {path}; ffmpeg "
	for arg in args:
		command += f"{arg[0]} {arg[1]} "

	command += filename

	return subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)

def video_record_stop(process):
	process.communicate(b"q")
	print("terminated")

						
class launcher:
	def __init__(self):
		pass
