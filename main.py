import tkinter
from tkinter import ttk
from tkinter import font
import random
import keyboard
import re
import threading
import os, sys
import tqdm
from itertools import chain
from time import sleep
from tkinter import filedialog


keywords = [
    'False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in',
     'raise', 'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for',
      'lambda', 'try', 'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del',
       'global', 'not', 'with', 'async', 'elif', 'if', 'or', 'yield'
       ]

#keywords = ['auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while']
sumn = ['self']
var_types = ['int','float','string','str']
other_chars = ["$","#","@","&","|","^","_",r"\ ".split()]
special_chars = ['"',"'",")","(","[","]","{","}"]
operators = ["<",'>',"+","-","*","=","/","%"]
nums = ['0','1','2','3','4','5','6','7','8','9']
modules = []
modules2 = []
all_key = [keywords, sumn, var_types, modules, operators, other_chars]
all_key = list(chain.from_iterable(all_key))
#print(all_key)

#print(chr(9619))

for i in tqdm.tqdm(range(10)):
   sleep(0.01)

class CustomText(tkinter.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tkinter.Text.__init__(self, *args, **kwargs)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''

        start = self.index(start)
        end = self.index(end)
        indexu = "{}.{}".format(int(self.index(tkinter.INSERT).split(".")[0]), int(self.index(tkinter.INSERT).split(".")[1])-1)
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit",indexu)

        count = tkinter.StringVar()
        while True:
            print(indexu)
            index = self.search(pattern, "1.0", stopindex="end",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            #print(count.get())
            if index:
                self.mark_set("matchStart", index)
                self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
                self.tag_add(tag, "matchStart", "matchEnd")



class win():
    def __init__(self, root, file=None):

        #self.background_color = "#000000"
        #self.foreground_color = "#9F005F"
        self.theme_options = {
            "cake": ["#000000", "#9F005F", "other_chars", "var_types", "special_chars"],
            "toast": ["#000000", "#9F005F", "special_chars", "modules", "special_chars"]
            }
        self.theme = self.theme_options["cake"]
        print(self.theme)

        self.command_definition = {
            "l" : "-get: gets last line number || -[LINE_NUMBER(.CHARACTER)]: puts you to line number (eg. 120(by default starts at column 0 but you can specify the column like: 120.5)",
            "highlighting" : "-on: turns highlighting on -off: turns highlighting off"
        }

        self.command_input_history = []
        self.command_input_history_index = 0

        self.current_file = None #open(f"{os.getcwd()}/untitled.txt", "w+") #stores path to currently opened file
        self.current_file_name = None
        try:
            self.current_file_name = sys.argv[1]
        except IndexError:
            pass

        self.line_count = None
        
        self.highlighting = True # turned off by default because it's not working properly (fucking regex)
        self.loading = False
        self.fullscreen = False
        self.run = True

        #configuring main window
        #root.overrideredirect(True)
        root.resizable(True,True)
        root.config(bg=self.theme[0])
        root.geometry("600x400")
        #root.minsize(width=200, height=200)
        self.title_bar = tkinter.Frame(bg="blue", relief='raised', bd=2)
        root.title(f"N Editor: <None>") #{os.path.basename(self.current_file.name)}
        root.font = font.Font(family="Px437 IBM CGA", size=9, weight="bold")
        root.smaller_font = font.Font(family="Px437 IBM CGA", size=7, weight="bold")
        #root.overrideredirect(True)
        root.resizable(1, 1)
        #prints all fonts you have installed
        #fonts = list(font.families())
        #for item in fonts:
        #    print(item)

        #configuring fonts
        self.font = font.Font(family="Px437 IBM CGA", size=9, weight="bold")
        self.smaller_font = font.Font(family="Px437 IBM CGA", size=7, weight="bold")
        # self.font = font.Font(family="Comic Sans", size=9, weight="bold")
        # self.smaller_font = font.Font(family="Comic Sans", size=7, weight="bold")

        #filediaolog pretty much self-explanatory
        self.filename = filedialog

        #text widget configuration
        self.txt = CustomText()

        #self.txt.grid(row=0, column=0 ,sticky="nsew")
        self.txt.configure(font=self.font,bg = self.theme[0],fg=self.theme[1], undo=True, spacing1=5,
            insertwidth=8, insertofftime=0, insertbackground="#A2000A", selectbackground="#0A00A2",
            borderwidth=0, relief="sunken", tabs=("1c"), wrap="word")
        self.txt.place(x=0,y=20,relwidth=0.985, relheight=0.9, anchor="nw")
            
        #scrollbar configuration
        # self.scrollb = tkinter.Scrollbar(root, command=self.txt.yview, relief="flat") #self.scrollb.grid(row=0,column=2,sticky="nsew")
        # self.scrollb.place(relx=0.985, rely=0.0, relwidth=0.15, relheight=.95)
        # self.txt['yscrollcommand'] = self.scrollb.set

        #line and column number label
        self.line_no = tkinter.Label(text="aaa",fill=None ,justify=tkinter.RIGHT, font=self.font,bg = self.theme[0],fg="#999999") #self.line_no.grid(row=1,column=2)
        self.line_no.place(relx=0.75, rely=0.99, height=15, anchor="sw")
        
        
        #command line entry
        self.command_entry = tkinter.Entry(text="aa", justify=tkinter.LEFT, font=self.font,
        bg = self.theme[0],fg="#999999", insertwidth=8, insertofftime=500, insertbackground="#fb2e01", relief="flat")
        #self.command_entry.grid(row=1,column=0,ipady=3);
        self.command_entry.place(x=0.0,rely=0.99, relwidth=0.25, height=15, anchor="sw")


        #command output
        self.command_out = tkinter.Label(font=self.smaller_font, text="biog bruh", bg=self.theme[0], fg="#00df00",
         justify=tkinter.CENTER, anchor="w")
        self.command_out.place(relx=0.28,rely=0.99, relwidth=0.25, height=15, anchor="sw")

        #progressbar
        #self.progress_bar = p_bar(root) #.grid(row=1,column=1)
        #self.style=ttk.Style()
        #self.style.theme_use("clam")
        #self.style.configure("color.Horizontal.TProgressbar", foreground="white", background="white")
        #self.progress_bar = ttk.Progressbar(orient=tkinter.HORIZONTAL, style="color.Horizontal.TProgressbar",
        # length=100, mode='determinate')
        #self.progress_bar.place(relx=0.35,rely=0.975,relwidth=0.3,relheight=0.025)

        #right click pop-up menu
        self.right_click_menu = tkinter.Menu(tearoff=0, font=self.smaller_font, bg=self.theme[0], fg="#ffffff")
        self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
        self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
        self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
        self.right_click_menu.add_separator()

        #menubar
        #self.menubar = tkinter.Menu(root, font=self.font, bg="black") #declare menubar
        #self.menubar.configure(font=self.font, bg="black") #configure font and background

        #self.menubar_button = tkinter.Button(root, text="File" ,font=self.font, bg=self.background_color, fg=self.foreground_color, command=self.popup).place(relx=0,rely=0,relwidth=0.05)

        self.menubar_label_file = tkinter.Label(root, text="File" ,font=self.font, bg=self.theme[0], fg="#999999")
        self.separator_label_file = tkinter.Label(root, text="----" ,font=self.font, bg=self.theme[0], fg="#999999").place(x=0, y=15, height=2, anchor="nw")
        self.menubar_label_file.bind("<Button-1>", self.file_menu_popup)
        self.menubar_label_file.place(x=0, y=0, anchor="nw")

        self.menubar_label_settings = tkinter.Label(root, text="Settings" ,font=self.font, bg=self.theme[0], fg="#999999")
        self.separator_label_settings = tkinter.Label(root, text="--------" ,font=self.font, bg=self.theme[0], fg="#999999").place(x=60, y=15, height=2, anchor="nw")
        self.menubar_label_settings.bind("<Button-1>", self.file_menu_popup)
        self.menubar_label_settings.place(x=60, y=0, anchor="nw")


        #dropdown for menubar
        self.file_dropdown = tkinter.Menu(font=self.font, tearoff=False,fg="#FFFFFF", bg=self.theme[0]) #declare dropdown
        self.file_dropdown.add_command(label="New file",command=self.new_file) #add commands
        self.file_dropdown.add_command(label="Open file",command=self.load_file)
        self.file_dropdown.add_command(label="Save file",command=self.save_file)
        self.file_dropdown.add_command(label="Save file as",command=self.save_file_as)
        #self.menubar.add_cascade(label="File",menu=self.file_dropdown) #add dropdown to menubar
        #self.file_dropdown.add_separator()
        #self.file_dropdown.add_command(label="EXIT")

        #root.config(menu=self.menubar)#adds menubar to main window

        #tags for highlighting
        self.txt.tag_configure("sumn", foreground="#74091D")
        self.txt.tag_configure("special_chars",foreground="#ff00bb")
        self.txt.tag_configure("var_types",foreground="#01cdfe")
        self.txt.tag_configure("operators",foreground="#05ffa1")
        self.txt.tag_configure("keywords", foreground="#ff5500")
        self.txt.tag_configure("modules", foreground="#f75f00")
        self.txt.tag_configure("default", foreground="#302387")
        self.txt.tag_configure("other_chars", foreground="#302387")

        #command binding
        self.command_entry.bind("<Return>", self.cmmand) #if you press enter in command line it executes the command and switches you back to text widget
        self.command_entry.bind("<Up>", self.command_history) # lets you scroll through commands you have already used
        self.command_entry.bind("<Down>", self.command_history)
        self.txt.bind("<Button-3>", self.popup) #right click pop-up window
        root.bind("<F11>", self.set_fullscreen)
        root.bind("<Alt-Right>", self.set_dimensions)
        root.bind("<Alt-Left>", self.set_dimensions)
        root.bind("<Alt-Up>", self.set_dimensions)
        root.bind("<Alt-Down>", self.set_dimensions)
        #self.txt.bind("<Tab>", self.cmmand)
        #self.txt.bind("<Control_L><k>", self.cmmand)

        #self.checked = [] #checked lines (for syntax highlighting optimization not yet added)
        #self.keys = [] #no idea 



        self.a=""
        if self.current_file_name:
            self.load_file()


        self.loading_label_background = tkinter.Label(root, bg="#999999", fg="#FFFFFF")
        self.loading_label_background.place(relx=0.5,rely=0.8, relwidth=0.205 ,relheight=0.015)
        self.loading_label = tkinter.Label(root, text="", bg=self.theme[0], fg="#FFFFFF")
        self.loading_label.place(relx=0.5,rely=0.8, relheight=0.015)


    def loading_widg(self):
        self.a += chr(9608)
        if len(self.a) < 11:
            print(len(self.a))
            sleep(0.1)
            self.loading_label.configure(text=self.a)
        
        else:
            print("aa")
            self.loading = False
            self.a = ""
            sleep(0.1)
            self.loading_label.configure(text=self.a)

    def get_line_count(self):
        """ returns total amount of lines in opened text """
        self.info = self.txt.get("1.0", "end-1c")
        return sum(1 for line in self.info.split("\n"))

    def error_win(self, e):
        """ set up error window """
        error_win = tkinter.Tk("aaa")
        error_win.configure(bg="#000000", bd=2)
        #error_win.geometry("600x200")
        error_win.title(f"Error Window")
        error_label = tkinter.Label(error_win, text=f"Error: {e}", justify=tkinter.CENTER, bg="#000000", fg="#ffffff"); error_label.pack()
        error_button = tkinter.Button(error_win, text="OK", command=error_win.destroy, bg="#000000", fg="#ffffff"); error_button.pack()
        #error_label.place(relx=0.0, rely=0.10, relwidth=1, relheight=0.20)
        #error_button.place(relx=0.25, rely=0.25, relwidth=0.35, relheight=0.26)

    def help_win(self, command=None):
        """ set up help window """
        help_win = tkinter.Tk("aaa")
        help_win.configure(bg="#000000")
        help_win.title(f"Help Window")
        if (command == None):
            help_label = tkinter.Label(help_win, text=f"Commands: \n l -options: get || [ LINE_NUMBER(.CHARACTER) ] (eg. 120 or 120.5)  \n highlighting -options: on || off \n", bg="#000000", fg="#ffffff", justify=tkinter.LEFT).pack()
        elif (command != None):
            help_label = tkinter.Label(help_win, text=f"{command}: {self.command_definition[command]}", bg="#000000", fg="#ffffff", justify=tkinter.LEFT).pack()
        #-puts you to line number (eg. 120(by default starts at column 0 but you can specify the column like: 120.5)

    #binded functions

    def set_fullscreen(self, arg):
        self.fullscreen = not self.fullscreen
        root.attributes("-fullscreen", self.fullscreen)

    def set_dimensions(self, arg):
        key = arg.keysym
        margin = 20
        if (key == "Right"):
            root.geometry(f"{root.winfo_width()+margin}x{root.winfo_height()}")
        if (key == "Left"):
            root.geometry(f"{root.winfo_width()-margin}x{root.winfo_height()}")
        if (key == "Up"):
            root.geometry(f"{root.winfo_width()}x{root.winfo_height()-margin}")
        if (key == "Down"):
            root.geometry(f"{root.winfo_width()}x{root.winfo_height()+margin}")

    def popup(self, arg):
        """ gets x, y position of mouse click """
        self.right_click_menu.tk_popup(arg.x_root+50, arg.y_root-50, 0)
        self.right_click_menu.grab_release()

    def file_menu_popup(self, arg):
        self.file_dropdown.tk_popup(arg.x_root+75, arg.y_root+25, 0)
        self.right_click_menu.grab_release()

    def command_history(self, arg):
        """ scroll through used commands with Up and Down arrows(?) """
        self.command_entry.delete(0, "end")
        try:
            if (arg.keysym == "Up"):
                self.command_input_history_index += 1
            else:
                self.command_input_history_index -= 1
            
            if (self.command_input_history_index <= 0):
                self.command_input_history_index = len(self.command_input_history)+1

            elif (self.command_input_history_index > len(self.command_input_history)):
                self.command_input_history_index = len(self.command_input_history)

            last_command = self.command_input_history[-self.command_input_history_index]
            self.command_entry.insert(0, last_command)

            #print(self.command_input_history_index)

        except IndexError:
            #print(self.command_input_history_index)
            self.command_input_history_index = 0
            self.command_entry.delete(0, "end")

    def command_O(self, arg):
        """ sets the text in command output"""
        #(I have no idea why past me made this into a function when it doesn't really have to be a function)
        self.command_out.configure(text=str(arg))

    def cmmand(self, arg):
        """ parses command(case insensitive) from command line and executes it"""
        self.command_input_history_index = 0
        command = self.command_entry.get().lower().split()#turns command into a list and turns it all into lowercase chars

        #help command
        if (command[0] == "help"):
            try:
                if (command[1] != None):
                    self.help_win(command[1])
            except IndexError:
                self.help_win()

        #highlighting command
        elif (command[0] == "highlighting"):
            #print("aaa")
            if (command[1] == "on"):
                self.command_O("highlighting on")
                self.highlight_all()
                self.highlighting = True
            elif (command[1] == "off"):
                self.command_O("highlighting off")
                self.highlighting = False

        #line/ line and column command        
        elif (command[0][0] == "l"):
            argument = command[0][2:]
            if (re.search("[0-9]", argument)):
                self.command_O(f"moved to: {float(argument)}")
                self.txt.mark_set("insert", float(argument))

            elif (re.search("get", argument)):
                self.command_O(f"total lines: {self.get_line_count()}")

        elif (command[0] == "quit"):
            self.run = False

        elif (command[0] == "save"):
            self.save_file()
            self.loading = True

        elif (command[0] == "open"):
            self.load_file(filename=command[1])
            #self.command_O(f"file saved")
        
        elif (command[0] == "theme"):
            self.theme = self.theme_options[command[1]]


        #append command to command history
        self.command_input_history.append(command)

        #sets focus back to text widget
        self.txt.focus_set()
        keyboard.press_and_release("enter+backspace")
        self.command_entry.delete(0, "end") #deletes command line input

        #set command history to newest index
        self.command_input_history_index = 0

    #menubar functions
    def new_file(self):
        try:
            self.current_file_name = f"{os.getcwd()}/untitled.txt"
            self.current_file = open(self.current_file_name, "w+")
            root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
        except Exception as e:
            self.current_file.close()
            self.error_win(e)

    def save_file(self):
        """ saves current text into opened file """
        content = str(self.txt.get("1.0", "end-1c"))
        
        # try:
        #     self.current_file = open(f"{os.getcwd()}/untitled.txt", "w+")
        #     root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
        # except:
        #     pass
        
        try:
            self.current_file = open(self.current_file_name, "w")
            self.current_file.write(content)
            self.current_file.close()
            self.command_O(f"total of {self.get_line_count()} lines saved")
        except TypeError:
            self.new_file()
            self.save_file()
            # self.error_win(f"{e}\n aka you probably didn't open any file yet")

    def save_file_as(self):
        """ saves current text into a new file """
        if (self.current_file_name != None):
            tmp = self.filename.asksaveasfilename(initialdir=f'{os.getcwd()}', title="Select file", defaultextension=".txt" ,filetypes=(("TXT files", "*.txt *.py"),("all files","*.*")))
            os.rename(self.current_file_name, tmp)
            self.current_file_name = tmp
        else:
            self.current_file_name = self.filename.asksaveasfilename(initialdir=f'{os.getcwd()}', title="Select file", defaultextension=".txt" ,filetypes=(("TXT files", "*.txt *.py"),("all files","*.*")))

        root.title(f"N Editor: <{os.path.basename(self.current_file_name)}>")
        self.save_file()

    def load_file(self, filename=None):
        """ opens a file and loads it's content into the text widget """
        if (filename):
            self.current_file_name = filename
        
        elif (filename == None):
            self.current_file_name = self.filename.askopenfilename(initialdir=f"{os.getcwd()}/", title="Select file", filetypes=(("TXT files", "*.txt *.py"),("all files","*.*")))
        
        try:
            self.current_file = open(self.current_file_name, "r+")
            content = self.current_file.read()
            root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
            self.txt.delete("1.0", "end-1c")
            self.txt.insert("1.0", content)
            self.current_file.close()
            self.command_O(f"total lines: {self.get_line_count()}")
        except Exception as e:
            self.error_win(e)


    def init(self):
        """ a completely useless initialize function """
        self.update_win()

    def update_win(self):
        """ updates window """
        try:
            root.update()
            root.update_idletasks()
        except Exception: #when exiting window it throws an error because root wasn't properly destroyed
            root.quit()
            raise SystemExit
            exit()
        

    def update_text(self, x=''):
        """ updates the text and sets current position of the insert cursor"""
        #basically the main function
        #counter = 0
        while self.run:
            self.update_win()
            #print(self.txt.index(tkinter.INSERT))
            #self.txt.after(0, self.update_line_numbers)
            self.cursor_index = self.txt.index(tkinter.INSERT).split(".") # gets the cursor's position
            self.line_no.configure(text=f"l:{self.cursor_index[0]} c:{self.cursor_index[1]}") # sets the cursor position into line number label
            try:
                if (self.txt.get(f"{self.cursor_index[0]}.{int(self.cursor_index[1])-1}", 'end-1c')[0] == '"'):
                    pass
            except Exception:
                pass
            if (self.loading):
                threading.Thread(target=self.loading_widg()).start()

            if (self.highlighting): # if the highlighting option is on then turn on highlighting :D
                self.highlight()

    
    def highlight(self):
        count = tkinter.IntVar()
        for keyword in keywords:

            index = self.txt.search(keyword, "1.0", "end", count=count, exact=True)
            #print(index, count)
            if index == "": continue
            print(self.txt.get("%s+%sc" % (index, count.get()+1)))
            if (self.txt.get("%s+%sc" % (index, count.get()+1)) == " "):
                self.txt.tag_add("var_types", index, "%s+%sc" % (index, count.get()))
                

        # offset = 0
        # line = self.txt.get(self.cursor_index[0]+".0", "end").split("\n")
        # for index, word1 in enumerate(line[0].split(), 0):

        #     word_list = word1.strip("()_.:;").split("(")
        #     for index1, word in enumerate(word_list, 0):
        #         offset1 = len(word1) - len(word)
        #         #print(f"1:{word1}\n2:{word}\n")
            
        #         self.txt.highlight_pattern(word, self.theme[2], start=f"{self.cursor_index[0]}.{offset}", end=f"{self.cursor_index[0]}.{offset+index+offset1+index1+len(word)}")
        #         if (word not in all_key):
        #             self.txt.tag_remove(self.theme[2], f"{self.cursor_index[0]}.{offset}", f"{self.cursor_index[0]}.{offset+index+offset1+index1+len(word)}")
        #         #offset += offset1
        #     offset += len(word1)
        #     print(offset)

                # for keyword in all_key:
                #     if (word == keyword):
                #         print("aha!")
        # for word in all_key:
        #     self.txt.highlight_pattern(word, self.theme[2], start=str(int(self.cursor_index[0])-30.0), end=str(int(self.cursor_index[0])+30.0))
        # #     #var_types, modules
        
        # for word in nums:
        #    self.txt.highlight_pattern(word, self.theme[3], start=str(int(self.cursor_index[0])-30.0), end=str(int(self.cursor_index[0])+30.0))

        # for word in special_chars:
        #     self.txt.highlight_pattern(word, self.theme[4], start=str(int(self.cursor_index[0])-30.0), end=str(int(self.cursor_index[0])+30.0))

        #some shitty bullshit i tried for highlighting but as you can see I don't really understand regex
        # line = self.txt.get(self.cursor_index[0]+".0", "end").split("\n")
        # for word in line:
        #     for keyword in all_key:
        #         if (re.search("%r"%keyword, word)):
        #             found = re.search(r"\s*[_]*"+"%r"%keyword, word)
        #             found_index = [ str(found.span()[0]), str(found.span()[1]-1) ]
        #             self.txt.tag_add("other_chars", f"{self.cursor_index[0]}.{found_index[0]}", f"{self.cursor_index[0]}.{found_index[1]}")

    def highlight_all(self):
        """ don't even ask """
        self.info = self.txt.get("1.0", 'end-1c')
        for line in self.info.split("\n"):
            for word in line:
                for keyword in all_key:
                    if (re.search(keyword, word)):
                        found = re.search(r"\s*[_]*"+keyword, word)
                        found_index = [ str(found.span()[0]), str(found.span()[1]-1) ]
                        self.txt.tag_add("sumn", f"{self.cursor_index[0]}.{found_index[0]}", f"{self.cursor_index[0]}.{found_index[1]}")
        # try:
        #     for index, line in enumerate(self.info.split('\n'), start=1):
        # #         #if (re.search(r"[.,_]*[0-9]+", line)):
        # #         for i in range(len(re.findall(r"\s*[.,_]*[0-9]+", line, re.X))):
        # #             split_line = ''.join(line.split())
        # #             offset = re.search(r"\s*", line[1:])
        # #             #print(offset)
        # #             num = re.search(r"[[0-9]+]*", split_line) #r"$[^,]*^[^(]*^[^)]*[0-9]+"
        # #             #print(num)
        # #             #offset = len(line) - len(split_line)
        # #             num = [ num.span()[0], num.span()[1] ]
        # #             #print(num[1])
        # #             #print(num)
        # #             self.txt.tag_add("operators", f"{index}.{num[0]}", f"{index}.{num[1]}")

        #         for keyword in all_key:
        #             self.txt.highlight_pattern(keyword, "sumn")
        #             #print(keyword, indx)
        #             # split_line = line.split("\n")
        #             # for indx, word in enumerate(split_line):
        #             #     if (re.search(keyword, word)):
        #             #         found = re.search(r"\s*[_]*"+keyword, word)
        #             #         found_index = [ str(found.span()[0]), str(found.span()[1]-1) ]
        #             #         self.txt.tag_add("sumn", f"{index}.{found_index[0]}", f"{index}.{found_index[1]}")

        # except AttributeError:
        #     pass

        def unhighlight(self):
            """  """
            pass



root = tkinter.Tk()
main_win = win(root)


if __name__ == '__main__':
    main_win.update_text()
