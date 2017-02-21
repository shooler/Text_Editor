import Tkinter
import font
import tkFileDialog
import tkMessageBox
import sys
import file
import windows
import ttk
import config
import utilityKeys
import itertools
import textConfig
from Tkinter import *
from ScrolledText import * # Because Tkinter textarea does not provide scrolling
from font import *
from windows import *
from textConfig import *



ukeys = utilityKeys
customfont = windows.customFont
mast = windows.root
searches = windows.searches

class main(object):
	def __init__(self,master):
			self.upd = 'on'
			self.master = master
			self.lineTracker = []
			fchange = font.fontChange()
			self.res = 0
			self.tabcount = 0
			self.toggleDevColors()
			textPad = windows.textPad
			searchDiag = windows.searchDiag
			
			
			menu = Menu(master)
			master.config(menu=menu)
			filemenu = Menu(menu, tearoff=0)
			menu.add_cascade(label="File", menu=filemenu)
			filemenu.add_command(label="New", command=windows.newTab)
			filemenu.add_command(label="Open", command=lambda: file.open_file(''))
			filemenu.add_command(label="Save", command=file.save_file)
			filemenu.add_separator()
			filemenu.add_command(label="Exit", command=file.exit)
			
			
			stylemenu = Menu(menu, tearoff=0)
			menu.add_cascade(label="Style", menu=stylemenu)
			stylemenu.add_command(label="Colors", command=self.popup)
			stylemenu.add_command(label="Fonts", command=lambda:fchange.startwindow(master))
			stylemenu.add_command(label="Resize: On", command=lambda: self.doublecall(stylemenu))
			stylemenu.add_command(label="Toggle Highlight", command = self.toggleDevColors)
			
			submenu = Menu(menu, tearoff=0)
			stylemenu.add_cascade(label="Presets", menu=submenu, underline=0)
			submenu.add_command(label = "White on Black", command=lambda:colors("white", "black", "white"))
			submenu.add_command(label = "Black on White", command=lambda:colors("black", "white", "black"))
			submenu.add_command(label = "Midnight", command=lambda:colors("light blue", "dark slate gray", "light blue"))
			
			helpmenu = Menu(menu, tearoff=0)
			menu.add_cascade(label="Help", menu=helpmenu)
			helpmenu.add_command(label="About...", command=self.about)
			
			#Non page specific keybinds
			#Page specific binds located in windows.py
			textPad.bind("<Up>", self.scrollup)
			textPad.bind("<Down>", self.scrolldn)
			master.bind_class("Text", "<Control-o>", file.open_file)
			master.bind("<Control-s>", file.save_file)
			master.bind("<Control-q>", file.exit)
			master.bind("<Control-Key-n>", windows.newTab)			
			master.bind("<Shift-MouseWheel>", windows.on_horizontal)
			#Utility (non file keybinds)
			master.bind("<Control-Key-f>", ukeys.searches.searchInit)
			#end keybinds
			self.master.after(0, windows.currentTab())
			self.master.mainloop()
			
	def toggleDevColors(self,*args):
		if self.upd == 'on':
			self.upd = "off"
			textConfig.textColor(windows.textPad, '', 'off')
			textConfig.textColor.toggleHighlights()
		else:
			self.upd = 'on'
			textConfig.textColor(windows.textPad, '/', 'on')
			textConfig.textColor.toggleHighlights()
					
		
	def doublecall(self, x):
		self.increment()
		windows.resizeMe(self.res)
		self.clicked(self.res, x)
		
	def increment(self):
		self.res += 1
	
	def clicked(self, res, x):
		if res %2 == 0:
			x.entryconfigure(3, label = "Resize: On")
		else:
			x.entryconfigure(3, label = "Resize: Off")
		
	#Track scrolling on arrowdown (line numbers will now correspond with actual lines)
	def scrolldn(self, thing):
			i = textPad.index(Tkinter.INSERT)
			ilist = i.split('.')
			ilist[0] = int(ilist[0])
			ilist[0] += 1
			lnText.mark_set("insert", str(ilist[0]) + '.' + str(ilist[1]))
			lnText.see(str(ilist[0])+ '.0')
	
	#Track scrolling on arrowup (line numbers will now correspond with actual lines)
	def scrollup(self, thing):
			i = textPad.index(Tkinter.INSERT)
			ilist = i.split('.')
			ilist[0] = int(ilist[0])
			ilist[0] -= 1
			lnText.mark_set("insert", str(ilist[0]) + '.' + str(ilist[1]))
			lnText.see(str(ilist[0])+ '.0')
			addline = False
			
	def popup(self):
			self.w=popupWindow(self.master)
			self.master.wait_window(self.w.top)
			
	def about(self):
		label = tkMessageBox.showinfo("About", "Its and editor ya dingus")

	def dummy(self, *args):
		return
		
class popupWindow(object):
	def __init__(self,master):
		top=self.top=Toplevel(master)
		self.l=Label(top,text="Enter Colors: Foreground, Background")
		self.l.pack()
		self.fg=Entry(top)
		self.fg.pack()
		self.bg=Entry(top)
		self.bg.pack()
		self.b=Button(top, text='OK', command=self.colorchange)
		self.b.pack()

	def colorchange(self):
			textPad.configure(foreground = str(self.fg.get()))
			textPad.configure(background = str(self.bg.get()))
			lnText.configure(foreground = str(self.fg.get()))
			lnText.configure(background = str(self.bg.get()))
			self.top.destroy()
			
def colors(fore, back, insert):
			textPad.configure(foreground = fore, background = back, insertbackground = insert)	
			lnText.configure(foreground = fore, background = back, insertbackground = insert)