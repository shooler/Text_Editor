import Tkinter
import tkFont
import ttk
import re
from Tkinter import *
from ScrolledText import * # Because Tkinter textarea does not provide scrolling
import tkFileDialog
import tkMessageBox
import sys
import os
import config
import textConfig
import utilityKeys
from textConfig import *

cfg = config
tabs = {}
tabcount = 0


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
style.configure("ButtonNotebook.Tab",width = 10, selected = "light blue")
style.map('ButtonNotebook.Tab',background=
    [('selected', "slate gray"), ('active', "dark slate gray")])


def lineNumbers(*args):
	index = textPad.index("insert")
	lnText.delete(1.0, "end-1c")
	i = int(textPad.index('end-1c').split('.')[0])
	for x in range(i):
		lnText.config(state = 'normal')
		if x != 0:
			lnText.insert("insert", '\n' + str(int(x+1)))
		else:
			lnText.insert("insert", str(int(x+1)))
	lnText.see(index)
	return "break"
			
def newLineAndlineNumbers(*args):
	utilities.newLine()
	lineNumbers()
	#This is a super lazy workaround to the ctrl-l function not updating line numbers
	
def newTab(*args):
	global frameName
	global tabcount
	if 'str' in str(type(args[0])):
		tabName = args[0].split('/')[-1]
		frameName = '__EDITORPADTAB__' + tabName.split('.')[0].lower()
	else:
		tabcount = tabcount + 1
		frameName = '__EDITORPADTAB__Tab' + str(tabcount) + "__UNSAVED__"
		tabName = "New Tab"
	frame = ttk.Frame(n, name = frameName)
	n.add(frame, text=tabName)
	n.select(frame)
	scrollbar = Scrollbar(frame)
	xscrollbar = Scrollbar(frame,  orient = HORIZONTAL, width=0)
	textPad = Text(frame, name = 'textPad',
						  background = config.colors['bgColor'],
						  foreground = config.colors['foregroundColor'],
						  insertbackground = config.colors['numLineColor'],
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
	lnText = Text(frame, name = 'lnText',
				  background = config.colors['bgColor'],
				  foreground = config.colors["numLineColor"],
				  insertbackground = config.colors["numLineColor"],
				  highlightthickness = 0,
				  width = 4,
				  padx = 3,
				  wrap = 'none',
				  pady = 0,
				  bd = 0,
				  font = customFont,
				  state = 'disabled'
				 )
	scrollbar.pack(side= RIGHT, fill = 'y')
	lnText.pack(side= LEFT, fill = 'y')#.grid(column=0, row = 1, rowspan=2, sticky=N+S+E+W)
	textPad.pack(side= LEFT, expand = True, fill = BOTH)#.grid(column=1, row = 1, rowspan=2, sticky=W+E+N+S)
	scrollbar.pack(side= RIGHT, fill = 'y')
	tabs.update({n.select() : [textPad, lnText]})
	textPad.focus_set()
	currentTab()
	tconf = textConfig.textColor(textPad, 'nofile', 'on')
	utilities = utilityKeys.utilities(textPad, customFont)
	lineNumbers()
	if 'str' in str(type(args[0])):
		textPad.configure(fg = config.colors["foregroundColor"])
		tconf.toggleHighlights()
	
def currentTab(*args):
	global textPad
	global lnText
	if n.select():
		texts = tabs[n.select()]
		textPad = texts[0]
		lnText = texts[1]
		root.after(500, currentTab)
		scrollbar['command'] = on_scrollbar
		xscrollbar['command'] = textPad.xview
		textPad['yscrollcommand'] = on_textscroll
		lnText['yscrollcommand'] = on_textscroll
		textPad.bind("<Return>", textConfig.textColor.callAll)
		textPad.bind("<KeyRelease-Left>", textConfig.textColor.callAll)
		textPad.bind("<KeyRelease-Right>", textConfig.textColor.callAll)
		textPad.bind("<KeyPress-Up>", textConfig.textColor.callAll)
		textPad.bind("<KeyPress-Down>", textConfig.textColor.callAll)
		textPad.bind("<KeyRelease-space>", textConfig.textColor.callAll)
		textPad.bind("<Control-Key-X>", lineNumbers)
		textPad.bind("<Control-Key-Z>", lineNumbers)
		textPad.bind("<KeyRelease-Return>", lineNumbers)
		textPad.bind("<KeyRelease-BackSpace>", lineNumbers)
		textPad.bind("<Control-Key-l>", newLineAndlineNumbers)
		textPad.bind("<Control-KP_Add>", utilities.zoom_in)
		textPad.bind("<Control-KP_Subtract>", utilities.zoom_out)
		textPad.bind("<Control-Key-comma>", utilities.backTab)
		textPad.bind("<Control-Key-period>", utilities.forwardTab)
		searchDiag.bind("<Down>", searches.searchNext)
		searchDiag.bind("<Up>", searches.searchLast)
		searchDiag.bind("<Return>", searches.searchReturn)
		searchDiag.bind_all("<Escape>", searches.doneSearch)
	
	
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
	searches = utilityKeys.searches(textPad, lnText, searchDiag)
	utilities = utilityKeys.utilities(textPad, customFont)
	tconf = textConfig.textColor(textPad, 'nofile', '')
	goto = tabs[n.select()][0]
	goto.focus_set()
	
def btn_release(event):
	x, y, widget = event.x, event.y, event.widget
	if not widget.instate(['pressed']):
		return
	elem =  widget.identify(x, y)
	index = widget.index("@%d,%d" % (x, y))
	if "close" in elem and widget.pressed_index == index:
		widget.forget(index)
		widget.event_generate("<<NotebookClosedTab>>")
		currentTab()
		utilities = utilityKeys.utilities(textPad, customFont)
		searches = utilityKeys.searches(textPad, lnText, searchDiag)
		tconf = textConfig.textColor(textPad, 'nofile', '')
		goto = tabs[n.select()][0]
		goto.focus_set()
	widget.state(["!pressed"])
	widget.pressed_index = None

def on_horizontal(event):
	canvas.xview_scroll(-1 * -event.delta, 'units')
			
root.bind_class("TNotebook", "<ButtonPress-1>", btn_press, True)
root.bind_class("TNotebook", "<ButtonRelease-1>", btn_release)

customFont = tkFont.Font(family="Ubuntu Mono", size=12)
displayfont = tkFont.Font(family = "Ubuntu Mono", size = 12)

n = ttk.Notebook(root, style="ButtonNotebook", name = 'n')
frame = ttk.Frame(n, name = '__EDITORPADTAB__Tab0')
n.add(frame, text='New Tab')
n.select(frame)
scrollbar = Scrollbar(frame)
xscrollbar = Scrollbar(frame,  orient = HORIZONTAL, width=0)
textPa = Text(frame, name = 'textPad',
					  background = config.colors["bgColor"],
					  foreground = config.colors['foregroundColor'],
					  insertbackground = config.colors['numLineColor'],
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
lnTex = Text(frame, name = 'lnText',
			  background = config.colors['bgColor'],
			  foreground = config.colors["numLineColor"],
			  insertbackground = config.colors["numLineColor"],
			  highlightthickness = 0,
			  width = 4,
			  padx = 3,
			  wrap = 'none',
			  pady = 0,
			  bd = 0,
			  font = customFont,
			  state = 'normal'
			)
lnTex.config(state = 'disabled')
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
tabs.update({n.select() : [textPa, lnTex]})
textPad = textPa
lnText = lnTex
lineNumbers()

n.grid(row = 0, column = 0, rowspan = 1, columnspan = 3,sticky=N+S+E+W)
searchDiag.grid(row = 1, columnspan = 2, sticky = E+W)
lnText.pack(side= LEFT, fill = 'y')#.grid(column=0, row = 1, rowspan=2, sticky=N+S+E+W)
textPad.pack(side= LEFT, expand = True, fill = BOTH)#.grid(column=1, row = 1, rowspan=2, sticky=W+E+N+S)
scrollbar.pack(side= RIGHT, fill = 'y')
searchDiag.grid_forget()#hides the search bar(default)
textPad.focus_set()

searches = utilityKeys.searches(textPad, lnText, searchDiag)
utilities = utilityKeys.utilities(textPad, customFont)
tconf = textConfig.textColor(textPad, 'nofile', 'off')
