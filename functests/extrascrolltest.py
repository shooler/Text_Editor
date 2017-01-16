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
        print args
        self.b1.yview(*args)
        self.b2.yview(*args)
        
app = App(root)
for item in range(0,40):
    for i in range(item):
        it=str(i)+' '
        app.b1.insert(1.0,it)
        app.b2.insert(1.0,it)
    app.b1.insert(1.0,'\n')
    app.b2.insert(1.0,'\n')
    
    
root.mainloop()