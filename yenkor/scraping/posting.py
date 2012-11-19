import datetime
import pickle
import re
import operator
import csv
from collections import Counter, OrderedDict

'''
A kind of silly module for dealing with craigslist posts.  
Origionally, when I wrote the code, I was planning on doing.
Some of the NLP in this class.  When I began using the 
NLTK, i moved the functionality into those classes.
This is now a hollow shell of its former self.
@Author Ben Haynor
'''


class Posting:
    '''
    
    '''

    #Static variables
    headerFields = ['title','postingFrom',
                    'permalink','shortDescription',
                    'postingDate','mailToLink']

    def __init__(self,postingFrom,title,permalink,shortDescription,
                 postingDate,mailToLink):
        '''
        An object which stores information relevant to a posting.
        
        Keyword arguments:
        title: the title of the post
        postingFrom: the city from which to go
        permalink: a link to the posting page, where I can later look for the full post
        shortDescription: the incomplete body of the post available from the xml feed
        postingDate: a string representation of the 
        '''
        self.title = title.lower()
        self.postingFrom = postingFrom.lower()
        self.permalink = permalink
        self.shortDescription = shortDescription.lower()
        self.postingDate = postingDate
        self.mailToLink = mailToLink

    def asCSVRow(self):
        '''
        Returns an array of all the fields to be stored in the CSV file.
        Allows the parsedPosting object to be created from CSV.
        '''
        return [self.title,self.postingFrom,
                self.permalink,self.shortDescription,
                self.postingDate,self.mailToLink]
    
    @staticmethod
    def createFromCSV(csvRow):
        ''' Reads a posting object from a file.
        Writes
        '''
        title = csvRow[0]
        postingFrom = csvRow[1]
        permalink = csvRow[2]
        shortDescription = csvRow[3]
        postingDate = csvRow[4]
        mailToLink = csvRow[5]
        return Posting(postingFrom,title,permalink,shortDescription,
                       postingDate,mailToLink)
    
    def __str__(self):
        return 'Posting from: %s\nTitle: %s\nDate: %s\n' % (self.postingFrom, self.title)

    def __repr__(self):
        return ('Posting\nPosting from: %s\nTitle: %s\nShort Description: %s\nPermalink: %s\n' 
                'Post date: %s\nMail to link: %s\n' % (self.postingFrom, self.title, self.shortDescription, self.permalink, self.postingDate,
                                     self.mailToLink))


class Postings:
    '''
    Stores an array of Posting objects
    '''
    def writeToCSV(self,outFileName):
	'''
        Writes to raw file.
        '''
        with open(outFileName, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(Posting.headerFields)
            for p in self.postings:
                csvwriter.writerow(p.asCSVRow())

    @staticmethod
    def readFromCSV(inFileName):
        '''
        Reads a CSV of raw posting objects. 
        '''
        postings = []
        with open('rawListingCSVs/' + inFileName, 'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            for i, row in enumerate(csvreader):
                if i > 0:
                    postings.append(Posting.createFromCSV(row))
        
        return Postings(postings)

    def __init__(self,postings):
        self.postings = postings
        
    def __str__(self):
        strRep = ''
        for p in self.postings:
            strRep += p.__str__() + '\n'
        return strRep

