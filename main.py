import tkinter
from tkinter import ttk
from tkinter import font
import keyboard
import re
import threading
import os, sys
import tqdm
from itertools import chain
from time import sleep
from tkinter import filedialog




keywords = ['if','elif','else','def ','class ','while']
sumn = ['import ','from ','in ','and ','self.']
var_types = ['int','float','string','str']
special_chars = ['"',"'","#","@","(",")","[","]","{","}"]
other_chars = ["_"]
operators = ['<','>',"+","-","*","/","="]
nums = ['0','1','2','3','4','5','6','7','8','9']
modules = []
modules2 = []
all_key = [keywords,sumn,var_types, modules, nums]
all_key = list(chain.from_iterable(all_key))
print(all_key)

#print(chr(9619))

for i in tqdm.tqdm(range(10)):
    sleep(0.05)

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
        self.mark_set("matchStart", start)
        self.mark_set("matchEnd", start)
        self.mark_set("searchLimit", end)

        count = tkinter.IntVar()
        while True:
            index = self.search(pattern, "matchEnd","searchLimit",
                                count=count, regexp=regexp)
            if index == "": break
            if count.get() == 0: break # degenerate pattern which matches zero-length strings
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            self.tag_add(tag, "matchStart", "matchEnd")


class p_bar(tkinter.Label):
    def __init__(self, root):
        self.char = chr(9608)
        #self.char = "|"
        self.bbar = super().__init__(root,font=root.smaller_font,text=f"  0/100%{self.char*25}", anchor="w",
        bg="#111111",fg="#FFFFFF", justify=tkinter.LEFT)
    
    def update(self):
        self.wbar = super().__init__(root,font=root.font,text=f"{self.char*5}",bg="#FFFFFF",fg="#FFFFFF", justify=tkinter.LEFT)




