from trainDriverClassifier import TrainedClassifier
from toFinder import findTo
from dateScraper import scrapeDate
import csv
import sys
import nltk
import os

DRIVER_THRESHOLD_PROBABILITY = 0.95 
VALID_SUBMISSION_THRESHOLD = 0.9

def classifyData(inFileName, outdir):
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

    with open(inFileName, 'rb') as csvfile:
        with open(outdir + 'parsed'+os.path.split(inFileName)[1],'wb') as csvfileout:
            spamreader = csv.reader(csvfile, delimiter=',')
            outwriter = csv.writer(csvfileout, delimiter=',')
            i = -1
            for row in spamreader:
                i += 1
                if (i > 0):
                    rowDoc = (nltk.word_tokenize(row[0]) + nltk.word_tokenize(row[3]))                
                    pDriver = driverClassifier.prob_classify(rowDoc).prob('TRUE')                        
                    confidentInDriver = abs(pDriver - 0.5) >= abs(DRIVER_THRESHOLD_PROBABILITY - 0.5)
                    #Returns none if it can't guess a date
                    dateGuess = scrapeDate(row)
                    pValid = invalidClassifier.prob_classify(rowDoc).prob('False')
                    confidentOfValidity = abs(pValid - 0.5) >= abs(VALID_SUBMISSION_THRESHOLD - 0.5)
                    if confidentOfValidity and confidentInDriver and dateGuess:
                    #if invalidClassifier.classify(rowDoc) == 'False' :
                        #If the centainty about the driver decision is less than 95%
                        #throw away the data
                        #Find the to field
                        to = findTo(row[0],row[3])
                        if to:
                            outwriter.writerow(row + [driverClassifier.classify(rowDoc), row[1],dateGuess,to])
                else:
                    outwriter.writerow(row + ['driver','from','leaving','to'])

if __name__ == "__main__":
    try:
        classifyData(sys.argv[1],sys.argv[2])
    except IndexError:
        classifyData(sys.argv[1],'')
