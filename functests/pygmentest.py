import  Tkinter
from Tkinter import *
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name
import tkFileDialog as fd
import tkFont as font
class CoreUI(object):
        def __init__(self, lexer):
            self.sourcestamp = {}
            self.filestamp = {}
            self.uiopts = []
            self.lexer = lexer
            self.lastRegexp = ""
            self.markedLine = 0
            self.root = Tkinter.Tk()
            self.textPad = Text(self.root)
            self.textPad.pack()
            file = fd.askopenfile(parent=self.root,mode='rb',title='Select a file')
            if file != None:
                contents = file.read()
                self.textPad.delete(1.0,"end-1c")
                self.textPad.insert('1.0', contents)
                file.close()
            self.create_tags()
            self.recolorize()
            
        def create_tags(self):

            bold_font = font.Font(self.textPad, self.textPad.cget("font"))
            bold_font.configure(weight=font.BOLD)
            italic_font = font.Font(self.textPad, self.textPad.cget("font"))
            italic_font.configure(slant=font.ITALIC)
            bold_italic_font = font.Font(self.textPad, self.textPad.cget("font"))
            bold_italic_font.configure(weight=font.BOLD, slant=font.ITALIC)
            style = get_style_by_name('default')

            for ttype, ndef in style:
                tag_font = None

                if ndef['bold'] and ndef['italic']:
                    tag_font = bold_italic_font
                elif ndef['bold']:
                    tag_font = bold_font
                elif ndef['italic']:
                    tag_font = italic_font

                if ndef['color']:
                    foreground = "#%s" % ndef['color'] 
                else:
                    foreground = None

                self.textPad.tag_configure(str(ttype), foreground=foreground, font=tag_font) 
            
        def recolorize(self):

            code = self.textPad.get("1.0", "end-1c")
            tokensource = self.lexer.get_tokens(code)
            start_line=1
            start_index = 0
            end_line=1
            end_index = 0

            for ttype, value in tokensource:
                if "\n" in value:
                    end_line += value.count("\n")
                    end_index = len(value.rsplit("\n",1)[1])
                else:
                    end_index += len(value)

                if value not in (" ", "\n"):
                    index1 = "%s.%s" % (start_line, start_index)
                    index2 = "%s.%s" % (end_line, end_index)

                    for tagname in self.textPad.tag_names(index1): # FIXME
                        self.textPad.tag_remove(tagname, index1, index2)

                    self.textPad.tag_add(str(ttype), index1, index2)

                start_line = end_line
                start_index = end_index
        
        def mainloop(self):
            self.root.mainloop()

ui_core = CoreUI(lexer = PythonLexer())    # default (no extension) lexer is python
ui_core.mainloop()

