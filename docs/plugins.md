# PLUGINS/MODULES

Flag in the config for enabling disabling modules `allow_external_modules`

There sort of is a system for plugins
Plugins are located in the `modules` directory

## How it works

- in a very hacky way the app looks for python files in the `modules` directory and imports the last class in the file under the filename
- the imported class can then get loaded as a plugin if it has an attribute `importable` set to `True`
- this means the imported class then gets added to `WIN` as `WIN.[plugin_filename]`]
- this basically executes arbitrary code in the class, which can be used to for example add new commands or functions, the options are limitless really
- There is a special case for plugins which are widget plugins, which as the name suggests are just new widgets
- You can define your own widget which will get added to `WIN.widgets`
- `WIN.widgets` are iterated and configured and placed according to their `configure_self` and `place_self` functions (see plugin structure below)



# PLUGIN STRUCTURE

Plugins need to have a class defined like below, with attributes `self.parent` and method `add_self`
`add_self` is called upon plugin loading so that's where you'll put all your code to extend the functionality

```
import ...

class NAME:
	def __init__(self, parent):
		self.parent = parent # needed
		self.importable = True # or False if you do not want to load the plugin

	def add_self(self, arg=None):
		"""This functions is called when plugin is loaded. Use for extending parent (WIN) class"""
		...
		
```

For example you could add new commands
```
import ...

class COMMAND_EXTENSION:
	def __init__(self, parent):
		self.parent = parent # needed
		self.importable = True # or False if you do not want to load the plugin
		self.commands = {
			"hello_world": [self.hello_world, "Usage: hello_world | prints Hello World"]
		}

	def hello_world(self, arg=None):
		self.parent.notify("Hello World")

	def add_self(self, arg=None):
		"""This functions is called when plugin is loaded. Use for extending parent (WIN) class"""
		self.parent.parser.commands.update(self.commands)
```

This plugin would get loaded and the `hello_world` command would then be available for use in app

## WIDGET PLUGIN

You can create a widget plugin, which will get placed and used if you define it properly. The structure is the same as normal plugin, but you add:
- an attribute `self.type = "widget"`
- method `configure_self` which should configure the widget to make it look however you want it to
- method `place_self` which is responsible for actually placing the widget

example:
```
import tkinter

class TASK_WIDGET(tkinter.Label):
	def __init__(self, parent):
		super().__init__(parent.info_frame)
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

	def add_self(self):
		self.parent.parser.commands.update(self.commands)

	def task_set(self, arg=None):
		if (not arg[1:]): self.parent.error("no argument"); return
		
		self.task = " ".join(arg[1:])
		self.configure_self()
		self.place_self()

	def task_delete(self, arg=None):
		self.task = ""

	def place_self(self):
		self.place(x=0, y=0, width=self.font.measure(self.task), height=self.font.metrics("linespace"), anchor="nw")

	def configure_self(self):
		self.configure(bg=self.parent.theme["window"]["bg"], fg=self.parent.theme["window"]["fg"], text=self.task, font=self.font)
```

This plugin widget would get loaded, and if you called the command `task_set New task` a little widget would show up in the `info_frame` saying `New task`
If you use a little imagination you could make a lot of things


