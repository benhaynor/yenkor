import datetime
import pickle
import re
import operator
import csv
from collections import Counter

def keyWithMaxVal(d):
    """ a) create a list of the dict's keys and values; 
    b) return the key with the max value"""  
    v=list(d.values())
    k=list(d.keys())
    return k[v.index(max(v))]

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

class Posting:

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
        self.postingFrom = postingFrom
        self.permalink = permalink
        self.shortDescription = shortDescription.lower()
        self.postingDate = postingDate
        self.mailToLink = mailToLink
        self.computeFields()
        
    def computeFields(self):
        '''
        Computes the csv fields.
        '''
        self.parsedPostingDate = Posting.__parseDate(self.postingDate)
        self.wordBag = Counter()
        for word in self.title.split(' '):
            self.wordBag[word] += 1
        for word in self.shortDescription.split(' '):
            self.wordBag[word] += 1

        
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
        '''
        Reads from a file
        '''
        title = csvRow[0]
        postingFrom = csvRow[1]
        permalink = csvRow[2]
        shortDescription = csvRow[3]
        postingDate = csvRow[4]
        mailToLink = csvRow[5]
        return Posting(postingFrom,title,permalink,shortDescription,
                       postingDate,mailToLink)

    
    @staticmethod
    def __parseDate(postingDate):
        year = int(postingDate[0:4])
        month = int(postingDate[5:7])
        day = int(postingDate[8:10])
        hour = int(postingDate[11:13])
        minute = int(postingDate[14:16])
        second = int(postingDate[17:19])
        return datetime.datetime(year,month,day,hour,minute,second)

    def guessLeavingFrom(self):
        '''
        @Retrun: a (string) best guess of where this ride is leaving from.
        Using my best NLP.
        '''
        title = self.title.lower()
        match = re.search('(from )([^ ]*)',title)
        if match:
            return match.group(2)
        else:
            return self.postingFrom

    def guessGoingTo(self):
        '''
        @Retrun: a (string) best guess of where this ride is going to.
        Using my best NLP
        '''
        title = self.title.lower()
        match = re.search('(to )([^ ]*)',title)
        if match:
            return match.group(2)
        else:
            return "hey"
    
    def guessLeavingOn(self):
        '''
        @Return: a date object best guess of when this ride is leaving.
        '''
        todayDay = self.parsedPostingDate.weekday()
        todayDate = self.parsedPostingDate.timetuple()[2]
        #if ((self.wordBag['today'] + self.wordBag['tomorrow']) > 0):
        #    return todayDate if self.wordBag['today'] >= self.wordBag['tomorrow'] else todayDate + 1
        days = ['mon', 'tues','wed','thur','fri','satur','sun']
        months = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        dayCounts = {day: 0 for day in days}
        dayNumber = {day: i for (i, day) in enumerate(days)}
        
        for day in days:
            dayMatches = re.findall(day,self.title.lower())
            if dayMatches:
                dayCounts[day] += len(dayMatches)
            bodyMatches = re.findall(day,self.shortDescription.lower())
            if bodyMatches:
                dayCounts[day] += len(bodyMatches)
        maxDay = keyWithMaxVal(dayCounts)
        maxCounts = dayCounts[maxDay]
        if maxCounts > 0:
            bestGuessOfDay = str(todayDate + ((dayNumber[maxDay] - todayDay + 7) % 7))
            print 'best guess: %s' % bestGuessOfDay
            return bestGuessOfDay
        else:
            return str(todayDate)
        
    def guessPassenger(self):
        '''
        @Return: a boolean guessing whether this is a passenger or a driver.
        '''
        return "hey"

    def __str__(self):
        return 'Posting from: %s\nTitle: %s\nDate: %s\n' % (self.postingFrom, self.title, self.parsedPostingDate.__str__())

    def __repr__(self):
        return ('Posting\nPosting from: %s\nTitle: %s\nShort Description: %s\nPermalink: %s\n' 
                'Post date: %s\nMail to link: %s\n' % (self.postingFrom, self.title,self.shortDescription, self.permalink, self.postingDate,
                                     self.mailToLink))

