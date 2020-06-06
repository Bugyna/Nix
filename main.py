import tkinter
import re
from itertools import chain
import tkinter.ttk as ttk
from time import sleep
import threading

keywords = ['if','elif','else','def','class','while']
sumn = ['import','from','in','and','self']
var_types = ['int','float','string','str']
special_chars = ['"',"'","#","@","(",")","[","]","{","}"]
other_chars = ["_"]
operators = ['<','>',"+","-","*","/","="]
nums = ['0','1','2','3','4','5','6','7','8','9']
modules = []
modules2 = []
all_key = [keywords,sumn,var_types]
all_key = list(chain.from_iterable(all_key))
print(all_key)

class win():
    def __init__(self,root):
        self.x=0
        root.resizable(True,True)
        root.geometry("1200x600")
        root.title("N Editor")
        self.txt = tkinter.Text()
        self.txt.grid(row=0, column=0 ,sticky="nsew")
        self.txt.configure(font=('Px437 IBM CGA', 9),bg = 'black',fg='#cccccc', undo=True, wrap='word', spacing1=5,
            insertwidth=8, insertofftime=500, insertbackground="#fb2e01", 
            borderwidth=0, relief="sunken", tabs=('1c'))
            
        self.scrollb = tkinter.Scrollbar(root, command=self.txt.yview)
        self.scrollb.grid(row=0,column=1,sticky="nsew")
        self.txt['yscrollcommand'] = self.scrollb.set
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)
        root.grid_rowconfigure(0,weight=1)


        self.menubar = tkinter.Menu(root, bg="black") 
        self.menubar.configure(bg="black")
        root.config(menu=self.menubar)
        self.file_dropdown = tkinter.Menu(self.menubar,tearoff=False)
        self.file_dropdown.configure(bg="black")
        self.file_dropdown.add_command(label="New file",command=self.new_file)
        self.file_dropdown.add_command(label="Open file",command=self.load_file)
        self.file_dropdown.add_command(label="Save file",command=self.save_file)
        self.file_dropdown.add_command(label="Save file as",command=self.save_file_as)
        #self.file_dropdown.add_separator()
        #self.file_dropdown.add_command(label="EXIT")
        self.menubar.add_cascade(label="File",menu=self.file_dropdown)


        #self.txt.tag_configure("other_chars", foreground="#302387")
        self.txt.tag_configure("sumn", foreground="#74091D")
        self.txt.tag_configure("special_chars",foreground="#ff00bb")
        self.txt.tag_configure("var_types",foreground="#01cdfe")
        self.txt.tag_configure("operators",foreground="#05ffa1")
        self.txt.tag_configure("keywords", foreground="#ff5500")
        self.txt.tag_configure("modules", foreground="#f75f00")
        self.txt.tag_configure("default", foreground="#302387")


        #self.txt.bind("<Tab>", self.indent)

        self.checked = []
        self.keys = []

    #def indent(self, arg):
    #    self.txt.insert(tkinter.INSERT, " "*4)
    #    return 'break'

    #def indent_del(self,arg=None):
    #    print(self.txt.index(tkinter.INSERT))
    #

    def new_file(self):
        pass

    def save_file(self):
        pass

    def save_file_as(self):
        pass

    def load_file(self):
        pass




    def init(self):
        self.update_win()


    def update_win(self):
        root.update()
        root.update_idletasks()


    def update_syntax(self, x=''):
        while 1:
            self.update_win()
            #print(self.txt.index(tkinter.INSERT))
            self.info = self.txt.get("1.0", 'end-1c')

            try:
                for index, line in enumerate(self.info.split('\n'), start=1):
                    for keyword in all_key:
                        print(keyword)
                        if (re.search(keyword, line)):
                            x = re.search(keyword, line)
                            print(line, index)
                            self.txt.tag_add("sumn", f"{index}.{str(x.span()[0])}", f"{index}.{str(x.span()[1])}")
                            print(x, x.span(), f"{index}.{str(x.span()[0])}", f"{index}.{str(x.span()[1])}")
                            #self.checked.append(index)
                        else:
                            pass
                                                                            #x = re.search('import', self.info)
                                                                            #self.txt.tag_add("sumn", "1"+"."+str(x.span()[0]), "1"+"."+str(x.span()[1]))
                                                                            #print(x, x.span(), "1"+"."+str(x.span()[0]))
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