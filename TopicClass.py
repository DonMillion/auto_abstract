# 主题类，用以表示K-means中的一个主题
class Topic:
	def __init__(self,center):
		self.center = center # 聚类中心
		self.attach = [center] # 子主题内的句子集合

	#计算并返回新的凝聚点
	def newCenter(self):
		pass

	def reInit(self, nC=None):
		self.attach = []
		if nC == None:
			self.center = self.newCenter()
		else:
			self.center = nC
		self.attach.append[self.center]

	def getAvgSim(SimMat):
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


