# A START OF SOMETHING TRULY HORRIBLE
import re
import os
import sys
# I have no idea why I did it this way
# Like sure it's kinda extendable and you can kinda add new functions easily, but it's like really fucking annoying
# I'll remake it someday, probably, maybe, hopefully, not really
# I have like 4 more things to remake and I am lazy

def ld(s, t, n):
	if (n >= 25): return 25
	n += 1
	if not s: return len(t)
	if not t: return len(s)
	if s[0] == t[0]: return ld(s[1:], t[1:], n)
	l1 = ld(s, t[1:], n)
	l2 = ld(s[1:], t, n)
	l3 = ld(s[1:], t[1:], n)
	if (n >= 25): return 25
	return 1 + min(l1, l2, l3)

class PARSER:
	def __init__(self, parent):
		""" OOP GONE WRONG NOT CLICKBAIT I HATE THIS """
		self.parent = parent
		
		self.commands = {
			"help": self.help,
			"highlighting": self.highlighting_set,
			"suggest": self.suggest_set,
			r"[0-9]": self.l,
			r"^l[0-9]+$|^l[0-9]+.[0-9]+$|^lget$": self.l,
			"find": self.find,
			"lyrics": self.lyrics_get,
			"temp": self.temp,
			"time": self.time_set,
			"blink": self.blink,
			"split": self.split,
			"unsplit": self.unsplit,
			"q|quit": self.win_quit,
			"sharpness": self.sharpness_set,
			"alpha|transparency": self.alpha_set,
			"convert": self.convert,
			"cap": self.video_capture,
			"screenshot|printscreen": self.screenshot,
			"resize": self.win_resize,
			"buffers": self.buffers,
			"save": self.file_save,
			"saveas": self.file_saveas,
			"open|load": self.file_load,
			"reopen|reload": self.file_reload,
			"rm|del": self.file_delete,
			"play": self.music_play,
			"pause": self.music_pause,
			"unpause": self.music_unpause,
			"stop": self.music_stop,
			"sys": self.system_execute,
			"exec": self.python_execute,
			"ls|dir": self.ls,
			"cd": self.cd,
			"theme": self.theme,
			"flashy": self.parent.flashy_loading_bar,
		}

	def parse_argument(self, arg=None):
		# for a in arg:
			# if (a.startswith("\"")):
				# q = True
			# elif (a.endswith("\"")):
				# q = False
			# elif (a.startswith("-")):
				# pass

		for key in self.commands.keys():
			if (re.match(f"\\b({key})\\b", arg[0])):
				self.command_execute = self.commands[key]
				self.command_execute(arg)
				break
		else:
			self.command_execute = self.command_not_found
			self.command_execute(arg)

	def execute(self, arg=None):
		pass

	def help(self, arg=None):
		try:
			self.parent.command_out_set(f"{self.commands[arg[1]]}")
		except IndexError:
			x = ""
			for item in list(self.parent.commands.keys()):
				x += "\n"+item
			self.parent.command_out_set(x)

	def highlighting_set(self, arg=None):
		if (arg[1] == "on"):
			self.parent.command_out_set("highlighting on")
			self.parent.highlight_chunk()
			self.parent.highlighting = True
		elif (arg[1] == "off"):
			self.parent.unhighlight_chunk()
			self.parent.command_out_set("highlighting off")
			self.parent.highlighting = False

	def suggest_set(self, arg=None):
		self.parent.suggest = not self.paernt.suggest

	# elif (re.match(r"[0-9]", arg[0][0])):
		# self.txt.mark_set(tkinter.INSERT, float(arg[0]))
		# self.txt.see(float(arg[0])+2)
		# self.command_out_set(f"moved to: {float(arg[0])}")

	# elif (re.match(r"^l[0-9]+$|^l[0-9]+.[0-9]+$|^lget$", arg[0])):
	def l(self, arg=None):
		for i, pnum in enumerate(arg[0][1:], 1):
			if (re.search("[0-9]", pnum)): 
				argument = arg[0][i:]
				break
			
			elif (re.search("[a-zA-Z]", pnum)):
				argument = arg[0][i:]
				break

		if (re.match(r"[0-9]", argument)):
			self.parent.txt.mark_set(tkinter.INSERT, float(argument))
			self.parent.txt.see(float(argument)+2)
			self.parent.command_out_set(f"moved to: {float(argument)}")

		elif (re.match("get", argument)):
			self.parent.command_out_set(f"total lines: {self.parent.get_line_count()}", tags=[["1.15", "end"]])

	def find(self, arg=None):
		self.parent.find_place(text=arg[1])
		self.parent.find(arg[1])

	def lyrics_get(self, arg=None):
		def lyr():
			command1 = ""
			for word in arg[1:]:
				command1 += "-"+word
			command1 = command1.split(",")
			url = f"http://www.songlyrics.com/{command1[0]}/{command1[1]}-lyrics/" #link to Stockholm's weather data
			html = requests.get(url).content #gets the html of the url
			lyrics = BeautifulSoup(html, features="html.parser").find(id="songLyricsDiv").text
			self.parent.command_out_set(lyrics)
		threading.Thread(target=lyr).start()

	def temp(self, arg=None):
		self.parent.get_temperature()
		self.parent.txt.focus_set()

	def time_set(self, arg=None):
		self.parent.command_out_set(self.get_time(), tags=[["1.0", "end"]])

	def blink(self, arg=None): #wonky as fuck
		if (arg[1] == "on"):
			self.parent.txt.insert_offtime = 300; self.txt.insert_ontime = 700

		elif (arg[1] == "off"):
			self.parent.txt.insert_offtime = 0; self.txt.insert_ontime = 1

		else:
			self.parent.command_out_set(f"ERROR: Invalid argument {arg[1:]}", tags=[["1.0", "1.7"]])
			
		self.parent.txt.configure(insertofftime=self.txt.insert_offtime, insertontime=self.txt.insert_ontime)
		self.parent.txt.focus_set()

	def split(self, arg=None):
		if (arg[1] == "n"):
			self.parent.unsplit(arg)

		elif (arg[1] == "vertical" or arg[1] == "v"):
			self.parent.split_mode = 1
			try: self.parent.txt_1 = self.parent.file_handler.buffer_list[self.parent.txt.buffer_index+1][0]
			except IndexError: self.parent.txt_1 = self.parent.file_handler.buffer_list[1][0]
			self.parent.command_out_set("split vertically")

		elif (arg[1] == "horizontal" or arg[1] == "h"):
			self.parent.split_mode = 2
			try: self.parent.txt_1 = self.parent.file_handler.buffer_list[self.parent.txt.buffer_index+1][0]
			except IndexError: self.parent.txt_1 = self.parent.file_handler.buffer_list[1][0]
			self.parent.command_out_set("split horizontally")

		self.parent.reposition_widgets()

	def unsplit(self, arg=None):
		self.parent.txt_1.place_forget()
		self.parent.split_mode = 0
		self.parent.txt_1 = None
		self.parent.reposition_widgets()

	def win_quit(self, arg=None):
		self.parent.run = False
		self.parent.quit()
		# self.destroy()

	def sharpness_set(self, arg=None):
		self.parent.sharpness = arg[1]
		self.parent.tk.call("tk", "scaling", arg[1])
		self.parent.command_out_set(f"sharpness: {arg[1]}")

	def alpha_set(self, arg=None):
		if (arg[1] == "default"): arg[1] = 90
		self.parent.wm_attributes("-alpha", int(arg[1])/100)
		self.parent.command_out_set(f"alpha: {arg[1]}")

	def convert(self, arg=None):
		try:
			if (arg[1][:2] == "0x"):
				decimal = int(arg[1], 16)
			elif (arg[1][:2] == "0b"):
				decimal = int(arg[1], 2)
			else:
				decimal = int(arg[1], 10)

			self.parent.command_out_set(f"DECIMAL: {decimal}, HEXADECIMAL: {hex(decimal)}, BINARY: {bin(decimal)}")
		except ValueError:
			self.parent.command_out_set("Error: wrong format; please, add prefix (0x | 0b)")

	def video_capture(self, arg=None):
		if (arg[1] == "start"):
			self.parent.process = self.parent.video_handler.video_record_start(self)
		
		elif (arg[1] == "stop"):
			self.parent.video_handler.video_record_stop(self.process)
			self.parent.command_out_set("screen capture terminated")
	
	def screenshot(self, arg=None):
		self.parent.video_handler.screenshot(self)
	
	def win_resize(self, arg=None):
		self.parent.update_win()
		self.parent.geometry(f"{int(arg[1])}x{int(arg[2])}")
		
	def buffers(self, arg=None):
		if (not arg[1:]):
			result = ""
			for val in self.parent.file_handler.buffer_list[1:]:
				result += f"<{val[1].name}> "
			if (not result): result = "<None>"
			self.parent.command_out_set("buffers: "+result)
		else:
			self.parent.file_handler.load_buffer(arg[1:])

	def file_save(self, arg=None):
		self.parent.file_handler.save_file()
	
	def file_saveas(self, arg=None):
		self.parent.file_handler.save_file_as(tmp=arg[1])

	def file_load(self, arg=None):
		self.parent.file_handler.load_file(filename="".join(arg[1:]))

	def file_reload(self, arg=None):
		self.parent.file_handler.load_file(filename=self.file_handler.current_file.name)

	def file_delete(self, arg=None):
		self.parent.file_handler.del_file(filename="".join(arg[1:]))
		
	def music_play(self, arg=None):
		self.parent.music_player.load_song(arg[1:])

	def music_pause(self, arg=None):
		self.parent.music_player.pause_song()

	def music_unpause(self, arg=None):
		self.parent.music_player.pause_song(unpause=True)

	def music_stop(self, arg=None):
		self.parent.music_player.stop_song()

	def system_execute(self, arg=None):
		self.parent.txt.run_subprocess(argv=arg[1:])

	def python_execute(self, arg=None):
		exec ("".join(arg[1:]))

	def ls(self, arg=None):
		self.parent.file_handler.ls(arg)

	def cd(self, arg=None):
		if (str(arg[1:])[0] == "/"):
			path = os.path.normpath(arg[1])
		else:
			path = os.path.normpath(f"{self.parent.file_handler.current_dir}/{arg[1]}")
			
		if (os.path.isdir(path)):
			self.parent.file_handler.current_dir = path
			self.parent.command_out_set(arg=f"current directory: {self.parent.file_handler.current_dir}")
		else:
			self.parent.command_out_set(arg=f"Error: File/Directory not found")

	def theme(self, arg=None):
		if (arg[1:]):
			self.parent.theme_set(arg[1:])
		else:
			self.parent.command_out.change_ex(self.parent.theme_set)
			result = ""
			for key in self.parent.theme_options.keys():
				result += key+"\n"
			self.parent.command_out_set(result, [["1.0", "end"]])


	def command_not_found(self, arg=None):
		res = ""
		for c in arg:
			res += c+" "
		self.parent.command_out_set(f"arg <{res[:-1]}> not found", [["1.0", "1.7"], [f"1.{8+len(res)+2}", "end"]])





















