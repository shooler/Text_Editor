import Tkinter
import windows
from Tkinter import *
from windows import *
from decimal import *

textPad = windows.textPad

count = 0
tagstart = 'x'
tagend = 'x'
changeTag = ''

highlightWords = {'if': 'yellow',
				  'elif': 'yellow',
				  'else': 'yellow',
				  'def' : 'yellow'
				 }
classlightWords = {'class ' : 'light blue',
				  'def '   : 'light blue'
				  }

def callAll(dummy):
	highlighter()
	Quotes()

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


def Quotes():
	global tagstart
	global tagend
	global changeTag
	global count
	ilist = map(int, textPad.index(Tkinter.INSERT).split('.'))
	if ilist[1] != 0:
		start = str(ilist[0]) + '.' + str(ilist[1] - 1)
	else:
		start = str(ilist[0]) + '.0'
	end = str(ilist[0]) + '.' + str(ilist[1]) #+ 1)
	key = textPad.get(start)
	if 'x' not in tagstart and 'x' not in tagend:
		textPad.tag_add(changeTag, tagstart, tagend)
		textPad.tag_config(changeTag, foreground = "green")
		tagstart = 'x'
		tagend = 'x'
		count = 0
	if ('"' in key or "'" in key) and count == 0:
		tagstart = str(start)
		count = 1
		key = ''
	if ('"' in key or "'" in key) and count == 1:
		tagend = str(end)
		count = 2
		key = ''
			
			
		