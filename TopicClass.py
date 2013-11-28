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