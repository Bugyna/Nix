from util import *
import json
import argparse

def tag_tool():
	for item in self.theme["highlighter"].items(): # iterate through the theme
		if (type(item[1]) == str):
			if (item[0][-2:] == "bg"): # if the name ends with bg we want to create a tag that uses the color specified as a background color
				buffer.tag_configure(item[0], background=item[1], foreground=self.theme["window"]["bg"], font=buffer.font)
				buffer.tag_configure(item[0][:-3], foreground=item[1], font=buffer.font) # but we create a tag with the specified color as the foreground color
				
				self.command_out.tag_configure(item[0], background=item[1], foreground=self.theme["window"]["bg"], font=self.command_out.font) # do the same for the other text widgets
				self.command_out.tag_configure(item[0][:-3], foreground=item[1], font=self.command_out.font)
				self.suggest_widget.tag_configure(item[0][:-3], foreground=item[1], font=self.suggest_widget.font)
				
			elif (item[0][-2:] == "_b"): # bold
				buffer.tag_configure(item[0][:-2], foreground=item[1], font=buffer.font_bold)
				self.command_out.tag_configure(item[0][:-2], foreground=item[1], font=self.command_out.font_bold)
				self.suggest_widget.tag_configure(item[0][:-2], foreground=item[1], font=self.suggest_widget.font_bold)
				
			else: # normal tag
			 	# , borderwidth=2, relief="groove", bgstipple="gray75, underline=False
				
				buffer.tag_configure(item[0], background="", bgstipple="gray50", selectbackground=item[1], selectforeground=self.theme["window"]["bg"], foreground=item[1], font=buffer.font, fgstipple="hourglass", underline=False)
			
				
				
				self.command_out.tag_configure(item[0], bgstipple="gray50", selectbackground=item[1], selectforeground=self.theme["window"]["bg"], foreground=item[1], font=self.command_out.font) # , borderwidth=2, relief="groove", bgstipple="gray75"
				# self.command_out.tag_configure(item[0], underline=True, underlinefg=item[1], foreground=item[1], font=self.command_out.font)
				self.suggest_widget.tag_configure(item[0], foreground=item[1], font=self.suggest_widget.font)

		else:
			item[1]["font"] = buffer.font
			if ("background" not in item[1]):
				item[1]["background"] = ""
			if ("bold" in item[1]):
				item[1]["font"] = buffer.font_bold
				item[1].pop("bold")

			if ("underline" not in item[1]):
				item[1]["underline"] = False
				 
			buffer.tag_configure(item[0], **item[1])
			item[1].pop("font")
			self.command_out.tag_configure(item[0], **item[1], font=self.command_out.font)
			self.suggest_widget.tag_configure(item[0], **item[1], font=self.suggest_widget.font)


		if (type(self.theme["highlighter"]["command_keywords"]) == str):
			self.command_entry.tag_configure("command_keywords", background="", foreground=self.theme["highlighter"]["command_keywords"])

		else:
			c = self.theme["highlighter"]["command_keywords"]
			c["font"] = self.command_entry.font
			if ("bold" in c):
				c["font"] = self.command_entry.font_bold
				c.pop("bold")

			if ("background" not in c):
					c["background"] = ""

			if ("underline" not in c):
					c["underline"] = False

			self.command_entry.tag_configure("command_keywords", **c)
			
		try:
			self.buffer.tag_raise("keywords")
			self.buffer.tag_lower("cursor")
		except Exception as e:
			print(e)


def add_option_to_window(option_name, value, filename=f'{SOURCE_PATH}/theme_conf.json'):
	if not filename: filename=f'{SOURCE_PATH}/theme_conf.json'

	themes = load_themes(filename)
	for theme_name, theme in themes.items():
		# print(theme['window'])
		theme['window'][option_name] = value

	print(json.dumps(themes, indent='\t'))

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
					prog='theme helper tool',
					description='managing themes',
					epilog='--aw add option to window')
	parser.add_argument('--add-win-option', action='extend', nargs='+', type=str)
	parser.add_argument('--add-highlighter-option', action='extend', nargs='+', type=str)
	parser.add_argument('--theme', action='extend', nargs='+', type=str)
	# parser.add_argument('--theme', action='extend', nargs='+', type=str)
	parser.add_argument('--filename', type=str)
	parser.add_argument('--overwrite', type=bool)
	parser.add_argument('--save', type=str)

	parsed = parser.parse_args()
	if (parsed.add_win_option):
		add_option_to_window(*parsed.add_win_option, parsed.filename)
