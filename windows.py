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


cfg = config
defslist = []
tabs = {}
frameName = 1

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
	global frameName
	frameName = frameName + 1
	tabName = "New Tab"
	if '/' in args[0]:
		tabName = args[0].split('/')[-1]
	frame = ttk.Frame(n, name = str(frameName))
	n.add(frame, text=tabName)
	n.select(frame)
	scrollbar = Scrollbar(frame)
	xscrollbar = Scrollbar(frame,  orient = HORIZONTAL, width=0)
	textPad = Text(frame, name = 'textPad',
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
	lnText = Text(frame, name = 'lnText',
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
	scrollbar.pack(side= RIGHT, fill = 'y')
	lnText.insert(1.0, "1\n")
	lnText.pack(side= LEFT, fill = 'y')#.grid(column=0, row = 1, rowspan=2, sticky=N+S+E+W)
	textPad.pack(side= LEFT, expand = True, fill = BOTH)#.grid(column=1, row = 1, rowspan=2, sticky=W+E+N+S)
	scrollbar.pack(side= RIGHT, fill = 'y')
	tabs.update({n.select() : [textPad, lnText]})
	currentTab()
	
	
def currentTab(*args):
	global textPad
	global lnText
	texts = tabs[n.select()]
	textPad = texts[0]
	lnText = texts[1]
	root.after(500, currentTab)
	scrollbar['command'] = on_scrollbar
	xscrollbar['command'] = textPad.xview
	textPad['yscrollcommand'] = on_textscroll
	lnText['yscrollcommand'] = on_textscroll
	textPad.bind("<KeyRelease-space>", callAll)
	textPad.bind("<Return>", callAll)
	textPad.bind("<KeyRelease-Down>", callAll)
	textPad.bind("<KeyRelease-Up>", callAll)

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
	


def callAll(*args):
	startIndex, endofline = textPad.index("insert").split('.')
	endofline = startIndex + '.' + endofline
	startIndex = startIndex + '.0'
	imports(startIndex, endofline)
	puncs(startIndex, endofline)
	for i in defslist:
		savedDefs(startIndex, endofline, i)
	keyColor(startIndex, endofline)
	dots(startIndex, endofline)
	selfUpdate(startIndex, endofline)
	updateComments(startIndex, endofline)
	updateQuoteColors(startIndex, endofline)
	
def callOnce(*args):
	startIndex = '1.0'
	endofline = 'end'
	imports(startIndex, endofline)
	puncs(startIndex, endofline)
	defs(startIndex, endofline)
	keyColor(startIndex, endofline)
	dots(startIndex, endofline)
	selfUpdate(startIndex, endofline)
	updateComments(startIndex, endofline)
	updateQuoteColors(startIndex, endofline)
	
def updateQuoteColors(startIndex, endofline):
	countVar = Tkinter.StringVar()
	while True:
		startIndex = textPad.search(r"('|\")[^\"']*('|\")", startIndex, endofline, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			textPad.tag_add("searchquotes", startIndex, endIndex)
			textPad.tag_config("searchquotes", foreground = cfg.colors['quoteColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def updateComments(startIndex, endofline):
	countVar = Tkinter.StringVar()
	while True:
		startIndex = textPad.search(r"[^\"](?:#)(.*)", startIndex, endofline, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			textPad.tag_add("comments", startIndex, endIndex)
			textPad.tag_config("comments", foreground = cfg.colors['commentColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break

#(?:def\s)(.*)(?=[(])
def defs(startIndex, endofline):
	countVar = Tkinter.StringVar()
	while True:
		startIndex = textPad.search(r'def\s(.*?)\(', startIndex, endofline, count=countVar, regexp=True)
		if startIndex:
			slist = startIndex.split('.')
			slist[1] = str(int(slist[1])+ 3)
			startIndex = '.'.join(slist)
			endIndex = textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-4))) # find end of k
			v = textPad.get(startIndex, endIndex)
			if v not in defslist:
				defslist.append(v)
			textPad.tag_add("defs", startIndex, endIndex)
			textPad.tag_config("defs", foreground = cfg.colors['defColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
def savedDefs(startIndex, endofline, k):
 	countVar = Tkinter.StringVar()
	while True:
		startIndex = textPad.search(r'(' + k + '\(\))', startIndex, endofline, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-2))) # find end of k
			textPad.tag_add("saveddefs", startIndex, endIndex)
			textPad.tag_config("saveddefs", foreground = cfg.colors['defColor']) 
			variable = textPad.get(startIndex, endIndex)
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def selfUpdate(startIndex, endofline):
	countVar = Tkinter.StringVar()
	while True:
		startIndex = textPad.search(r'self[\.]|self[\(]', startIndex, endofline, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex)
			textPad.tag_add("selfTag", startIndex, endIndex)
			textPad.tag_config("selfTag", foreground = cfg.colors['selfColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def imports(startIndex, endofline):
	countVar = Tkinter.StringVar()
	while True:
		startIndex = textPad.search('(?:import\s.*)(?=$)', startIndex, endofline, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex)
			textPad.tag_add("imp", startIndex, endIndex)
			textPad.tag_config("imp", foreground = cfg.colors['importColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break

def keyColor(startIndex, endofline):
	'''the highlight function, called when a Key-press event occurs'''
	countVar = Tkinter.StringVar()
	while True:
		r = r'(\sif\s|\selif\s|\selse|\sdef\s|import\s|global\s|len(?:\()|\sfor\s|\sand\s|(range)(?:[(])|print\s|int(?:\()|str(?:\()|float(:?\()|break|True|False|\swhile\s|\sin\s|lambda\s|not\s)'
		startIndex = textPad.search(r, startIndex, endofline, count = countVar, regexp=True) # search for occurence of k
		if startIndex:
			endIndex = textPad.index('%s+%sc' % (startIndex, (countVar.get())))
			if '(' in textPad.get(startIndex, endIndex):
				endIndex = textPad.index('%s+%sc' % (startIndex, (str(int(countVar.get())-1)))) # find end of k
			textPad.tag_add("keyColor", startIndex, endIndex) # add tag to k
			textPad.tag_config("keyColor", foreground=cfg.colors['keyColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break

def puncs(startIndex, endofline):
	countVar = Tkinter.StringVar()
	while True:
		r = r'(\=|\=\=|\!\=|\<|\<\=|\>|\>\=|\+|\-|\*|\/|\\|\%|\*\*|\+\=|\-\=|\*\=|\/\=|\%\=|\^|\||\&|\~|\>\>|\<\<|\{|\}|\(|\)|\[|\]|\,|\.|\:|\;)'
		startIndex = textPad.search(r, startIndex, endofline, count = countVar, regexp=True) # search for occurence of k
		if startIndex:
			endIndex = textPad.index('%s+%sc' % (startIndex, (countVar.get())))
			textPad.tag_add("puncolor", startIndex, endIndex) # add tag to k
			textPad.tag_config("puncolor", foreground=cfg.colors['puncColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def dots(startIndex, endofline):
	countVar = Tkinter.StringVar()
	while True:
		r = '(\.[^(\"\']*)'
		startIndex = textPad.search(r, startIndex, endofline, count = countVar, regexp=True) # search for occurence of k
		if startIndex:
			endIndex = textPad.index('%s+%sc' % (startIndex, (countVar.get())))
			textPad.tag_add("dotColor", startIndex, endIndex) # add tag to k
			textPad.tag_config("dotColor", foreground=cfg.colors['dotColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
	
root.bind_class("TNotebook", "<ButtonPress-1>", btn_press, True)
root.bind_class("TNotebook", "<ButtonRelease-1>", btn_release)

customFont = tkFont.Font(family="Ubuntu Mono", size=12)
displayfont = tkFont.Font(family = "Ubuntu Mono", size = 12)


n = ttk.Notebook(root, style="ButtonNotebook", name = 'n')
frame = ttk.Frame(n, name = '1')
n.add(frame, text='New Tab')
n.select(frame)
scrollbar = Scrollbar(frame)
xscrollbar = Scrollbar(frame,  orient = HORIZONTAL, width=0)
textPa = Text(frame, name = 'textPad',
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
textPa.mark_set("insert", "1.0")

lnTex = Text(frame, name = 'lnText',
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
lnTex.insert(1.0, "1\n")
	
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

n.grid(row = 0, column = 0, rowspan = 1, columnspan = 3,sticky=N+S+E+W)
searchDiag.grid(row = 1, columnspan = 2, sticky = E+W)
lnText.pack(side= LEFT, fill = 'y')#.grid(column=0, row = 1, rowspan=2, sticky=N+S+E+W)
textPad.pack(side= LEFT, expand = True, fill = BOTH)#.grid(column=1, row = 1, rowspan=2, sticky=W+E+N+S)
scrollbar.pack(side= RIGHT, fill = 'y')
searchDiag.grid_forget()#hides the search bar(default)