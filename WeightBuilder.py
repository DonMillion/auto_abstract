import PreProcessor,re
import jieba.posseg as posseg
from TopicClass import Topic

cuewordFileLoc = "cuewords.txt"

def LexRank(sentenceList, SimMat):
	"""在每个子主题内用LexRank算法计算每个句子的显著度"""
	
	indexList = {s.index for s in sentenceList}
	N = len(sentenceList)
	d = 0.15 # 阻尼系数，介于[0.1,0.2]之间
	Threshold = None # 变化程度阈值

	while True:
		enough = True
		for u in sentenceList:
			firstWeight = 0

			# 句子的显著度由其相邻节点的显著度决定
			for v in sentenceList:
				if SimMat[u.index][v.index] > 0:
					secondWeight = 0

					# 相邻节点的显著度再由其自身的相邻节点的显著度决定
					for z in indexList:
						if SimMat[v.index][z] > 0:
							secondWeight += SimMat[v.index][z]
					firstWeight += SimMat[u.index][v.index]/firstWeight*v.LexScore

			newLexScore = d/N + (1-d)*firstWeight
			if abs(newLexScore-u.LexScore) > Threshold:
				enough = False
			u.LexScore = newLexScore

		if enough:
			break

def calculateLexScore(topicList, SimMat):
	"""计算所有句子的LexScore"""

	for t in topicList:
		LexRank(t, SimMat) # 用LexRank算法
		t.getAvgSim(SimMat) # 同时主题内计算矩阵平均值


def getPSS(document=PreProcessor.fullDoc):
	"""getParagraphSpecialSentences
		获取所有段落的第一,二个句子,最后一个句子,标题
		@return set
	"""

	firSen = {}
	secSen = {}
	lastSen = {}
	titles = {}

	paragraphs = document.splitlines()
	delimiters = r'[;.!?。？！；～\s]\s*'
	i = 0
	for paragraph in paragraphs:
		sentences = re.split(delimiters, paragraph)
		count = len(sentences)

		# 如果这个段落只有一个句子，说明是个标题
		if count == 1:
			titles[sentences[0]] = i

		# 如果有两个或以上的句子，说明是个正常段落
		else:
			firSen[sentences[0]] = i
			secSen[sentences[1]] = i
			lastSen[sentences[count-1]] = i
		i += 1
		
	return firSen, secSen, lastSen, titles

def loadTitleword(titles):
	"""加载标题中的所有词（去除停用词）"""

	titleWord = {}
	for title in titles:
		words = posseg.cut(title)
		for w in words:
			if w.word not in PreProcessor.STOPWORDS and w.flag == 'n':
				titleWord[w.word] = None
	return titleWord

def loadCueword():
	"""加载线索词字典"""

	cuewordFile = open(cuewordFileLoc)
	cuewords = {} #遍历字典时速度会快点
	for word in cuewordFile.read().split('\n'):
		cuewords[word] = None
	cuewordFile.close()
	return cuewords

# CUEWORDS = loadCueword()

def calculateFeatureScore(sentences):
	"""计算所有句子特征"""

	firSen, secSen, lastSen, titles = getPSS()
	titleWord = loadTitleword(titles)

	for s in sentences:
		# 先判断是否为段首句，第二句，或者最后一句
		if s.source in firSen:
			s.wp = 1
		elif s.source in secSen or s.source in lastSen:
			s.wp = 0.5
		else:
			s.wp = 0

		# 检查线索词
		hasCUE = False
		for word in s.segements:
			if word in CUEWORDS:
				hasCUE = True
				break
		s.wc = 1 if hasCUE else 0

		# 检查标题词
		hasTitle = False
		for word in s.segements:
			if word in titleWord:
				hasTitle = True
				break
		s.wt = 1 if hasTitle else 0

		# 检查句子是否陈述句且含有名词
		startIndex = PreProcessor.fullDoc.find(s.source)
		endSymble = PreProcessor.fullDoc[startIndex+len(s.source)] # 这个句子的结束符号
		# 如果是陈述句
		hasNoun = False
		if endSymble in '.;。；':
			for word in s.segements:
				if s.segements[word][flag] == 'n':
					hasNoun = True
					break
		s.ws = 1 if hasNoun else 0

		# 四个调节因子，a+b+c+d = 1
		a = 0.5
		b = 0.2
		c = 0.15
		c = 0.15
		s.FeatureScore = a*s.wp+b*s.wc+c*s.wt+d*s.ws

def calculSentenceWeight(sentences, topicList, SimMat):
	""" 计算所有句子的权重 """
	
	# 先计算LexScore和FeatureScore
	calculateLexScore(topicList, SimMat)
	calculateFeatureScore(sentences)

	for s in sentences:
		# 过短的句子意义不大，舍弃之
		if s.wordcount <= 6:
			s.weight = 0
		else:
			s.weight = s.LexScore+s.FeatureScore*s.belong.SimMatAvg