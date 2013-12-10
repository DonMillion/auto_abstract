# -*- coding: utf-8 -*-
# GUI主界面
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import getAbstract

def newFile():
	pass

def openFile():
	filetype = [('txt', '*.txt')]
	filename = filedialog.askopenfilename(filetypes=filetype)
	handle = open(filename, mode='r', encoding='utf8')
	content = handle.read()

	handle.close()
	docText.delete('1.0', 'end')
	docText.insert('1.0', content)
	

def exitProgram():
	root.destroy()

def transform(*args):
	text = docText.get('1.0', 'end')
	abstractText.delete('1.0', 'end')
	abstract = getAbstract.fetch(text)
	abstractText.insert('1.0', abstract)

def clip(*args):
	text = docText.get('1.0','end')
	root.clipboard_clear()
	root.clipboard_append(text)

root = Tk()
root.title('自动文摘生成器')
root.option_add('*tearoff', False)

# 设置菜单
menubar = Menu(root)
menu_file = Menu(menubar)
menu_edit = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='file')
menubar.add_cascade(menu=menu_edit, label='edit')
menu_file.add_command(label='New', command=newFile)
menu_file.add_command(label='Open...', command=openFile)
menu_file.add_command(label='Exit', command=exitProgram)

# frame
mainframe = ttk.Frame(root, padding='5 5')

# 显示文档的text widget
docText = Text(mainframe, width=60, height=20)
abstractText = Text(mainframe, width=60, height=10)

# scrollbar
docScrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=docText.yview)
docText.configure(yscrollcommand=docScrollbar.set)
abstractScrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=abstractText.yview)
abstractText.configure(yscrollcommand=abstractScrollbar.set)

# Label
docLabel = ttk.Label(mainframe, text='文档内容：')
abstractLabel = ttk.Label(mainframe, text='自动文摘：')
percentLabel = ttk.Label(mainframe, text='压缩率：')
docSC = StringVar()
docSCLabel = ttk.Label(mainframe, textvariable=docSC)
abstractSC = StringVar()
abstractSCLabel = ttk.Label(mainframe, textvariable=abstractSC)

# entry
entry = DoubleVar()
percentEntry = ttk.Entry(mainframe, textvariable=entry, width=5)

# 按钮
runButton = ttk.Button(mainframe, text="提取文摘", command=transform, width=6)
clipButton = ttk.Button(mainframe, text='复制文摘', command=clip)

# 布局，左边
root.config(menu=menubar)
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
docLabel.grid(column=1, row=1, columnspan=2, sticky=(E, W))
docText.grid(column=1, row=2, rowspan=4, sticky=(N,W), pady=5)
docScrollbar.grid(column=2, row=2, rowspan=4, sticky=(N,S), pady=5)
# 右上
percentLabel.grid(column=3, row=1)
percentEntry.grid(column=4, row=1)
docSCLabel.grid(column=5, row=1)
runButton.grid(column=3, row=2, columnspan=2, rowspan=2, sticky=(N, S, E, W))
abstractSCLabel.grid(column=5, row=2, columnspan=2)
clipButton.grid(column=5, row=3, columnspan=2, sticky=N)

# 右下
abstractSCLabel.grid(column=3, row=4, columnspan=4)
abstractText.grid(column=3, row=5, columnspan=4, sticky=(N,W), pady=5)
abstractScrollbar.grid(column=6, row=5, sticky=(N,S), pady=5)

root.mainloop()