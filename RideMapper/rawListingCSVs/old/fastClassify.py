import nltk
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
            drivers.append(row[10] == 'TRUE')
