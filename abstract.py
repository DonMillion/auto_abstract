#!/usr/bin/python3
# -*- coding: utf-8 -*-
# GUI主界面
# 同时进行输入检查
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox
import getAbstract

def openFile(*args):
	"""从文件读取内容"""
	filetype = [('txt', '*.txt')] # 目前只支持txt文件
	filename = filedialog.askopenfilename(filetypes=filetype)
	if not filename:
		return 0
	try:
		# Windows 的txt文件默认中文编码是gbk
		handle = open(filename, mode='r')
		content = handle.read()
	except Exception:
		# 如果不是就尝试用utf8
		try:
			handle = open(filename, mode='r', encoding='utf8')
			content = handle.read()
		except Exception as err:
			messagebox.showinfo(message=str(err))
	handle.close()
	docText.delete('1.0', 'end')
	docText.insert('1.0', content)	

def exitProgram(*args):
	"""退出程序"""
	root.destroy()

def transform(*args):
	"""运行"""
	# 设置压缩率
	try:
		getAbstract.setPercent((percent.get()))
		p= percent.get()
		if p <= 0 or p >= 1:
			raise Exception()
		# 调用
		text = docText.get('1.0', 'end')
		abstractText.delete('1.0', 'end')
		abstract = getAbstract.fetch(text)
		# 显示
		abstractText.insert('1.0', abstract)
		docSC.set(getAbstract.getDocSC())
		abstractSC.set(getAbstract.getN())
	except Exception:
		messagebox.showinfo(message='请输入0-1之间的小数')



def clip(*args):
	"""把文摘中的内容复制到粘贴板"""
	text = abstractText.get('1.0','end')
	root.clipboard_clear()
	root.clipboard_append(text)

def selectAll(*args):
	docText.tag_add("sel", '1.0','end')

root = Tk()
root.title('自动文摘生成器')
root.option_add('*tearoff', False)

# 设置菜单
menubar = Menu(root)
menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='file')
menu_file.add_command(label='Open    ctrl+o', command=openFile)
menu_file.add_command(label='Exit    ctrl+e', command=exitProgram)

# frame
mainframe = ttk.Frame(root, padding='15 15 5 15')

# 显示文档的text widget
docText = Text(mainframe, width=60, height=30)
abstractText = Text(mainframe, width=60, height=20)

# scrollbar
docScrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=docText.yview)
docText.configure(yscrollcommand=docScrollbar.set)
abstractScrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=abstractText.yview)
abstractText.configure(yscrollcommand=abstractScrollbar.set)

# 设置字体
topLabelFont = font.Font(family='微软雅黑', size=10)
showLabelFont = font.Font(family='微软雅黑', size=10)
s=ttk.Style()
s.configure('TButton', font='微软雅黑 11 bold')
s.configure('TText', font='微软雅黑 14')
s.configure('TButton', foreground='#6b93b5')

# 设置背景颜色
styleArray = ('TButton', 'TFrame', 'TLabel', 'TEntry')
for style in styleArray:
	s.configure(style, background='#ebf0f6')
 

# Label
docLabel = ttk.Label(mainframe, text='文档内容：', font=topLabelFont)
abstractLabel = ttk.Label(mainframe, text='自动文摘：', font=topLabelFont)
percentLabel = ttk.Label(mainframe, text='压   缩   率：', font=showLabelFont)
docSCLabel = ttk.Label(mainframe, text='原文句子数：', font=showLabelFont)
abstractSCLabel = ttk.Label(mainframe, text='文摘句子数：', font=showLabelFont)
docSC = StringVar()
docSCShow = ttk.Label(mainframe, textvariable=docSC)
abstractSC = StringVar()
abstractSCShow = ttk.Label(mainframe, textvariable=abstractSC)

# entry
percent = DoubleVar()
percent.set(getAbstract.getPercent())
percentEntry = ttk.Entry(mainframe, textvariable=percent, width=5)

# 按钮
runButton = ttk.Button(mainframe, text="提取文摘", command=transform)
clipButton = ttk.Button(mainframe, text='复制文摘', command=clip)

# 布局，左边
root.config(menu=menubar)
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
docLabel.grid(column=1, row=1, sticky=(E, W))
docText.grid(column=1, row=2, rowspan=4, sticky=(N,W), pady=5)
docScrollbar.grid(column=2, row=2, rowspan=4, sticky=(N,S), pady=5, padx=8)
# 右上
abstractLabel.grid(column=3, row=1, columnspan=4, sticky=(W, S))
abstractText.grid(column=3, row=2, columnspan=4, sticky=(N,W), pady=5)
abstractScrollbar.grid(column=7, row=2, sticky=(N,S), pady=5, padx=8)
# 右下
percentLabel.grid(column=3, row=3)
percentEntry.grid(column=4, row=3, sticky=W)
docSCLabel.grid(column=3, row=4)
docSCShow.grid(column=4, row=4,sticky=W)
abstractSCLabel.grid(column=3, row=5)
abstractSCShow.grid(column=4, row=5,sticky=W)
runButton.grid(column=6, row=3, rowspan=2, sticky=E)
clipButton.grid(column=6, row=5, sticky=(N,E))

# 事件绑定
docText.focus()
root.bind('<Return>', transform)
# root.bind('<Control-c>', clip)
root.bind('<Control-o>', openFile)
root.bind('<Control-e>', exitProgram)
root.bind('<Control-a>', selectAll)

root.mainloop()