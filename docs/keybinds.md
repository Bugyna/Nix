# Keybinds

## keybinds.json
- keybinds are stored in this file
- they are specified for each individual widget
- Keybind specifiers are formatted like <Modifier-Letter>
- Due to how tkinter works the keybinds cannot be very complex (so the most you can do is bundle modifiers-letter and then at most one letter)
	- eg. `<Control-Alt-b>w` which will only work if you hold `control` `alt` and `b` at the same time and then press `w`

- When changing keybinds do not delete or modify binds that are triggered by:
	- `<FocusIn>`
	- `<FocusOut>`
	- `<Enter>`
	- `<Configure>`
	- `<KeyPress>`
	- `<KeyRelease>`
- as these are generally internally used for correct working of the app


### How it works
- You bind a function to a key sequence
- functions are referenced to by their name in the code so it might not be exactly clear how they work or what they do I will try to list out what the general config does and how and you can try to change it from there on your own
- First of all the way you can bind functions is either
	- by it's name as followed `<Modifier-Key>: "function_name_in_quotes"`
	- or you can specify what arguments it should be called with like this:
		- `<Modifier-Key>: ["function_name_in_quotes", {"arg_name": "value"}]`
		- so if you know what you're doing you can for example bind keys to call commands you'd have to normally type into the `command_entry`
		- like this `"<Control-t>" : ["parent.command_parser.parse_argument, {"arg": "write_todo"}]`
		- which calls the command write_todo when you press Control-t


### Default keybinds

- In general you navigate normally with arrow(or mouse if you even use that)
- Mouse should go unused and with the exception of some older binds it doesn't have any role in this editor and you can use it without one

#### Default keybinds for window control
- To escape the window you can press either Control-Escape, or Control-W
- F11 to fullscreen
- F12 to hide(minimze) the window

#### Default keybinds for manipulating widgets and moving between them
- `Control-space` to open the command_entry
- `Control-.` (`Control-period`) to increase font size
- `Control-`, (`Control-comma`) to decrease font size
- `Control-MouseWheel` increase/decrease font size
- `Insert` change the way the cursor looks
- `Control-Tab` switch to next buffer
- `Control-Shift-Tab` switch to previous buffer


#### Text editing (should work for all text widgets (TEXT BUFFER, FIND_ENTRY, COMMAND_ENTRY, etc)
- `Control-Caps_Lock` change selected text to lowercase
- `Control-Shift-Caps_Lock` change selected text to uppercase
- `Control-'` (`Control-apostrophe`) enclose selected text with single quote characters `'`
- `Control-"` (`Control-quotebl`) enclose selected text with double quote characters `"`
- `Control-(` (`Control-parenleft`) enclose selected text with parenthesis `()`
- `Control-[` (`Control-bracketleft`) enclose selected text with brackets `[]`
- `Control-{` (`Control-braceleft`) enclose selected text with curly brackets `{}`
- `Control-Delete` Delete current (or next if on space or other delimeter) word
- `Control-Backspace` Delete current (or previous if on space or other delimeter) word
- `Control-D` Delete current (or next if on space or other delimeter) word
- `Control-Shift-D` Delete current (or previous if on space or other delimeter) word
- `Control-Shift-Delete` Delete part of line before cursor
- `Control-Shift-Backspace` Delete part of line after cursor
- `Alt-D` Delete current line

#### Various other
- `Control-~` (`Control-asciitilde`) inserts comment of current day time and date in a nice format

#### Other manipulation
- Control-K kill last process ran



### Widget specific default binds

#### FIND_ENTRY

- `Up` (up arrow) go to previous found match
- `Down` (down arrow) go to next found match
- `Shift-Up` go to previously search query(history)
- `Shift-Down` go to the next search query(if scrolled back in history with `Shift-Up`)
- `Escape` escapes from the widget and the buffer should stay at current match
- `Control-w` escapes from the widget and the buffer should go back to where you originally searched from

##### modes

- there is the find mode which is the default mode for searching
- find mode
	- `Enter` (`Return`) which searches for the query you typed in
	- `Control-R` which changes the mode to `replace`
- replace mode
	- `Enter` (`Return`) which replaces current match found with the thing you typed in the `FIND_ENTRY`
	- `Control-F` which changes the mode back to `find`
	- `Control-A-R` which replaces the current match and all the ones after it with what you typed

#### COMMAND_ENTRY

- `Up` go back in history
- `Down` go back from history
- `Shift-Enter` (`Shift-Return`) inserts new line
- `Enter` (`Return`) run the command

