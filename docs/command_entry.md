# PSEUDO COMMAND LINE

The COMMAND_ENTRY serves as a pseudo command line of sorts, it's supposed to be used mainly for editor commands, but one of the editor commands `sys` can be used to pipe commands into the terminal in which the editor was opened (through `python3 main.py [...]`) so you don't have to always switch to a terminal. This really only works for one-off commands/programs that don't require interactive input(as you cannot currently pipe input into running terminal programs (although it is possible)).

- (The underlying components in code are `COMMAND_ENTRY`, `PARSER`, `COMMAND_OUT`)

To get to the command_entry use `Control-space` (according to the default [keybinds](keybinds.md)
type `help` and press `enter` to show the list of available commands(which shows what they are called how they are used and what they do) so I wll not list them here

##What you should look out for:

- commands aren't really formatted or normalized in a way you might expect them to for example you cannot use `sys touch "this should be one file.txt"` as the `"this should be one file.txt"` part gets split into `this`, `should`, `be`, `one`, `file.txt` which will create these 5 files individually
- some of the editor commands are interactive (for example `theme` or `ls`, `buffers`), they will list a few options to choose from and you select the one you'd like by pressing `enter` when the cursor is on it. If you'd like to select more than one(which is not always necessarily possible in which case the last one you selected (the one you pressed `enter` on) will get used), press the left `Control` button, which will select the entry and will get processed once you press `enter`




