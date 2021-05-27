import os
import time
import random
import tkinter
import threading
import subprocess

from ascii_art import *
from widgets import *

# thanks to everyone on https://www.asciiart.eu/

class FILE_HANDLER(object):
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

	def closing_sequence(self) -> None:
		for b in self.buffer_list[1:]:
			self.close_buffer(buffer_name=b[0].full_name)

	def init(self, buffer_name: str):
		self.buffer_list.append([TEXT(self.parent, buffer_name), BUFFER_TAB(buffer_name, self.parent)])
		self.buffer_dict[buffer_name] = self.buffer_list[-1]
		self.parent.txt = self.buffer_list[-1][0]
		self.buffer_tab = self.buffer_list[-1][1]
		self.buffer_tab_list.append(self.buffer_list[-1][1])
		self.parent.title(f"Nix: <{self.parent.txt.name}>")
		self.parent.txt.insert("1.0", "\nhttps://www.asciiart.eu/")
		self.parent.txt.insert("1.0", art[random.randint(0, len(art)-1)])
		self.parent.txt.mark_set("insert", len(self.parent.txt.get("1.0", "end").split("\n"))/2)
		
		self.parent.txt.tag_add("center", "1.0", "end")

	def load_scratch(self, arg=None):
		self.parent.txt.place_forget()
		self.parent.txt = self.buffer_list[0][0]
		self.parent.txt.focus_set()
		self.parent.reposition_widgets()
		
		self.parent.title(f"Nix: <{self.parent.txt.name}>")
		self.parent.txt.font_size_set()
		self.parent.theme_load()

		if (arg): return "break"


	def rename_buffer(self, buffer_name: str, new_buffer_name: str):
		for buffer in self.buffer_list:
			if (buffer_name == buffer[0].full_name):
				buffer[0].change_name(new_buffer_name)
				buffer[1].change_name(new_buffer_name)
				break

		self.buffer_dict[new_buffer_name] = self.buffer_dict.pop(buffer_name)
		self.current_file_name = self.current_buffer = new_buffer_name


	def new_buffer(self, buffer_name: str, buffer_type="TEXT"):
		try: self.buffer_dict[buffer_name]; return # Checks for existing buffers
		except KeyError: pass

		self.parent.hide_text_widget()

		if (buffer_type == "TEXT"): self.buffer_list.append([TEXT(self.parent, buffer_name), BUFFER_TAB(buffer_name, self.parent)])
		elif (buffer_type == "GRAPHICAL"): self.buffer_list.append([GRAPHICAL_BUFFER(self.parent, buffer_name), BUFFER_TAB(buffer_name, self.parent)])
		self.buffer_dict[buffer_name] = self.buffer_list[-1]
		self.buffer_tab_list.append(self.buffer_list[-1][1])

		self.load_buffer(buffer_name=buffer_name)

	def close_buffer(self, arg=None, buffer_name: str=None):
		if (not buffer_name): buffer_name = self.parent.txt.full_name
		buffer_index = self.buffer_dict[buffer_name][0].buffer_index
		self.buffer_dict[buffer_name][0].place_forget()
		self.buffer_dict[buffer_name][1].pack_forget()

		print("base: ", os.path.basename(buffer_name), "file: ", f".{os.path.basename(buffer_name)}.error_swp")
		if (self.parent.backup_files): self.del_file(filename=f".{os.path.basename(buffer_name)}.error_swp")
		# if (len(self.buffer_dict[buffer_name].get("1.0", "end-1c")) == 0): self.del_file(filename=buffer_name) # deletes created file if the text buffer is empty
		
		self.buffer_tab_list.pop(buffer_index)
		self.buffer_list.pop(buffer_index)
		self.buffer_dict.pop(buffer_name)

		# pointers have came to bite my ass cuz this shit ain't working and I am not even surprised
		# tbh this is a pretty serious bug I can't really fix it for whatever reason
		for i in range(1, len(self.buffer_list)):
			self.buffer_list[i][0].buffer_index = i
			self.buffer_list[i][1].buffer_index = i
			self.buffer_list[i][1].reposition()


		self.load_buffer(buffer_index=len(self.buffer_list)-1)

		if (arg): return "break"


	def load_buffer(self, arg=None, buffer_name: str = None, buffer_index: int = None):
		if (self.parent.split_mode == 0): self.parent.hide_text_widget()
		
		# this conditional is gross why can't it just be (buffer_index)
		# THIS IS PROBABLY THE MOST PYTHONIC LINE OUT OF ALL THE FILES
		if (buffer_index is not None): buffer_name = self.buffer_list[buffer_index][0].full_name
		
		self.current_file_name = self.current_buffer = buffer_name
		self.parent.txt = self.buffer_dict[buffer_name][0]
		self.buffer_tab = self.buffer_dict[buffer_name][1]
		self.buffer_tab_index = self.parent.txt.buffer_index # text widget's buffer_index is the same as their buffer tab's buffer_index

		if (buffer_index != 0): self.current_file_name = self.current_buffer = self.parent.txt.full_name; self.current_dir = os.path.dirname(self.current_buffer)
		
		self.parent.title(f"Nix: <{self.parent.txt.name}>")
		if (type(self.parent.txt) == "TEXT"): self.parent.txt.font_size_set()
		self.parent.theme_load()
		self.buffer_tab.focus_highlight()
		self.parent.txt.focus_set()
		self.parent.reposition_widgets()
		
		if (arg): return "break"

	def del_file(self, arg=None, filename:str=""):
		try:	self.buffer_dict[filename] ; self.close_buffer(buffer_name=filename)
		except KeyError: pass
			
		if (not filename): filename=self.current_file_name
		if (os.path.isfile(filename)): os.remove(filename); self.parent.command_out_set(f"File [{filename}] was deleted")
		else: self.parent.command_out_set(f"File ({filename}) does not exist")

		if (arg): return "break"

	def new_file(self, arg=None, filename: str=""):
		if (not filename):
			i = 0
			filename = f"{self.current_dir}/untitled_{i}.txt"
			while (os.path.isfile(filename)):
				i += 1
				filename = f"{self.current_dir}/untitled_{i}.txt"

		self.current_file_name = filename
		self.current_file = open(f"{self.current_dir}/{filename}", "w+")
		self.new_buffer(self.current_file.name)

		self.current_dir = os.path.dirname(self.current_file.name)
		self.parent.title(f"Nix: <{self.parent.txt.name}>")
		
		self.parent.txt.set_highlighter()

		if (arg): return "break"

	def save_file(self, arg = None):
		""" saves current text into opened file """
		if (self.current_file_name):
			size0 = os.path.getsize(self.current_file_name)

			self.current_file = open(self.current_file_name, "w")
			self.current_file.write(self.parent.txt.get("1.0", "end-1c"))
			self.current_file.close()

			self.parent.txt.set_highlighter()
			size1 = os.path.getsize(self.current_file_name)
			
			self.current_dir = os.path.dirname(self.current_file_name)
			self.parent.title(f"Nix: <{os.path.basename(self.current_file_name)}>")
			self.buffer_tab.change_name(extra_char=" ")
			# self.parent.command_out_set(f"total of {self.parent.get_line_count()} lines saved")
			self.parent.command_out_set(rf"saved [{size1-size0}B|{size1}B|{self.parent.get_line_count()}L] to {os.path.basename(self.current_file_name)}")
			
		elif (not self.current_file_name):
			self.new_file()
			self.save_file()

		if (arg): return "break"


	def save_file_as(self, arg=None, filename=None):
		""" saves current text into a new file """

		self.current_dir = os.path.dirname(self.parent.txt.full_name)
		filename = f"{self.current_dir}/{filename}"
		os.rename(self.parent.txt.full_name, filename)
		self.rename_buffer(self.parent.txt.full_name, filename)
		self.save_file()
		self.parent.highlight_chunk()

		if (arg): return "break"

	def load_file(self, arg=None, filename=None):
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
			self.new_file(filename=filename)
			return


		t0 = time.time() # timer| gets current time in miliseconds
		self.current_dir = os.path.dirname(self.current_file.name)
		try:
			file_content = self.current_file.read()
		# except UnicodeDecodeError:
		except Exception:
			self.new_buffer(self.current_file_name, buffer_type="GRAPHICAL"); return

		self.new_buffer(self.current_file.name)
		if (self.parent.backup_files):
			file = open("."+os.path.basename(self.current_file_name)+".error_swp", "w+")
			file.write(file_content)
			file.close()

		self.parent.txt.delete("1.0", "end") #deletes the buffer so there's not any extra text
		self.parent.txt.insert("1.0", file_content) #puts all of the file's text in the text widget
		self.parent.txt.change_index = len(file_content)+1
		self.parent.txt.mark_set(tkinter.INSERT, "1.0") #puts the cursor at the start of the file
		self.parent.txt.see(tkinter.INSERT)

		print("filename: ", self.current_file.name, "dir: ", self.current_dir)
	
		self.current_file.close()
	
		self.parent.highlight_chunk() #highlights the text in the text widget
		t1 = time.time() # timer| gets current time in miliseconds
		elapsed_time = round(t1-t0, 3) #elapsed time
		print(t1-t0)
		# puts the time it took to load and highlight the text in the command output widget
		self.parent.command_out_set(f"total lines: {self.parent.get_line_count()};	loaded in: {elapsed_time} seconds", tags=[
			["1.12", f"1.{13+len(str(self.parent.get_line_count()))}"], 
			[f"1.{15+len(str(self.parent.get_line_count()))+11}", f"1.{15+len(str(self.parent.get_line_count()))+11+len(str(elapsed_time))}"]
			]) # wild...
		self.parent.title(f"Nix: <{self.parent.txt.name}>")

		del file_content

		if (arg): return "break"

	def new_directory(self, arg=None, filename=None):
		path = f"{self.current_dir}/{filename}"
		if (os.path.isdir(path)):
			self.parent.command_out_set(f"Directory <{filename}> already exists")
		else:
			os.mkdir(path)
			self.parent.command_out_set(f"Directory <{filename}> was created")

	def delete_directory(self, arg=None, filename=None):
		path = f"{self.current_dir}/{filename}"
		if (os.path.isdir(path)):
			os.rmdir(path)
			self.parent.command_out_set(f"Directory <{filename}> was succesfully deleted")
		else:
			self.parent.command_out_set(f"Directory <{filename}> does not exist")

	def directory_list_get(self, dir):
		dir = os.listdir(self.current_dir)
		dir.sort()
		dir.insert(0, "..")

		return dir
			
	def ls(self, command=[]):
		self.parent.command_out.change_ex(self.parent.command_out.file_explorer)
		dir = self.directory_list_get(self.current_dir)
		result, tags = self.highlight_ls(dir)
		self.parent.command_out_set(result[:-1], tags) # excludes newline at the end


	def highlight_ls(self, dir):
		result = ""
		tags = []
		for i, file in enumerate(dir, 0):
			if (os.path.isdir(f"{self.current_dir}/{file}")):
				tags.append([f"{i+1}.0", f"{i+1}.{len(file)}"])
			result += file+"\n"

		return result, tags

