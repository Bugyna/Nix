# widgets.py


## BUFFER_TAB_FRAME

- it is a simple tkinter.Frame
- children are BUFFER_TAB from `widgets.py`
- can be hidden
	- add `show_buffer_tab=0` to the `conf` file

### theme configurations

- [refer to BUFFER_TAB section](##BUFFER_TAB)

## BUFFER_TAB

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


