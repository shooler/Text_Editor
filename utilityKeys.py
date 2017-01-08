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
searchStartIndex = 0
searchindex = 0
searchtext = ''

#function/attribute imports
textPad = windows.textPad
lnText = windows.lnText
customfont = windows.customFont
searchDiag = windows.searchDiag
#imports

searchList = []

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


def lineNumbers(i, lineList):
			ilist=i.split('.', 1)
			lnText.see(i)
			insert = str(int(ilist[0]) + 1)
			lnText.mark_set("insert", insert + '.0')
			if i not in lineList: 
				#this keeps the program from adding already existing line numbers
				lnText.insert("insert", insert + "\n")
				lnText.update()
		
def searchInit(*args):
	searchDiag.focus_set()
	
def searchClear(*args):
	searchDiag.delete("1.0", END)

def doneSearch(*args):
	global searchStartIndex
	global searchIndex
	global searchtext
	searchClear()
	textPad.focus_set()
	textPad.tag_delete("searchMatch")
	searchStartIndex = 0
	searchindex = 0
	searchtext = ''
	
def searchReturn(*args):
	global searchStartIndex
	global searchList
	global searchtext
	text = searchDiag.get('1.0', "end-1c")
	searchtext = searchDiag.get('1.0', "end-1c")
	searchClear()
	startIndex = "1.0"
	while True:
		startIndex = textPad.search(text, startIndex, END)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, len(text))) # find end of k
			searchList.append(startIndex)
			startIndex = endIndex # reset startIndex to continue searching
	
def searchNext(*args):
	global searchindex
	global searchtext
	global searchStartIndex
	searchindex = searchindex + 1
	if searchStartIndex == 0:
		searchindex = 0
		searchStartIndex += 1
	if searchindex >= len(searchList):
		searchindex = 0
	if "searchMatch" in textPad.tag_names():
		textPad.tag_delete("searchMatch")
	startIndex = searchList[searchindex]
	endIndex = textPad.index("%s + %sc" % (startIndex, len(searchtext)))
	textPad.see(startIndex)
	textPad.mark_set("insert", startIndex)
	textPad.tag_add("searchMatch", startIndex, endIndex)
	textPad.tag_config("searchMatch", background = "gray")
	#removeSearchTag()
	textPad.update()
	searchClear()
	searchDiag.insert("insert", "Match #: " + str(searchindex))
	
def searchLast(*args):
	global searchindex
	global searchtext
	global searchStartIndex
	if searchStartIndex == 0:
		searchindex = len(searchList)
		searchStartIndex += 1
	searchindex = searchindex - 1
	if searchindex < 0:
		searchindex = len(searchList) - 1
	if "searchMatch" in textPad.tag_names():
		textPad.tag_delete("searchMatch")
	startIndex = searchList[searchindex]
	endIndex = textPad.index("%s + %sc" % (startIndex, len(searchtext)))
	textPad.see(startIndex)
	textPad.mark_set("insert", startIndex)
	textPad.tag_add("searchMatch", startIndex, endIndex)
	textPad.tag_config("searchMatch", background = "gray")
	#removeSearchTag()
	textPad.update()
	searchClear()
	searchDiag.insert("insert", "Match #: " + str(searchindex))
	
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