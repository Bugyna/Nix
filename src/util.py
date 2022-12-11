import os
import json

from functools import wraps

import platform
platform = platform.system()

if (platform == "Windows"):
	import ctypes
	ctypes.windll.shcore.SetProcessDpiAwareness(True)
	
def get_source_path(file):
	return os.path.dirname(os.path.abspath(file))

SOURCE_PATH = get_source_path(__file__)

def bind_keys(widget, bindings: dict):
	if (hasattr(widget, "parent")): supress_warning = getattr(widget, "parent").conf["supress_keybind_warning"]
	else: supress_warning = widget.conf["supress_keybind_warning"]

	# set mode to None as every widget should have a mode even if it's never used
	if (not hasattr(widget, "mode")):	widget.mode = None

	# check for mode-specific bindings
	# unbinding has to occur first ( otherwise it would unbind the wrong bindings )
	# mode-specific binding has to occur last to overwrite the default bindings
	to_bind = []
	func_args = []
	for key, value in bindings.items():
		if (type(value) == dict): # set of bindings
			if (key == widget.mode):
				to_bind.append(value) # add to list that is iterated at the end of this function

			else: # unbind them if the widget mode is different
				for binding, ptr in value.items():
					widget.unbind(binding)
	
	for key, value in bindings.items(): # iterate through the bindings
		if (type(value) == dict):
			continue

		elif (type(value) == list):
			func_args = value[1]
			# print(key, value, value[1], value[1]["argv"])
			value = value[0]

		func_name = value.split(".") # split the function name by dots
		subclass_ptr = widget
		# we're trying to parser the function name to get the function pointer
		# name: parent.update_buffer -> ptr: update_buffer
		
		for ptr_name in func_name[:-1]: # iterate through the function name
			try: subclass_ptr = getattr(subclass_ptr, ptr_name) # get the sub object pointer
			except Exception as e:
				if (not supress_warning): print(e)
			
		try:
			func_ptr = getattr(subclass_ptr, func_name[-1]) # get the function pointer of the last iterated pointer

			if (func_args):
				def f(func, widget, func_args):
					def f1(self, *args, **kwargs):
						return func(self, *args, **func_args)
					return f1
					
				func_ptr = f(func_ptr, widget, func_args)
				func_args = []
	
			widget.bind_class(widget, key, func_ptr) # bind the function to the keybinding
		except Exception as e:
			if (not supress_warning): print(f"BINDING ERROR: {e}")

	for bind_set in to_bind:
		bind_keys(widget, bind_set)

def bind_keys_from_conf(widget, filename=f"{SOURCE_PATH}/keybinds_conf.json"):
	keybinds = json.load(open(filename, "r"))
	widget_name = [type(widget), *type(widget).__bases__] # get name of class and all the classess it inherits from
	# widget_name = [type(widget)]

	for name in widget_name:
		name = name.__name__
		try: keybinds[name]
		except Exception: continue

		bind_keys(widget, keybinds[name])
	

def load_themes(filename):
	return json.load(open(filename, "r"))

def add_command_to_history(func):
	def wrapped_func(self, *args, **kwargs):
		# buffer command history or global command_history?
		# NOTE: it's global history
		if (hasattr(self, "parent")): parent = self.parent
		else: parent = self
		
		print("appending: ", [func, self, args, kwargs])
		parent.command_history.append([func, self, args, kwargs])
		return func(self, *args, **kwargs)

	return wrapped_func


def parse_path(expr):
	expr = expr.replace(".", ".")
	expr = expr.replace("*", "(.)*")
	expr = r"^"+expr
	return expr

