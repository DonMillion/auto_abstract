# -*- coding: utf-8 -*-
# 整个文摘程序对外的统一接口
import TopicClass, PreProcessor, SubTopic, AbstractBuilder, WeightBuilder
from operator import attrgetter

def init():
	"""初始化，清理各个模块中的问题全局变量"""
	# 预处理模块
	PreProcessor.SC = 0
	PreProcessor.fullDoc = ''
	PreProcessor.fullDocLen = 0
	PreProcessor.sentences = []

	# 子主题
	SubTopic.nodeRoot = []
	SubTopic.SimSum = 0
	SubTopic.topicList = []
	SubTopic.SimMat = []

	# 权重构造模块
	WeightBuilder.firSent = []

	# 文摘抽取模块

def setPercent(percent):
	"""设置压缩率"""
	AbstractBuilder.fetchPercent = percent

def getPercent():
	"""获取压缩率"""
	return AbstractBuilder.fetchPercent

def getDocSC():
	"""获取源文档的句子数"""
	return PreProcessor.SC

def getN():
	"""获取文摘的句子数"""
	return AbstractBuilder.N


def fetch(document):
	# 初始化
	init()

	# 预处理文档
	sentences = PreProcessor.process(document)
	# 如果句子数少于或等于5则直接返回
	if PreProcessor.SC <= 5:
		AbstractBuilder.N = PreProcessor.SC
		return document

	topicList = SubTopic.buildTopic(sentences)

	WeightBuilder.buildSentenceWeight(sentences, topicList, SubTopic.SimMat)

	abstract = AbstractBuilder.fetchSentence(topicList, SubTopic.SimMat)

	# 按照原文顺序排序
	abstract.sort(key=attrgetter('index'))

	sentList = [sent.source for sent in abstract]
	result = '。\n'.join(sentList) + '。'
	return result

def main():
	fileLoc = 'example.txt'
	docfile = open(fileLoc, mode='r', encoding='utf8')
	content = docfile.read()
	docfile.close()

	abstract = fetch(content)
	print(abstract)

if __name__ == '__main__':
	main()