import threading
import tkinter
import random
import time

__status__ = """
completely useless graphical module for creating simple drawings if you're bored to death
absolutely meaningless
"""

def clear(parent):
	for widget in parent.winfo_children():
		if (type(widget) == rect): widget.destroy()

class rect(tkinter.Label):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent

	def blit(self, x, y, w=50, h=50):
		self.place(x=x, y=y, width=w, height=h)

	def transform(self, w, h):
		pass

	def fill(self, bg):
		pass

	def get_size(self):
		return (self.winfo_width(), self.winfo_height())

	def get_width(self):
		return self.winfo_width()

	def get_height(self):
		return self.winfo_height()

	def _config(self, bg=None, fg=None):
		pass