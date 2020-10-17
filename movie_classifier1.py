import pandas as pd 
import numpy as np 
import nltk 
import random
import pickle

df = pd.read_csv('star-wars-or-harry-potter.csv')

documents = []
for i in range(len(df)):
	documents.append((df.iloc[i, 2], df.iloc[i, 1]))

random.shuffle(documents)

file =  open('documents.pickle', 'wb')
pickle.dump(documents, file)
file.close()

all_words = []

for sentence in df['sentence'].values:
	words = sentence.split()
	all_words += words

all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:5000]

file =  open('word_features.pickle', 'wb')
pickle.dump(word_features, file)
file.close()

def find_features(document):
	words = set(document.split())
	features = {}
	for word in word_features:
		features[word] = (word in words)
	return features

featuresets = [(find_features(sentence), movie) for (sentence, movie) in documents]
file =  open('featuresets.pickle', 'wb')
pickle.dump(featuresets, file)
file.close()

# print(featuresets[1])
# print(len(featuresets))

testing_set = featuresets[6000:]
training_set = featuresets[:6000]

classifier = nltk.NaiveBayesClassifier.train(training_set)
file =  open('classifier.pickle', 'wb')
pickle.dump(classifier, file)
file.close()

print('Accuracy :', (nltk.classify.accuracy(classifier, testing_set))*100)

text = 'hey anakin, i am luke your son. you will turn into darth vader and i will bring you back'
feats = find_features(text)
print(text, classifier.classify(feats))