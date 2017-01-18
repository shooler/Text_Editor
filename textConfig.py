import ttk
import Tkinter
import windows
import config as cfg
from Tkinter import *

defslist = []


class textColor(object):
	@classmethod
	def __init__(self, textPad, filepass, toggle):
		self.textPad = textPad
		self.filepass = filepass
		self.toggle = toggle
	@classmethod
	def toggleHighlights(self, *args):
		for tag in windows.textPad.tag_names():
			windows.textPad.tag_delete(tag)
		if self.toggle == "on":
			self.cancelColoring = False
			self.callAll()
		else:
			self.cancelColoring = True
	@classmethod
	def callAll(self, *args):
		if self.cancelColoring:
			return
		if '/' in self.filepass:
			startIndex = '1.0'
			endofline = 'end'
		else:
			startIndex, endofline = self.textPad.index("insert").split('.')
			endofline = startIndex + '.' + endofline
			startIndex = startIndex + '.0'
			self.defs(startIndex, endofline)
			for i in defslist:
				self.savedDefs(startIndex, endofline, i)
			self.defs(startIndex, endofline)
		self.imports(startIndex, endofline)
		self.puncs(startIndex, endofline)
		self.keyColor(startIndex, endofline)
		self.dots(startIndex, endofline)
		self.selfUpdate(startIndex, endofline)
		self.updateComments(startIndex, endofline)
		self.updateQuoteColors(startIndex, endofline)
	@classmethod
	def updateQuoteColors(self, startIndex, endofline):
		countVar = Tkinter.StringVar()
		while True:
			startIndex = self.textPad.search("('[^']*'|\"[^\"]*\")", startIndex, endofline, count=countVar, regexp=True)
			if startIndex:
				endIndex = self.textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
				self.textPad.tag_add("searchquotes", startIndex, endIndex)
				self.textPad.tag_config("searchquotes", foreground = cfg.colors['quoteColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
	@classmethod
	def updateComments(self, startIndex, endofline):
		countVar = Tkinter.StringVar()
		while True:
			startIndex = self.textPad.search(r"(?![\"'])(?:#)(.*)(?![\"'])", startIndex, endofline, count=countVar, regexp=True)
			if startIndex:
				endIndex = self.textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
				self.textPad.tag_add("comments", startIndex, endIndex)
				self.textPad.tag_config("comments", foreground = cfg.colors['commentColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break

	#(?:def\s)(.*)(?=[(])
	@classmethod
	def defs(self, startIndex, endofline):
		countVar = Tkinter.StringVar()
		while True:
			startIndex = self.textPad.search(r'def\s(.*?)\(', startIndex, endofline, count=countVar, regexp=True)
			if startIndex:
				slist = startIndex.split('.')
				slist[1] = str(int(slist[1])+ 3)
				startIndex = '.'.join(slist)
				endIndex = self.textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-4))) # find end of k
				v = self.textPad.get(startIndex, endIndex)
				if v not in defslist:
					defslist.append(v)
				self.textPad.tag_add("defs", startIndex, endIndex)
				self.textPad.tag_config("defs", foreground = cfg.colors['defColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
	@classmethod
	def savedDefs(self, startIndex, endofline, k):
		countVar = Tkinter.StringVar()
		while True:
			startIndex = self.textPad.search(r'(' + k + '\(\))', startIndex, endofline, count=countVar, regexp=True)
			if startIndex:
				endIndex = self.textPad.index("%s + %sc" % (startIndex, str(int(countVar.get())-2))) # find end of k
				self.textPad.tag_add("saveddefs", startIndex, endIndex)
				self.textPad.tag_config("saveddefs", foreground = cfg.colors['defColor']) 
				variable = self.textPad.get(startIndex, endIndex)
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
	@classmethod
	def selfUpdate(self, startIndex, endofline):
		countVar = Tkinter.StringVar()
		while True:
			startIndex = self.textPad.search(r'self[\.]|self[\(]', startIndex, endofline, count=countVar, regexp=True)
			if startIndex:
				endIndex = self.textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
				variable = self.textPad.get(startIndex, endIndex)
				self.textPad.tag_add("selfTag", startIndex, endIndex)
				self.textPad.tag_config("selfTag", foreground = cfg.colors['selfColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
	@classmethod
	def imports(self, startIndex, endofline):
		countVar = Tkinter.StringVar()
		while True:
			startIndex = self.textPad.search('(?:import\s.*)(?=$)', startIndex, endofline, count=countVar, regexp=True)
			if startIndex:
				endIndex = self.textPad.index("%s + %sc" % (startIndex, countVar.get())) # find end of k
				variable = self.textPad.get(startIndex, endIndex)
				self.textPad.tag_add("imp", startIndex, endIndex)
				self.textPad.tag_config("imp", foreground = cfg.colors['importColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
	@classmethod
	def keyColor(self, startIndex, endofline):
		'''the highlight function, called when a Key-press event occurs'''
		countVar = Tkinter.StringVar()
		while True:
			r = r'((?!\w)\d|((\\h)*if\s)|\sNone|((\\h)*elif\s)|((\\h)*else)|((\\h)*def\s)|(^import\s)|((\\h)*global\s)|len(?:\()|((\\h)*for\s)|((\\h)*and\s)|(range)(?:[(])|print\s|int(?:\()|str(?:\()|float(:?\()|break|True|False|((\\h)*while\s)|((\\h)*in\s)|lambda\s|not\s|def\s)'
			startIndex = self.textPad.search(r, startIndex, endofline, count = countVar, regexp=True) # search for occurence of k
			if startIndex:
				endIndex = self.textPad.index("%s + %sc" % (startIndex, (countVar.get())))
				if '(' in self.textPad.get(startIndex, endIndex):
					endIndex = self.textPad.index("%s + %sc" % (startIndex, (str(int(countVar.get())-1)))) # find end of k
				self.textPad.tag_add("keyColor", startIndex, endIndex) # add tag to k
				self.textPad.tag_config("keyColor", foreground=cfg.colors['keyColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
	@classmethod
	def puncs(self, startIndex, endofline):
		countVar = Tkinter.StringVar()
		while True:
			r = '(\\W)'
			startIndex = self.textPad.search(r, startIndex, endofline, count = countVar, regexp=True) # search for occurence of k
			if startIndex:
				endIndex = self.textPad.index('%s+%sc' % (startIndex, (countVar.get())))
				self.textPad.tag_add("puncolor", startIndex, endIndex) # add tag to k
				self.textPad.tag_config("puncolor", foreground=cfg.colors['puncColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
	@classmethod
	def dots(self, startIndex, endofline):
		countVar = Tkinter.StringVar()
		while True:
			r = '(\.(?![0-9])[^(\"\']*)'
			startIndex = self.textPad.search(r, startIndex, endofline, count = countVar, regexp=True) # search for occurence of k
			if startIndex:
				endIndex = self.textPad.index('%s+%sc' % (startIndex, (countVar.get())))
				self.textPad.tag_add("dotColor", startIndex, endIndex) # add tag to k
				self.textPad.tag_config("dotColor", foreground=cfg.colors['dotColor'])      # and color it with v
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break