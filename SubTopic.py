import PreProcessor,math
from operator import itemgetter,attrgetter
from TopicClass import Topic

# 子主题模块
# 计算句子之间的相似度，构建相似矩阵
# 用K-means聚类，以划分出子主题

nodeRoot = []
SimSum = 0

def calculateFrequency(sentences):
	"""计算每个单词在所有句子中的出现频率"""
	DocFrequency = {}
	for sentence in sentences:
		for word in sentence.segements:
			if word in DocFrequency:
				DocFrequency[word] += 1
			else:
				DocFrequency[word] = 1
	return DocFrequency

def calculateWeight(sentences):
	"""计算每个特征项（词语）的权重"""
	DocFrequency = calculateFrequency(sentences)
	#从每个句子算
	for sentence in sentences:
		for word in sentence.segements:
			TF = sentence.segements[word]['TF']/sentence.wordcount
			IDF = math.log(PreProcessor.SC/DocFrequency[word],10) + 0.01
			sentence.segements[word]['weight'] = TF * IDF
	return DocFrequency

#构建相似矩阵
def buildSimilarMatrix(sentences):
	"""初始化相似矩阵，所有元素置0"""
	SimMat = [[0] * PreProcessor.SC for i in range(PreProcessor.SC)]
	SimList = []
	for x in range(0,PreProcessor.SC):
		for y in range(x+1,PreProcessor.SC):
			if x != y:
				xSege = sentences[x].segements
				ySege = sentences[y].segements
				intersection = set(xSege) & set(ySege)

				#余弦定理计算相似度
				if len(intersection) == 0:
					sim = 0
				else:
					print('x:%s, y:%s, inter:%s' % (x,y,intersection))
					numerator = 0
					for word in intersection:
						numerator += xSege[word]['weight'] * ySege[word]['weight']
					xlength,ylength = 0,0
					for word in xSege:
						xlength += xSege[word]['weight'] ** 2
					for word in ySege:
						ylength += ySege[word]['weight'] ** 2
					denominator = math.sqrt(xlength) * math.sqrt(ylength)
					sim = numerator/denominator
				SimMat[x][y] = sim
				SimMat[y][x] = sim
				SimList.append({'xy':(x,y),'sim':sim})

			# else:#相同句子设为-1
			# 	SimMat[x][y] = -1
			# 	SimList.append({'xy':(x,y),'sim':-1})
	return SimMat,SimList

def findRoot(n):
	"""寻找并返回节点所在树的节点"""
	if nodeRoot[n] == -1:
		return n
	else:
		nodeRoot[n] = findRoot(nodeRoot[n])
		return nodeRoot[n]

def merge(x,y):
	"""合并两个节点所在的树，若成功，返回1,否则0"""
	xr = findRoot(x)
	yr = findRoot(y)
	if xr == yr :
		return 0
	else:
		global nodeRoot
		if xr < yr:
			nodeRoot[yr] = xr
		else:
			nodeRoot[xr] = yr
	return 1
		

def buildTree(SimList):
	"""生成最大生成树,kruskal算法"""
	T = [] #初始化树边集为空集
	TreeMatrix = [[0] * PreProcessor.SC for i in range(PreProcessor.SC)]
	E = sorted(SimList,key=itemgetter('sim'),reverse=True)
	global nodeRoot,SimSum
	nodeRoot = [-1 for i in range(PreProcessor.SC)]
	count = 0
	for e in E:
		x,y = e['xy']
		if (merge(x,y)) == 1:
			T.append(e)
			SimSum += e['sim']
			TreeMatrix[x][y] = e['sim']
			TreeMatrix[y][x] = e['sim']
			count += 1
			if count == PreProcessor.SC-1:	
				break
	return T,TreeMatrix

def findClosestTopic(TreeMatrix,node,topiclist):
	"""寻找最相近的主题，即直接到达，且路径上的相似度之和最大"""
	# 初始化，先把相邻的点加入候选集
	candidate = [ { 'index':i, 'sim': TreeMatrix[node][i] } for i in range(PreProcessor.SC) if TreeMatrix[node][i] > 0]
	end = [] #终端，即直接相连的topic的集合
	travel = [ 0 for i in range(PreProcessor.SC)] #记录已经遍历过的点
	travel[node] = 1

	for search in candidate:
		travel[search['index']] = 1
		# 已经是topic的话，直接加入终端集合
		if search['index'] in topiclist:
			end.append(search)
		# 否则，把其相邻的点加入候选，等待遍历
		else:
			for i in TreeMatrix[node] if travel[i] == 0 and TreeMatrix[node][i] > 0:
				member = {'index':i, 'sim':search['sim']+TreeMatrix[node][i]}
				candidate.append(member)

	closest = max(end,key=itemgetter('sim'))
	return closest['index']

def devideTree(Tree,TreeMatrix,sentences):
	"""划分子主题，用K-means聚类"""
	global SimSum
	#计算平均相似度
	avg = SimSum/(PreProcessor.SC-1)
	#遍历整个最大生成树集合计算顶点(句子)重要度：与其相似度大于avg的顶点的数目和顶点的度
	for e in Tree:
		x,y = e['xy']
		if not hasattr(sentences[x],'d'):
			sentences[x].imp = 0
			sentences[x].d = 0
		if not hasattr(sentences[y],'d'):
			sentences[y].imp = 0
			sentences[y].d = 0

		if e['sim'] > avg:
			sentences[x].imp += 1
			sentences[y].imp += 1
		sentences[x].d += 1
		sentences[y].d += 1

	#按重要度优先，度次要排序顶点（句子）
	sortedSentences = sorted(sentences,key=attrgetter('imp','d'),reverse = True)

	#第一次选择凝聚点
	Knodes = [] # Topic类 的集合
	Kdict = {} # Kdict和newKdict为记录{句子:子主题}映射的字典
	for s in sortedSentences:
		if s.imp > 0:
			newNode = True
			sIndex = s.index
			#从已选上的凝聚点中查看是否已有连通（相邻）
			for K in Knodes:
				KIndex = K.center.index
				if TreeMatrix[sIndex][KIndex] > 0 or TreeMatrix[KIndex][sIndex] > 0:
					newNode = False
					break
			if newNode:
				newTopic = Topic(s)
				Knodes.append(newTopic)
				Kdict[s] = newTopic
	
	# 循环选择凝聚点
	newKdict = {}
	while newKdict != Kdict:
		# 把其他点分到凝聚点
		Klist = {s.index for s in Kdict}
		for s in sentences:
			if s not in Kdict:
				TopCenterNum = findClosestTopic(TreeMatrix, s.index, Klist)
				selectedTopic = Kdict[sentences[TopCenterNum]]
				selectedTopic.attach.append(s)
				s.belong = selectedTopic # belong 用于记录句子属于哪个子主题
		
		# 重新计算聚类中心
		newKdict.clear()
		for Top in Knodes:
			newCenter = Top.newCenter()
			Top.reInit(newCenter)
			newKdict[newCenter] = Top
			newCenter.belong = Top

		newKdict, Kdict = Kdict, newKdict
	return Knodes


def main():
	result = PreProcessor.process('预处理文档，同时去除停用的得得词哎呦。预处理文档。每次一个函数调用另外一个函数时，在下一次发生调用时，它自己的值和状态都会被挂起')
	doc = calculateWeight(result)
	SimMat,SimList = buildSimilarMatrix(result)
	print('\n')
	for i in SimMat:
		print(i)
		print('\n')
	Tree,TreeMatrix = (buildTree(SimList))
	devideTree(Tree,TreeMatrix,result)

if __name__ == '__main__':
	main()