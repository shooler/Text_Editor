import Tkinter
import tkFont
from Tkinter import *
from ScrolledText import * # Because Tkinter textarea does not provide scrolling
import tkFileDialog
import tkMessageBox
import sys
	
root = Tkinter.Tk(className="Editor")
root.geometry("500x500")
root.pack_propagate(0)


def resizeMe(x):
	if x %2 == 0:
		root.resizable(1,1)
	if x %2 != 0:
		root.resizable(0,0)
	
customFont = tkFont.Font(family="Helvetica", size=12)

lnText = Text(root,
			  background = "black",
			  foreground = "white",
			  insertbackground = "white",
			  width = 4,
			  padx = 0,
			  bd = 0,
			  font = customFont,
			 )
lnText.pack(side=LEFT, fill='y')
lnText.insert(1.0, "1\n")



textPad = ScrolledText(root, width=100, height=25,
					  background = "black",
					  foreground = "white",
					  insertbackground = "white",
					  font = customFont,
					  undo = True,
					  maxundo = -1,
					  wrap = Tkinter.WORD
					  )
textPad.pack(side=LEFT, expand=TRUE, fill=BOTH)
textPad.mark_set("insert", "1.0")
textPad.focus_set()


searchDiag = Text(textPad,
				  background = "black",
				  foreground = "white",
				  insertbackground = "white",
				  height = 1,
				  padx = 0,
				  pady = 0,
				  bd = 0,
				  highlightthickness = 0,
				  font = customFont,
				  width = 100,
				 )
searchDiag.pack(side=BOTTOM, fill='x')