# Nix
Text editor made with python(3), tkinter and a bunch of other stuff

It can load and highlight a python file(~1200 lines) in an "instant". It takes around 0.5 seconds to highlight the whole file, but since it's multithreaded, there is no lag and the first few lines you see are highlighted very fast.

It's not a perfect text editor, but I think it's very usable. It has a syntax highlighter which supports Python, C/C++, Go, a bit of bash and a bit of html/css. It supports multiple opened files. It has themes (which you can change or even create your own).

to get to the command line press Control+Space (there are somewhat detailed descriptions for each command)

## Keybindings

| Function | Keybinding | Description |
| ------- | ---------- | ----------- |
| Access commands | Control+Space | Opens built-in "console" |
| Copy | Control+C | Copies selection |
| Paste| Control+V | Pastes clipboard |
| Cut | Control+X | Cuts selection |
| Undo | Control+Z | Undo |
| Redo | Control+Y | Redo |
| Select all| Control+A | selects all text in opened buffer |
| Indent | Control+Tab | Indents line or all lines in selection |
| Unindent | Control+Shift+Tab | Unindents line or all lines in selection |
| Comment | Control+/ | Comments out a line or all lines in selection |
| Change case | Control+L | Makes selected text lowercase |
| Change case | Control+Shift+L | Makes selected text uppercase |
| Enclose selected text | Control+'/"/(/[/{ | | Encloses selected text with character |
| Get length | Control+K | Gets length of selected text |
| Find | Control+F | Finding in text |
| Make | Shift+Enter | Runs/Compiles(needs a Makefile) current file |
| Save | Control+S | Saves file |
| Save as| Control+Shift+S | Saves file as |
| New file | Control+N | Creates new file |
| Load file | Control+B+L | Loads a file |
| Switch buffer | Control+Tab | Switches to next opened buffer |
| Switch buffer | Control+Shift+Tab | Switches to previous opened buffer |
| Change font size | Control+, | Makes font smaller |
| Change font size | and Control+. | Makes font larger |
| Change font size | Control+MouseWheel | Changes font size |
| Close window | Control+w | Closes window |
| Close buffer | Control+b+w | Closes opened buffer (if there is only the scratch buffer left it closes the whole window) |
| Change window size | Alt+Arrows | Makes window bigger |
| Change window size | Alt+Shift+Arrows | Makes window smaller |
| Acess menubar | Control+Alt | Switches focus to menubar |
| Bell | F1 | Rings the bell :) |
| Insert time | F2 | Inserts current day, date and time |
| Screenshot | F3 | Takes a screenshot of the window |
| Fullscreen | F11 | Makes window fullscreen |

There are also some very dumb/esoteric features like a music player(requires pygame), window recorder(only for linux and requires ffmpeg), lyrics(requires bs4), scrapes current temperature in Stockholm(also requires bs4)
