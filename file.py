import main
import windows
import Tkinter
import tkFileDialog as fd
import utilityKeys as ukeys
import os
from main import *
from windows import *

openedFiles = {}
updateColors = windows.callAll
master = windows.root
filename = ""


def open_file(*arg):
	global filename
	file = fd.askopenfile(parent=master,mode='rb',title='Select a file')
	filename = str(file) 		#next few lines convert askopenfile object to readable filepath
	flist = filename.split(' ') #this allows us to save without the dialog if the file already exists
	filename = flist[2]
	filename = re.sub('[\'\",]', '', filename)
	filekey = (filename.split('/')[-1]).lower().split('.')[0].lower()
	windows.newTab(filename, filekey)
	openedFiles.update({filekey : filename})
	textPad = windows.textPad
	lnText = windows.lnText
	if file != None:
		contents = file.read()
		textPad.delete(1.0,"end")
		textPad.insert('1.0', contents)
		file.close()
	#get line numbers
	lnText.delete(1.0, "end-1c")
	i = int(textPad.index('end-1c').split('.')[0])
	for x in range(i):
		lnText.config(state = 'normal')
		if x != 0:
			lnText.insert("insert", '\n' + str(int(x+1)))
		else:
			lnText.insert("insert", str(int(x+1)))
	#textPad.insert(END, "\n")
	textPad.see("1.0")
	lnText.see("1.0")
	updateColors(filename)
	lnText.config(state = 'disabled')
	ukeys.searches(textPad, lnText, windows.searchDiag)
	return "break"

def save_file(x):
		global filename
		if filename == "":
			save_as()
		else:
			quicksave(filename)
			
def quicksave(filename):
	print openedFiles
	filename = openedFiles[n.select().split('_=_')[-1]]
	textPad = windows.textPad
	file = open(filename, 'w')
	data = textPad.get('1.0', END+'-1c')
	file.write(data)
	file.close()
	
		
def save_as():
	global filename
	file = fd.asksaveasfile(mode='w')
	filename = str(file) 		#next few lines convert askopenfile object to readable filepath
	flist = filename.split(' ') #this allows us to save without the dialog if the file already exists
	filename = flist[2]
	filename = re.sub('[\'\",]', '', filename)
	filekey = (filename.split('/')[-1])
	openedFiles.update({filekey : filename})
	if file != None:
		#slice off the last character from get, as an extra return is added
		data = textPad.get('1.0', END+'-1c')
		file.write(data)
		file.close()

def exit(*arg):
	if tkMessageBox.askokcancel("Quit", "Quit?"):
		master.destroy()