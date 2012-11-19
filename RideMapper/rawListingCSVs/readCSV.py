import csv

class TandB:

    def __init__(self,fileName):
        self.titles = []
        self.bodies = []
        self.rows = []
        with open(fileName, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            i = -1
            for row in spamreader:
                self.rows.append(row)
                i += 1
                if i > 0:
                    self.titles.append(row[0])
                    self.bodies.append(row[3])
