from graphics_helper import *
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter import filedialog
import windnd
from main_without_GUI import *

# def redrawAll(app, canvas):
#     text_size = app.width // 15
#     canvas.create_text(app.width/2, app.height/6, text="Dataploting", 
#                         font=f"Arial {text_size} bold")


# runApp(width=1080, height=720)

# def dragg(files):
#     msg = '\n'.join((item.decode('gbk') for item in files))
#     showinfo('您拖放的文件', msg)

# tks =tk.Tk()
# windnd.hook_dropfiles(tks,func=dragg)
# tks.mainloop()


window =tk.Tk()
# Set the title of window.
window.title('DataPloting')
# Set the window size.
# Make the window is aligned center.
width = 1080
height = 720
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
# The initial size of the window is 1080x720
window.geometry(size_geo)
# Change the background colour.
window.config(background="#6fb765")
# Set the window at the top level.
window.attributes('-topmost',True)
# Set the transparency of the window.
window.attributes('-alpha',1)
# Change the icon in the top left corner of the window
window.iconbitmap('.\\Tower.ico')
# Set the title.
title_size = window.winfo_width() // 15
software_title=tk.Label(window,text="DataPloting",bg="yellow",fg="red",font=('Times', f"{title_size}", 'bold italic underline'))
software_title.grid(row=0, column=0)

def select_path():
    """
    This function is for get the directory of choosed file.
    """
    # Select a file from the local area and return the file's directory.
    path_ = filedialog.askdirectory()
    if path_ == "":
        path.get()
    else:
        path_ = path_.replace("/", "\\")   
        path.set(path_)

# def open_path():
#     dir = os.path.dirname(path.get()+"\\")
#     os.system('start ' + dir)

def initialize_analysis():
    """
    This function is for initializing Analysis class.
    """
    # globals[analysis_name]
    # analysis_name = analysis_name_entry.get()
    # analysis_dict[analysis_name.get()] = Analysis(analysis_name.get(), path.get())
    analysis_dict[analysis_name_entry.get()] = Analysis(analysis_name_entry.get(), path.get())


def show_analysis_dict():
    msg_list_name = []
    msg_list_dir = []
    for dict_key in analysis_dict.keys():
        msg_list_name.append(analysis_dict[dict_key].name)
        msg_list_dir.append(analysis_dict[dict_key].file_directory)
        msg_list_name.append("; ")
        msg_list_dir.append("; ")
    msg = 'Name: '.join(msg_list_name) + "\n"
    msg += msg.join(msg_list_dir)
    messagebox.showinfo(message=msg)
    
show_analysis_dict_btn = tk.Button(window, text="Show analysis dict", command=show_analysis_dict)

analysis_dict = {}

path = StringVar()
path.set(os.path.abspath("."))
tfd_label = tk.Label(window, text="Target File Directory:")
path_entry = tk.Entry(window, textvariable=path, state="readonly")
# e.insert(0,os.path.abspath("."))
choose_dir_btn = tk.Button(window, text="Choose Directory", command=select_path)


analysis_name = StringVar()
analysis_name.set("New Analysis")
analysis_name_label = tk.Label(window, text="Analyse Name:")
analysis_name_entry = tk.Entry(window, textvariable=analysis_name, state="normal")
create_analysis_btn = tk.Button(window, text="Create Analysis", command=initialize_analysis())
# Button(window, text="打开文件位置", command=open_path).grid(row=1, column=3)
# print(path.get())

tfd_label.grid(row=1, column=0)
path_entry.grid(row=1, column=1,ipadx=200)
choose_dir_btn.grid(row=1, column=2)

analysis_name_label.grid(row=3, column=0)
analysis_name_entry.grid(row=3, column=1,ipadx=200)
create_analysis_btn.grid(row=3, column=2)

show_analysis_dict_btn.grid(row=4)

# Display the window.
window.mainloop()

