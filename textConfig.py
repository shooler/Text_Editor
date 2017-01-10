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

variablesavestate = []
arglist = []
defslist = []


highlightWords = ['if ', 'elif ', 'else', 'def ', 'import ', 'global ', 'len(' ,
				  'for ', 'and ', 'range( ', 'print ', 'int(', 'str(',
				  'float(', 'break', 'True', 'False', 'while', 'in ', 'lambda',
				 '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'not',
				 ]
#whitechars = ['[', ']', '{', '}', '(', ')', '=']


def callAll(*args):
	variables()
	imports()
	defs()
	savedDefs()
	argColors()
	dotvariables()
	#variableUpdate()
	keyColor()
	selfUpdate()
	updateQuoteColors()
	updateComments()
	
def updateQuoteColors():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r"['\"](.*?)['\"]", startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			textPad.tag_add("searchquotes", startIndex, endIndex)
			textPad.tag_config("searchquotes", foreground = cfg.colors['quoteColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
def updateComments():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r"[^\"](?:#)(.*)", startIndex, END, count=countVar, regexp=True)
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
 		r = r'(' + k + '\(\))'
 		while True:
 			startIndex = textPad.search(r, startIndex, END, count=countVar, regexp=True)
 			if startIndex:
 				endIndex = textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-2))) # find end of k
 				textPad.tag_add("saveddefs", startIndex, endIndex)
 				textPad.tag_config("saveddefs", foreground = cfg.colors['defColor']) 
 				variable = textPad.get(startIndex, endIndex)
 				#fxnColors("savedDefs", variable)
 				startIndex = endIndex # reset startIndex to continue searching
 			else:
 				break
			
def selfUpdate():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'self[\.]|self[\(]', startIndex, END, count=countVar, regexp=True)
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
		startIndex = textPad.search(r'(?:import\s.*)(?=$)', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex)
			textPad.tag_add("imp", startIndex, endIndex)
			textPad.tag_config("imp", foreground = cfg.colors['importColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
			
#TODO set up splitting on commas and only highlighting words
#r'\((.*?[^,])\):'
def argColors():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'\((.*?[^,0-9])\):', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			slist = startIndex.split('.')
			slist[1] = str(int(slist[1])+1)
			startIndex = '.'.join(slist)
			endIndex = textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-3))) # find end of k
			variable = textPad.get(startIndex, endIndex).strip()
			vlist = variable.split(',')
			for i in vlist:
				i = i.strip()
				if i not in arglist:
					arglist.append(i)
		else:
			break
	#([\(,]?[' + k + '](?=[ (])
	countVar = Tkinter.StringVar()
	if arglist:
		for k in arglist:	
			startIndex = '1.0'
			while True:
				for char in "[]()?^.":
					if char in k:
						k = ' '
				if '*' in k:
					k = re.sub(r'\*', '\\\*', k)
				for char in '0123456789 - +=':
					if char in k:
						k = re.sub(r'[0-9\-\+\=]', '', k)
				r = r'' + k + '(?=[\s*\,\)])'
				startIndex = textPad.search(r, startIndex, END, count = countVar, regexp=True) # search for occurence of k
				if startIndex:
					endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
					textPad.tag_add("argtag", startIndex, endIndex)
					textPad.tag_config("argtag", foreground = cfg.colors['varColor'])      # and color it with v4
					startIndex = endIndex # reset startIndex to continue searching
				else:
					break
				
def dotvariables():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'([a-zA-Z]+\s*)(?=[.]|[=])', startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex).strip()
			if variable not in variablesavestate:
				variablesavestate.append(variable.strip())
			textPad.tag_add("dots", startIndex, endIndex)
			textPad.tag_config("dots", foreground = cfg.colors['varColor'])      # and color it with v
			startIndex = endIndex # reset startIndex to continue searching
		else:
			break
#r'/^' + k + '$/'
# (?:\,|\s*|for|if|\+|\-)+'('+k+')'+(?:\s|\+|\-|in)

def variables():
	countVar = Tkinter.StringVar()
	startIndex = '1.0'
	while True:
		startIndex = textPad.search(r'([a-zA-Z]+\s?)|([a-zA-Z]+\s?)(?![==])([a-zA-Z]+\s?)(?=[=]|[+=]|[-=])(?:\\n)?'
									, startIndex, END, count=countVar, regexp=True)
		if startIndex:
			endIndex = textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
			variable = textPad.get(startIndex, endIndex).strip()
			for x in ["if", "in", "for", "define", "\n"]:
				variable = re.sub("^(?:if|in|for)$", '', variable)
				variable = re.sub("\\n(.*)", '', variable)
			if ' ' in variable:
				variable = re.sub("(.*)\s", '', variable)
			if variable not in variablesavestate and '[]' not in variable:
				variablesavestate.append(variable.strip())
			textPad.tag_add("vartag", startIndex, endIndex)
			textPad.tag_config("vartag", foreground = cfg.colors['varColor'])      # and color it with v
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
				if '(' not in k:
					endIndex = textPad.index('%s+%dc' % (startIndex, (len(k)))) # find end of k
				else:
					endIndex = textPad.index('%s+%dc' % (startIndex, (len(k)-1)))
					
				textPad.tag_add(k, startIndex, endIndex) # add tag to k
				textPad.tag_config(k, foreground=cfg.colors['keyColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
			