class win():
    def __init__(self, root, file=None):
        
        self.command_definition = {
            "l" : "-get: gets last line number || -[LINE_NUMBER(.CHARACTER)]: puts you to line number (eg. 120(by default starts at column 0 but you can specify the column like: 120.5)",
            "highlighting" : "-on: turns highlighting on -off: turns highlighting off"
        }

        self.command_input_history = []
        self.command_input_history_index = 0

        self.current_file = None #open(f"{os.getcwd()}/untitled.txt", "w+") #stores path to currently opened file
        self.current_file_name = None

        self.line_count = None
        
        self.highlighting = False # turned off by default because it's not working properly (fucking regex)

        #configuring main window
        #root.overrideredirect(True)
        root.resizable(True,True)
        root.config(bg="black")
        root.geometry("1200x600")
        self.title_bar = tkinter.Frame(bg="blue", relief='raised', bd=2)
        root.title(f"N Editor: <None>") #{os.path.basename(self.current_file.name)}
        root.font = font.Font(family="Px437 IBM CGA", size=9, weight="bold")
        root.smaller_font = font.Font(family="Px437 IBM CGA", size=7, weight="bold")


        #prints all fonts you have installed
        #fonts = list(font.families())
        #for item in fonts:
        #    print(item)

        #configuring fonts
        self.font = font.Font(family="Px437 IBM CGA", size=9, weight="bold")
        self.smaller_font = font.Font(family="Px437 IBM CGA", size=7, weight="bold")

        #filediaolog pretty much self-explanatory
        self.filename = filedialog


        #text widget configuration
        self.txt = CustomText()

        #self.txt.grid(row=0, column=0 ,sticky="nsew")
        self.txt.place(relx=0,rely=0.0,relwidth=0.985,relheight=0.95)
        self.txt.configure(font=self.font,bg = 'black',fg='#cccccc', undo=True, spacing1=5,
            insertwidth=8, insertofftime=500, insertbackground="#A2000A", selectbackground="#0A00A2",
            borderwidth=0, relief="sunken", tabs=('1c'))
            
        #scrollbar configuration
        # self.scrollb = tkinter.Scrollbar(root, command=self.txt.yview, relief="flat") #self.scrollb.grid(row=0,column=2,sticky="nsew")
        # self.scrollb.place(relx=0.985, rely=0.0, relwidth=0.15, relheight=.95)
        # self.txt['yscrollcommand'] = self.scrollb.set

        #line and column number label
        self.line_no = tkinter.Label(text="aaa",fill=None ,justify=tkinter.RIGHT, font=self.font,bg = 'black',fg='#cccccc') #self.line_no.grid(row=1,column=2)
        self.line_no.place(relx=0.70,rely=0.96, relwidth=0.3, relheight=0.05)

        
        #command line entry
        self.command_entry = tkinter.Entry(text="aa", justify=tkinter.LEFT, font=self.font,
        bg = '#111111',fg='#cccccc', insertwidth=8, insertofftime=500, insertbackground="#fb2e01", relief="flat")
        #self.command_entry.grid(row=1,column=0,ipady=3);
        self.command_entry.place(relx=0.005,rely=0.97, relwidth=0.25, relheight=0.0275)


        #command output
        self.command_out = tkinter.Label(font=self.smaller_font, text="biog bruh", bg="#000000", fg="#00df00",
         justify=tkinter.CENTER, anchor="w")
        self.command_out.place(relx=0.28,rely=0.97, relwidth=0.25, relheight=0.0275)

        #progressbar
        #self.progress_bar = p_bar(root) #.grid(row=1,column=1)
        #self.style=ttk.Style()
        #self.style.theme_use("clam")
        #self.style.configure("color.Horizontal.TProgressbar", foreground="white", background="white")
        #self.progress_bar = ttk.Progressbar(orient=tkinter.HORIZONTAL, style="color.Horizontal.TProgressbar",
        # length=100, mode='determinate')
        #self.progress_bar.place(relx=0.35,rely=0.975,relwidth=0.3,relheight=0.025)

        #right click pop-up menu
        self.right_click_menu = tkinter.Menu(tearoff=0, font=self.smaller_font, bg="#000000", fg="#ffffff")
        self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
        self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
        self.right_click_menu.add_command(label="aaaaa", font=self.smaller_font)
        self.right_click_menu.add_separator()

        #menubar
        self.menubar = tkinter.Menu(root, font=self.font, bg="black") #declare menubar
        self.menubar.configure(font=self.font, bg="black") #configure font and background

        #dropdown for menubar
        self.file_dropdown = tkinter.Menu(self.menubar, font=self.font, tearoff=False,fg="#FFFFFF", bg="black") #declare dropdown
        self.file_dropdown.add_command(label="New file",command=self.new_file) #add commands
        self.file_dropdown.add_command(label="Open file",command=self.load_file)
        self.file_dropdown.add_command(label="Save file",command=self.save_file)
        self.file_dropdown.add_command(label="Save file as",command=self.save_file_as)
        self.menubar.add_cascade(label="File",menu=self.file_dropdown) #add dropdown to menubar
        #self.file_dropdown.add_separator()
        #self.file_dropdown.add_command(label="EXIT")

        root.config(menu=self.menubar)#adds menubar to main window

        #tags for highlighting
        self.txt.tag_configure("other_chars", foreground="#302387")
        self.txt.tag_configure("sumn", foreground="#74091D")
        self.txt.tag_configure("special_chars",foreground="#ff00bb")
        self.txt.tag_configure("var_types",foreground="#01cdfe")
        self.txt.tag_configure("operators",foreground="#05ffa1")
        self.txt.tag_configure("keywords", foreground="#ff5500")
        self.txt.tag_configure("modules", foreground="#f75f00")
        self.txt.tag_configure("default", foreground="#302387")



        #command binding
        self.command_entry.bind("<Return>", self.cmmand) #if you press enter in command line it executes the command and switches you back to text widget
        self.command_entry.bind("<Up>", self.command_history) # lets you scroll through commands you have already used
        self.txt.bind("<Button-3>", self.popup) #right click pop-up window
        #self.txt.bind("<Tab>", self.cmmand)
        #self.txt.bind("<Control_L><k>", self.cmmand)

        #self.checked = [] #checked lines (for syntax highlighting optimization not yet added)
        #self.keys = [] #no idea 


        #grid configuration
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)
        root.grid_rowconfigure(0,weight=1)

    #def indent(self, arg):
    #    self.txt.insert(tkinter.INSERT, " "*4)
    #    return 'break'

    #def indent_del(self,arg=None):
    #    print(self.txt.index(tkinter.INSERT))
    #

    #def cmmand(self, event):
    #    pass



    def get_line_count(self):
        """ returns total amount of lines in opened text """
        self.info = self.txt.get("1.0", "end-1c")
        return sum(1 for line in self.info.split("\n"))

    def error_win(self, e):
        """ set up error window """
        error_win = tkinter.Tk("aaa")
        error_win.configure(bg="#000000", bd=2)
        #error_win.geometry("600x200")"C:\Users\Admin\Desktop\instagram data\sx.bugy_20200512_part_1\messages.json"
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
    def popup(self, arg):
        """ gets x, y position of mouse click """
        self.right_click_menu.tk_popup(arg.x_root+50, arg.y_root, 0)
        self.right_click_menu.grab_release()

    def command_history(self, arg):
        """ scroll through used commands with Up and Down arrows(?) """
        try:
            self.command_entry.delete(0, "end")
            self.command_input_history_index += 1
            last_command = self.command_input_history[-self.command_input_history_index]
            self.command_entry.insert(0, last_command)
        except Exception:
            self.command_input_history_index -= 2

    def command_O(self, arg):
        """ sets the text in command output"""
        #(I have no idea why past me made this into a function when it doesn't really have to be a function)
        self.command_out.configure(text=str(arg))

    def cmmand(self, arg):
        """ parses command(case insensitive) from command line and executes it"""

        command = self.command_entry.get().lower().split()#turns command into a list and turns it all into lowercase chars
        #print(command[0])

        #help command
        if (command[0] == "help"):
            try:
                if (command[1] != None):
                    self.help_win(command[1])
            except IndexError:
                print("l: line number -options: get, [line_number.character] -puts you to line number (eg. 120(by default starts at column 0 but you can specify the column like: 120.5)")
                print("highlighting -options: on, off")
                self.help_win()

        #highlighting command
        if (command[0] == "highlighting"):
            #print("aaa")
            if (command[1] == "on"):
                self.command_O("highlighting on")
                self.highlighting = True
            elif (command[1] == "off"):
                self.command_O("highlighting off")
                self.highlighting = False

        #line/ line and column command        
        if (command[0][0] == "l"):
            argument = command[0][2:]
            if (re.search("[0-9]", argument)):
                self.command_O(f"moved to: {float(argument)}")
                self.txt.mark_set("insert", float(argument))

            elif (re.search("get", argument)):
                self.command_O(f"total lines: {self.get_line_count()}")
        
        #append command to command history
        self.command_input_history.append(command)
        print(self.command_input_history)

        #sets focus back to text widget
        self.txt.focus_set()
        keyboard.press_and_release("enter+backspace")
        self.command_entry.delete(0, "end") #deletes command line input

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
        except Exception as e:
            self.current_file.close()
            self.error_win(e)

    def save_file_as(self):
        """ saves current text into a new file """
        self.current_file = self.filename.asksaveasfile(initialdir=f'{os.getcwd()}', title="Select file", defaultextension=".txt" ,filetypes=(("TXT files", "*.txt *.py"),("all files","*.*")))
        self.current_file_name = self.current_file.name
        try:
            content = self.txt.get("1.0", "end-1c")
            self.current_file.write(content)
            self.current_file.close()

        except Exception as e:
            print(e)
            self.error_win(e)

    def load_file(self):
        """ opens a file and loads it's content into the text widget """
        try:
            if (self.current_file.read()==""):
                self.get_line_count()
                self.current_file.close()
                os.remove(f"{os.getcwd()}/untitled.txt")
        except Exception as e:
            self.error_win(e)

        self.current_file_name = self.filename.askopenfilename(initialdir=f"{os.getcwd()}/", title="Select file", filetypes=(("TXT files", "*.txt *.py"),("all files","*.*")))
        try:
            self.current_file = open(self.current_file_name, "r+")
            content = self.current_file.read()
            root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
            self.txt.delete("1.0", "end-1c")
            self.txt.insert("1.0", content)
            self.current_file.close()
            self.command_O(f"total lines: {self.get_line_count()}")

            # a bug I thought I could fix with loading the file in chunks but it seems to be a problem of tkinter.Text wrapping
            # content_len = len(content)
            # chunksize = int(content_len/1000)
            # chunk0 = 0
            # chunk1 = chunksize
            # for i in range(int(content_len/1000)):
            #     self.txt.insert("end-1c", content[chunk0:chunk1])
            #     chunk0 += chunksize
            #     chunk1 += chunksize

        except Exception as e:
            self.error_win(e)


    def init(self):
        """ a completely useless initialize function """
        self.update_win()

    def update_win(self):
        """ updates window """
        root.update()
        root.update_idletasks()


    def update_text(self, x=''):
        """ updates the text and sets current position of the insert cursor"""
        #basically the main function
        while 1:
            self.update_win()
            #print(self.current_file)
            #print(self.txt.index(tkinter.INSERT))
            #self.txt.after(0, self.update_line_numbers)
            cursor_index = self.txt.index(tkinter.INSERT).split(".") # gets the cursor's position
            #print(cursor_index)
            self.line_no.configure(text=f"line: {cursor_index[0]}   column: {cursor_index[1]}") # sets the cursor position into line number label
            
            if (self.highlighting): # if the highlighting option is on then turn on highlighting
                self.highlight()
            else:
                pass

    def highlight(self):
        """ the highlight function """
        self.info = self.txt.get("1.0", 'end-1c')
        try:
            for index, line in enumerate(self.info.split('\n'), start=1):
        #         #if (re.search(r"[.,_]*[0-9]+", line)):
        #         for i in range(len(re.findall(r"\s*[.,_]*[0-9]+", line, re.X))):
        #             split_line = ''.join(line.split())
        #             offset = re.search(r"\s*", line[1:])
        #             #print(offset)
        #             num = re.search(r"[[0-9]+]*", split_line) #r"$[^,]*^[^(]*^[^)]*[0-9]+"
        #             #print(num)
        #             #offset = len(line) - len(split_line)
        #             num = [ num.span()[0], num.span()[1] ]
        #             #print(num[1])
        #             #print(num)
        #             self.txt.tag_add("operators", f"{index}.{num[0]}", f"{index}.{num[1]}")

                for keyword in all_key:
                    self.txt.highlight_pattern(keyword, "sumn")
                    #print(keyword, indx)
                    # split_line = line.split("\n")
                    # for indx, word in enumerate(split_line):
                    #     if (re.search(keyword, word)):
                    #         found = re.search(r"\s*[_]*"+keyword, word)
                    #         found_index = [ str(found.span()[0]), str(found.span()[1]-1) ]
                    #         self.txt.tag_add("sumn", f"{index}.{found_index[0]}", f"{index}.{found_index[1]}")

        except AttributeError:
            pass

        def unhighlight(self):
            pass



root = tkinter.Tk()
main_win = win(root)

if __name__ == '__main__':
    main_win.update_text()