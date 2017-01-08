try:
    from Tkinter import *
except ImportError: ## Python 3
    from tkinter import *
root = Tk()
class App:
    def __init__(self,master):
        scrollbar = Scrollbar(master, orient=VERTICAL)
        self.b1 = Text(master, yscrollcommand=scrollbar.set)
        self.b2 = Text(master, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.b1.pack(side=LEFT, fill=BOTH, expand=1)
        self.b2.pack(side=LEFT, fill=BOTH, expand=1)
    
    def yview(self, *args):
        self.b1.yview(*args)
        self.b2.yview(*args)
        

app = App(root)

def lineNumbers(*args):
    app.b1.delete(1.0, END)
    i = int(app.b2.index('end-1c').split('.')[0])
    for x in range(i):
        app.b1.insert("insert", str(int(x+1)) + '\n')
    current = int(app.b1.index('insert').split('.')[0])
    app.b2.mark_set("insert", str(current) + '.0' )
    app.b2.see(str(current) + '.0')

for item in range(0,40):
    for i in range(item):
        it=str(i)+' '
        app.b2.insert(1.0,it)
        app.b2.insert(1.0,'\n')
lineNumbers()
    
root.mainloop()