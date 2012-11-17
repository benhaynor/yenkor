from collections import Counter
from collections import Set
from string import punctuation

class BagOfWords():
    '''
    Takes as an input a list of strings
    '''
    @staticmethod
    def cleanString(rawString):
        rawString = rawString.lower()
        for (l,r) in [('sfo','sanfrancisco'),
                      ('san francisco', 'sanfrancisco'),
                      ('la','losangeles'),
                      ('los angeles','los algeles'),
                      ('sb','santabarbara'),
                      ('santa barbara','santabarbara'),
                      ('slo','sanluisobispo'),
                      (',',' '),
                      ('\n',' ')]:
            rawString = rawString.replace(l,r)
        exclude = set(punctuation)
        rawString= ''.join(ch for ch in rawString if ch not in exclude)
        return rawString
            
    def __init__(self, strings):
        self.wordCounts = Counter()
        for string in strings:
            string = BagOfWords.cleanString(string)
            for word in string.split(' '):
                self.wordCounts[word] += 1
        self.setTopWords()

    def setTopWords(self):
        d = self.wordCounts
        self.topKeys = sorted(d, key=d.get, reverse=True):

class predictor():
    
    def __init__(self, wordBag):
        
    
if __name__ == '__main__':
    f = open('rawListingCSVs/sfTitle.csv')
    fstring = f.read()
    f.close()
    fbag = BagOfWords([fstring])
    d = fbag.wordCounts
    i = 0;
     
        i += 1
        if i > 100:
            break
        print w, d[w]
