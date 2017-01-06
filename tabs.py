import ttk
import Tkinter as tk
import ScrolledText
import windows
from ScrolledText import *
from windows import *

master = windows.root

inc = 0

def tab():
    notebook = ttk.Notebook(master)
    notebook.pack()
    subframe = Tkinter.Frame(master)
    subframe.pack()
    notebook.add(subframe, text = "Tab", state="normal")
    