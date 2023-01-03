from graphics_helper import *
import tkinter as tk
from tkinter.messagebox import showinfo
import windnd

def redrawAll(app, canvas):
    text_size = app.width // 15
    canvas.create_text(app.width/2, app.height/6, text="Dataploting", 
                        font=f"Arial {text_size} bold")


runApp(width=1080, height=720)

def dragg(files):
    msg = '\n'.join((item.decode('gbk') for item in files))
    showinfo('您拖放的文件', msg)

tks =tk.Tk()
windnd.hook_dropfiles(tks,func=dragg)
tks.mainloop()
