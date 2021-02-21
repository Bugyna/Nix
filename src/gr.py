import threading
import tkinter
import random
import time

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

class rain:
	def __init__(self, parent):
		self.parent = parent
		self.particles = []
		self.particle = None

	def gen_particles(self):
		for i in range(500):
			self.particles.append(tkinter.Label(self.parent.txt))

	def rain(self):
		def a():
			x,y = self.parent.txt.cursor_xy_get()
			# for i in range(10):
			self.particle = tkinter.Label(self.parent.txt)
			tkinter.Label(self.parent.txt).place(x=x, y=y, width=2, height=2)
			for i in range(500):
				y = self.particle.winfo_y()+5
				self.particle.place(x=x, y=y)
				self.particle.update()

			time.sleep(1)
			self.particle.place_forget()
			# self.parent.update_win()

		threading.Thread(target=a, daemon=True).start()

class cursor:
	def __init__(self, parent):
		self.parent = parent
		self.particles = []

	def spawn_particles(self):
		# def a():
		x,y = self.parent.cursor_xy_get()
		for i in range(10):
			self.particles.append(tkinter.Label(self.parent))
			self.particles[-1].place(x=random.randint(x-20, x+20), y=random.randint(y-20, y+20), width=2, height=2)
		
		def a():
			for particle in self.particles:
				x = particle.winfo_x()+random.randint(-5,5)
				y = particle.winfo_y()+random.randint(-5,5)
				particle.place(x=x,y=y)
				
		threading.Thread(target=a, daemon=True).start()