import csv
class TandB:

    def __init__(self,fileName):
        self.titles = []
        self.bodies = []
        with open(fileName, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            i = -1
            for row in spamreader:
                i += 1
                if i > 0:
                    self.titles.append(row[0])
                    self.bodies.append(row[3])
