import main
import windows
from main import *
from windows import *

master = windows.root

def open_file():
	file = tkFileDialog.askopenfile(parent=master,mode='rb',title='Select a file')
	if file != None:
		contents = file.read()
		textPad.insert('1.0', contents)
		file.close()
	
	lnText.delete(1.0, END)
	#get line numbers
	linecount = int(textPad.index('end').split('.')[0]) - 1 
	for i in range(linecount - 2):
		lnText.mark_set("insert", str(i) + ".0")
		lnText.insert("insert", str(i) + "\n")
	lnText.delete(END+'-1c')

def save_file():
	file = tkFileDialog.asksaveasfile(mode='w')
	if file != None:
		#slice off the last character from get, as an extra return is added
		data = textPad.get('1.0', END+'-1c')
		file.write(data)
		file.close()

def new_file():
	if tkMessageBox.askokcancel("New", "Do you want to save before you close?"):
		save_file()
		textPad.delete(1.0,END)

def exit():
	if tkMessageBox.askokcancel("Quit", "Quit?"):
		master.destroy()