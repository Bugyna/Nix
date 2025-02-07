# General config file

## default version

- the default version of the config is hardcoded as a dictionary in the `WIN` class in `main.py`
- looks like this and *SHOULD NOT BE CHANGED( TO CHANGE CONFIG USE THE `conf` FILE )*
	```
	self.conf: Dict[str, str|int|Callable|bool] = {
			"theme": "spacey",
			"tab_size": 4,
			"orientate": "down",
			"backup_files": 0,
			"underline_pairs": 0,
			"font_size": 12,
			"smaller_font_size": 11,
			"command_entry_font_size": 11,
			"find_entry_font_size": 12,
			"command_out_font_size": 11,
			"suggest_widget_font_size": 11,
			"start_width": 80,
			"start_height": 32,
			"show_buffer_tab": 1,
			"line_end": LF,
			"suggest": 1,
			"font": "Consolas",
			"default_find_mode": "?",
			"username": "",
			"default_split_mode": "vertical",
			"keybinds_file": "keybinds_conf.json",
			"themes_file": "theme_conf.json",
			"show_speed": False,
			"show_temperature": True,
			"show_time": True,
			"show_line_no": True,
			"show_fps": True,
			"show_keypress": True,
			"show_code_location": True,
			"show_buffer_name": True,
			"show_line_numbers": True,
			"highlight_line": False,
			"cursor_style": 2,
			"cursor_blink_time": 0,
			"cursor_border_width": 0,
			"selection_border_width": 0,
			"allow_external_modules": 1,
			"allow_notifications": 1,
			"alpha": 100,
			"percentage_pos_func": self.get_abs_percentage_pos,
			"line_numbers_expand": 0,
			"buffer_border_style": "ridge",
			"command_entry_border_style": "ridge",
			"command_out_border_style": "ridge",
			"find_border_style": "ridge",
			"suggest_widget_border_style" : "ridge",
			"buffer_tab_border_style": "ridge",
			"line_numbers_border_style": "ridge",
			"supress_keybind_warning": 1,
			"find_on_key": 1,
			"timezone": "GMT-8",
			"show_info": 1,
			"highlighting": 1,
			"alert_unsaved_quit": 1,
			"change_line_no": self.change_line_no_number,
			"time_pos": "up",
			"temperature_pos": "up",
			"line_no_pos": "up",			
		}
		```
