import main
import windows
import textConfig
import Tkinter
import tkFileDialog as fd
import os
from main import *
from textConfig import *
from windows import *

openedFiles = []
tc = textConfig.callAll
master = windows.root
filename = ""

def open_file(*arg):
	global filename
	file = fd.askopenfile(parent=master,mode='rb',title='Select a file')
	filename = str(file) 		#next few lines convert askopenfile object to readable filepath
	flist = filename.split(' ') #this allows us to save without the dialog if the file already exists
	filename = flist[2]
	filename = re.sub('[\'\",]', '', filename)
	if file != None:
		contents = file.read()
		textPad.delete(1.0,"end-1c")
		textPad.insert('1.0', contents)
		file.close()
	#get line numbers
	lnText.delete(1.0, "end-1c")
	i = int(textPad.index('end-1c').split('.')[0])
	for x in range(i+1):
		lnText.insert("insert", str(int(x+1)) + '\n')
	textPad.see("1.0")
	lnText.see("1.0")
	tc()

def save_file(x):
		global filename
		if filename == "":
			save_as()
		else:
			quicksave(filename)
			
def quicksave(filename):
	file = open(filename, 'w')
	data = textPad.get('1.0', END+'-1c')
	file.write(data)
	file.close()
		
def save_as():
	global filename
	file = fd.asksaveasfile(mode='w')
	if file != None:
		#slice off the last character from get, as an extra return is added
		data = textPad.get('1.0', END+'-1c')
		file.write(data)
		file.close()
		filename = fd.askopenfilename()
			
def new_file():
	if tkMessageBox.askokcancel("New", "Do you want to save before you close?"):
		save_file()
		textPad.delete(1.0,END)

def exit(*arg):
	if tkMessageBox.askokcancel("Quit", "Quit?"):
		master.destroy()