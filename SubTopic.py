import PreProcessor,math
from operator import itemgetter,attrgetter
from ResultAnalyzer import Analyzer

nodeRoot = []
SimSum = 0

#计算每个单词在所有句子中的出现频率
def calculateFrequency(sentences):
	DocFrequency = {}
	for sentence in sentences:
		for word in sentence.segements:
			if word in DocFrequency:
				DocFrequency[word] += 1
			else:
				DocFrequency[word] = 1
	return DocFrequency

#计算每个特征项（词语）的权重
def calculateWeight(sentences):
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
	#初始化相似矩阵，所有元素置0
	SimMat = [[-1] * PreProcessor.SC for i in range(PreProcessor.SC)]
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
				SimList.append({'xy':(x,y),'sim':sim})

			# else:#相同句子设为-1
			# 	SimMat[x][y] = -1
			# 	SimList.append({'xy':(x,y),'sim':-1})
	return SimMat,SimList

#寻找并返回节点所在树的节点
def findRoot(n):
	if nodeRoot[n] == -1:
		return n
	else:
		nodeRoot[n] = findRoot(nodeRoot[n])
		return nodeRoot[n]

#合并两个节点所在的树，若成功，返回1,否则0
def merge(x,y):
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
		

#生成最大生成树,kruskal算法
def buildTree(SimList):
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
			count += 1
			if count == PreProcessor.SC-1:
				break
	return T,TreeMatrix

def devideTree(Tree,TreeMatrix,sentences):
	global SimSum
	#计算平均相似度
	avg = SimSum/(PreProcessor.SC-1)
	#遍历整个最大生成树集合计算顶点(句子)重要度：与其相似度大于avg的顶点的数目和顶点的度
	for e in range(Tree):
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

# 	print(SimSum)
# 	print(avg)
# 	#按重要度优先，度次要排序顶点（句子）
	sortedSentences = sorted(sentences,key=attrgetter('imp','d'),reverse = True)

# 	#选择凝聚点
# 	Kmeans = []
# 	for s in sortedSentences:
		
		

def main():
	result = PreProcessor.process('预处理文档，同时去除停用的得得词哎呦。预处理文档。每次一个函数调用另外一个函数时，在下一次发生调用时，它自己的值和状态都会被挂起')
	doc = calculateWeight(result)
	SimMat,SimList = buildSimilarMatrix(result)
	print('\n')
	for i in SimMat:
		print(i)
		print('\n')
	print(buildTree(SimList))

if __name__ == '__main__':
	main()