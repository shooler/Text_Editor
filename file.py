import main
import windows
import Tkinter
import tkFileDialog as fd
import utilityKeys as ukeys
import os
import textConfig
from textConfig import *
from main import *
from windows import *
import ttk
import config

openedFiles = {}

def open_file(*args):
	file = fd.askopenfile(parent=windows.root,mode='rb',title='Select a file')
	filename = str(file) 		#next few lines convert askopenfile object to readable filepath
	flist = filename.split(' ') #this allows us to save without the dialog if the file already exists
	filename = flist[2]
	filename = re.sub('[\'\",]', '', filename)
	filekey = (filename.split('/')[-1])
	windows.newTab(filename, filekey)
	openedFiles.update({filekey : filename})
	textPad = windows.textPad
	lnText = windows.lnText
	if file != None:
		contents = file.read()
		textPad.delete('1.0',"end")
		textPad.insert('1.0', contents)
		file.close()
	#get line numbers
	ukeys.searches(textPad, lnText, windows.searchDiag)
	ukeys.utilities(textPad, windows.customFont)
	windows.lineNumbers()
	tconf = textConfig.textColor(textPad, '/', '')
	textConfig.textColor.callAll()
	return 'break'

def save_file(x):
	currtab = windows.n.index(windows.n.select())
	filename = windows.n.tab(currtab, 'text')
	if filename not in openedFiles:
		save_as()
	else:
		quicksave(filename)
			
def quicksave(filename):
	textPad = windows.textPad
	file = open(filename, 'w')
	data = textPad.get('1.0', END+'-1c')
	file.write(data)
	file.close()
		
def save_as():
	textPad = windows.textPad
	lnText = windows.lnText
	file = fd.asksaveasfile(mode='w')
	filename = str(file) 		#next few lines convert askopenfile object to readable filepath
	flist = filename.split(' ') #this allows us to save without the dialog if the file already exists
	filename = flist[2]
	filename = re.sub('[\'\",]', '', filename)
	filekey = (filename.split('/')[-1])
	openedFiles.update({filekey : filename})
	currtab = windows.n.index(windows.n.select())
	windows.n.tab(currtab, text = filename.split('/')[-1])
	if file != None:
		#slice off the last character from get, as an extra return is added
		data = textPad.get('1.0', END+'-1c')
		file.write(data)
		file.close()
		textPad.config(fg = config.colors['foregroundColor'])	
		textConfig.textColor(textPad, '/', 'on')
		textConfig.textColor.toggleHighlights()
		

def exit(*arg):
	if tkMessageBox.askokcancel("Quit", "Quit?"):
		windows.root.destroy()