import nltk
import random
from nltk.corpus import movie_reviews

import csv

titles = []
bodies = []
invalids = []
drivers = []
fromFields = []
toFields = []

with open('sfIsGood.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    i = -1
    for row in spamreader:
        i += 1
        if (i > 0):
            titles.append(row[0])
            bodies.append(row[3])
            fromFields.append(row[6])
            toFields.append(row[7])
            invalids.append(row[6] == 'invalid')
            drivers.append(row[10])

words = []
for i in range(len(titles)):
    words += nltk.word_tokenize(titles[i])
    words += nltk.word_tokenize(bodies[i])

documents = [((nltk.word_tokenize(titles[i]) +
               nltk.word_tokenize(bodies[i]))
              , drivers[i]) for i in range(len(titles))]
random.shuffle(documents)

all_words = nltk.FreqDist(w.lower() for w in words)



def document_features(document): 
    document_words = set(document) 
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

for k in [10,20,30,40,50,60,70,80,90,100]:
    word_features = all_words.keys()[:100] 
    totalAccuracy = 0;
    for i in range(5):
        random.shuffle(documents)
        featuresets = [(document_features(d), c) for (d,c) in documents]
        train_set, test_set = featuresets[20:], featuresets[:20]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        totalAccuracy += nltk.classify.accuracy(classifier, test_set)
    print k
    print totalAccuracy / 5
    
