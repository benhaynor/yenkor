import datetime
import pickle

class Postings:
    '''
    Stores an array of Posting objects
    '''

    def __init__(self,postings):
        self.postings = postings

    def __str__(self):
        strRep = ''
        for p in self.postings:
            strRep += p.__str__() + '\n'
        return strRep

class Posting:
    
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
        self.title = title
        self.postingFrom = postingFrom
        self.permalink = permalink
        self.shortDescription = shortDescription
        self.postingDate = postingDate
        self.parsedPostingDate = Posting.__parseDate(postingDate)
        self.mailToLink = mailToLink

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
        return "hey"

    def guessGoingTo(self):
        '''
        @Retrun: a (string) best guess of where this ride is going to.
        Using my best NLP
        '''
        return "hey"
    
    def guessLeavingDate(self):
        '''
        @Return: a date object best guess of when this ride is leaving.
        '''
        return "hey"
        
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
    
    def __init__(self, parsedPostings):
        '''
        Store a list of postings.
        '''
        self.parsedPostings = parsedPostings

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
    
    def 

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
            return -1
        else if (self.posting.guessGoingTo() == self.goingTo):
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
            return -1
        else if (self.posting.guessLeavingFrom() == self.leavingFrom):
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
            return -1
        else if (self.posting.guessLeavingFrom() == self.leavingFrom):
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
        if self.posting.goingTo == "invalid":
            return -1
        else if (self.posting.guessLeavingOn() == self.leavingOn):
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
        if self.posting.goingTo == "invalid":
            return -1
        else if (self.posting.guessDriver() == self.driver):
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
