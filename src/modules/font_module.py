class FONT_MODULE:
	""" font name too long can't remember """
	def __init__(self, parent):
		self.parent = parent
		
		self.commands = {
			"retro": self.retro,
			"futurism": self.futurism,
			"stream": self.stream,
			"default": self.default,
		}

		self.add_self()

	def retro(self, arg=None):
		self.parent.font_set(family="Ac437 IBM VGA 9x8")
		self.font_set_all()

	def futurism(self, arg=None):
		self.parent.font_set(family="Px437 DOS/V re. JPN30")
		self.font_set_all()

	def stream(self, arg=None):
		self.parent.font_set_all(size=20)

	def default(self, arg=None):
		self.parent.font_set_all(size=12)

	def add_self(self, arg=None):
		self.parent.parser.commands.update(self.commands)