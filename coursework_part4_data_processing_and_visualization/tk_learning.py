# Author: Kaifeng ZHU
# First creation: 2023/1/4
# This file is for learning tkinter

# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import ttk

# 调用Tk()创建主窗口
root_window =tk.Tk()
# 设置窗口title
root_window.title('Test')
# 设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
root_window.geometry('450x300')
# 更改左上角窗口的的icon图标,加载tower's logo标
root_window.iconbitmap(r'C:\Users\lenovo1\OneDrive - The University of Nottingham Ningbo China\Architectural Environment Engineering\Architectural Environment Design 1\UNNC-F22-ABEE1025-Group22\coursework_part4_data_processing_and_visualization\Tower.ico')
# 设置主窗口的背景颜色,颜色值可以是英文单词，或者颜色值的16进制数,除此之外还可以使用Tk内置的颜色常量
root_window["background"] = "#C9C9C9"
# 添加文本内,设置字体的前景色和背景色，和字体类型、大小
text=tk.Label(root_window,text="Hellow, World!",bg="green",fg="blue",font=('Times', 20, 'bold italic'))
# 将文本内容放置在主窗口内
text.pack()
# 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
button=tk.Button(root_window,text="关闭",command=root_window.quit)
# 将按钮放置在主窗口内
button.pack(side="bottom")
#进入主循环，显示主窗口
root_window.mainloop()



#------------------------------------------
window =tk.Tk()
#设置窗口title
window.title('C语言中文网')
#设置窗口大小:宽x高,注,此处不能为 "*",必须使用 "x"
window.geometry('450x300')
# 获取电脑屏幕的大小
print("电脑的分辨率是%dx%d"%(window.winfo_screenwidth(),window.winfo_screenheight()))
# 要求窗口的大小，必须先刷新一下屏幕
window.update()
print("窗口的分辨率是%dx%d"%(window.winfo_width(),window.winfo_height()))
# 如使用该函数则窗口不能被拉伸
# window.resizable(0,0)
# 改变背景颜色
window.config(background="#6fb765")
# 设置窗口处于顶层
window.attributes('-topmost',True)
# 设置窗口的透明度
window.attributes('-alpha',1)
# 设置窗口被允许最大调整的范围，与resizble()冲突
window.maxsize(600,600)
# 设置窗口被允许最小调整的范围，与resizble()冲突
window.minsize(50,50)
#更改左上角窗口的的icon图标,加载C语言中文网logo标
# window.iconbitmap('C:/Users/Administrator/Desktop/favicon.ico')
#添加文本内容,并对字体添加相应的格式 font(字体,字号,"字体类型")
text=tk.Label(window,text="C语言中文网，网址：c.biancheng.net",bg="yellow",fg="red",font=('Times', 15, 'bold italic underline'))
#将文本内容放置在主窗口内
text.pack()
# 添加按钮，以及按钮的文本，并通过command 参数设置关闭窗口的功能
button=tk.Button(window,text="关闭",command=window.quit)
# 将按钮放置在主窗口内
button.pack(side="bottom")
#进入主循环，显示主窗口
window.mainloop()



window = tk.Tk()
window.title('c语言中文网')
window.geometry('300x300')
# window.iconbitmap('C:/Users/Administrator/Desktop/favicon.ico')
# 定义回调函数
def callback():
    print("执行回调函数","C语言中文网欢迎您")
# 点击执行按钮
button = tk.Button(window, text="执行", command=callback)
button.pack()
window.mainloop()


window = tk.Tk()
window.title('c语言中文网')
# window.iconbitmap('C:/Users/Administrator/Desktop/favicon.ico')
# 设置窗口大小变量
width = 300
height = 300
# 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = window.winfo_screenwidth()
screenheight = window.winfo_screenheight()
size_geo = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
window.geometry(size_geo)
window.mainloop()

win = tk.Tk()
win.title("C语言中文网")
win.geometry('300x300')
# win.iconbitmap('C:/Users/Administrator/Desktop/C语言中文网logo.ico')
# 创建一个容器来包括其他控件
frame = tk.Frame (win)
# 创建一个计算器
def calc() :
# 用户输入的表达式，计算结果后转换为字符串
    result = "= "+ str (eval(expression.get()))
    #将计算的结果显示在Label控件上
    label.config(text =result)
#创建一个Label控件
label = tk.Label (frame)
#创建一个Entry控件
entry = tk.Entry (frame)
#读取用户输入的表达式
expression = tk.StringVar ()
#将用户输入的表达式显示在Entry控件上
entry ["textvariable"] = expression
#创建-一个 Button控件.当用户输入完毕后，单击此按钮即计算表达式的结果
button1 = tk.Button (frame, text="等 于",command=calc)
#设置Entry控件为焦点所在
entry.focus ()
frame.pack ()
#Entry控件位于窗体的上方
entry .pack()
#Label控件位于窗体的左方
label .pack (side="left")
#Button控件位于窗体的右方
button1.pack (side="right")
#开始程序循环
frame .mainloop()

from tkinter import *
from tkinter.filedialog import askdirectory
import os


def selectPath():
    path_ = askdirectory() #使用askdirectory()方法返回文件夹的路径
    if path_ == "":
        path.get() #当打开文件路径选择框后点击"取消" 输入框会清空路径，所以使用get()方法再获取一次路径
    else:
        path_ = path_.replace("/", "\\")  # 实际在代码中执行的路径为“\“ 所以替换一下
        path.set(path_)


def openPath():
    dir = os.path.dirname(path.get()+"\\")
    os.system('start ' + dir)
    #print(dir)

root = Tk()
root.title("路径选择和文件位置打开功能演示")
path = StringVar()
path.set(os.path.abspath("."))

Label(root, text="目标路径:").grid(row=0, column=0)
Entry(root, textvariable=path,state="readonly").grid(row=0, column=1,ipadx=200)


# e.insert(0,os.path.abspath("."))
Button(root, text="路径选择", command=selectPath).grid(row=0, column=2)
Button(root, text="打开文件位置", command=openPath).grid(row=0, column=3)
root.mainloop()

