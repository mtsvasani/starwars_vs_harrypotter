import pandas as pd 
import numpy as np 
import nltk 
import random
import pickle



documents_f = open('documents.pickle', 'rb')
documents = pickle.load(documents_f)
documents_f.close()

##featuresets_f = open('featuresets.pickle', 'rb')
##featuresets = pickle.load(featuresets_f)
##featuresets_f.close()

word_features_f = open('word_features.pickle', 'rb')
word_features = pickle.load(word_features_f)
word_features_f.close()


def find_features(document):
	words = set(document.split())
	features = {}
	for word in word_features:
		features[word] = (word in words)
	return features


classifier_f = open('classifier.pickle', 'rb')
classifier = pickle.load(classifier_f)
classifier_f.close()



def guess_movie(text):
	feats = find_features(text.lower())
	return classifier.classify(feats)


print('success')
