import Tkinter
import tkFileDialog
import tkMessageBox
from Tkinter import *
from ScrolledText import * 


tab = "\n"
spacetab = "    "

class utilities(object):
	@classmethod
	def __init__(self, textPad, customFont):
		self.textPad = textPad
		self.font = customFont
		self.tablength = 1
		
	@classmethod
	def backTab(self, *args):
		i = self.textPad.index(Tkinter.INSERT).split('.')
		self.textPad.delete(i[0] + '.0', i[0] + '.1')
		returnTab = i[0] + '.' + str(int(i[1]) - self.tablength)
		self.textPad.mark_set("insert", returnTab)

	@classmethod
	def forwardTab(self, *args):
		i = self.textPad.index("insert").split('.')
		self.textPad.mark_set("insert", i[0] + '.0')
		self.textPad.insert("insert", "\t")
		returnTab = i[0] + '.' + str(int(i[1]) + self.tablength)
		self.textPad.mark_set("insert", returnTab)
		
	#bound to Ctrl l
	@classmethod
	def newLine(self, *args):
			i = self.textPad.index("insert") # get index of current line "1.1" etc...
			ilist=i.split('.')
			lineinsert = str(ilist[0]) + '.end';
			self.textPad.mark_set("insert", lineinsert) #change the insertion marker location to end of line
			self.textPad.mark_gravity("insert",RIGHT)#set gravity so it inserts to the right of line
			self.textPad.insert("insert", "\n")
			
	#bound to Ctrl -
	#Zooms in on both frames
	@classmethod
	def zoom_in(self, *args):
			size = self.font.actual()["size"]+2
			self.font.configure(size=size)

	#bound to Ctrl +
	#Zooms out on both frames
	@classmethod
	def zoom_out(self, *args):
			size = self.font.actual()["size"]-2
			self.font.configure(size=max(size, 8))
#Next massive block dedicated to searching-----------------------------
	
#bound to enter
class searches(object):
	@classmethod
	def __init__(self, textPad, lnText, searchDiag):
		self.searchStartIndex = 0
		self.searchindex = 0
		self.searchtext = ''
		self.searchList = []
		self.searchDiag = searchDiag
		self.textPad = textPad
		self.lnText = lnText

		#bound to Ctrl - f
	@classmethod
	def searchInit(self, *args):
		self.searchDiag.grid(row=2, columnspan=2) 
		self.searchDiag.focus_set() # sets focus to the search bar at the bottom

	@classmethod
	def searchClear(self, *args):
		self.searchDiag.delete("1.0", END)

	@classmethod
	#bound to esc
	def doneSearch(self, *args):#on pressing escape, resets search bar to defaults
		self.searchDiag.grid_forget()#hides the search bar
		self.searchClear()
		self.textPad.focus_set()
		self.textPad.tag_delete("searchMatch")
		self.searchStartIndex = 0
		self.searchList = []
		self.searchindex = 0
		self.searchtext = ''
		
	@classmethod
	def searchReturn(self, *args):#pressing enter initializes the list of indexes for the search
		self.searchtext = self.searchDiag.get('1.0', "end-1c")
		text = self.searchtext
		if text == '':
				self.doneSearch()
				return "break"
		self.searchClear()
		startIndex = '1.0'
		while True:
			startIndex = self.textPad.search(text, startIndex, "end")
			if startIndex:
				endIndex = self.textPad.index("%s + %sc" % (startIndex, len(text))) # find end of k
				self.searchList.append(startIndex)
				startIndex = endIndex # reset startIndex to continue searching
			else:
				break
		self.searchNext()
		
	@classmethod
	#bound to Down
	def searchNext(self, *args):
		self.searchindex = self.searchindex + 1		#Iterates forwards through the list
		if self.searchStartIndex == 0:				#if the tag is detected in the program it is deleted
			self.searchindex = 0					#after that however, a new tag is made at the current
			self.searchStartIndex += 1				#search index, which will be deleted upon calling for the
		if self.searchindex >= len(self.searchList):#next search index
			self.searchindex = 0					#this will work between both forward and backwards indexing
		if "searchMatch" in self.textPad.tag_names():
			self.textPad.tag_delete("searchMatch")
		startIndex = self.searchList[self.searchindex]
		endIndex = self.textPad.index("%s + %sc" % (startIndex, len(self.searchtext)))
		self.textPad.see(startIndex)
		self.textPad.mark_set("insert", startIndex)
		self.textPad.tag_add("searchMatch", startIndex, endIndex)
		self.textPad.tag_config("searchMatch", background = "gray")
		self.textPad.update()
		self.searchClear()
		self.searchDiag.insert("insert", "Match #: " + str(self.searchindex))

	@classmethod
	#bound to Up
	def searchLast(self, *args):				#Iterates backwards through the list
		if self.searchStartIndex == 0:
			self.searchindex = len(self.searchList)
			self.searchStartIndex += 1
		self.searchindex = self.searchindex - 1
		if self.searchindex < 0:
			self.searchindex = len(self.searchList) - 1
		if "searchMatch" in self.textPad.tag_names():
			self.textPad.tag_delete("searchMatch")
		startIndex = self.searchList[self.searchindex]
		endIndex = self.textPad.index("%s + %sc" % (startIndex, len(self.searchtext)))
		self.textPad.see(startIndex)
		self.textPad.mark_set("insert", startIndex)
		self.textPad.tag_add("searchMatch", startIndex, endIndex)
		self.textPad.tag_config("searchMatch", background = "gray")
		self.textPad.update()
		self.searchClear()
		self.searchDiag.insert("insert", "Match #: " + str(self.searchindex))

#-----------------------END SEARCH DEDICATION------------------------------