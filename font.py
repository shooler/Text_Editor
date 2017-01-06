import Tkinter
import tkFileDialog
import tkMessageBox
import sys
import tkFont
import windows
from windows import *
from Tkinter import *

customfont = windows.customFont

class fontChange(object):
#def __init__(self,master):
	def startwindow(self, master):
		self.master = master
		top=self.top=Toplevel(self.master)
		self.l=Label(top,text="Change font")
		self.l.pack()

		self.lbf=Listbox(top, exportselection = 0)
		self.lbf.pack(side = LEFT, expand = True)
		self.lbf.insert(END, "")
		for item in tkFont.families():
				self.lbf.insert(END, item)

		self.lbs=Listbox(top, exportselection = 0)
		self.lbs.pack(side = RIGHT, expand = True)
		self.lbs.insert(END, "")
		for item in range(12, 34):
				self.lbs.insert(END, item)

		self.fbutton=Button(top, text="Set", command=self.finishFont)
		self.fbutton.pack(side = LEFT)

		self.sbutton=Button(top, text="Set", command=self.finishSize)
		self.sbutton.pack(side = RIGHT)

		top.bind("<Button-1>", self.setFont)

	
	def setFont(self, none):		
		if self.lbs.curselection() != None:
			fontsize=self.lbs.curselection()
			self.sizeval = self.lbs.get(fontsize[0], last=None)
		if self.lbf.curselection() != None:
			font=self.lbf.curselection()
			self.value = self.lbf.get(font[0], last=None)

	def finishFont(self):
		customfont = self.value

	def finishSize(self):
		customfont.configure(size = self.sizeval)