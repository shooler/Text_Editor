import Tkinter
import windows
import re
import config
from Tkinter import *

textPad = windows.textPad
cfg = config

defslist = []


def callAll(*args):
	imports()
	defs()
	savedDefs()
	keyColor()
	puncs()
	dots()
	selfUpdate()
	updateComments()
	updateQuoteColors()
	
def updateQuoteColors():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search("r('|\")[^\"']*('|\")", startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			textPad.tag_add("searchquotes", startIndex, endIndex)
			textPad.tag_config("searchquotes", foreground = cfg.colors['quoteColor']) 
			nextIndex = str(int(endIndex.split('.')[1])+1)
			slist = startIndex.split('.')
			slist[1] = nextIndex
			startIndex = ('.').join(slist)# and color it with v
		else:
			break
			
def updateComments():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search("[^\"](?:#)(.*)", startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			textPad.tag_add("comments", startIndex, endIndex)
			textPad.tag_config("comments", foreground = cfg.colors['commentColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break

#(?:def\s)(.*)(?=[(])
def defs():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'def\s(.*?)\(', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			slist = startIndex.split('.')
			slist[1] = str(int(slist[1])+ 3)
			startIndex = '.'.join(slist)
			endIndex = textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-4))) # find end of k
			variable = textPad.get(startIndex, endIndex)
			defslist.append(variable.strip())
			textPad.tag_add("defs", startIndex, endIndex)
			textPad.tag_config("defs", foreground = cfg.colors['defColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def savedDefs():
 	countVar = Tkinter.StringVar()
 	for k in defslist:
 		startIndex = '1.0'
 		r = '(' + k + '\(\))'
 		while True:
 			startIndex = textPad.search(r, startIndex, END, count=countVar, regexp=True)
 			if startIndex:
 				endIndex = textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-2))) # find end of k
 				textPad.tag_add("saveddefs", startIndex, endIndex)
 				textPad.tag_config("saveddefs", foreground = cfg.colors['defColor']) 
 				variable = textPad.get(startIndex, endIndex)
 				startIndex = endIndex # reset startIndex to continue searching
 			else:
 				break
			
def selfUpdate():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search('self[\.]|self[\(]', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex)
			textPad.tag_add("selfTag", startIndex, endIndex)
			textPad.tag_config("selfTag", foreground = cfg.colors['selfColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def imports():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search('(?:import\s.*)(?=$)', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex)
			textPad.tag_add("imp", startIndex, endIndex)
			textPad.tag_config("imp", foreground = cfg.colors['importColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break


def keyColor():
	'''the highlight function, called when a Key-press event occurs'''
	startIndex = '1.0'
	countVar = Tkinter.StringVar()
	while True:
		r = '(if\s|elif\s|else\s|def\s|import\s|global\s|len(?:\()|for\s|and\s|(range)(?:[(])|print\s|int(?:\()|str(?:\()|float(:?\()|break|True|False|while\s|in\s|lambda\s|not\s)'
		startIndex = textPad.search(r, startIndex, END, count = countVar, regexp=True) # search for occurence of k
		if startIndex:
			endIndex = textPad.index('%s+%sc' % (startIndex, (countVar.get())))
			endIndex = textPad.index('%s+%sc' % (startIndex, (str(int(countVar.get()))))) # find end of k
			textPad.tag_add("keyColor", startIndex, endIndex) # add tag to k
			textPad.tag_config("keyColor", foreground=cfg.colors['keyColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def puncs():
	'''the highlight function, called when a Key-press event occurs'''
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		r = '(\=|\=\=|\!\=|\<|\<\=|\>|\>\=|\+|\-|\*|\/|\\|\%|\*\*|\+\=|\-\=|\*\=|\/\=|\%\=|\^|\||\&|\~|\>\>|\<\<|\{|\}|\(|\)|\[|\]|\,|\.|\:|\;)'
		startIndex = textPad.search(r, startIndex, END, count = countVar, regexp=True) # search for occurence of k
		if startIndex:
			endIndex = textPad.index('%s+%sc' % (startIndex, (countVar.get())))
			textPad.tag_add("puncolor", startIndex, endIndex) # add tag to k
			textPad.tag_config("puncolor", foreground=cfg.colors['puncColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break

def dots():
	'''the highlight function, called when a Key-press event occurs'''
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		r = '(\.(.*)\()'
		startIndex = textPad.search(r, startIndex, END, count = countVar, regexp=True) # search for occurence of k
		if startIndex:
			endIndex = textPad.index('%s+%sc' % (startIndex, (countVar.get())))
			textPad.tag_add("dotColor", startIndex, endIndex) # add tag to k
			textPad.tag_config("dotColor", foreground=cfg.colors['dotColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