class ParsedPostings:

    '''
    Stores a list of ParsedPostings, with methods to read, and write from file.
    as well as easily annotate things.
    '''
    
    def __str__(self):
        outStr = ''
        for p in self.parsedPostings:
            outStr += p.__str__() + '\n'
        return outStr
    
    def __init__(self, parsedPostings):
        '''
        Store a list of postings.
        '''
        self.parsedPostings = parsedPostings

    @staticmethod
    def readFromCSV(inFileName):
        '''
        Reads from two CSV files.
        '''
        with open('parsedListings/rawVersion' + outFileName, 'wb') as csvfile:
            with open('parsedListings/yvalues' + outFileName, 'wb') as rawFile:
                csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
                csvwriter.writerow(Posting.headerFields)
                for p.Posting in self.parsedPostings:
                    csvwriter.writerow(p.asCSVRow())
 
 
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(ParsedPosting.yvalHeaders)
            for p in self.parsedPostings:
                csvwriter.writerow(p.yvalCSVRow())
        

    def writeToCSV(self,outFileName):
        with open('parsedListings/parsedVersion' + outFileName, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(ParsedPosting.headerFields)
            for p in self.parsedPostings:
                csvwriter.writerow(p.asCSVRow())
        with open('parsedListings/rawVersion' + outFileName, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(Posting.headerFields)
            for p.Posting in self.parsedPostings:
                csvwriter.writerow(p.asCSVRow())
        with open('parsedListings/yvalues' + outFileName, 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(ParsedPosting.yvalHeaders)
            for p in self.parsedPostings:
                csvwriter.writerow(p.yvalCSVRow())
            

    def dump(self, outFileName):
        ''' Pickles the list'''
        out = open('parsedandpickled/' + outFileName,'w')
        pickle.dump(self,out)
        out.close()

    @staticmethod
    def load(inFileName):
        ''' Unpickles the list '''
        inFile = open('parsedandpickled/' + inFileName,'r')
        p = pickle.load(inFile)
        inFile.close()
        return p
    
    def testGoingTo(self):
        '''
        return fraction correct
        '''
        correct = 0
        incorrect = 0
        for pp in self.parsedPostings:
            if pp.checkGoingTo() is not None:
                if pp.checkGoingTo() == 1:
                    correct += 1
                else:
                    incorrect += 1
        return float(correct) / float(correct + incorrect)

    def testLeavingFrom(self):
        '''
        return fraction correct
        '''
        correct = 0
        incorrect = 0
        for pp in self.parsedPostings:
            if pp.checkLeavingFrom() is not None:
                if pp.checkLeavingFrom() == 1:
                    correct += 1
                else:
                    incorrect += 1
        return float(correct) / float(correct + incorrect)

    def testLeavingOn(self):
        '''
        return fraction correct
        '''
        correct = 0
        incorrect = 0
        for pp in self.parsedPostings:
            check = pp.checkLeavingOn()
            if check is not None:
                if check == 1:
                    correct += 1
                else:
                    incorrect += 1
        return float(correct) / float(correct + incorrect)
                
    @staticmethod
    def parseAndPickle(postingsObject,outFileName, maxnumber):
        '''
        Takes a postings object, for each posting, prints it out,
        asks the user to give a name. For testing, I'll only parse
        the first 10 object.
        '''
        parsedPostings = []
        for i in range(min(maxnumber,len(postingsObject.postings))):
            print 'entry %d' % i
            print '\n\n\n'
            print postingsObject.postings[i].__repr__()
            leavingFrom = raw_input('Where is this post leaving from?')
            goingTo = raw_input('Where is this post going to?')
            #TODO: This is hard coded
            leavingOnYear = 2012#int(raw_input('What year is this post leaving on?'))
            #TODO This is hard coded
            leavingOnMonth = 11#int(raw_input('What month is this post leaving on?'))
            leavingOnDay = int(raw_input('What day of the month is this post leaving on?'))
            #TODO: I'm not yet trying to parse what time of dat they're leaving
            leavingOnHour = 0 #int(raw_input('What time of day  (0,6) (broken into chunks of 6)?'))
            driving = "d" == raw_input('Is the person a driver (d)')
            leavingOn = datetime.datetime(leavingOnYear,leavingOnMonth,leavingOnDay,leavingOnHour)
            pp = ParsedPosting(postingsObject.postings[i],leavingFrom,goingTo,leavingOn, driving)
            parsedPostings.append(pp)
            #DUMP EACH TIME
            pps = ParsedPostings(parsedPostings)
            pps.dump(outFileName)

class ParsedPosting:
    '''
    Has a posting object, as well as the important fields,
    leaving from, going to, date.  Should be using inheritance
    but I'm not going to bother right now.
    '''
        
    def __str__(self):
        outStr = self.posting.__str__()
        outStr += '\ndriver :' + str(self.driver)
        outStr += '\ngoingTo :' + self.goingTo
        outStr += '\nleavingOn :' + self.leavingOn.__str__()
        return outStr
        
    def checkGoingTo(self):
        '''
        Checks whether the best guess goingTo agrees with the
        human parsed version of going to.  
        @return: an int: 1 is a match. 0 is a miss.  -1 for an 
        invalid Postring
        @rtype: int
        '''

        if self.goingTo == "invalid":
            return None
        elif (self.posting.guessGoingTo() == self.goingTo):
            return 1
        else: 
            return 0

    def checkLeavingFrom(self):
        '''
        Checks whether the best guess goingTo agrees with the
        human parsed version of going to.  
        @return: an int: 1 is a match. 0 is a miss.  -1 for an 
        invalid Postring
        @rtype: int
        '''
        if self.goingTo == "invalid":
            return None
        elif (self.posting.guessLeavingFrom() == self.leavingFrom):
            return 1
        else: 
            return 0

    def checkLeavingOn(self):
        '''
        Checks whether the best guess goingTo agrees with the
        human parsed version of going to.  
        @return: an int: 1 is a match. 0 is a miss.  -1 for an 
        invalid Postring
        @rtype: int
        '''
        if self.goingTo == "invalid":
            return None
        else: 
            print "value: %s" % self.leavingOn.timetuple()[2]
            if (int(self.posting.guessLeavingOn()) == int(self.leavingOn.timetuple()[2])):
            #DELETE ME
                return 1
            else: 
                return 0

    def checkPassenger(self):
        '''
        Checks whether the best guess goingTo agrees with the
        human parsed version of going to.  
        @return: an int: 1 is a match. 0 is a miss.  -1 for an 
        invalid Postring
        @rtype: int
        '''
        if self.goingTo == "invalid":
            return None
        elif (self.posting.guessDriver() == self.driver):
            return 1
        else: 
            return 0

    def __init__(self,posting, leavingFrom, goingTo, leavingOn, driver):
        '''
        Keyword arguments:
        posting: the posting object (string)
        leavingFrom:  the city origin (currently assumed to be the city where it was posted) (string)
        goingTo: the destination (string)
        leavingOn: the datetime when the person is leaving
        '''
        self.posting = posting
        self.leavingFrom = leavingFrom
        self.goingTo = goingTo
        self.leavingOn = leavingOn
        self.driver = driver

    headerFields = ['from','to',
                    'departureDate','postingID',
                    'replyto','isDriver',
                    'title','body']
    
    yvalHeaders = ['from','to','departureDate','isDriver']

    def yvalCSVRow(self):
        '''
        Prints all the predicted variables.  I'll want help reading more.
        '''
        return [self.leavingFrom, self.goingTo,
                self.leavingOn, self.driver]

    def asCSVRow(self):
        '''
        Returns an array of fields in a particular order
        to be sent to a CSV file
        '''
        return [self.leavingFrom, self.goingTo,
                self.leavingOn,self.posting.permalink,
                self.posting.mailToLink, self.driver,
                self.posting.title,self.posting.shortDescription]

    @staticmethod
    def ParsePosting(posting):
        '''
        Takes a Posting object, and attempts to parse it, 
        returning a ParsedPosting object
        '''
        leavingFrom = posting.postingFrom
        #TODO: Actually parse the goingTo field
        goingTo = 'not yet implemented.  This should be a guess'
        #TODO: Actually parse the leavingOn field
        leavingOn = posting.parsedPostingDate 
        return ParsedPosting(posting,leavingFrom,goingTo,leavingOn)

