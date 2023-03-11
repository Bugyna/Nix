import os
import time
import random
import tkinter
import threading
import subprocess
import glob
import magic

from ascii_art import *
from widgets import *

import platform
platform = platform.system()

# thanks to everyone on https://www.asciiart.eu/

class FILE_HANDLER(object):
	""" File opening and closing yes"""
	def __init__(self, parent):
		self.current_dir = os.getcwd()
		print("start dir: ", self.current_dir)
		self.current_file = None
		self.current_file_name = None
		self.current_buffer = None

		self.magic = magic.Magic(mime=True, mime_encoding=True)

		self.buffer_dict = {}
		self.buffer_list = []
 
		self.buffer_tab = None
		self.buffer_tab_index = None # buffer tabs have the same index as text widgets
		self.buffer_tab_list = []

		self.scratch_buffer = None

		self.parent = parent

	def closing_sequence(self) -> None:
		for b in self.buffer_list[1:]:
			self.close_buffer(buffer_name=b[0].full_name)

	def init(self, buffer_name: str):
		self.scratch_buffer = TEXT(self.parent, buffer_name, "temp")
		self.buffer_list.append([self.scratch_buffer, BUFFER_TAB(buffer_name, self.parent, render=False)])
		self.buffer_dict[buffer_name] = self.buffer_list[-1]
		self.parent.buffer_render_list.insert(self.parent.buffer_render_index, self.buffer_list[-1][0])
		self.parent.buffer = self.parent.buffer_render_list[self.parent.buffer_render_index]
		self.buffer_tab = self.buffer_list[-1][1]
		self.buffer_tab_list.append(self.buffer_list[-1][1])
		self.parent.title(f"Nix: <{self.parent.buffer.name}>")
		# self.parent.buffer.insert("1.0", "\nhttps://www.asciiart.eu/")
		self.parent.buffer.insert("1.0", art[random.randint(0, len(art)-1)])
		self.parent.buffer.mark_set("insert", len(self.parent.buffer.get("1.0", "end").split("\n"))/2)
		
		self.parent.buffer.tag_add("center", "1.0", "end")

	def renew_scratch(self):
		buffer_name = self.scratch_buffer.name
		self.buffer_list.append([self.scratch_buffer, BUFFER_TAB(buffer_name, self.parent, render=False)])
		self.buffer_dict[buffer_name] = self.buffer_list[-1]
		self.load_buffer(buffer_name=buffer_name)
		# self.parent.buffer_render_list.insert(self.parent.buffer_render_index, self.buffer_list[-1][0])
		# self.parent.buffer = self.parent.buffer_render_list[self.parent.buffer_render_index]
		# self.buffer_tab = self.buffer_list[-1][1]
		# self.buffer_tab_list.append(self.buffer_list[-1][1])

	# def load_scratch(self, arg=None):
		# self.parent.buffer_unplace()
		# self.parent.buffer_render_list.insert(self.parent.buffer_render_index, self.buffer_list[0][0])
		# self.parent.buffer = self.parent.buffer_render_list[self.parent.buffer_render_index]
		# self.parent.buffer.focus_set()
		# self.parent.reposition_widgets()
		
		# self.parent.title(f"Nix: <{self.parent.buffer.name}>")
		# self.parent.buffer.font_size_set()
		# self.parent.theme_load()

		# if (arg): return "break"

	def buffer_exists(self, buffer_name):
		try:
			self.buffer_dict[buffer_name]
			return 1
			
		except KeyError: return 0

	def rename_buffer(self, buffer_name: str, new_buffer_name: str):
		old = self.buffer_dict.pop(buffer_name)
		index = old[0].buffer_index

		self.buffer_list[index][0].change_name(new_buffer_name)
		self.buffer_list[index][1].change_name(new_buffer_name)
		self.buffer_tab_list[index].change_name(new_buffer_name)
		
		old[0].change_name(new_buffer_name)
		old[1].change_name(new_buffer_name)
		
		self.buffer_dict[new_buffer_name] = old
		self.parent.buffer = self.buffer_dict[new_buffer_name][0]
		
		self.current_file_name = self.current_buffer = new_buffer_name

	def new_buffer(self, buffer_name, buffer_type="normal", load=True):
		if (self.buffer_exists(buffer_name)): self.load_buffer(buffer_name=buffer_name); return

		if (buffer_type == "GRAPHICAL"): self.buffer_list.append([GRAPHICAL_BUFFER(self.parent, buffer_name), BUFFER_TAB(buffer_name, self.parent)])
		else: self.buffer_list.append([TEXT(self.parent, buffer_name, buffer_type), BUFFER_TAB(buffer_name, self.parent)])
		
		self.buffer_dict[buffer_name] = self.buffer_list[-1]
		self.buffer_tab_list.append(self.buffer_list[-1][1])

		if (load): self.load_buffer(buffer_name=buffer_name)
		return self.buffer_list[-1][0]


	def close_buffer(self, arg=None, buffer_name: str=None):
		if (not buffer_name): buffer_name = self.parent.buffer.full_name
		buffer_index = self.buffer_dict[buffer_name][0].buffer_index
		
		for i, buffer in enumerate(self.parent.buffer_render_list, 0):
			if (buffer == self.buffer_dict[buffer_name][0]):
				self.parent.buffer_render_list.pop(i)
				self.parent.split_mode = "nosplit"
				self.parent.buffer_render_index = i-1 if i-1 > 0 else 0

		self.buffer_dict[buffer_name][0].unplace()
		self.buffer_dict[buffer_name][1].unplace()

		if (self.parent.conf["backup_files"]): self.del_file(filename=f".{os.path.basename(buffer_name)}.error_swp")
		# if (len(self.buffer_dict[buffer_name].get("1.0", "end-1c")) == 0): self.del_file(filename=buffer_name) # deletes created file if the text buffer is empty
		
		self.buffer_tab_list.pop(buffer_index)
		self.buffer_list.pop(buffer_index)
		self.buffer_dict.pop(buffer_name)

		for i in range(0, len(self.buffer_list)):
			self.buffer_list[i][0].buffer_index = i
			self.buffer_list[i][1].buffer_index = i
			self.buffer_list[i][1].reposition()

		# self.load_buffer(buffer_index=len(self.buffer_list)-1)
		# if (len(self.buffer_list) == 0):
		self.load_buffer(buffer_index=buffer_index-1)

		if (arg): return "break"


	def load_buffer(self, arg=None, buffer_name: str = None, buffer_index: int = None):
		if (len(self.buffer_list) == 0):
			self.renew_scratch()
			return

		if (buffer_index and buffer_index >= len(self.buffer_list)):
			buffer_index = 0
			
		if (buffer_index is not None): buffer_name = self.buffer_list[buffer_index][0].full_name
			
		if (self.parent.buffer.full_name == buffer_name): return
		
		p = self.parent.buffer
		if (len(self.parent.buffer_render_list)-1 < self.parent.buffer_render_index): self.parent.buffer_render_list.insert(self.parent.buffer_render_index, self.buffer_dict[buffer_name][0])
		else: self.parent.buffer_render_list[self.parent.buffer_render_index] = self.buffer_dict[buffer_name][0]
		self.parent.buffer = self.parent.buffer_render_list[self.parent.buffer_render_index]
			
		self.buffer_tab = self.buffer_dict[buffer_name][1]
		self.buffer_tab_index = self.parent.buffer.buffer_index # text widget's buffer_index is the same as their buffer tab's buffer_index

		# if (buffer_index != 0): self.current_file_name = self.current_buffer = self.parent.buffer.full_name; self.current_dir = os.path.dirname(self.current_buffer)
		self.set_current_file(buffer_name=buffer_name)
		
		self.parent.title(f"Nix: <{self.parent.buffer.name}>")
		
		if (type(self.parent.buffer) == "TEXT"): self.parent.buffer.font_size_set()
		self.parent.theme_load()
		
		if (self.parent.conf["show_buffer_tab"]): self.buffer_tab.focus_highlight()
		
		self.parent.reposition_widgets()
		self.parent.notify(arg=f"buffer [{self.parent.buffer.name}] was loaded", tags=[["1.7", "1.8", "logical_keywords"], ["1.8", f"1.{8+len(self.parent.buffer.name)}"], [f"1.{8+len(self.parent.buffer.name)}", f"1.{9+len(self.parent.buffer.name)}", "logical_keywords"]])
		if (self.parent.focus_get() == p or self.parent.focus_get() == self.parent.command_out): self.parent.buffer.focus_set()
		elif (self.parent.focus_get() == self.parent.find_entry): self.parent.find_entry.focus_set()
		p.unplace() # weird (seemingly) optimalization trick
		os.chdir(self.current_dir)
		
		if (arg): return "break"

	def set_current_file(self, arg=None, buffer_name=None):
		self.current_file_name = self.current_buffer = self.parent.buffer.full_name
		tmp = os.path.dirname(self.current_buffer)
		if (tmp): self.current_dir = tmp
		
		self.buffer_tab_index = self.parent.buffer.buffer_index

		if (self.parent.conf["show_buffer_tab"]):
			self.buffer_tab.configure_self()
			self.buffer_tab = self.buffer_dict[buffer_name][1]
			self.buffer_tab.focus_highlight()
		else:
			self.buffer_tab = self.buffer_dict[buffer_name][1]	

	def list_buffer(self, arg=None):
		result = ""
		for val in self.parent.file_handler.buffer_list:
			result += f"{val[1].full_name}\n"
			self.parent.command_out.change_ex(self.parent.command_out.buffer_load)
		if (not result): result = "<None>"
		self.parent.command_out_set(result)

		return "break"

	def del_file(self, arg=None, filename:str=""):
		if (not filename): filename=self.parent.buffer.full_name
		
		if (self.buffer_exists(filename)): self.close_buffer(buffer_name=filename)

		if (os.path.isfile(filename)): os.remove(filename); self.parent.notify(f"File [{filename}] was deleted")
		else: self.parent.notify(f"File ({filename}) does not exist")

		if (arg): return "break"

	def new_file(self, arg=None, filename: str=""):
		if (not filename):
			i = 0
			filename = f"{self.current_dir}/untitled_{i}.txt"
			while (os.path.isfile(filename) and i < 9):
				i += 1
				filename = f"{self.current_dir}/untitled_{i}.txt"

		filename = os.path.abspath(filename)
		
		try:
			current_file = open(filename, "w+")
			self.new_buffer(filename)
			current_file.close()
		except PermissionError:
			self.new_buffer(filename, buffer_type="readonly")

		self.current_dir = os.path.dirname(filename)
		self.parent.title(f"Nix: <{self.parent.buffer.name}>")
		
		self.parent.buffer.set_highlighter()

		if (arg): return "break"

	def save_file(self, arg = None):
		""" saves current text into opened file """
		if (self.parent.buffer.type != "normal"): self.parent.error(f"{self.parent.buffer.type} buffer"); return "break"
		elif (self.parent.buffer.state == []): return "break"

		if (self.parent.buffer.full_name):
			size0 = os.path.getsize(self.parent.buffer.full_name)

			current_file = open(self.parent.buffer.full_name, "w")
			current_file.write(self.parent.buffer.get("1.0", "end-1c"))
			current_file.close()
			self.parent.buffer.file_start_time = os.stat(self.parent.buffer.full_name).st_mtime

			self.parent.buffer.set_highlighter()
			size1 = os.path.getsize(self.parent.buffer.full_name)
			
			self.current_dir = os.path.dirname(self.parent.buffer.full_name)
			self.parent.title(f"Nix: <{os.path.basename(self.parent.buffer.name)}>")
			self.parent.buffer.state_set(pop=["*", "!"])
			# self.buffer_tab.change_name(extra_char=" ")
			
			self.parent.notify(rf"saved [{size1-size0}B|{size1}B|{self.parent.buffer.get_line_count()}L] to {self.current_file_name}")
			
		elif (not self.current_file_name):
			self.new_file()
			self.save_file()

		if (arg): return "break"

	def save_file_as(self, arg=None, filename=None, new_filename=None):
		""" saves current text into a new file """

		if (filename): filename = os.path.abspath(f"{self.current_dir}/{filename}")
		else: filename = self.parent.buffer.full_name
		new_filename = os.path.abspath(f"{self.current_dir}/{new_filename}")
		print("saveas: ", new_filename)
		
		os.rename(filename, new_filename)
		self.rename_buffer(filename, new_filename)
		self.save_file()
		self.parent.highlight_chunk()

		if (arg): return "break"

	def load_file(self, arg=None, filename=None):
		""" opens a file and loads it's content into the text widget """

		buffer_type = "normal"
		binary = False

		# if (filename):
			# if (not os.path.isfile(filename)): filename = os.path.abspath(f"{self.current_dir}/{filename}")
			# if (self.buffer_exists(filename)): self.load_buffer(buffer_name=filename)

		if (not os.path.isfile(filename)):
			self.new_file(filename=filename)
			return

		self.cd(os.path.dirname(filename))
		
		if (os.access(filename, os.R_OK)):
			info = self.magic.from_file(filename).split(';')
			filetype = info[0].split('/')[0]
			encoding = info[1].split('=')[1]

			if encoding != "binary":
				if os.access(filename, os.W_OK):
					current_file = open(filename, "r+") #opens the file
				else:
					current_file = open(filename, "r")
					buffer_type = "readonly"

			elif filetype == "image":
				self.new_buffer(filename, buffer_type="GRAPHICAL")
				return
			
			else:
				current_file = open(filename, "rb")
				buffer_type = "readonly"
				binary = True

		else:
			raise Exception(f"Do not have permission to read file {filename}")

		file_content = current_file.read()

		t0 = time.time() # timer| gets current time in miliseconds
			

		buffer = self.new_buffer(filename, buffer_type=buffer_type)
		if (binary):
			buffer.highlighter.highlight = buffer.highlighter.empty_highlight
		if (self.parent.conf["backup_files"]):
			file = open("."+os.path.basename(filename)+".error_swp", "w+")
			file.write(file_content)
			file.close()

		buffer.delete("1.0", "end") # deletes the buffer so there's not any extra text
		buffer.insert("1.0", file_content) # puts all of the file's text in the text widget
		buffer.total_chars = len(file_content)+1
		buffer.total_lines = self.parent.buffer.get_line_count()
		# if (platform == "Windows"): self.parent.convert_to_crlf()
		# else: self.parent.convert_to_lf()
		buffer.mark_set("insert", "1.0") #puts the cursor at the start of the file
		buffer.see("insert")
	
		current_file.close()
	
		self.parent.highlight_chunk() #highlights the text in the text widget
		t1 = time.time() # timer| gets current time in miliseconds
		elapsed_time = round(t1-t0, 3) #elapsed time
		# puts the time it took to load and highlight the text in the command output widget
		self.parent.notify(f"total lines: {self.parent.buffer.get_line_count()};	loaded in: {elapsed_time} seconds", tags=[
			["1.13", f"1.{13+len(str(self.parent.buffer.get_line_count()))}"], 
			[f"1.{15+len(str(self.parent.buffer.get_line_count()))+11}", f"1.{15+len(str(self.parent.buffer.get_line_count()))+11+len(str(elapsed_time))}"]
			]) # wild...
		self.parent.title(f"Nix: <{self.parent.buffer.name}>")

		del file_content
		# buffer.lexer.lex()
		buffer.edit_modified(False)

		if (arg): return "break"

	def new_directory(self, arg=None, filename=None):
		path = f"{self.current_dir}/{filename}"
		if (os.path.isdir(path)):
			self.parent.notify(f"Directory <{filename}> already exists")
		else:
			os.mkdir(path)
			self.parent.notify(f"Directory <{filename}> was created")

	def delete_directory(self, arg=None, filename=None):
		path = f"{self.current_dir}/{filename}"
		if (os.path.isdir(path)):
			os.rmdir(path)
			self.parent.notify(f"Directory <{filename}> was succesfully deleted")
		else:
			self.parent.notify(f"Directory <{filename}> does not exist")

	def directory_list_get(self, dir=None, expr=None):
		if (not dir): dir = self.current_dir
		dir = os.listdir(dir)

		fdir = dir
		if (expr):
			expr = expr.replace(".", r"\.")
			expr = expr.replace("*", r"(.)*")
			dir = [file for file in fdir if re.match(expr, file)]

		dir.sort()
		dir.insert(0, "..")

		return dir

	def cd(self, dir):
		if (os.path.isdir(dir)):
			self.current_dir = dir
			self.parent.notify(arg=f"current directory: {self.current_dir}")
		else:
			self.parent.error(arg=f"File/Directory {dir} not found")
			return False

		os.chdir(self.current_dir)
		return True
			
	def ls(self, dir=None, sep=" ", expr=None):
		if (not dir): dir = self.directory_list_get()
		result = ""
		for i, file in enumerate(dir, 0):
			result += file+sep

		return result

	def highlight_ls(self, dir=None):
		if (not dir): dir = self.directory_list_get()
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
		except ImportError as e: parent.notify(f"ERROR: couldn't create music player, because pygame module couldn't be imported \n {e}"); return
		
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
			self.parent.notify("invalid file")
		
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




