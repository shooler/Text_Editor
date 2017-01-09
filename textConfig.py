import Tkinter
import windows
import re
import config
from Tkinter import *
from windows import *
from decimal import *
from config import *

textPad = windows.textPad
cfg = config

variablesavestate = {}

highlightWords = ['if ', 'elif ', 'else ', 'def ', 'import ', 'global ',
				  'for ', 'and ', 'range ', 'print ', 'int(', 'str(',
				  'float(', 'break', 'True', 'False', 'while', 'in ', 'lambda']

def callAll(*args):
	variables()
	dotvariables()
	variableSaves()
	imports()
	keyColor()
	defs()
	updateQuoteColors()
	updateComments()
	argColors()
	selfUpdate()
	#textPad.after(2000, callAll)
	
	
def updateQuoteColors():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r"['\"](.*?)['\"]", startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			textPad.tag_add("searchquotes", startIndex, endIndex)
			textPad.tag_config("searchquotes", foreground = cfg.quoteColor)      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def updateComments():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r"(?:#)(.*)", startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			textPad.tag_add("comments", startIndex, endIndex)
			textPad.tag_config("comments", foreground = cfg.commentColor)      # and color it with v
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
			textPad.tag_add("defs", startIndex, endIndex)
			textPad.tag_config("defs", foreground = cfg.defColor)      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def selfUpdate():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'self\.?', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex)
			textPad.tag_add("selfTag", startIndex, endIndex)
			textPad.tag_config("selfTag", foreground = cfg.selfColor)      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def imports():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'(?:import.*)(?=$)', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex)
			textPad.tag_add("imp", startIndex, endIndex)
			textPad.tag_config("imp", foreground = cfg.importColor)      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def variables():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'([a-zA-Z0-9.\[\]]+ *)(?![==])([a-zA-Z0-9.\[\]]+ *)(?=[=]|[+=]|[-=])', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex).strip()
			variablesavestate.update({variable : cfg.varColor})
			textPad.tag_add("vartag", startIndex, endIndex)
			textPad.tag_config("vartag", foreground = cfg.varColor)      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
#TODO set up splitting on commas and only highlighting words
def argColors():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'\((.*?[^,])\):', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			slist = startIndex.split('.')
			slist[1] = str(int(slist[1])+1)
			startIndex = '.'.join(slist)
			endIndex = textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-3))) # find end of k
			variable = textPad.get(startIndex, endIndex).strip()
			variablesavestate.update({variable : cfg.varColor})
			textPad.tag_add("argtag", startIndex, endIndex)
			textPad.tag_config("argtag", foreground = cfg.varColor)      # and color it with v4
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def dotvariables():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'([a-zA-Z0-9.\[\]]+ *)(?=[.])', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex).strip()
			variablesavestate.update({variable : cfg.varColor})
			textPad.tag_add("dots", startIndex, endIndex)
			textPad.tag_config("dots", foreground = cfg.varColor)      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
#(,|\=)?
# r = r'/^=?,?' + k + '=?,?$/'
def variableSaves():
	for k,v in variablesavestate.iteritems(): # iterate over dict
		startIndex = '1.0'
		r = r'/^' + k + '$/'
		while True:
			startIndex = textPad.search(r, startIndex, END, regexp=True) # search for occurence of k
			if startIndex:
				endIndex = textPad.index('%s+%dc' % (startIndex, (len(k)))) # find end of k
				textPad.tag_add("saves", startIndex, endIndex) # add tag to k
				textPad.tag_config("saves", foreground=v)      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
				
def keyColor():
	'''the highlight function, called when a Key-press event occurs'''
	for k in (highlightWords): # iterate over dict
		startIndex = '1.0'
		while True:
			startIndex = textPad.search(k, startIndex, END) # search for occurence of k
			if startIndex:
				endIndex = textPad.index('%s+%dc' % (startIndex, (len(k)))) # find end of k
				textPad.tag_add(k, startIndex, endIndex) # add tag to k
				textPad.tag_config(k, foreground=cfg.keyColor)      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
			