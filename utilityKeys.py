import Tkinter
import tkFileDialog
import tkMessageBox
import windows
from windows import *
from Tkinter import *
from ScrolledText import * 


tab = "\n"
spacetab = "    "
tablength = 1

#function/attribute imports
textPad = windows.textPad
lnText = windows.lnText
customfont = windows.customFont
#imports

def getIndex(dummy):
	print textPad.index(Tkinter.INSERT)

def backTab(dummy):
	global tablength
	i = textPad.index(Tkinter.INSERT).split('.')
	textPad.delete(i[0] + '.0', i[0] + '.1')
	returnList = '.'.join(i)
	returnTab = i[0] + '.' + str(int(i[1]) - tablength)
	textPad.mark_set("insert", returnTab)
	
def forwardTab(dummy):
	global tablength
	i = textPad.index(Tkinter.INSERT).split('.')
	textPad.mark_set("insert", i[0] + '.0')
	textPad.insert("insert", "\t")
	returnList = '.'.join(i)
	returnTab = i[0] + '.' + str(int(i[1]) + tablength)
	textPad.mark_set("insert", returnTab)

#bound to Ctrl l
def newLine(dummy):
		i = textPad.index(Tkinter.INSERT) # get index of current line "1.1" etc...
		ilist=i.split('.', 1)
		lineinsert = str(ilist[0]) + '.end';
		textPad.mark_set("insert", lineinsert) #change the insertion marker location to end of line
		textPad.mark_gravity("insert",RIGHT)#set gravity so it inserts to the right of line
		textPad.insert("insert", "\n")
		new = lnText.get(1.0, END)
		lineNumbers(i, new)
		"""
		nextLine = str(int(ilist[0]) + 1)
		if nextLine not in new:
			lnText.mark_set("insert", ilist[0] + '.end')
			lnText.insert("insert", "\n")
			lnText.mark_set("insert", ilist[0] + '.0')
			lnText.insert("insert", ilist[0])
		"""
def lineNumbers(i, lineList):
			ilist=i.split('.', 1)
			lnText.see(i)
			insert = str(int(ilist[0]) + 1)
			lnText.mark_set("insert", insert + '.0')
			if i not in lineList: 
				#this keeps the program from adding already existing line numbers
				lnText.insert("insert", insert + "\n")
				lnText.update()
		
#bound to Ctrl -
#Zooms in on both frames
def zoom_in(dummy):
		font = customfont
		size = font.actual()["size"]+2
		font.configure(size=size)
		
#bound to Ctrl +
#Zooms out on both frames
def zoom_out(dummy):
		font = customfont
		size = font.actual()["size"]-2
		font.configure(size=max(size, 8))