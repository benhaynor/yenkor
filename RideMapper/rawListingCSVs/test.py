#import nltk
#from nltk.corpus import brown
#brown_tagged_sents = brown.tagged_sents(categories='news')
#brown_sents = brown.sents(categories='news')
#unigram_tagger = nltk.UnigramTagger(brown_tagged_sents)
#unigram_tagger.tag(brown_sents[2007])
#size = int(len(brown_tagged_sents) * 0.9)
#train_sents = brown_tagged_sents[:size]
#test_sents = brown_tagged_sents[size:]
#unigram_tagger = nltk.UnigramTagger(train_sents)
#print unigram_tagger.evaluate(test_sents)
#bigram_tagger = nltk.BigramTagger(train_sents)
#print bigram_tagger.tag(nltk.word_tokenize(tb.titles[7]))
import readCSV
import trainDriverClassifier
tb = readCSV.TandB('boston2012-11-1809:45:50.295898.csv')
tbclassifier = trainDriverClassifier.TrainedClassifier('driver')
