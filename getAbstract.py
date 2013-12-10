import TopicClass, PreProcessor, SubTopic, AbstractBuilder, WeightBuilder
from operator import attrgetter

def init():
	SubTopic.SimSum = 0

def setPercent(percent):
	AbstractBuilder.fetchPercent = percent

def getPercent():
	return AbstractBuilder.fetchPercent

def getDocSC():
	return PreProcessor.SC


def fetch(document):
	init()

	sentences = PreProcessor.process(document)

	topicList = SubTopic.buildTopic(sentences)

	WeightBuilder.buildSentenceWeight(sentences, topicList, SubTopic.SimMat)

	abstract = AbstractBuilder.fetchSentence(topicList, SubTopic.SimMat)

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