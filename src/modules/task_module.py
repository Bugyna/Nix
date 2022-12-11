import tkinter

class TASK_WIDGET(tkinter.Label):
	def __init__(self, parent):
		super().__init__(parent)
		self.type = "widget"
		self.importable = True
		self.parent = parent
		self.font = self.parent.widget_font
		self.font_size = self.parent.conf["smaller_font_size"]
		self.task = ""
		self.configure_self()

		self.commands = {
			"task_set" : self.task_set,
			"task_del(ete)*" : self.task_delete,
		}

		self.add_self()

	def add_self(self):
		if (self.importable): self.parent.parser.commands.update(self.commands)

	def task_set(self, arg=None):
		if (not arg[1:]): self.parent.error("no argument"); return
		
		for a in arg:
			if (a[0] == "-"):
				if (a[1] == "p"):
					arg[1:] = "working on fixing bugs and other alghoritm stuff y'know".split()
					
		self.task = "CURRENT TASK: "+" ".join(arg[1:])
		self.configure_self()

	def task_delete(self, arg=None):
		self.task = ""

	def place_self(self):
		if (self.task):
			self.place(x=self.parent.key_label.winfo_width()+20, y=0, width=self.font.measure(self.task), height=self.font.metrics("linespace")//1.5+4, anchor="nw")
		else:
			self.unplace()

	def unplace(self):
		self.place_forget()

	def configure_self(self):
		self.configure(bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"], text=self.task, font=self.font)

			