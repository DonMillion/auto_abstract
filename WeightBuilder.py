import PreProcessor,re
from TopicClass import Topic

def LexRank(sentenceList, SimMat):
	"""用LexRank算法计算每个句子的显著度"""
	
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

def getPSS(document=PreProcessor.fullDoc):
	"""getParagraphSpecialSentences
		获取所有段落的第一,二个句子,最后一个句子,标题
		@return set
	"""

	firSen = {}
	secSen = {}
	lastSen = {}
	title = {}

	paragraphs = document.splitlines()
	delimiters = r'[;.!?。？！；～\s]\s*'
	i = 0
	for paragraph in paragraphs:
		sentences = re.split(delimiters, paragraph)
		count = len(sentences)

		# 如果这个段落只有一个句子，说明是个标题
		if count == 1:
			title[sentences[0]] = i

		# 如果有两个或以上的句子，说明是个正常段落
		else:
			firSen[sentences[0]] = i
			secSen[sentences[1]] = i
			lastSen[sentences[count-1]] = i
		i += 1
		
	return firSen, secSen, lastSen, title

def getCharacter():
	"""计算句子特征
	"""