import cv2
import tkinter
from PIL import Image, ImageTk
import threading

class CAM_MODULE(tkinter.Toplevel):
	def __init__(self, parent):
		self.parent = parent
		self.importable = True
		self.commands = {
			"cam_start" : self.start,
			"cam_stop" : self.stop,
		}

		self.add_self()

	def update_image(self):
		if (self.parent.run and self.run):
			material, frame = self.capture.read()
			# if (self.winfo_width() < self.width and self.winfo_height() < self.height):
			frame = cv2.resize(frame, [self.winfo_width(), self.winfo_height()])
			
			self.image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
			self.image = Image.fromarray(self.image)
			self.image = ImageTk.PhotoImage(image=self.image)
			self.image_frame.image = self.image
			self.image_frame.configure(image=self.image)

		else:
			capture.release()
			cv2.destroyAllWindows()

		self.after(5, self.update_image)

	def start(self, arg=None):
		if (arg[1:]): self.width = int(arg[1]); self.height = int(arg[2])
		else: self.width = 1280; self.height = 960
		
		super().__init__(self.parent)
		self.title("CAM")
		
		self.capture = cv2.VideoCapture(0)

		self.capture.set(3, self.width)
		self.capture.set(4, self.height)

		self.image_frame = tkinter.Label(self)
		self.image_frame.place(relwidth=1, relheight=1)

		self.run = True
		
		self.proc = threading.Thread(target=self.update_image, daemon=True)
		self.proc.start()

	def stop(self, arg=None):
		self.run = False
		self.proc.join()
		self.destroy()

	def add_self(self):
		if (self.importable): self.parent.parser.commands.update(self.commands)

	def configure_self(self):
		self.configure(bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"], font=self.font)
		