class TODO_HANDLER:
	def __init__(self, parent):
		self.parent = parent
		self.filename = self.parent.todo_filename

	def create_task(self):
		pass

	def delete_task(self):
		pass

	def set_task(self):
		pass

	def create_file(self):
		pass

	def format_file(self):
		pass

	def delete_file(self):
		pass

	def create_task_from_file(self):
		pass
	

class MUSIC_PLAYER(object):
	def __init__(self, parent):
		try: from pygame import mixer
		except ImportError as e: parent.command_out_set(f"ERROR: couldn't create music player, because pygame module couldn't be imported \n {e}"); return
		
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
			self.parent.command_out_set("invalid file")
		
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


class VIDEO_HANDLER:
	def __init__(self, parent):
		self.parent = parent

	def video_record_start(self, filename=f"{time.time()}"):
		""" if you wanna record some video of your code (probably only works on linux (and you have to have ffmpeg installed"""
		pos = f":1.0+{self.parent.winfo_rootx()},{self.parent.winfo_rooty()}"
		videosize = f"{self.parent.winfo_width()}x{self.parent.winfo_height()}"
		path = self.parent.file_handler.current_dir
		filename = f"{filename}.mkv"

		args = [
			["-f", "x11grab"],
			["-framerate", "120"],
			# ["-video_size", videosize],
			["-i", f"{self.parent.title()}"],
			["-vcodec", "libx264"],
			["-qscale", "0"]
		]

		print(args)
		command = f"cd {path}; ffmpeg "
		for arg in args:
			command += f"{arg[0]} {arg[1]} "

		command += filename

		return subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)

	def video_record_stop(self, process):
		process.communicate(b"q")
		print("terminated")

	def screenshot(self):
		def s():
			process = self.video_record_start(filename="screenshot")
			time.sleep(0.5)
			self.video_record_stop(process)

			command = f"ffmpeg -i screenshot.mkv -ss 00:00:00 -frames:v 1 {time.time()}.png"
			process = subprocess.Popen(command, stdin=subprocess.PIPE, shell=True)
			while (process.poll() == None):
				continue

			os.remove("screenshot.mkv")
		threading.Thread(target=s, daemon=True).start()




