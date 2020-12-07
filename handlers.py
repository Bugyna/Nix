import os
import time
import tkinter
import threading
import subprocess
try: from pygame import mixer
except ImportError: pass

from widgets import BUFFER_TAB, TEXT

class file_handler(object):
	""" File opening and closing yes"""
	def __init__(self, parent):
		self.supported_filetypes = ["TXT files", "*.txt *.py *.c *.cc *.cpp *.h *.hh *.hpp *.html *.htm *.css *.java *.class *.go *.sh *.diary"]
		self.current_dir = os.getcwd()
		self.current_file = None
		self.current_file_name = None
		self.current_buffer = None

		self.buffer_dict = {}
		self.buffer_list = []

		self.buffer_tab = None
		self.buffer_tab_index = None # buffer tabs have the same index as text widgets
		self.buffer_tab_list = []

		self.parent = parent

	def init(self):
		self.current_buffer = "<~NONE>"
		self.buffer_list.append(TEXT(self.parent, "<~NONE>"))
		print(self.buffer_list[-1].buffer_index)
		self.buffer_dict[self.current_buffer] = self.buffer_list[-1]


	def rename_buffer(self, buffer_name: str, new_buffer_name: str):
		for buffer in self.buffer_tab_list:
			if (buffer_name == buffer.full_name): buffer.change_name(new_buffer_name); break

		self.buffer_dict[new_buffer_name] = self.buffer_dict.pop(buffer_name)
		self.current_buffer = new_buffer_name


	def new_buffer(self, buffer_name: str):
		try: self.buffer_dict[buffer_name]; return # Checks for existing buffers
		except KeyError: pass

		self.parent.hide_text_widget()

		self.buffer_list.append([TEXT(self.parent, buffer_name), BUFFER_TAB(buffer_name, self.parent)])
		self.buffer_dict[buffer_name] = self.buffer_list[-1]
		self.parent.txt = self.buffer_list[-1][0]
		self.buffer_tab = self.buffer_list[-1][1]
		self.buffer_tab_list.append(self.buffer_list[-1][1])
		self.buffer_tab_index = self.parent.txt.buffer_index # text widget's buffer_index is the same as their buffer tab's buffer_index


		self.parent.theme_load()
		self.current_file_name = self.current_buffer = buffer_name
		self.current_dir = os.path.dirname(self.current_file_name)

		self.parent.set_font_size()
		self.parent.title(f"Nix: <{self.parent.txt.name}>")

	def del_buffer(self, buffer_name: str=None):
		buffer_index = self.buffer_dict[buffer_name][1].buffer_index
		self.buffer_dict[buffer_name][0].place_forget()
		self.buffer_dict[buffer_name][1].place_forget()
		
		self.buffer_list.pop(buffer_index)
		self.buffer_dict.pop(buffer_name)

		last_buffer_tab = None
		for buffer in self.buffer_list[1:]:
			buffer[1].reposition(last_buffer_tab)
			last_buffer_tab = buffer[1]


	def load_buffer(self, buffer_name: str = None, buffer_index: int = None):
		if (self.parent.split_mode == 0): self.parent.hide_text_widget()
		
		if (not buffer_name and not buffer_index): print("error"); return -1
		if (buffer_index and not buffer_name): buffer_name = self.buffer_list[buffer_index][1].name

		self.current_file_name = self.current_buffer = buffer_name
		self.parent.txt = self.buffer_dict[buffer_name][0]
		self.buffer_tab = self.buffer_dict[buffer_name][1]
		self.buffer_tab_index = self.parent.txt.buffer_index # text widget's buffer_index is the same as their buffer tab's buffer_index

		self.current_dir = os.path.dirname(self.current_file_name)
		
		self.parent.reposition_widgets()
		self.parent.title(f"Nix: <{self.parent.txt.name}>")
		self.parent.set_font_size()
		self.parent.theme_load()

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
		self.new_buffer(self.current_file.name)

		self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{self.parent.txt.name}>")
		
		self.parent.txt.set_highlighter()

	def save_file(self, arg = None):
		""" saves current text into opened file """
		self.buffer = str(self.parent.txt.get("1.0", "end-1c"))
		
		if (self.current_file_name):
			size0 = os.path.getsize(self.current_file_name)

			self.current_file = open(self.current_file_name, "w")
			self.current_file.write(self.parent.txt.get("1.0", "end"))
			self.current_file.close()

			self.parent.txt.set_highlighter()
			size1 = os.path.getsize(self.current_file_name)
			
			self.current_dir = os.path.dirname(self.current_file.name)
			self.parent.title(f"Nix: <{os.path.basename(self.current_file_name)}>")
			self.buffer_tab.change_name(extra_char="")
			# self.parent.command_O(f"total of {self.parent.get_line_count()} lines saved")
			self.parent.command_O(rf"saved {size1-size0}\{size1}\{self.parent.get_line_count()} new bytes to {os.path.basename(self.current_file_name)}")
			
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

		self.current_file_name = tmp
		self.rename_buffer(self.current_buffer, tmp)
		os.rename(self.current_file.name, tmp)

		self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{os.path.basename(self.current_file_name)}>")
		self.save_file()
		self.parent.unhighlight_chunk()
		self.parent.highlight_chunk()

	def load_file(self, filename=None):
		""" opens a file and loads it's content into the text widget """

		if (filename): #if the filename arguments is given: set the current filename to be the argument (pretty self explanatory)
			if (os.path.dirname(filename)): self.current_file_name = f"{filename}"
			else: self.current_file_name = self.current_buffer = f"{self.current_dir}/{filename}"
		
		elif (filename == None): #if the filename argument is not provided open a file menu to provide a filename
			try:
				self.current_file_name = self.current_buffer = self.parent.filename.askopenfilename(initialdir=f"{self.current_dir}/", title="Select file", filetypes=(self.supported_filetypes, ("all files","*.*")))
			except TypeError: #throws an error when closing the menu without choosing anything
				pass
			
		try:
			self.current_file = open(self.current_file_name, "r+") #opens the file
		except FileNotFoundError:
			self.new_file(self.current_file_name)
			return


		t0 = time.time() # timer| gets current time in miliseconds
		self.new_buffer(self.current_file.name)

		self.current_dir = os.path.dirname(self.current_file.name)
		file_content = self.current_file.read()

		file = open("."+os.path.basename(self.current_file_name)+".error_swp", "w+")
		file.write(file_content)
		file.close()

		self.parent.txt.delete("1.0", "end-1c") #deletes the buffer so there's not any extra text
		self.parent.txt.insert("1.0", file_content) #puts all of the file's text in the text widget
		self.parent.txt.text_len = len(self.parent.txt.get("1.0", "end"))
		self.parent.txt.mark_set(tkinter.INSERT, "1.0") #puts the cursor at the start of the file
		self.parent.txt.see(tkinter.INSERT) #puts the cursor at the start of the file
	
		self.current_file.close() #closes current file
	
		self.parent.highlight_chunk() #highlights the text in the text widget
		t1 = time.time() # timer| gets current time in miliseconds
		elapsed_time = round(t1-t0, 3) #elapsed time
		print(t1-t0)
		self.parent.command_O(f"total lines: {self.parent.get_line_count()};	loaded in: {elapsed_time} seconds") #puts the time it took to load and highlight the text in the command output widget
		self.parent.title(f"Nix: <{self.parent.txt.name}>") #sets the title of the window to the current filename

		del file_content

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

