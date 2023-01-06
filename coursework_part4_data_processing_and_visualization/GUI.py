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
    analysis_dict[analysis_name_entry.get()] = Analysis(analysis_name_entry.get(), path_entry.get())


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


#日期时间选择器
import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk
from tkinter import *
import datetime
 
 
 
def start_calendar():
    def print_sel():
        start_time_text.configure(state="normal")
        print(str(cal.selection_get()) + " " + str(hour.get()) + ":" + str(minute.get()))
        s_data = str(cal.selection_get()) + " " + str(hour.get()) + ":" + str(minute.get())
        start_time_text.delete(0, END)
        start_time_text.insert("0", s_data)
        start_time_text.configure(state="disabled")
        cal.see(datetime.date(year=2016, month=2, day=5))
 
    top = tk.Toplevel()
    top.geometry("300x250")
 
    today = datetime.date.today()
 
    mindate = datetime.date(year=2022, month=1, day=1)
    maxdate = today + datetime.timedelta(days=5)
 
    cal = Calendar(top, font="Arial 14", selectmode='day', locale='zh_CN', mindate=mindate, maxdate=maxdate,
                   background="red", foreground="blue", bordercolor="red", selectbackground="red",
                   selectforeground="red", disabledselectbackground=False)
    cal.place(x=0, y=0, width=300, height=200)
    value = 0
    values_h = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                20, 21, 22, 23]
    values_m = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                20, 21, 22, 23, 24, 25, 26, 27, 28,
                29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53,
                54,
                55, 56, 57, 58, 59]
 
    hour = ttk.Combobox(
        master=top,  # 父容器
        height=15,  # 高度,下拉显示的条目数量
        width=3,  # 宽度
        state="normal",  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
        cursor="arrow",  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=("", 20),  # 字体
        values=values_h,  # 设置下拉框的选项
    )
    hour.place(x=0, y=200)
    ttk.Label(top, text="时").place(x=60, y=195, width=20, height=40)
 
    minute = ttk.Combobox(
        master=top,  # 父容器
        height=15,  # 高度,下拉显示的条目数量
        width=3,  # 宽度
        state="normal",  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled
        cursor="arrow",  # 鼠标移动时样式 arrow, circle, cross, plus...
        font=("", 20),  # 字体
        values=values_m,  # 设置下拉框的选项
    )
    minute.place(x=80, y=200)
    ttk.Label(top, text="分").place(x=140, y=195, width=20, height=40)
 
    tk.Button(top, text="确定", command=print_sel).place(x=240, y=205)
 
root =Tk()
start_time = tk.Button(root, text="开始时间", command=start_calendar)
start_time.place(x=10,y=10)
start_time_text = tk.Entry(root, width=20)
start_time_text.place(x=100,y=10)
root.geometry("400x200")
root.mainloop()

from tkcalendar import Calendar, DateEntry
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk


def example1():
    def print_sel():
        print(cal.selection_get())
        cal.see(datetime.date(year=2016, month=2, day=5))

    top = tk.Toplevel(root)

    import datetime
    today = datetime.date.today()

    mindate = datetime.date(year=2018, month=1, day=21)
    maxdate = today + datetime.timedelta(days=5)
    print(mindate, maxdate)

    cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                   mindate=mindate, maxdate=maxdate, disabledforeground='red',
                   cursor="hand1", year=2018, month=2, day=5)
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="ok", command=print_sel).pack()


def example2():

    top = tk.Toplevel(root)

    cal = Calendar(top, selectmode='none')
    date = cal.datetime.today() + cal.timedelta(days=2)
    cal.calevent_create(date, 'Hello World', 'message')
    cal.calevent_create(date, 'Reminder 2', 'reminder')
    cal.calevent_create(date + cal.timedelta(days=-2), 'Reminder 1', 'reminder')
    cal.calevent_create(date + cal.timedelta(days=3), 'Message', 'message')

    cal.tag_config('reminder', background='red', foreground='yellow')

    cal.pack(fill="both", expand=True)
    ttk.Label(top, text="Hover over the events.").pack()


def example3():
    top = tk.Toplevel(root)

    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010)
    cal.pack(padx=10, pady=10)


root = tk.Tk()
ttk.Button(root, text='Calendar', command=example1).pack(padx=10, pady=10)
ttk.Button(root, text='Calendar with events', command=example2).pack(padx=10, pady=10)
ttk.Button(root, text='DateEntry', command=example3).pack(padx=10, pady=10)

root.mainloop()
