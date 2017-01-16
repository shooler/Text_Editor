import Tkinter
import ttk
import os
from Tkinter import *


tabs = {}
textPad = ''
lnText = ''

root = Tkinter.Tk()

imgdir = os.path.join(os.path.dirname(__file__), 'imgdir')
i1 = Tkinter.PhotoImage("img_close", file=os.path.join(imgdir, 'close.png'))
i2 = Tkinter.PhotoImage("img_closeactive",
    file=os.path.join(imgdir, 'close_active.png'))
i3 = Tkinter.PhotoImage("img_closepressed",
    file=os.path.join(imgdir, 'close_pressed.png'))
style = ttk.Style()
style.element_create("close", "image", "img_close",
    ("active", "pressed", "!disabled", "img_closepressed"),
    ("active", "!disabled", "img_closeactive"), border=8, sticky='')
style.layout("ButtonNotebook", [("ButtonNotebook.client", {"sticky": "nswe"})])
style.layout("ButtonNotebook.Tab", [
    ("ButtonNotebook.tab", {"sticky": "nswe", "children":
        [("ButtonNotebook.padding", {"side": "top", "sticky": "nswe",
                                     "children":
            [("ButtonNotebook.focus", {"side": "top", "sticky": "nswe",
                                       "children":
               [("ButtonNotebook.label", {"side": "left", "sticky": 'nsew'}),
                ("ButtonNotebook.close", {"side": "left", "sticky": 'nsew'})]
            })]
        })]
    })]
)
style.configure("ButtonNotebook.Tab",width = 10)
def btn_press(event):
    x, y, widget = event.x, event.y, event.widget
    elem = widget.identify(x, y)
    index = widget.index("@%d,%d" % (x, y))
    if "close" in elem:
        widget.state(['pressed'])
        widget.pressed_index = index
def btn_release(event):
    x, y, widget = event.x, event.y, event.widget
    if not widget.instate(['pressed']):
        return
    elem =  widget.identify(x, y)
    index = widget.index("@%d,%d" % (x, y))
    if "close" in elem and widget.pressed_index == index:
        widget.forget(index)
        widget.event_generate("<<NotebookClosedTab>>")
    widget.state(["!pressed"])
    widget.pressed_index = None
root.bind_class("TNotebook", "<ButtonPress-1>", btn_press, True)
root.bind_class("TNotebook", "<ButtonRelease-1>", btn_release)

def newFile(*args):
        frame = ttk.Frame(n)
        n.add(frame, text='New Tab')
        n.select(frame)
        textPad = Text(frame,
                  background = "black",
                  foreground = "orange",
                  insertbackground = "white",
                  undo = True,
                  maxundo = -1,
                  padx = 0,
                  pady = 0,
                  bd = 0,
                  wrap = Tkinter.NONE,
                  highlightthickness = 0,
                  )
        textPad.grid(column=1, row = 0, sticky=N+W+S+E)
        textPad.mark_set("insert", "1.0")
        textPad.focus_set()
        lnText = Text(frame,
              background = "black",
              foreground = "white",
              insertbackground = "white",
              highlightthickness = 0,
              width = 4,
              padx = 0,
              pady = 0,
              bd = 0,
                 )
        lnText.grid(column = 0, row=0, sticky=W+N+S)
        lnText.insert(1.0, "1\n")
        tabs.update({n.index("current") : [textPad, lnText]})
    
def lineNumbers(self, *args):
    startIndex = '2.0'
    linecount = int(textPad.index("end-1c").split('.')[0])+1
    tIndex = textPad.index("insert")
    lnText.delete('2.0', END)
    for i in range(linecount):
        if i > 1:
            lnText.insert("insert", str(i) + '\n')
    lnText.see(tIndex)
    textPad.see(tIndex)
    
def currentTab(*args):
    global textPad
    global lnText
    texts = tabs[n.index("current")]
    textPad = texts[0]
    lnText = texts[1]
    root.after(500, currentTab)
        
n = ttk.Notebook(root, style="ButtonNotebook")
n.grid()
frame = ttk.Frame(n)
n.add(frame, text='New Tab')
n.select(frame)
textPad = Text(frame,
                      background = "black",
                      foreground = "orange",
                      insertbackground = "white",
                      undo = True,
                      maxundo = -1,
                      padx = 0,
                      pady = 0,
                      bd = 0,
                      wrap = Tkinter.NONE,
                      highlightthickness = 0,
                      )
textPad.grid(column=1, row = 0, sticky=N+W+S+E)
textPad.mark_set("insert", "1.0")

lnText = Text(frame,
              background = "black",
              foreground = "white",
              insertbackground = "white",
              highlightthickness = 0,
              width = 4,
              padx = 0,
              pady = 0,
              bd = 0,
                           )
lnText.grid(column = 0, row=0, sticky=W+N+S)
lnText.insert(1.0, "1\n")

n.pressed_index = None
tabs.update({n.index("current") : [textPad, lnText]})
print tabs

root.bind("<Control-n>", newFile)
root.bind("<KeyRelease-Return>", lineNumbers)

root.after(0, currentTab())
root.mainloop()
