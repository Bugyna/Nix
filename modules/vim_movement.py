import sys
import os
sys.path.append(os.path.abspath(f'{__file__}/../../'))

from widgets import bind_keys_from_conf

class VIM_MOVE_MODULE:
	""" adds h j k l movement when Alt-i is pressed and disables it once Alt-i is pressed again """
	def __init__(self, parent):
		self.parent = parent
		self.importable = True

	def vim_move_standard(self, arg=None, key=None):
		arg = arg.char.lower()
		if (arg == "h"): self.parent.buffer.move_standard(key="Left")
		elif (arg == "j"): self.parent.buffer.move_standard(key="Down")
		elif (arg == "k"): self.parent.buffer.move_standard(key="Up")
		elif (arg == "l"): self.parent.buffer.move_standard(key="Right")
		return "break"
		
	def vim_move_jump(self, arg=None, key=None):
		arg = arg.char.lower()
		if (arg == "h"): self.parent.buffer.move_jump(key="Left")
		elif (arg == "j"): self.parent.buffer.move_jump(key="Down")
		elif (arg == "k"): self.parent.buffer.move_jump(key="Up")
		elif (arg == "l"): self.parent.buffer.move_jump(key="Right")
		return "break"
		
	def vim_move_select(self, arg=None, key=None):
		arg = arg.char.lower()
		if (arg == "h"): self.parent.buffer.move_select(key="Left")
		elif (arg == "j"): self.parent.buffer.move_select(key="Down")
		elif (arg == "k"): self.parent.buffer.move_select(key="Up")
		elif (arg == "l"): self.parent.buffer.move_select(key="Right")
		return "break"
		
	def vim_move_jump_select(self, arg=None, key=None):
		arg = arg.char.lower()
		if (arg == "h"): self.parent.buffer.move_jump_select(key="Left")
		elif (arg == "j"): self.parent.buffer.move_jump_select(key="Down")
		elif (arg == "k"): self.parent.buffer.move_jump_select(key="Up")
		elif (arg == "l"): self.parent.buffer.move_jump_select(key="Right")
		return "break"

	def mode_set_move(self, arg=None):
		self.parent.buffer.mode_set(mode="move")
		if (self.parent.buffer.mode == "move"):
			self.parent.buffer.bind_key_with_all_mod("H", [self.vim_move_jump_select, self.vim_move_jump, self.vim_move_select, self.vim_move_standard])
			self.parent.buffer.bind_key_with_all_mod("J", [self.vim_move_jump_select, self.vim_move_jump, self.vim_move_select, self.vim_move_standard])
			self.parent.buffer.bind_key_with_all_mod("K", [self.vim_move_jump_select, self.vim_move_jump, self.vim_move_select, self.vim_move_standard])
			self.parent.buffer.bind_key_with_all_mod("L", [self.vim_move_jump_select, self.vim_move_jump, self.vim_move_select, self.vim_move_standard])

			self.parent.buffer.bind_key_with_all_mod("h", [self.vim_move_jump_select, self.vim_move_jump, self.vim_move_select, self.vim_move_standard])
			self.parent.buffer.bind_key_with_all_mod("j", [self.vim_move_jump_select, self.vim_move_jump, self.vim_move_select, self.vim_move_standard])
			self.parent.buffer.bind_key_with_all_mod("k", [self.vim_move_jump_select, self.vim_move_jump, self.vim_move_select, self.vim_move_standard])
			self.parent.buffer.bind_key_with_all_mod("l", [self.vim_move_jump_select, self.vim_move_jump, self.vim_move_select, self.vim_move_standard])

		else:
			self.parent.buffer.unbind_key_with_all_mod("H")
			self.parent.buffer.unbind_key_with_all_mod("J")
			self.parent.buffer.unbind_key_with_all_mod("K")
			self.parent.buffer.unbind_key_with_all_mod("L")

			self.parent.buffer.unbind_key_with_all_mod("h")
			self.parent.buffer.unbind_key_with_all_mod("j")
			self.parent.buffer.unbind_key_with_all_mod("k")
			self.parent.buffer.unbind_key_with_all_mod("l")
			bind_keys_from_conf(self.parent.buffer)
		return "break"
		