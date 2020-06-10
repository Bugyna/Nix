import tkinter
from tkinter import font
import keyboard
import re
import threading
import os
from itertools import chain
from time import sleep
from tkinter import filedialog


keywords = ['if','elif','else','def ','class ','while']
sumn = ['import','from','in ','and ','self']
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



class win():
    def __init__(self, root):
        
        self.current_file = None #open(f"{os.getcwd()}/untitled.txt", "w+") #stores path to currently opened file

        self.highlighting = False # turned off by default because it's not working properly (fucking regex)

        #configuring main window
        root.resizable(True,True)
        root.config(bg="black")
        root.geometry("1200x600")
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
        self.txt = tkinter.Text()
        self.txt.grid(row=0, column=0 ,sticky="nsew")
        self.txt.configure(font=self.font,bg = 'black',fg='#cccccc', undo=True, wrap='word', spacing1=5,
            insertwidth=8, insertofftime=500, insertbackground="#fb2e01", 
            borderwidth=0, relief="sunken", tabs=('1c'))
            
        #scrollbar configuration
        self.scrollb = tkinter.Scrollbar(root, command=self.txt.yview)
        self.scrollb.grid(row=0,column=2,sticky="nsew")
        self.txt['yscrollcommand'] = self.scrollb.set

        #line and column number label
        self.line_no = tkinter.Label(text="aaa",fill=None ,justify=tkinter.RIGHT, font=self.font,bg = 'black',fg='#cccccc'); self.line_no.grid(row=1,column=1)
        
        #command line entry
        self.command_entry = tkinter.Entry(text="aa", justify=tkinter.LEFT, font=self.font,bg = 'black',fg='#cccccc', insertwidth=8, insertofftime=500, insertbackground="#fb2e01"); self.command_entry.grid(row=1,column=0,ipady=3)

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


    #error window
    def error_win(self, e):
        error_win = tkinter.Tk("aaa")
        error_win.configure(bg="#000000", bd=2)
        #error_win.geometry("600x200")"C:\Users\Admin\Desktop\instagram data\sx.bugy_20200512_part_1\messages.json"
        error_win.title(f"Error Win")
        error_label = tkinter.Label(error_win, text=f"Error: {e}", justify=tkinter.CENTER, bg="#000000", fg="#ffffff"); error_label.pack()
        error_button = tkinter.Button(error_win, text="OK", command=error_win.destroy, bg="#000000", fg="#ffffff"); error_button.pack()
        #error_label.place(relx=0.0, rely=0.10, relwidth=1, relheight=0.20)
        #error_button.place(relx=0.25, rely=0.25, relwidth=0.35, relheight=0.26)

    #binded functions
    def popup(self, arg):
        """ gets x, y position of mouse click """
        self.right_click_menu.tk_popup(arg.x_root+50, arg.y_root, 0)
        self.right_click_menu.grab_release()

    def cmmand(self, arg):
        """ parses command(case insensitive) from command line and executes it"""

        command = self.command_entry.get().lower().split()#turns command into a list and turns it all into lowercase chars
        #print(command[0])

        #help command
        if (command[0] == "help"):
            print("l: line number --puts you to line number (eg. 120(by default starts at column 0 but you can specify the column like: 120.5)")
        
        #highlighting command
        if (command[0] == "highlighting"):
            #print("aaa")
            if (command[1] == "on"):
                #print("turn on")
                self.highlighting = True
            elif (command[1] == "off"):
                #print("turn off")
                self.highlighting = False

        #line/ line and column command        
        if (command[0][0] == "l"):
            #print(float(command[0][2:]))
            self.txt.mark_set("insert", float(command[0][2:]))
        
        #sets focus back to text widget
        self.txt.focus_set()
        keyboard.press_and_release("enter+backspace")
        self.command_entry.delete(0, "end") #deletes command line input

    #menubar functions
    def new_file(self):
        try:
            self.current_file = open(f"{os.getcwd()}/untitled.txt", "w+")
            root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
        except Exception as e:
            self.current_file.close()
            self.error_win(e)

    def save_file(self):
        content = str(self.txt.get("1.0", "end-1c"))
        
        try:
            self.current_file = open(f"{os.getcwd()}/untitled.txt", "w+")
            root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
        except:
            pass
        
        try:
            self.current_file.write(content)
            self.current_file.close()
        except Exception as e:
            self.current_file.close()
            self.error_win(e)

    def save_file_as(self):
        path = self.filename.asksaveasfile(initialdir=f'{os.getcwd()}', title="Select file", defaultextension=".txt" ,filetypes=(("TXT files", "*.txt *.py"),("all files","*.*")))
        try:
            content = self.txt.get("1.0", "end-1c")
            path.write(content)
            path.close()

        except Exception as e:
            self.error_win(e)

    def load_file(self):
        if (self.current_file.read()==""):
            self.current_file.close()
            os.remove(f"{os.getcwd()}/untitled.txt")
        path = self.filename.askopenfilename(initialdir=f"{os.getcwd()}/", title="Select file", filetypes=(("TXT files", "*.txt *.py"),("all files","*.*")))
        try:
            self.current_file = open(path, "r+")
            root.title(f"N Editor: <{os.path.basename(self.current_file.name)}>")
            self.txt.insert("1.0",self.current_file.read())
            self.current_file.close()

        except Exception as e:
            self.error_win(e)


    def init(self):
        self.update_win()


    def update_win(self):
        root.update()
        root.update_idletasks()


    def update_syntax(self, x=''):
        while 1:
            self.update_win()
            #print(self.current_file)
            #print(self.txt.index(tkinter.INSERT))
            #self.txt.after(0, self.update_line_numbers)
            cursor_index = self.txt.index(tkinter.INSERT).split(".")
            #print(cursor_index)
            self.line_no.configure(text=f"line: {cursor_index[0]}   column: {cursor_index[1]}")
            if (self.highlighting):
                self.highlight()
            else:
                pass

    def highlight(self):
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

                for indx, keyword in enumerate(all_key):
                    #print(keyword, indx)
                    if (re.search(keyword, line)):
                        found = re.search(r"\s*[_]*"+keyword, line)
                        found_index = [ str(found.span()[0]), str(found.span()[1]) ]
                        #if (keyword == "import" and keyword == found.group()):
                        #    modules.append(line.split()[1])
                        #print(line, index)
                        self.txt.tag_add("sumn", f"{index}.{found_index[0]}", f"{index}.{found_index[1]}")
                        #print(x, x.span(), f"{index}.{str(x.span()[0])}", f"{index}.{str(x.span()[1])}")
                        #self.checked.append(index)

        except AttributeError:
            pass

        def unhighlight(self):
            pass



root = tkinter.Tk()
main_win = win(root)

if __name__ == '__main__':
    main_win.update_syntax()