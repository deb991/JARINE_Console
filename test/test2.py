import tkinter as tk
from tkinter import *
from tkinter.messagebox import askokcancel
from tkinter import filedialog, Frame
import logo as logo
from logo import *
from commands import *

root = tk.Tk()
root.iconbitmap("D:\\PycharmProjects\\JARINE_Console\\icons\\appheader_main2.ico")


class TextLineNumbers(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        try:
            result = self.tk.call(cmd)
        except Exception:
            return None

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")

        # return what the actual widget returned
        return result


    #fName = askopenfilename()
    #print(fName)
    #if os.path.isfile(fName):
    #    with open(fName, 'r') as f:
    #        contents = f.read()
    #        notepad.insert(INSERT, contents)

    #if fName != None:
    #    contents = fName.read()
    #    notepad.insert(INSERT, contents)
    #    fName.close()


##t_openFile = threading.Thread(target=open__file)


    ##_thread.start_new_thread(open__file, ())


#==========================================
#Right mouse click option starts
#==========================================

def rClicker(e):
    ''' right click context menu for all Tk Entry and Text widgets
    '''

    try:
        def rClick_Copy(e, apnd=0):
            e.widget.event_generate('<Control-c>')

        def rClick_Cut(e):
            e.widget.event_generate('<Control-x>')

        def rClick_Paste(e):
            e.widget.event_generate('<Control-v>')

        def rClick_Run(e):
            e.widget.event_generate(run())

        def rClick_Debug(e):
            e.widget.event_generate()

        e.widget.focus()

        nclst=[
               (' Cut', lambda e=e: rClick_Cut(e)),
               (' Copy', lambda e=e: rClick_Copy(e)),
               (' Paste', lambda e=e: rClick_Paste(e)),
            (' Run', lambda e=e: rClick_Run(e)),
            (' Debug', lambda e=e: rClick_Debug(e))
               ]

        rmenu = Menu(None, tearoff=0, takefocus=0)

        for (txt, cmd) in nclst:
            rmenu.add_command(label=txt, command=cmd)

        rmenu.tk_popup(e.x_root+40, e.y_root+10,entry="0")
        rmenu.config(foreground='grey', background='black')

    except TclError:
        print(' - rClick menu, something wrong')
        pass

    return "break"


def rClickbinder(r):

    try:
        for b in [ 'Text', 'Entry', 'Listbox', 'Label']: #
            r.bind_class(b, sequence='<Button-3>',
                         func=rClicker, add='')
    except TclError:
        print(' - rClickbinder, something wrong')

#==========================================
#Right mouse click option Ends Here.
#==========================================


#CustomText.tag_config('class', background='grey', forground='yellow')
#CustomText.tag_config('def', background='grey', forground='yellow')

def save__file():
    print('save a file')
    file = filedialog.asksaveasfile(mode='w')
    if file != None:
        # slice off the last character from get, as an extra return is added
        data = CustomText.get(0, END + '-1c')
        file.write(data)
        file.close( )
        # return 'EOF'

def open__file():
    print('Open an existing file from the system.')
    # return 'EOF'
    file = filedialog.askopenfile(mode='r', title='Select a file')
    if file != None:
        #contents = file.read( )
        #data = "".join(map(bytes.decode, contents))
        # print(type(contents))
        CustomText.insert(tk.END, file.read())
        file.close()

def exit():
    if askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

t_exit = threading.Thread(target=exit)

class wndo(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = CustomText(self)
        self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.text.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
        self.linenumbers = TextLineNumbers(self, width=30)
        self.linenumbers.attach(self.text)

        self.vsb.pack(side="right", fill="y")
        self.linenumbers.pack(side="left", fill="y")
        self.text.pack(side="right", fill="both", expand=True)

        self.text.bind("<<Change>>", self._on_change)
        self.text.bind("<Configure>", self._on_change)

        self.text.insert("end", "")

    def _on_change(self, event):
        self.linenumbers.redraw()


    t_save__file = threading.Thread(target=save__file)

    menubar = Menu(root, background='#000099', foreground='white',
                   activebackground='#004c99', activeforeground='white')
    fileMenu = Menu(menubar, tearoff=0, background="grey", foreground='black',
                    activebackground='#004c99', activeforeground='white')
    menubar.add_cascade(label='File', menu=fileMenu)

    fileMenu.add_command(label='New', command=new__file)
    fileMenu.add_command(label='Open', command=open__file)
    fileMenu.add_command(label='Save', command=save__file)
    fileMenu.add_command(label='Save as', command=save_as__file)
    fileMenu.add_command(label='Save All', command=save__all)
    fileMenu.add_command(label='Export to HTML', command=export__html)
    fileMenu.add_command(label='Make file read only', command=mkFleRdOnly)
    fileMenu.add_command(label='Exit', command=t_exit.start)
    fileMenu.add_separator( )

    editMenu = Menu(menubar, tearoff=0, background="grey", foreground='black')
    menubar.add_cascade(label='Edit', menu=editMenu)

    editMenu.add_command(label='Cut', command=cut)
    editMenu.add_command(label='Copy', command=copy)
    editMenu.add_command(label='ClipBoard', command=clpBrd)
    editMenu.add_command(label='Paste', command=paste)
    editMenu.add_separator( )
    editMenu.add_command(label='Delete', command=delt)

    viewMenu = Menu(menubar, tearoff=0, background="grey", foreground='black')
    menubar.add_cascade(label='View', menu=viewMenu)

    viewMenu.add_command(label='Full Screen mode', command=FSM)
    viewMenu.add_command(label='Presentation mode', command=PsM)
    viewMenu.add_separator( )

    runMenu = Menu(menubar, tearoff=0, background="grey", foreground='black')
    menubar.add_cascade(label='Run', menu=runMenu)

    runMenu.add_command(label='Run', command=run)
    runMenu.add_command(label='Debug', command=dbug)
    runMenu.add_separator( )
    runMenu.add_command(label='View Break points', command=VBP)

    sett = Menu(menubar, tearoff=0, background="grey", foreground='black')
    menubar.add_cascade(label='Settings', menu=sett)

    sett.add_command(label='Settings', command=sett)
    sett.add_separator( )
    sett.add_command(label='Project Setting', command=sett__P)

    help = Menu(menubar, tearoff=0, background="grey", foreground='black')
    menubar.add_cascade(label='Help', menu=help)

    help.add_command(label='About', command=abt)
    help.add_command(label='File Manager', command=fleAnlzer)

    L_Side_menubar = Frame(root, background="grey")
    L_Side_menubar.pack(fill=X, side=BOTTOM)

    fileManager__button = Button(L_Side_menubar, text='File Manager',
                                 command=f__Manager)  # .pack(side=LEFT, padx=1, pady=1)
    fileManager__button.grid(column=0, row=1, columnspan=1, padx=1, sticky=SW)

    project_window__button = Button(L_Side_menubar, text='Project Window', command=f__Manager)
    project_window__button.grid(column=1, row=1, columnspan=1, padx=1, sticky=SW)

    debugLogo = PhotoImage(file="D:\\PycharmProjects\\JARINE_Console\\icons\\debug.ico")
    debug__button = Button(L_Side_menubar, text='Debug', command=f__Manager)
    debug__button.grid(column=2, row=1, columnspan=1, padx=1, sticky=SW)
    debug__button.config(image=debugLogo, height=20,
                         width=70, activebackground="black", bg="black", bd=0, compound=LEFT)

    console__button = Button(L_Side_menubar, text='Console', command=t_console.start)
    console__button.grid(column=3, row=1, columnspan=1, padx=1, sticky=SW)

root.config(bg='#2A2C2B', menu=wndo.menubar)
root.bind('<Button-3>',rClicker, add='')
root.title('J-Console >> ')


if __name__ == "__main__":
    wndo(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
