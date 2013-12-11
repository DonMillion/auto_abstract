# -*- coding: utf-8 -*-
import PreProcessor, math, WeightBuilder
from operator import attrgetter,itemgetter

# 文摘抽取模块

# 文摘抽取率
fetchPercent = 0.2
N = 0

def fetchSentence(topicList, SimMat):
	"""从主题中抽取文摘"""

	# 先计算每个子主题的重要度
	for t in topicList:
		topicScore = 0
		for s in t.attach:
			topicScore += s.weight
		t.score = topicScore
		# 主题内句子按重要度排序
		t.attach.sort(key=attrgetter('weight'), reverse=True)

	# 初始化
	finalAbstract = [] # 最终文摘
	topicList.sort(key=attrgetter('score'), reverse=True)
	global N
	N = math.ceil(PreProcessor.SC*fetchPercent) # 抽取的句子数
	i = 0
	count = 0 # 已抽取的文摘句子数
	SubTopicNum = len(topicList)

	while count < N :
		if i == SubTopicNum: # 意味把所有主题着遍历完一次，把下表i重置0
			i = 0
		if len(topicList[i].attach) == 1:
			# 子主题中只剩下一个句子时，如果是段首句则加入文摘
			if topicList[i].attach[0] in WeightBuilder.firSent:
				s = topicList[i].attach.pop()
				finalAbstract.append(s)
				count += 1

		elif len(topicList[i].attach) >= 2:
			# 剩下的句子大于或等于2个

			# 把权重最大的句子加入到文摘中
			fitstSent = topicList[i].attach.pop(0)
			finalAbstract.append(fitstSent)
			# 重新计算主题内句子的权重并排序
			topicList[i].updateSentenScore(SimMat)
			topicList[i].attach.sort(key=attrgetter('weight'), reverse=True)
			count += 1

		i += 1
	return finalAbstract