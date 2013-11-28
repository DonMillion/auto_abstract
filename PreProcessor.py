import jieba,re
from ResultAnalyzer import Analyzer

#用结巴（jieba）分词系统分词
#去除停用词

stopwordFileLoc = 'stopwords.txt'
SC = 0 #所有句子的总数(Sentence Count)

def loadStopwords():
	"""加载停用词表"""
	stopwordFile = open(stopwordFileLoc)
	stopwords = {} #遍历字典时速度会快点
	for word in stopwordFile.read().split('\n'):
		stopwords[word] = None
	stopwordFile.close()
	return stopwords

STOPWORDS = loadStopwords()

class sentence:
	"""每个对象储存一个句子"""

	def __init__(self, content, mode = False):
		self.source = content
		temp = list(jieba.cut(content, cut_all=mode))
		self.wordcount = 0
		#去除停用词(包括标点符号)，同时计算每个词的出现次数
		self.segements = {}
		for word in temp:
			if word not in STOPWORDS:
				if word not in self.segements:
					self.segements[word] = {}
					self.segements[word]['TF'] = 1
				else:
					self.segements[word]['TF'] += 1
				self.wordcount += 1

def process(document, mode = False):
	"""预处理文档，同时去除停用词"""
	#设置分段标识符号，句号、问号等
	delimiters = r'[;.!?。？！；～\s]\s*'
	sentences = re.split(delimiters, document)
	result = []
	index = 0
	for s in sentences:
		item = sentence(s)
		if item.wordcount > 0:
			item.index = index
			result.append(item)
			index += 1

	global SC
	SC = index-1
	return result

if __name__ == '__main__':
	result = process('预处理文档，同时去除停用的得得词哎呦。正如您可以看到的一样。每次一个函数调用另外一个函数时，在下一次发生调用时，它自己的值和状态都会被挂起')
	for s in result:
		print (s.segements)
	print('\n')
	print('SC= %s' %  SC)
