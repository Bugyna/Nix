# widgets.py

## BUFFER_FRAME

- it is a simple `tkinter.Frame`
- children are `BUFFER`s (and it's subclasses `TEXT`s etc.) from `widgets.py`


## BUFFER_TAB_FRAME

- it is a simple `tkinter.Frame`
- children are BUFFER_TAB from `widgets.py`
- can be hidden
	- add `show_buffer_tab=0` to the `conf` file

## INFO_FRAME

- it is a simple `tkinter.Frame`
- children are various widgets(labels) mostly showing information like time, position in opened text buffer, etc.



### theme configurations

- [refer to BUFFER_TAB section](##BUFFER_TAB)


### general info for custom extension of tkinter widgets below
- each class defintion which is an extension of tkinter widgets need to have a method called `configure_self`, which is responsible for configuring the visuals according to the loaded theme as well as setting correct fonts etc.
- refer to `configure` methods in tkinter widgets
- each class defintion needs to have `self.parent` configured to be the instance of the `WIN` application class, however when calling super().__init__ you can pass a different tkinter parent so you can set the tkinter hierarchy to be whatever you want, but each widget should have the `WIN` instance easily available
- generally many classes also have a place_self, unplace_self methods which are responsible for proper positioning(usually pertains to widgets that are placed in the same tkinter container/`Frame`. So things like `BUFFER_TAB`s and `BUFFER`s (and it's subclasses)

## BUFFER_TAB

- extension of `tkinter.Label`
- a part on the top of the window where individual buffer/file names are shown
- can be hidden
	- add `show_buffer_tab=0` to the `conf` file

### theme configurations

- it's the `window` part of the themes
- options for it are
	- `widget_fg` which refers to the default foreground(text) color
	- `select_widget_fg` which refers to the default foreground(text) color when widget is selected(the buffer for it is open)
	- background color is the default window `bg` color
	- when the widget is selected background and foreground colors simply switch


## BUFFER

- base class for all BUFFERs that can be opened(defines base operations like switching between opened buffers etc.) that are necessary in every BUFFER
- is an extension of `tkinter.Frame`



## DEFAULT_TEXT_BUFFER

- inherits `BUFFER`
- base class for all text BUFFERs, which means it defines base operations for managing text editing etc.
- is an extension of `tkinter.Text`
- also has support for names(which then correspond to filenames for `TEXT` buffers)
- defines some general tkinter tags(text tags) (refer to tkinter docs) which are used for highlighting(and underlining, overstriking etc.) text

### theme configurations

- it's the `window` part of the themes
- options for it are
	- `fg` which refers to the default foreground(text) color
	- background color is the default window `bg` color


## COMMAND_ENTRY

- inherits `DEFAULT_TEXT_BUFFER`
- defines the widget in which you input commands
- pretty much the same as `DEFAULT_TEXT_BUFFER`, but defines an input history, which you can scroll through


## FIND_ENTRY

- inherits `DEFAULT_TEXT_BUFFER`
- defines the widget in which you input text you want to search for in opened text buffer(s)
- also defines input history
- defines the actual search and replace operations for text buffers(you may ask "why on earth is search and replace not defined in the actual text buffer classes" and frankly I cannot say anything in my defense except I was young and stupid once)
- defines moving between found matches in the text buffer(s)



## COMMAND_OUT

- inherits `DEFAULT_TEXT_BUFFER`
- a very special widget which defines the widget in which output of commands gets shown
- defines the methods for showing the output as well as filtering through the output
- also defines a few special methods for working with the output (for example when you run `Make` you might get a warning or error with a line number and column, if you press enter while having the text cursor on that line of the output you will move in the text buffer to the line and column in the error)
- this is very universal as it basically passes the selected line to another function when you press enter


## TEXT

- inherits `DEFAULT_TEXT_BUFFER`
- basically the main thing you will use
- is the text buffer in which you edit opened files
- defines all methods which are specific to coding and useful for editing text while coding(so things like commenting lines and many other)