import TopicClass, PreProcessor, SubTopic, AbstractBuilder, WeightBuilder
from operator import attrgetter

def fetch(document):
	sentences = PreProcessor.process(document)

	topicList = SubTopic.buildTopic(sentences)

	WeightBuilder.buildSentenceWeight(sentences, topicList, SubTopic.SimMat)

	abstract = AbstractBuilder.fetchSentence(topicList, SubTopic.SimMat)

	abstract.sort(key=attrgetter('index'))

	return abstract

def main():
	fileLoc = 'example.txt'
	docfile = open(fileLoc, mode='r', encoding='utf8')
	content = docfile.read()
	docfile.close()

	abstract = fetch(content)

	for ab in abstract:
		print(ab.source)

if __name__ == '__main__':
	main()