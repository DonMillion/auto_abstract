# -*- coding: utf-8 -*-
import re
import jieba.posseg as posseg
from ResultAnalyzer import Analyzer

#用结巴（jieba）分词系统分词
#去除停用词

stopwordFileLoc = 'stopwords.txt'
SC = 0 #所有句子的总数(Sentence Count)
fullDoc = '' # 整个完整的原文
fullDocLen = 0 # 原文句子数量
sentences = [] 

def loadStopwords():
	"""加载停用词表"""
	stopwordFile = open(stopwordFileLoc, mode='r', encoding='utf8') # 打开停用词字典
	stopwords = {} #遍历字典时速度会快点
	for word in stopwordFile.read().split('\n'):
		stopwords[word] = None
	stopwordFile.close()
	return stopwords

STOPWORDS = loadStopwords()

class sentence:
	"""每个对象储存一个句子"""

	__slots__ = ['source', 'belong', 'wordcount', 'LexScore', 'imp', 'd', 'FeatureScore', 'segements', 'index', 'weight', 'wp', 'ws', 'wt', 'wc']

	def __init__(self, content):
		self.source = content
		temp = posseg.cut(content)
		self.wordcount = 0
		self.LexScore = 1
		self.imp = 0
		self.d = 0
		#去除停用词(包括标点符号)，同时计算每个词的出现次数
		self.segements = {}
		for w in temp:
			if w.word not in STOPWORDS:
				if w.word not in self.segements:
					self.segements[w.word] = {}
					self.segements[w.word]['TF'] = 1
					self.segements[w.word]['flag'] = w.flag
				else:
					self.segements[w.word]['TF'] += 1
				self.wordcount += 1

	def __repr__(self):
		return 'sentence({})'.format(self.source)

# def splitSentence(symbol, sents):
# 	"""以symbol作为分界符号把个个句子分开"""
# 	regx = '[^'+symbol+'“]+(?:'+symbol+'|“.*?”)'
# 	result = []
# 	for sent in sents:
# 		subsent = re.findall(regx, sent)
# 		print(subsent)
# 		if subsent:
# 			result.extend(subsent)
# 		else:
# 			result.append(sent) # 如果没有相应的符号就会为空，需要把原来的句子补上去
# 	return result

def process(document):
	"""预处理文档，同时去除停用词"""
	#设置分段标识符号，句号、问号等
	global fullDoc, fullDocLen
	fullDoc = document
	fullDocLen = len(document)

	delimiters = r'[;!?。？！；～\s]\s*'
	# 分句
	sent = re.split(delimiters, document)
	
	# 断句，按。？！；~五个符号分句，五次循环
	# 先从"。"开始
	# sent = re.findall(r'[^。“]+(?:。|“.*?”)', document)
	# # "？"
	# sent = splitSentence('？', sent)
	# sent = splitSentence('！', sent)
	# print(sent)

	result = []
	index = 0

	# 对每个句子进行处理
	for s in sent:
		item = sentence(s)
		if item.wordcount > 0:
			item.index = index
			result.append(item)
			index += 1

	global SC, sentences
	SC = index
	sentences = result
	return result