import Tkinter
import tkFont
import ttk
from Tkinter import *
from ScrolledText import * # Because Tkinter textarea does not provide scrolling
import tkFileDialog
import tkMessageBox
import sys
	
root = Tkinter.Tk(className="Editor")
root.geometry("500x500")
root.grid_propagate(0)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)

def resizeMe(x):
	if x %2 == 0:
		root.resizable(1,1)
	if x %2 != 0:
		root.resizable(0,0)
	
customFont = tkFont.Font(family="Ubuntu Mono", size=12)
displayfont = tkFont.Font(family = "Ubuntu Mono", size = 12)


lnText = Text(root,
			  background = "black",
			  foreground = "white",
			  insertbackground = "white",
			  highlightthickness = 0,
			  width = 4,
			  padx = 0,
			  pady = 0,
			  bd = 0,
			  font = customFont,
			 )
lnText.grid(column = 0, row=0, sticky=W+N+S)
lnText.insert(1.0, "1\n")

scrollbar = Scrollbar(root)
scrollbar.grid(row = 0, column=2, sticky=N+S)
xscrollbar = Scrollbar(root,  orient = HORIZONTAL, width=0)
xscrollbar.grid(row=1)


textPad = Text(root,
					  background = "black",
					  foreground = "white",
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
textPad.grid(column=1, row = 0, sticky=N+W+S+E)
textPad.mark_set("insert", "1.0")
textPad.focus_set()
#textPad.configure(scrollregion=textPad.bbox(ALL))

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
searchDiag.grid(row = 2,columnspan=2, sticky=S)
searchDiag.grid_forget()#hides the search bar(default)

def on_scrollbar(*args):
	'''Scrolls both text widgets when the scrollbar is moved'''
	textPad.yview(*args)
	lnText.yview(*args)
	

def on_textscroll(*args):
	'''Moves the scrollbar and scrolls text widgets when the mousewheel
	is moved on a text widget'''
	scrollbar.set(*args)
	on_scrollbar('moveto', args[0])


# Changing the settings to make the scrolling work
scrollbar['command'] = on_scrollbar
xscrollbar['command'] = textPad.xview
textPad['yscrollcommand'] = on_textscroll
lnText['yscrollcommand'] = on_textscroll

def on_horizontal(event):
    canvas.xview_scroll(-1 * -event.delta, 'units')