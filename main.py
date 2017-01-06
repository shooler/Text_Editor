import Tkinter
import font
import tkFileDialog
import tkMessageBox
import sys
import tabs
import file
import windows
import ttk
from Tkinter import *
from ScrolledText import * # Because Tkinter textarea does not provide scrolling
from font import *
from windows import *
from tabs import *


highlightWords = {'if': 'yellow',
				  'elif': 'yellow',
				  'else': 'yellow',
				  'def' : 'yellow'
				 }
classlightWords = {'class ' : 'light blue',
				  'def '   : 'light blue'
				  }

def colors(fore, back, insert):
			textPad.configure(foreground = fore, background = back, insertbackground = insert)	
			lnText.configure(foreground = fore, background = back, insertbackground = insert)

customfont = windows.customFont
mast = windows.root

class main(object):
	def __init__(self,master):
			self.master = master
			self.lineTracker = "0.0"
			fchange = font.fontChange()
			self.res = 0
			self.tabcount = 0
			
			
			
			menu = Menu(master)
			master.config(menu=menu)
			filemenu = Menu(menu)
			menu.add_cascade(label="File", menu=filemenu)
			filemenu.add_command(label="New", command=file.new_file)
			filemenu.add_command(label="Open", command=file.open_file)
			filemenu.add_command(label="Save", command=file.save_file)
			filemenu.add_command(label="Tab", command=tabs.tab)
			filemenu.add_separator()
			filemenu.add_command(label="Exit", command=file.exit)
			
			
			stylemenu = Menu(menu)
			menu.add_cascade(label="Style", menu=stylemenu)
			stylemenu.add_command(label="Colors", command=self.popup)
			stylemenu.add_command(label="Fonts", command=lambda:fchange.startwindow(master))
			stylemenu.add_command(label="Resize: On", command=lambda: self.doublecall(stylemenu))
			
			submenu = Menu(menu)
			stylemenu.add_cascade(label="Presets", menu=submenu, underline=0)
			submenu.add_command(label = "White on Black", command=lambda:colors("white", "black", "white"))
			submenu.add_command(label = "Black on White", command=lambda:colors("black", "white", "black"))
			submenu.add_command(label = "Midnight", command=lambda:colors("light blue", "dark slate gray", "light blue"))
			
			helpmenu = Menu(menu)
			menu.add_cascade(label="Help", menu=helpmenu)
			helpmenu.add_command(label="About...", command=self.about)
			
				#adding some keybindingsimport main
			textPad.bind("<Control-Key-l>", self.newLine)
			textPad.bind("<KeyRelease-Return>", self.lineNumbers)
			textPad.bind("<KeyRelease-Up>", self.scrollup)
			textPad.bind("<KeyRelease-Down>", self.scrolldn)
			textPad.bind("<Control-KP_Add>", self.zoom_in)
			textPad.bind("<Control-KP_Subtract>", self.zoom_out)
			textPad.bind("<Button-1>", self.clickline)
			textPad.bind("<Key>", self.highlighter)
			#textPad.bind("<Key>", self.classlighter)
				#End keybindingdef lineNumbers(self, thing):
				
			self.master.mainloop()

	def highlighter(self, event):
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
	
	def clickline(self, dummy):
		textPad.mark_set("insert", CURRENT)
		i = textPad.index(Tkinter.INSERT)
		lnText.see(i)
		
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
		
	def newLine(self, pointless):
			i = textPad.index(Tkinter.INSERT) # get index of current line "1.1" etc...
			ilist=i.split('.', 1)
			lineinsert = str(ilist[0]) + '.end';
			textPad.mark_set("insert", lineinsert) #change the insertion marker location to end of line
			textPad.mark_gravity("insert",RIGHT)#set gravity so it inserts to the right of line
			textPad.insert("insert", "\n")
						
	def lineNumbers(self, thing):
			i = textPad.index(Tkinter.INSERT)
			ilist=i.split('.', 1)
			lnText.see(i)
			lnText.mark_set("insert", ilist[0] + ".0")
			if i not in self.lineTracker: 
				#this keeps the program from adding already existing line numbers
				lnText.insert("insert", ilist[0] + "\n")
				lnText.update()
				self.lineTracker += (i + " ")

	#Track scrolling on arrowdown (line numbers will now correspond with actual lines)
	def scrolldn(self, thing):
			i = textPad.index(Tkinter.INSERT)
			ilist = i.split('.', 1)
			ilist[0] = int(ilist[0])
			ilist[0] += 1
			lnText.mark_set("insert", str(ilist[0]) + '.0')
			lnText.see(str(ilist[0])+ '.0')
	
	#Track scrolling on arrowup (line numbers will now correspond with actual lines)
	def scrollup(self, thing):
			i = textPad.index(Tkinter.INSERT)
			ilist = i.split('.', 1)
			ilist[0] = int(ilist[0])
			ilist[0] -= 1
			lnText.mark_set("insert", str(ilist[0])+ '.0')
			lnText.see(str(ilist[0])+ '.0')
			addline = False
			
	def zoom_in(self, bogus):
			font = customfont
			size = font.actual()["size"]+2
			font.configure(size=size)

	def zoom_out(self, bogus):
			font = customfont
			size = font.actual()["size"]-2
			font.configure(size=max(size, 8))
			
	def popup(self):
			self.w=popupWindow(self.master)
			self.master.wait_window(self.w.top)
			
	def about(self):
		label = tkMessageBox.showinfo("About", "Its and editor ya dingus")

	def dummy():
		print "stll a dummy"
		
		
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
			
			