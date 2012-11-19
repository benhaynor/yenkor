from trainDriverClassifier import TrainedClassifier
from toFinder import findTo
import csv
import sys
import nltk

if __name__ == "__main__":
    titles = []
    bodies = []
    fromFields = []
    toFields = []
    inavlids = []
    drivers = []
    ctitles = []
    cbodies = []
    cdrivers = []
    driverClassifier = TrainedClassifier('driver')
    invalidClassifier = TrainedClassifier('invalid')

    with open(sys.argv[1], 'rb') as csvfile:
        with open('parsed'+sys.argv[1],'wb') as csvfileout:
            spamreader = csv.reader(csvfile, delimiter=',')
            outwriter = csv.writer(csvfileout, delimiter=',')
            i = -1
            for row in spamreader:
                i += 1
                if (i > 0):
                    rowDoc = (nltk.word_tokenize(row[0]) + nltk.word_tokenize(row[0]))
                    #If it's a valid entry
                    if invalidClassifier.classify(rowDoc) == 'False':
                        #Find the to field
                        to = findTo(row[0],row[3])
                        if to:
                            outwriter.writerow(row + [driverClassifier.classify(rowDoc), row[1],row[4],to])
                else:
                    outwriter.writerow(row + ['driver','from','leaving','to'])
