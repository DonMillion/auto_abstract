# 主题类，用以表示K-means中的一个主题
from operator import attrgetter

class Topic:
	def __init__(self,center):
		self.center = center # 聚类中心
		self.attach = [center] # 子主题内的句子集合

	def newCenter(self, TreeMatrix):
		"""计算并返回新的凝聚点"""

		avg = self.getAvgSim(TreeMatrix)

		# 在主题内计算重要度和度
		for sent in self.attach:
			sent.imp = 0
			sent.d = 0
			for s in self.attach:
				if TreeMatrix[sent.index][s.index] > 0:
					if TreeMatrix[sent.index][s.index] > avg:
						sent.imp += 1
					sent.d += 1

		result = max(self.attach, key=attrgetter('imp', 'd'), reverse=True)
		return result


	def reInit(self, nC=None):
		"""重新初始化"""

		self.attach = []
		if nC == None:
			self.center = self.newCenter()
		else:
			self.center = nC
		self.attach.append[self.center]

	def getAvgSim(self, SimMat):
		"""计算整个子主题内所有句子之间的相似度矩阵的平均值"""

		simSum = 0
		length = len(self.attach)
		for i in range(length):
			for j in range(i+1, length):
				x = self.attach[i].index
				y = self.attach[j].index
				simSum += SimMat[x][y]
		avg = simSum/(length*(length-1)/2)

		self.SimMatAvg = avg
		return avg

	def updateSentenScore(self, SimMat):
		"""更新主题中每个句子的权重"""

		for sent in attach:
			attachSim = [SimMat[sent.index][i.index] for i in attach]
			maxSim = max(attachSim)
			sent.score = sent.score*(1-maxSim)
