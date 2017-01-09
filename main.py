import Tkinter
import font
import tkFileDialog
import tkMessageBox
import sys
import tabs
import file
import windows
import ttk
import textConfig
import utilityKeys
from Tkinter import *
from ScrolledText import * # Because Tkinter textarea does not provide scrolling
from font import *
from windows import *
from tabs import *
from textConfig import *


ukeys = utilityKeys
customfont = windows.customFont
mast = windows.root
tconf = textConfig.callAll


class main(object):
	def __init__(self,master):
			self.master = master
			self.lineTracker = []
			fchange = font.fontChange()
			self.res = 0
			self.tabcount = 0
			
			
			
			menu = Menu(master)
			master.config(menu=menu)
			filemenu = Menu(menu)
			menu.add_cascade(label="File", menu=filemenu)
			filemenu.add_command(label="New", command=file.new_file)
			filemenu.add_command(label="Open", command=lambda: file.open_file(''))
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
			
			#adding some General keybindings
			textPad.bind("<KeyRelease-Return>", self.lineNumbers)
			textPad.bind("<KeyRelease-BackSpace>", self.lineNumbers)
			textPad.bind("<Up>", self.scrollup)
			textPad.bind("<Down>", self.scrolldn)
			textPad.bind("<Button-1>", self.clickline)
			textPad.bind("<Control-o>", file.open_file)
			textPad.bind("<Control-s>", file.save_file)
			textPad.bind("<Control-q>", file.exit)
			
			#Utility (non file keybinds)
			textPad.bind("<Control-Key-l>", ukeys.newLine)
			textPad.bind("<Control-KP_Add>", ukeys.zoom_in)
			textPad.bind("<Control-KP_Subtract>", ukeys.zoom_out)
			textPad.bind("<Control-Key-comma>", ukeys.backTab)
			textPad.bind("<Control-Key-period>", ukeys.forwardTab)
			textPad.bind("<Control-Key-f>", ukeys.searchInit)
			textPad.bind("<Key-F1>", ukeys.getIndex)
			searchDiag.bind("<Down>", ukeys.searchNext)
			searchDiag.bind("<KeyRelease-Down>", self.scrolldn)
			searchDiag.bind("<Up>", ukeys.searchLast)
			searchDiag.bind("<KeyRelease-Up>", self.scrolldn)
			searchDiag.bind("<KeyRelease-f>", ukeys.searchClear)
			searchDiag.bind("<Return>", ukeys.searchReturn)
			searchDiag.bind("<Escape>", ukeys.doneSearch)
			#end keybinds
			textPad.after(0, tconf)
			self.master.mainloop()
	
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
						
	def lineNumbers(self, *args):
		#textPad.after(75, self.lineNumbers)
		lnText.delete(1.0, END)
		i = int(textPad.index(END).split('.')[0])
		x = int(lnText.index('insert').split('.')[1])
		current = textPad.index('insert')
		clist = current.split('.')
		nextline = str(int(clist[0]) + 1)
		current = '.'.join(clist)
		for x in range(i-1):
			if x == 0:
				lnText.insert("insert", str(int(x+1)))
			else:
				lnText.insert("insert", '\n' + str(int(x+1)))
		textPad.mark_set("insert", (current))
		lnText.see(current)
		textPad.see(current)
		
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
			
def colors(fore, back, insert):
			textPad.configure(foreground = fore, background = back, insertbackground = insert)	
			lnText.configure(foreground = fore, background = back, insertbackground = insert)