- Some of the actual options can and probably are already changed in the `conf` file
- for the format of the `conf` refer below to [conf file](##conf)
- To list what the actual options do (I encourage you to try changing some of them to see what they do)
	- *If an option doesn't have the format specified(if it's a string("") or bool(1|0) or a function/constant(string but without the quotes) You can assume it's supposed to be a number*
	- `theme="name"` changes the default theme (for theme names refer to the documentation about themes or just look into `theme_conf.json` or use the theme command)
	- `tab_size` changes tab size (this editor is opinionated and doesn't allow using spaces instead of tabs because it's stupid for many reasons including accessability, file size, and generally why should you be able to force your formatting size onto me)
	- `orientate="up" | "down"` changes the way some widgets are orientated(up or down) (for example COMMAND_OUT can on the top or upper side of the screen instead of down)
	- `backup_files=1|0` whether to backup files(I am actually not sure about how that's done so probably do not use
	- `font_size` specify main font size (BUFFER font as well as some other widget font sizes)
	- `smaller_font_size` used for widgets mostly in the info_frame and buffer_tab_frame
	- `command_entry_font_size` override font size for COMMAND_ENTRY
	- `find_entry_font_size` override font size for FIND_ENTRY
	- `command_out_font_size` override font size for COMMAND_OUT
	- `suggest_widget_font_size` override font size for SUGGEST_WIDGET
	- `start_width` The width of the window when the application start measured in characters(of current font_size)
	- `start_height` The height of the window when the application start measured in characters(of current font_size)
	- `show_buffer_tab=1|0` Whether to show buffer_tab_frame (the list of file names on the upper side of the window)
	- `line_end=LF|CRLF|CR` Specify whether a line is supposed to end in LF(good) or CRLF(windows bad) CR(good ig although I don't know how well it plays with this editor)
	- `suggest=1|0` I don't think this does anything anymore (used to show completion options in COMMAND_OUT
	- 'font="font name"' Set the font name/family for the application (defaults to Consolas) (best refer to the list of fonts installed on your computer)
	- `default_find_mode="?"|"/"` set the default find mode `?` is for normal search `/` is for regex search (you can switch them out as you go in the find entry as the character is just there and you can delete it)
	- `default_split_mode="vertical"|"horizontal"` whether to split vertically or horizontally when using the split command (without specifying `split horizontal` or `split vertical`)
	- `show_info` whether to show info_frame(all widgets in it will be also hidden regardless of their respective options)
	- `show_speed=1|0` whether to show the widget in the info_frame (the one that changes a lot with KHz)
	- `show_temperature=1|0` whether to show the widget in the info_frame with temperature
	- `show_time=1|0` whether to show the widget in the info_frame with time
	- `show_line_no=1|0` whether to show the widget in the info_frame with current location(line number.column number)
	- `show_fps=1|0` I think this is the same `show_speed` and I am not sure which is currently really used
	- `show_keypress=1|0` whether to show the widget in the info_frame with keypressed(left corner)
	- `highlight_line=1|0` whether to highlight current line(I am not sure this works tbh)
	- `cursor_style=0|1|2|3`
		- cursor style 0 is a simple thin line
		- cursor style 1 is a simple block but the color of current character is default foreground color
		- cursor style 2 is a simple block but the color of current character is current foreground tag color
		- cursor style 3 highlights the whole line
	- `cursor_blink_time` how long the cursor should blink(0 turn blinking off)(specified in miliseconds)
	- `cursor_border_width` just change it and see what it does(measured in pixels so stay in range of 0 to around 10)
	- `selection_border_width` similar effect as `cursor_border_width` but for selection
	- `allow_external_modules` Whether to allow importing modules
	- `allow notifications` not in use anymore, but might return so I am keeping it there
	- `alpha` set window alpha/transparency (range of 0-100) (0 = completely transparent) (100 = completely opaque)
	- `percentage_pos_func=get_abs_percentage_pos` I don't think this works either anymore
	- border styles have options
		- "ridge"
		- "solid"
		- "flat"
		- "raised"
		- "sunken"
		- "groove"
	- `buffer_border_style="ridge"|"solid"|"flat"|"raised"|"sunken"|"groove"` set buffer border style
	- `command_entry_border_style="ridge"|"solid"|"flat"|"raised"|"sunken"|"groove"` set command_entry border style
	- `command_out_border_style="ridge"|"solid"|"flat"|"raised"|"sunken"|"groove"` set command_out border style
	- `find_border_style="ridge"|"solid"|"flat"|"raised"|"sunken"|"groove"` set find_entry border style
	- `suggest_widget_border_style="ridge"|"solid"|"flat"|"raised"|"sunken"|"groove"` set suggest_widget border style
	- `buffer_tab_border_style="ridge"|"solid"|"flat"|"raised"|"sunken"|"groove"` set buffer_tab_frame border style
	- `line_numbers_tab_border_style="ridge"|"solid"|"flat"|"raised"|"sunken"|"groove"` set line numbers(left) border style
	- `supress_keybind_warning=1|0` whether to print out keybind warnings and erros (refer to keybinds documentation)
	- `find_on_key` whether to search for text immediately upon key entry or wait untill after enter is pressed in the find_entry(look in the widget find_entry docs for more info about this)
	- `timezone` set timezone for time shown
	- `change_line_no=change_line_no_number|change_line_no_text` sets formatting of line_no widget in info_frame
		- change_line_no_numbers shows line and column numbers like [1.0][selection end line.selection end column]
		- change_line_no_text shows line and column numbers like line: 1 (+ selection end line) column: 1 (+ selection end column)
		- try it for yourself and see which you like better
	- `time_pos="up"|"down"` whether to show the time widget down or up (bottom or top)
	- `temperature_pos="up"|"down"` whether to show the temperature widget down or up (bottom or top)
	- `line_no_pos="up"|"down"` whether to show the line_no widget down or up (bottom or top)
	


## conf
- The conf file has a very simple format of just keyname=somevalue
- where value can be a number (also serves as a bool 1|0)
- a "string"
- or a constant/function(which should get automatically resolved if it exists in `main.py`)
- The options are as listed above
- look in the default `conf` file included for inspiration