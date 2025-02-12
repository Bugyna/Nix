

# WIN



```
                                      --this is not UML--

                                                              ┌──────────────────┐                     
                                               ┌──────────────┤    FIND_ENTRY    ├──────┐              
                                               │              │                  │      │              
                                               │              └──────────────────┘      │              
      ┌──────────────────┐                     │                                        │              
      │                  │ component of        │              ┌──────────────────┐      │              
      │      PARSER      ├───────────┐         ├──────────────┤   COMMAND_OUT    ├──────┤              
      │(manages commands)│           │         │              │                  │      │              
      └──────────────────┘           │    components of       └──────────────────┘      │              
                                     │         │                                        │              
                                     │         │              ┌──────────────────┐      │              
                                     │         ├──────────────┤  COMMAND_ENTRY   │      │              
                                     │         │              │                  │      │              
   component of                  ┌───▼─────────▼─────────┐    └─────────┬────────┘      │              
┌────────────────────────────────►                       │              │               │              
│                            ┌───┤          WIN          ◄───┐          │               │              
│                            │   │                       │   │   tkinter│parent         │              
│                            │   └───────────────────────┘   │          │        tkinter│parent        
│                     tkinter│parent                  tkinter│parent    │  ┌────────────┘              
│                            │                               │          │  │                           
│          ┌─────────────────┴─┐                         ┌───┴──────────▼──▼                           
│          │                   │                         │                 │                           
│          │ .buffer_tab_frame │                         │  .buffer_frame  │                           
│          │                   │                         │                 │                           
│          └───────────────────▲                         ▲─────────────────┘                           
│                              │                         │                                             
│                       tkinter│parent            tkinter│parent                                       
│                              │                         │                                             
│                    ┌─────────┴─────────┐        ┌──────┴─────────────┐                               
│                    │                   │        │                    │                               
│                    │   BUFFER_TAB(s)   ◄────┬───►       TEXT(s)      ◄────┐                          
│                    │                   │    │   │                    │    │component─of─────────────┐
│                    └───────────────────┘    │   └────────────────────┘    └────────┤                │
│                                             │                                      │     LEXER      │
│                                             │                                      │                │
│                                   COUPLED IN│FILE_HANDLER.buffer_dict              └────────────────┘
│                                             │                                                        
│                                    ┌────────┴──────────┐                                             
│                                    │                   │                                             
└────────────────────────────────────┤   FILE_HANDLER    │                                             
                                     │                   │                                             
                                     └───────────────────┘                                                                               
```

Widgets were explained in [widgets](widgets.md) (so read that first if you wish to understand the architecture of the applicaiton as it also explains the basic logical structure of widgets and how they communicate)
So we'll go over other individual important parts that are not widgets

- by the way there is a semantic difference between `BUFFER` and buffer. `BUFFER` is a custom widget class in `src/widgets.py`, while a (file) buffer is an instance of `BUFFER` or the `TEXT` which is an extension of `BUFFER`. What that means is that when reffering to buffers you should imagine the `TEXT` buffer opened in the application where you can edit the contents of an opened file basically.


## STARTUP FLOW

When the app is started the `tkinter.Tk` application is created along with the main window. The window is then configured and widgets are added accordingly. Config file and theme file are also loaded along with the keybinds, which are actually only bound when a custom widget is being created.
The window and it's widgets are configured through the `WIN.theme_load`, `WIN.font_set`.

Helper objects are also created: `FILE_HANDLER`, `PARSER`(you can read about them in this file)
A scratch buffer is created through the `FILE_HANDLER`, which is technically not necessary, but makes the workflow a lot nicer as most keybinds are bound to buffers and not to the main window(so if you close the scratch buffer along with all other opened buffers, you might for example find out that you cannot close the application through `Control-w` as you might be used to)

Along with that modules/plugins are loaded(read [plugins](plugins.md))

After all this the widgets are placed through the `WIN.reposition_widgets` function, which places the widgets to where they should be. Similar to `WIN.theme_load` some custom widgets have their own logic for placing themeselves which is located in their respective `place_self` functions.

At the end of the `WIN.__init__` function the application opens buffers according to the arguments passed through the command line in which you open the app.

### `WIN.theme_load`

`theme_load` is a function which configures the window and widgets according to the current theme set. Custom widgets are configured through their `configure_self` functions, while other basic widgets are configured directly. It calls another important function called `WIN.theme_make` which configures `TEXT` buffers and other important custom widgets(`COMMAND_ENTRY`, `COMMAND_OUT`, `SUGGEST`, note: it is not entirely neccessary to configure these as well, but it looks nicer that way) and creates `tkinter.Tag`s in them according to the `highlighter` part of the theme. `tkinter.Tag`s are important for highlighting text.

