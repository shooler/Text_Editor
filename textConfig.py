import Tkinter
import windows
import re
from Tkinter import *
from windows import *
from decimal import *

textPad = windows.textPad

variablesavestate = {}

highlightWords = {'if ' : 'yellow',
				  'elif ': 'yellow',
				  'else ': 'yellow',
				  'def ' : 'yellow',
				  'import ' : 'yellow',
				  'global ' : 'yellow',
				  'for ' : 'yellow',
				  'range' : 'light blue',
				  'print' : 'yellow'
				 }

def callAll(*args):
	textPad.after(1000, callAll)
	variables()
	dotvariables()
	variableSaves()
	imports()
	highlighter()
	defs()
	updateQuoteColors()

def updateQuoteColors():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r"['\"](.*?)['\"]", startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			textPad.tag_add("search", startIndex, endIndex)
			textPad.tag_config("search", foreground="green")      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break

#(?:def\s)(?=[(])
def defs():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'(?:def\s)(.*)(?=[(])', startIndex, END, count=countVar, regexp=True)
		slist = startIndex.split('.')
		second = str(int(slist[1]) + 3)
		slist[1] = second
		startIndex = '.'.join(slist)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-3))) # find end of k
			variable = textPad.get(startIndex, endIndex)
			textPad.tag_add("defs", startIndex, endIndex)
			textPad.tag_config("defs", foreground="blue")      # and color it with v
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
			textPad.tag_config("imp", foreground="orange")      # and color it with v
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
			variablesavestate.update({variable : "orange"})
			textPad.tag_add("vartag", startIndex, endIndex)
			textPad.tag_config("vartag", foreground="orange")      # and color it with v
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
			variablesavestate.update({variable : "orange"})
			textPad.tag_add("dots", startIndex, endIndex)
			textPad.tag_config("dots", foreground="orange")      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break

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
				
def highlighter():
	'''the highlight function, called when a Key-press event occurs'''
	for k,v in highlightWords.iteritems(): # iterate over dict
		startIndex = '1.0'
		while True:
			startIndex = textPad.search(k, startIndex, END) # search for occurence of k
			if startIndex:
				endIndex = textPad.index('%s+%dc' % (startIndex, (len(k)))) # find end of k
				textPad.tag_add(k, startIndex, endIndex) # add tag to k
				textPad.tag_config(k, foreground=v)      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
			