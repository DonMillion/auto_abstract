import PreProcessor
from TopicClass import Topic

def LexRank(sentenceList, SimMat):
	"""用LexRank算法计算每个句子的显著度"""
	
	indexList = {s.index for s in sentenceList}
	N = len(sentenceList)
	d = 0.15 # 阻尼系数，介于[0.1,0.2]之间
	Threshold = None # 变化程度阈值
	enough = True

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
		