### `WIN.font_set`

loads and creates proper `tkinter.Font`s for use in the application. This function will also try to call `WIN.theme_load`, to configure the widgets with the proper font as well as to modify the tags, which can use custom fonts. This function also gets called if the font size changes in `TEXT` buffers, which is necessary because of `tkinter.Tag`s.


### `WIN.reposition_widgets`

places all the widgets in the application window, if they are configured to show(some widgets can be configured to now actually be placed or be placed differently, see [the config file docs](conf.md))
Some widgets(mostly ones that have a simple placing mechanism, for example `BUFFER_TAB`s)  have their own placing logic located in their respecitve `place_self` functions. The `TEXT` (and other file buffers) are placed according to functions stored in the `WIN` class. That happens because you can place buffers in a split view, which is managed by `WIN.nosplit`, `WIN.split`, `WIN.split_vertical`, `WIN.split_horizontal`. The placing functions for `COMMAND_OUT`, `COMMAND_ENTRY`, `FIND_ENTRY`, `SUGGEST` are also in the `WIN` class, which is mostly because they do extra stuff other than just place themselves.

#### `WIN.nosplit`

places the focused buffer in a simple nosplit view

#### `WIN.split`

places the buffers stored in the `WIN.buffer_render_list` according to the `default_split_mode` option in the `conf` file, which can be either `WIN.split_vertical` or `WIN.split_horizontal` (or something else if you have created a new splitting function or if one was imported in a plugin)



## APPLICATION FLOW AFTER INITIALIZATION

most background logic happens in `WIN` because it is the main `tkinter.Tk` application which manages everything, but we do not concern ourselves with that because we're simple library users. Most of the explicit logic which you might need to know about located in `WIN` are the update functions. I'll skip the unimportant ones like the ones that update the shown time and similar.


### `WIN.update_index`

Is a function which updates the line number and the column of the typing cursor, depending on where you are in the buffer. Should be called everytime you move the typing cursor(which you should keep in mind if you wish to create plugins. It is also responsible for updating the line numbers(the ones on the left if you've configured to have them shown).

### `WIN.update_buffer`

is a function which is supposed to get called every single time a key is released in a buffer. It is responsible for updating the status of the buffer
- if it is unsaved the `*` gets shown in the corresponding `BUFFER_TAB`
- if it has been modified outside of the editor the `!`symbol gets shown in the corresponding `BUFFER_TAB`

it is also responsible for highlighting the current line(it is a bit wasteful to lex and highlight the whole file on every key release so we only do it on the line)
- Note: lexing on the whole file gets called when a chunk bigger than one line gets edited(so for example when commenting, uncommenting a selection) and most notably when the `TEXT.keep_indent` function is called, which according to the default keybindings get called when you press enter.


## LEXER

is mostly explained in [docs/highlighting.md](highlighting.md), but generally what happens is
a part (or the whole content) of a `TEXT` buffer gets passed into it's lexer(every `TEXT` buffer has a lexer) `LEXER.lex` function, which is mostly useful for highlighting the part of the content passed into it with the `tkinter.Tag`s defined earlier.



## FILE_HANDLER

`handlers.py` `FILE_HANDLER`
`WIN.file_handler` is responsbile for handling `BUFFER`s and `BUFFER_TAB`s as well as creating them, loading them and generally managing their existence, `BUFFER`s specifically `TEXT`s are tied to files so `WIN.file_handler` is also responsible for opening, creating, deleting files. So anything pertaining to files (except for commands) should be located there


## COMMAND_PARSER

`command_parser.py`, `PARSER`
`WIN.parser` is responsible for managing and executing commands inputted through `WIN.command_entry`.
All commands should be there.
What happens generally is a command goes through `WIN.command_entry` -> `WIN.parser.parse_argument(arg=[input command])`
Which parses the command splits it into command and it's arguments and looks up the command in `PARSER.commands` and passes the arguments into the corresponding function (if there is one)


## util.py

has various util functions, but mostly used for the `bind_keys`, `bind_keys_from_conf` functions which are used for parsing the `keybinds.json` and binding the actual keybinds to their respective widgets


### UNDOCUMENTED CLASSES ARE MOSTLY UNUSED OR ARE NOT NECESSARY TO UNDERSTAND HOW THE APPLICATION WORKS