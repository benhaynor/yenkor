import nltk
import random
from nltk import NaiveBayesClassifier
import csv
import os

class TrainedClassifier:
    
    def classify(self,document):
        '''
        Takes a document classifies it
        '''
        df = self.document_features(document)
        return self.classifier.classify(df)

    def prob_classify(self,document):
        '''
        Takes a document classifies it
        '''
        df = self.document_features(document)
        return self.classifier.prob_classify(df)

    def trainingSetAccuracy(self):
        return nltk.classify.accuracy(self.classifier, self.training_set)

    def testSetAccuracy(self):
        '''
        
        '''
        accuracy = 0
        for i in range(5):
            print 'iteration %d' % i
            random.shuffle(self.training_set)
            train_set = self.training_set[20:]
            test_set = self.training_set[:20]
            tempClassifier = nltk.NaiveBayesClassifier(self.training_set)
            accuracy += nltk.classify.accuracy(tempClassifier, test_set)
        return accuracy / 5

    def document_features(self,document): 
        #word_features = ["offered","offering","get","around",
        #                 "take","pay","leaving","before","room",
        #                 "$","please","good","?","tomorrow",
        #                 "$","an","going","there","my"]
        document_words = set(document) 
        features = {}
        for word in self.word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features

    def __init__(self,classifierType):

        titles = []
        bodies = []
        invalids = []
        drivers = []
        fromFields = []
        toFields = []
        ctitles = []
        cbodies = []
        cdrivers = []

        
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname,'sfIsGood.csv'), 'rb') as csvfile:
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
                    if not row[6] == 'invalid':
                        ctitles.append(row[0])
                        cbodies.append(row[3])
                        cdrivers.append(row[10])

        words = []
        if classifierType == 'driver':
            for i in range(len(ctitles)):
                words += nltk.word_tokenize(ctitles[i])
                words += nltk.word_tokenize(cbodies[i])

            documents = [((nltk.word_tokenize(ctitles[i]) +
                           nltk.word_tokenize(cbodies[i]))
                          , cdrivers[i]) for i in range(len(ctitles))]
            random.shuffle(documents)

        elif classifierType == 'invalid':
            for i in range(len(titles)):
                words += nltk.word_tokenize(titles[i])
                words += nltk.word_tokenize(bodies[i])

            documents = [((nltk.word_tokenize(titles[i]) +
                           nltk.word_tokenize(bodies[i]))
                          , str(invalids[i])) for i in range(len(ctitles))]
            random.shuffle(documents)
            
        all_words = nltk.FreqDist(w.lower() for w in words)
        self.word_features = all_words.keys()[:500]
        self.training_set = [(self.document_features(d), c) for (d,c) in documents]
        self.classifier = NaiveBayesClassifier.train(self.training_set)
        
