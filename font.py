import Tkinter
import tkFileDialog
import tkMessageBox
import sys
import tkFont
import windows
from windows import *
from Tkinter import *

customfont = windows.customFont
displayfont = windows.displayfont

class fontChange(object):
	def startwindow(self, master):
		self.master = master
		top=self.top=Toplevel(self.master)
		self.l=Label(top,text="Change font", font = displayfont)
		self.l.pack()
		
		self.lbf=Listbox(top, exportselection = 0)
		self.lbf.pack(side = LEFT, expand = True)
		self.lbf.insert(END, "")
		self.fonts=list(tkFont.families())
		self.fonts.sort()
		for item in self.fonts:
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

	def finishFont(self):
		if self.lbf.curselection() != None:
			font=self.lbf.curselection()
			self.value = self.lbf.get(font[0])
		customfont.configure(family = self.value)
		displayfont.configure(family = self.value)

	def finishSize(self):
		if self.lbs.curselection() != None:
			sizeval = self.lbs.curselection()
			self.sizeval=self.lbs.get(sizeval[0])
		customfont.configure(size = self.sizeval)