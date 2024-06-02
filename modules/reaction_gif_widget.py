import sys
import os
import random

sys.path.append("../")
from widgets import IMAGE_LABEL


class reaction_gif_widget(IMAGE_LABEL):
	def __init__(self, parent, name=""):
		super().__init__(parent, name)
		self.dir = self.parent.conf["reaction_gif_path"]
		self.type = "widget"
		self.importable = True
		self.configure_self()

		self.commands = {
			"react" : self.react,
			"reaction_unplace" : self.unplace,
		}

		self.add_self()

	def add_self(self):
		if (self.importable): self.parent.parser.commands.update(self.commands)

	def react(self, arg=None):
		self.dir = self.parent.conf["reaction_gif_path"]
		dir = self.dir + random.choice(os.listdir(self.dir))
		while (True):
			if (os.path.isdir(dir)):
				dir = dir + "/" + random.choice(os.listdir(dir))
			else:
				break

		# print(dir)
		self.set_filename(dir)
		self.show()
