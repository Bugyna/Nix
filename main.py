import tkinter
import keyboard
from tkinter import font
import re
import threading
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
all_key = [keywords,sumn,var_types, modules]
all_key = list(chain.from_iterable(all_key))
print(all_key)


#pyglet.font.add_file("Px437_IBM_CGA.ttf")


class win():
    def __init__(self,root):
        self.x=0
        root.resizable(True,True)
        root.config(bg="black")
        root.geometry("1200x600")
        root.title("N Editor")
        root.font = font.Font(family="Px437 IBM CGA", size=9, weight="bold")
        fonts = list(font.families())
        for item in fonts:
            print(item)
        self.font = font.Font(family="Px437 IBM CGA", size=9, weight="bold")
        self.filename = filedialog #.askopenfilename(initialdir='/', title="Select file", filetypes=(("txt files", "*.txt", "*.py"),("all files","*.*")))

        self.txt = tkinter.Text()
        self.txt.grid(row=0, column=0 ,sticky="nsew")
        self.txt.configure(font=self.font,bg = 'black',fg='#cccccc', undo=True, wrap='word', spacing1=5,
            insertwidth=8, insertofftime=500, insertbackground="#fb2e01", 
            borderwidth=0, relief="sunken", tabs=('1c'))
            
        self.scrollb = tkinter.Scrollbar(root, command=self.txt.yview)
        self.scrollb.grid(row=0,column=2,sticky="nsew")
        self.txt['yscrollcommand'] = self.scrollb.set
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)
        root.grid_rowconfigure(0,weight=1)

        self.line_no = tkinter.Label(text="aaa",fill=None ,justify=tkinter.RIGHT, font=self.font,bg = 'black',fg='#cccccc'); self.line_no.grid(row=1,column=1)
        
        self.command_entry = tkinter.Entry(text="aa", justify=tkinter.LEFT, font=self.font,bg = 'black',fg='#cccccc', insertwidth=8, insertofftime=500, insertbackground="#fb2e01"); self.command_entry.grid(row=1,column=0,ipady=3)

        self.menubar = tkinter.Menu(root, font=self.font, bg="black") 
        self.menubar.configure(font=self.font, bg="black")
        root.config(menu=self.menubar)
        self.file_dropdown = tkinter.Menu(self.menubar, font=self.font, tearoff=False,fg="#FFFFFF")
        self.file_dropdown.configure(bg="black")
        self.file_dropdown.add_command(label="New file",command=self.new_file)
        self.file_dropdown.add_command(label="Open file",command=self.load_file)
        self.file_dropdown.add_command(label="Save file",command=self.save_file)
        self.file_dropdown.add_command(label="Save file as",command=self.save_file_as)
        #self.file_dropdown.add_separator()
        #self.file_dropdown.add_command(label="EXIT")
        self.menubar.add_cascade(font=self.font, label="File",menu=self.file_dropdown)


        #self.txt.tag_configure("other_chars", foreground="#302387")
        self.txt.tag_configure("sumn", foreground="#74091D")
        self.txt.tag_configure("special_chars",foreground="#ff00bb")
        self.txt.tag_configure("var_types",foreground="#01cdfe")
        self.txt.tag_configure("operators",foreground="#05ffa1")
        self.txt.tag_configure("keywords", foreground="#ff5500")
        self.txt.tag_configure("modules", foreground="#f75f00")
        self.txt.tag_configure("default", foreground="#302387")


        #self.txt.bind("<Tab>", self.cmmand)
        #self.txt.bind("<Control_L><k>", self.cmmand)

        self.command_entry.bind("<Return>", self.cmmand)
        self.checked = []
        self.keys = []


    #def indent(self, arg):
    #    self.txt.insert(tkinter.INSERT, " "*4)
    #    return 'break'

    #def indent_del(self,arg=None):
    #    print(self.txt.index(tkinter.INSERT))
    #

    #def cmmand(self, event):
    #    pass

    def cmmand(self, arg):
        command = self.command_entry.get()
        if (command[0] == "l"):
            self.txt.mark_set("insert", float(command[2:]))
        
        
        self.txt.focus_set()
        keyboard.press_and_release("enter+backspace")


    def new_file(self):
        pass

    def save_file(self):
        pass

    def save_file_as(self):
        pass

    def load_file(self):
        path = self.filename.askopenfilename(initialdir='/', title="Select file", filetypes=(("TXT files", "*.txt *.py"),("all files","*.*")))
        try:
            file = open(path, "r+").read()
            self.txt.insert("1.0",file)
        except Exception as e:
            error_win = tkinter.Tk("aaa")
            error_win.configure(bg="#000000", bd=2)
            #error_win.geometry("600x200")"C:\Users\Admin\Desktop\instagram data\sx.bugy_20200512_part_1\messages.json"
            error_win.title(f"Error Win")
            error_label = tkinter.Label(error_win, text=f"Error: {e}", justify=tkinter.CENTER, bg="#000000", fg="#ffffff"); error_label.pack()
            error_button = tkinter.Button(error_win, text="OK", command=error_win.destroy, bg="#000000", fg="#ffffff"); error_button.pack() 
            #error_label.place(relx=0.0, rely=0.10, relwidth=1, relheight=0.20)
            #error_button.place(relx=0.25, rely=0.25, relwidth=0.35, relheight=0.26)


    def init(self):
        self.update_win()


    def update_win(self):
        root.update()
        root.update_idletasks()


    def update_syntax(self, x=''):
        while 1:
            self.update_win()
            #print(self.txt.index(tkinter.INSERT))
            #self.txt.after(0, self.update_line_numbers)
            self.info = self.txt.get("1.0", 'end-1c')
            cursor_index = self.txt.index(tkinter.INSERT).split(".")
            #print(cursor_index)
            self.line_no.configure(text=f"line: {cursor_index[0]}   column: {cursor_index[1]}")
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



root = tkinter.Tk()
main_win = win(root)

thread0=threading.Thread(target=main_win.update_syntax, args=())
#thread1=threading.Thread(target=main_win.update1, args=())
thread2=threading.Thread(target=root.update)
thread3=threading.Thread(target=root.update_idletasks)

if __name__ == '__main__':
    main_win.update_syntax()