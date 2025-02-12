# WIN, tkinter

`WIN` located in `src/main.py` is the main application class and inherits the `tkinter.Tk` application class
which basically means it's the main window of the application in which everything happens. It contains all of the application logic as well as a hierarchical layout for how it manages it's components called `widget`s, if these widgets have the `WIN` as their parent, they are WIN's children from the point of WIN. It doesn't mean they inherit anything, but that they are hierarchically contained inside the WIN.

We shall call this hierarchy the 'tkinter hierarchy', because we have a slightly different logical hierarchy for how the custom widgets communicate.

overview:
```
                      ┌──────────────────┐                  
                      │                  │                  
                      │       WIN        │                  
           ┌──────────┤                  ├─────────┐        
           │          └───────┬──────────┘         │        
           │                  │                    │        
           │                  │                    │        
           │                  │                    │        
           │                  │                    │        
┌──────────┴─────┐   ┌────────┴───────┐   ┌────────┴───────┐
│                │   │                │   │                │
│     child0     │   │     child1     │   │     child2     │
│                │   │                │   │                │
└────────────────┘   └────────────────┘   └────────────────┘
```

Each widget can also be a parent of ofther widgets, some widgets in tkinter are defined exactly to be a simple container for other widgets and do not really have other behaviour defined(except for the standard behaviour defined in the base widget class)

example:
```
                               ┌──────────────────┐                  
                               │                  │                  
                               │  tkinter.Frame   │                           
                    ┌──────────┤                  ├─────────┐        
                    │          │                  │         │        
                    │          └───────┬──────────┘         │        
                    │                  │                    │        
                    │                  │                    │        
                    │                  │                    │        
                    │                  │                    │        
         ┌──────────┴─────┐   ┌────────┴───────┐   ┌────────┴───────┐
         │                │   │                │   │                │
         │ tkinter.Canvas │   │  tkinter.Label │   │  tkinter.Text  │
         │                │   │                │   │                │
         └──┬────────┬────┘   └────────────────┘   └────────────────┘
            │        │                                               
            │        │                                               
            │        │                                               
┌───────────┴─┐   ┌──┴──────────┐                                    
│tkinter.Label│   │tkinter.Label│                                                    
│             │   │             │                                                                        
└─────────────┘   └─────────────┘                                    
```

##### If one widget is a child of some parent, it cannot be displayed(placed/shown) inside any other parent of the same level. 

example:
```
                               ┌──────────────────┐                  
                               │                  │                  
                               │  tkinter.Frame   │                           
                    ┌──────────┤                  ├─────────┐        
                    │          │                  │         │        
                    │          └───────┬──────────┘         │        
                    │                  │                    │        
                    │                  │                    │        
                    │                  │                    │        
                    │                  │                    │        
         ┌──────────┴─────┐   ┌────────┴───────┐   ┌────────┴───────┐
         │                │   │                │   │                │
         │ tkinter.Frame  │   │  tkinter.Frame │   │  tkinter.Text  │
         │       D        │   │        F       │   │                │
         └──┬────────┬────┘   └────────────────┘   └────────────────┘
            │        │                                               
            │        │                                               
            │        │                                               
┌───────────┴─┐   ┌──┴──────────┐                                    
│tkinter.Label│   │tkinter.Label│                                                    
│      A      │   │      B      │                                                                        
└─────────────┘   └─────────────┘                                    
```

in this example you cannot place any of D's children inside F.



# widgets.py

In this file we define custom widgets that are more specialized for their respective purposes, for example the `TEXT` class is built on top of `tkinter.Text` to provide more text editing options you'd normally want from a text editor for programmers.

They have their respective hierarchies(which widgets are shown in which containers) which can be seen on the diagrams below.

WIN and it's base containers in which basically all other widgets should go.
```
                 ┌─────────────────┐                      
                 │                 │                      
                 │       WIN       │                      
        ┌────────┤                 ├────────┐             
        │        │                 │        │             
        │        └────────┬────────┘        │             
        │                 │                 │             
        │                 │                 │             
        │                 │                 │             
┌───────┴───────┐  ┌──────┴──────┐  ┌───────┴────────────┐
│               │  │             │  │                    │
│ .buffer_frame │  │ .info_frame │  │ .buffer_tab_frame  │
│               │  │             │  │                    │
└───────────────┘  └─────────────┘  └────────────────────┘
```

`WIN.info_frame` is a base `tkinter.Frame` object in which other basic tkinter objects go. It's used for showing arbitrary text information, for example line and column number of where you are currently in an opened buffer, information about current time, which key(s) were pressed last etc.


`WIN.buffer_frame` is a base `tkinter.Frame` object in which most of our custom widgets go, it's mostly meant, as the name suggests, for buffers, which mostly means objects where you edit text, but other specialized BUFFERs can exist as long as they define the base behaviour which every specialized buffer in `WIN.buffer_frame` should have(which is defined in `widgets.BUFFER` so you can just inherit it)

`WIN.buffer_tab_frame` is a base `tkinter.Frame` object in which we store the custom widgets `BUFFER_TAB`, the BUFFER_TAB is for coupled with opened buffers to show it's name and status(`*` for modified and not saved, `!` when the file is modified outside of the editor)


## WIN.info_frame

- the part on the top of the window where time, temperature, and line number is shown
- it is a simple `tkinter.Frame`
- children are various widgets(labels) mostly showing information like time, position in opened text buffer, etc.

## WIN.buffer_tab_frame

- the part on the top of the window where individual buffer/file names are shown (under the info_frame)
- it is a simple `tkinter.Frame`
- children are BUFFER_TAB from `widgets.py`
- can be hidden
	- add `show_buffer_tab=0` to the `conf` file

## WIN.buffer_frame

- it is a simple `tkinter.Frame`
- children are `BUFFER`s (and it's subclasses `TEXT`s etc.) from `widgets.py`






### general info for custom extension of tkinter widgets below

- each class defintion which is an extension of tkinter widgets need to have a method called `configure_self`, which is responsible for configuring the visuals according to the loaded theme as well as setting correct fonts etc.
- refer to `configure` methods in tkinter widgets
- each class defintion needs to have `self.parent` configured to be the instance of the `WIN` application class, however when calling super().__init__ you can pass a different tkinter parent so you can set the tkinter hierarchy to be whatever you want, but each widget should have the `WIN` instance easily available, for easy inter-widget communication.
- generally many classes also have a place_self, unplace_self methods which are responsible for proper positioning(usually pertains to widgets that are placed in the same tkinter container/`Frame`. So things like `BUFFER_TAB`s and `BUFFER`s (and it's subclasses)


## BUFFER_TAB

- extension of `tkinter.Label`
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

- base class for all (file) buffers that can be opened(defines base operations like switching between opened buffers etc.) that are necessary in every BUFFER
- is an extension of `tkinter.Frame`
- `BUFFER` is a sort of default custom widget
- `BUFFER`s should be placed in the `WIN.buffer_frame`


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


## SUGGEST_WIDGET
- inherits `DEFAULT_TEXT_BUFFER`
- defines a simple widget which receives a bunch of words to choose from, display each on a separate line, and writes it out once you press `enter`(or whatever you bind it to) into the `TEXT` buffer in which you are currently editing


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

