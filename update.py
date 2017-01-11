import Tkinter
import windows
import textConfig
import re
import config
from Tkinter import *

textPad = windows.textPad
cfg = config


def callAll(*args):
	startIndex, endofline = textPad.index("insert").split('.')
	endofline = startIndex + '.' + endofline
	startIndex = startIndex + '.0'
	imports(startIndex, endofline)
	defs(startIndex, endofline)
	for i in textConfig.defslist:
		k = i
		savedDefs(startIndex, endofline, k)
	keyColor(startIndex, endofline)
	selfUpdate(startIndex, endofline)
	updateComments(startIndex, endofline)
	updateQuoteColors(startIndex, endofline)

def updateQuoteColors(startIndex, endofline):
	countVar = Tkinter.StringVar()
	while True:
		startIndex = textPad.search(r"['\"](.*)['\"]", startIndex, endofline, count=countVar, regexp=True)
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
			if v not in textConfig.defslist:
				textConfig.defslist.append(v)
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
		startIndex = textPad.search(r'(?:import\s.*)(?=$)', startIndex, endofline, count=countVar, regexp=True)
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
		r = r'(if\s|elif\s|else\s|def\s|import\s|global\s|len(?:\()|for\s|and\s|(range)(?:[(])|print\s|int(?:\()|str(?:\()|float(:?\()|break|True|False|while\s|in\s|lambda\s|not\s)'
		startIndex = textPad.search(r, startIndex, endofline, count = countVar, regexp=True) # search for occurence of k
		if startIndex:
			if '(' in textPad.get(startIndex, endofline):
				endIndex = textPad.index('%s+%sc' % (startIndex, (str(int(countVar.get())-1)))) # find end of k
			else:
				endIndex = textPad.index('%s+%sc' % (startIndex, (countVar.get())))
			textPad.tag_add("keyColor", startIndex, endIndex) # add tag to k
			textPad.tag_config("keyColor", foreground=cfg.colors['keyColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			