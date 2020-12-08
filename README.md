# Nix
Text editor made with python(3), tkinter and a bunch of other stuff

It can load and highlight a python file(~1200 lines) in an "instant". It takes around 0.5 seconds to highlight the whole file, but since it's multithreaded, there is no lag and the first few lines you see are highlighted very fast.

It's not a perfect text editor, but I think it's very usable. It has a syntax highlighter which supports Python, C/C++, Go, a bit of bash and a bit of html/css. It supports multiple opened files. It has themes (which you can change or even create your own).

to get to the command line press Control+Space (there are somewhat detailed descriptions for each command)

Control+C to copy, Control+V to paste, Control+X to cut, Control+Z to undo, Control+Y to redo, Control+A to select all

Control+Tab/Control+Shift+Tab to indent/unindent
Control+/ to comment line/selected text out

Control+L to make selected text lowercase Control+Shift+L to make selected text uppercase
Control-K to get length of selected text

Control-F for finding in text
Shift+Enter for compiling(if you have a Makefile created in your directory)

Control+S to save file, Control+Shift+S to save file as, Control+N to create new file

Control+Tab/Control+Shift+Tab to change between buffers/opened files
Control+, and Control+. to change font size
Control-W to close the window
Alt+Arrows to expand window
Alt+Shift+Arrows to shrink the window
Control+Alt to access menu at the top
F1 to ring the bell :)
F2 to insert current day, date and time
F11 to make window fullscreen

There are also some very dumb/esoteric features like a music player(requires pygame), window recorder(only for linux and requires ffmpeg), lyrics(requires bs4), scrapes current temperature in Stockholm(also requires bs4)