#### COMMAND_OUT

- When you type something in it shows up in a little box and according to what you type in the output is filtered
- If you wish to untype just press backspace (beware: instead of going back to the beggining of the output you stay at the line you scrolled to when filtered) (is there instead of search)
- You can move and select text normally and copy it, but the output should be immutable so you can't cut or delete anything
- `Escape` to exit
- `Control` (`Control_L`) (left control) to add current line to the selection
- `Enter` (`Return`) uses selection for whatever mode you are currently in (file explorer, jumping around lines from compilation output, etc.)
- `Control-|` (`Control-bar`) save current output as a buffer
- `Control-\` (`Control-backslash`) save current output as a compilation buffer



#### TEXT

- this is the main buffer widget where you edit all your code

##### buffer/file manipulation

- `Control-S` to save
- `Control-N` to create new file (with a filename you cant specify) (you should really use the `open` command in the command_entry though)
- `Control-B-W` to close current buffer (be careful `Control-W` closes whole window)
- `Control-B-Delete` deletes current buffer(in file system)
- `Control-\` (`Control-backslash`) moves into split view of buffers
- `Control-|` (`Control-bar`) unsplits buffers
- `Control-Q` toggle line wrap


##### manipulating other widgets

- `Control-E` shows last output from `COMMAND_OUT`
- `Alt-W` shows autocomplete options
- `Alt-E` show helper widget(currently doesn't do anything except show up)
- `Control-T` writes a todo checkbox at the start of the line (`[ ]`)
- `Control-F` Show FIND_ENTRY widget (is for searching)
- `Control-Shift-F` Show FIND_ENTRY widget and inputs curret token(word under cursor)
- `Control-G` Show COMMAND_OUT and works as a file explorer

##### Selections

- works as you'd expect you press shift and select stuff normally
- `Control-Shift-L` selects the current line
- `Control-A` selects all text
- `Control-C` to copy
- `Control-V` to paste
- `Control-Shift-C` to copy current token (the word currently under the cursor)
- `Control-X` to cut
- `Tab` to indent selection (if nothing is selected just inserts a tab)
- `Shift-Tab` to unindent selection
- `Control-/` (`Control-slash`) (un)comment (works like a toggle) line or selection
- `Control-Shift-/` (`Control-Shift-slash`) force comment line or selection
- `Alt-S` Change cursor with the other end of the selection
- `Alt-J` move line or selection down
- `Alt-K` move line or selection up

##### Undo/Redo

- `Control-Z` undo (even `Control-Shift-Z` does undo although you can rebind it)
- `Control-Y` redo

##### Other moving
- `Alt-M` jumps to an index ( you have two indexes or marks you can jump between) try it out can't really explain how it works
- `Alt-N` jumps to the last place you typed something in


##### Special stuff
- `Shift-Enter` (`Shift-Return`) either start compilation or run file(if it's python)
- `Control-Enter` (`Control-Return`) run project/file(usually the current python file or an executable file under the name of `main`)



### Structure
- The widget is specified and it you can specify individual bindings
- Modes can be specified
- for example in the `FIND_ENTRY`
```
"FIND_ENTRY":
	{
		"<Up>" : "scroll_through_found",
		"<Down>" : "scroll_through_found",
		"<Shift-Up>" : "scroll_through_find_history",
		"<Shift-Down>" : "scroll_through_find_history",
		"<Escape>" : "move_to_find_index",

		"<Control-W>" : "move_to_start_index",
		"<Control-w>" : "move_to_start_index",

		"<Control-Tab>" : "parent.buffer.switch_buffer_next",
		"<Control-ISO_Left_Tab>" : "parent.buffer.switch_buffer_next",
		"<Control-Shift-ISO_Left_Tab>" : "parent.buffer.switch_buffer_prev",
		"<Control-Shift-Tab>" : "parent.buffer.switch_buffer_prev",

		"find" :
		{
			"<Return>" : "find",
			"<KP_Enter>" : "find",
			"<Control-R>" : "mode_change",
			"<Control-r>" : "mode_change"
			
		},

		"replace" :
		{
			"<Return>" : "replace",
			"<KP_Enter>" : "replace",
			"<Control-F>" : "mode_change",
			"<Control-f>" : "mode_change",
			"<Control-A>R" : "replace_all",
			"<Control-a>r" : "replace_all"
		}
	},
```
- there are modes `find` and `replace` which are fairly obvious
- to add modes you would have to add a function to the widget which changes it's internal state (however I might add a general change mode/state function which can be used straight from keybinds)