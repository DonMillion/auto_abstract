# -*- coding: utf-8 -*-
# GUI主界面
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import getAbstract

def openFile():
	"""从文件读取内容"""
	filetype = [('txt', '*.txt')] # 目前只支持txt文件
	filename = filedialog.askopenfilename(filetypes=filetype)
	if filename:
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

def exitProgram():
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
		docSC.set('原文句子数：{}'.format(getAbstract.getDocSC()))
		abstractSC.set('文摘句子数：{}'.format(getAbstract.getN()))
	except Exception:
		messagebox.showinfo(message='请输入0-1之间的小数')



def clip(*args):
	"""把文摘中的内容复制到粘贴板"""
	text = abstractText.get('1.0','end')
	root.clipboard_clear()
	root.clipboard_append(text)

root = Tk()
root.title('自动文摘生成器')
root.option_add('*tearoff', False)

# 设置菜单
menubar = Menu(root)
menu_file = Menu(menubar)
menubar.add_cascade(menu=menu_file, label='file')
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
docSC.set('原文句子数：')
docSCLabel = ttk.Label(mainframe, textvariable=docSC)
abstractSC = StringVar()
abstractSC.set('文摘句子数：')
abstractSCLabel = ttk.Label(mainframe, textvariable=abstractSC)

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
docLabel.grid(column=1, row=1, columnspan=2, sticky=(E, W))
docText.grid(column=1, row=2, rowspan=4, sticky=(N,W), pady=5)
docScrollbar.grid(column=2, row=2, rowspan=4, sticky=(N,S), pady=5)
# 右上
percentLabel.grid(column=3, row=1)
percentEntry.grid(column=4, row=1)
docSCLabel.grid(column=5, row=1, columnspan=2)
runButton.grid(column=3, row=2, columnspan=2, rowspan=2)
abstractSCLabel.grid(column=5, row=2, columnspan=2)
clipButton.grid(column=5, row=3, columnspan=2, sticky=N)

# 右下
abstractLabel.grid(column=3, row=4, columnspan=4, sticky=(W, S))
abstractText.grid(column=3, row=5, columnspan=3, sticky=(N,W), pady=5)
abstractScrollbar.grid(column=6, row=5, sticky=(N,S), pady=5)

root.mainloop()