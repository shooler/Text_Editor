import Tkinter
import tkFont
import ttk
from Tkinter import *
from ScrolledText import * # Because Tkinter textarea does not provide scrolling
import tkFileDialog
import tkMessageBox
import sys
import os
import config
	
tabs = {}
textPad = ''
lnText = ''

root = Tkinter.Tk(className="Editor")
root.geometry("500x500")
root.grid_propagate(1)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

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

def newTab(*args):
	tabName = "New Tab"
	frame = ttk.Frame(n)
	n.add(frame, text=tabName)
	n.select(frame)
	textPad = Text(frame,
						  background = "black",
						  foreground = config.colors['foregroundColor'],
						  insertbackground = "white",
						  font = customFont,
						  undo = True,
						  maxundo = -1,
						  padx = 0,
						  pady = 0,
						  bd = 0,
						  wrap = Tkinter.NONE,
						  highlightthickness = 0,
						  xscrollcommand = xscrollbar.set
						  )
	textPad.mark_set("insert", "1.0")
	textPad.focus_set()
	lnText = Text(frame,
				  background = "black",
				  foreground = config.colors["numLineColor"],
				  insertbackground = "white",
				  highlightthickness = 0,
				  width = 4,
				  padx = 0,
				  pady = 0,
				  bd = 0,
				  font = customFont,
				 )
	lnText.insert(1.0, "1\n")
	lnText.pack(side= LEFT, fill = 'y')#.grid(column=0, row = 1, rowspan=2, sticky=N+S+E+W)
	textPad.pack(side= LEFT, expand = True, fill = BOTH)#.grid(column=1, row = 1, rowspan=2, sticky=W+E+N+S)
	scrollbar.pack(side= RIGHT, fill = 'y')
	tabs.update({n.index("current") : [textPad, lnText]})
	
	
def currentTab(*args):
    global textPad
    global lnText
    texts = tabs[n.index("current")]
    textPad = texts[0]
    lnText = texts[1]
    root.after(500, currentTab)

def resizeMe(x):
	if x %2 == 0:
		root.resizable(1,1)
	if x %2 != 0:
		root.resizable(0,0)

def on_scrollbar(*args):
	'''Scrolls both text widgets when the scrollbar is moved'''
	textPad.yview(*args)
	lnText.yview(*args)
	

def on_textscroll(*args):
	'''Moves the scrollbar and scrolls text widgets when the mousewheel
	is moved on a text widget'''
	scrollbar.set(*args)
	on_scrollbar('moveto', args[0])
	
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

def on_horizontal(event):
    canvas.xview_scroll(-1 * -event.delta, 'units')
    
root.bind_class("TNotebook", "<ButtonPress-1>", btn_press, True)
root.bind_class("TNotebook", "<ButtonRelease-1>", btn_release)

customFont = tkFont.Font(family="Ubuntu Mono", size=12)
displayfont = tkFont.Font(family = "Ubuntu Mono", size = 12)


n = ttk.Notebook(root, style="ButtonNotebook")
frame = ttk.Frame(n)
n.add(frame, text='New Tab')
n.select(frame)
scrollbar = Scrollbar(frame)
xscrollbar = Scrollbar(frame,  orient = HORIZONTAL, width=0)
textPad = Text(frame,
					  background = "black",
					  foreground = config.colors['foregroundColor'],
					  insertbackground = "white",
					  font = customFont,
					  undo = True,
					  maxundo = -1,
					  padx = 0,
					  pady = 0,
					  bd = 0,
					  wrap = Tkinter.NONE,
					  highlightthickness = 0,
					  xscrollcommand = xscrollbar.set
					  )
textPad.mark_set("insert", "1.0")

lnText = Text(frame,
			  background = "black",
			  foreground = config.colors["numLineColor"],
			  insertbackground = "white",
			  highlightthickness = 0,
			  width = 4,
			  padx = 0,
			  pady = 0,
			  bd = 0,
			  font = customFont,
			 )
lnText.insert(1.0, "1\n")
	
searchDiag = Text(root,
				  background = "white",
				  foreground = "black",
				  insertbackground = "black",
				  height = 1,
				  padx = 0,
				  pady = 0,
				  bd = 0,
				  highlightthickness = 0,
				  font = customFont,
				  yscrollcommand=scrollbar.set
				 )


n.pressed_index = None
tabs.update({n.index("current") : [textPad, lnText]})

n.grid(row = 0, column = 0, rowspan = 1, columnspan = 3,sticky=N+S+E+W)
#n.columnconfigure(0, weight = 1)
#n.rowconfigure(0, weight = 1)

searchDiag.grid(row = 1, columnspan = 2, sticky = E+W)
lnText.pack(side= LEFT, fill = 'y')#.grid(column=0, row = 1, rowspan=2, sticky=N+S+E+W)
textPad.pack(side= LEFT, expand = True, fill = BOTH)#.grid(column=1, row = 1, rowspan=2, sticky=W+E+N+S)
scrollbar.pack(side= RIGHT, fill = 'y')


searchDiag.grid_forget()#hides the search bar(default)

# Changing the settings to make the scrolling work
scrollbar['command'] = on_scrollbar
xscrollbar['command'] = textPad.xview
textPad['yscrollcommand'] = on_textscroll
lnText['yscrollcommand'] = on_textscroll