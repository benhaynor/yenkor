'''
Uses regex to scrape a row of a post for a date, a destination,
or (to be implemented), an origin.
'''

import nltk
import datetime
import re
import string

DAYRES = ['mon','tue','wed','thu','fri','sat','sun']
TODAYRE = 'today'
TOMORROWRE = 'tomorrow'
DATERE = '(\d{1,2})[/-](\d{1,2})'
MONRE = '(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)([^ ]*) (\d{1,2})'
MONRE2 = '(the)( )(\d{1,2})(th|nd)'
MONTHNUM = {'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}

def scrapeDate(row):
    '''
    Takes as an input a rows from a raw CSV file.
    As an output, gives the best guess of the departure date
    '''
    cldate = row[4]
    todayYear = row[4][0:4]
    todayMonth = row[4][5:7]
    todayDay = row[4][8:10]
    title = nltk.word_tokenize(row[0])
    body = nltk.word_tokenize(row[3])
    joined = title + body
    line = row[0] + ' ' + row[3]
    
    def formatDate(monthInt,dayInt):
        try:
            return '%s%02d-%02d%s' % (row[4][:5],monthInt,dayInt,row[4][10:])
        except ValueError:
            return cldate
    m = re.search(DATERE,line)
    if m:
        try:
            return formatDate(int(m.groups()[0]),int(m.groups()[1]))
        except ValueError:
            pass
            #2012-11-17T21:31:54-05:00
    
    m = re.search('asap',line)
    if m:
        return cldate

    m = re.search('(today)',line)
    if m:
        return cldate

    m = re.search('(tomorrow)',line)
    if m:
        try:
            return formatDate(int(todayMonth),int(todayDay))
        except ValueError:
            pass

    m = re.search(MONRE,line)
    if m:
        print "MONRE"
        return formatDate(MONTHNUM[(m.groups()[0])],int(m.groups()[2]))

    m = re.search(MONRE2,line)
    if m:
        print "MONRE2"
        return formatDate(int(todayMonth),int(m.groups()[2]))

    for i,day in enumerate(DAYRES):
        m = re.search(day,line)
        if m:
            print 'DAYRES'
            weekday = datetime.date(int(todayYear),int(todayMonth),int(todayDay)).weekday()
            return formatDate(int(todayMonth),int(todayDay) + (i - weekday) % 7)
        
    
def findTo(row):
    title = row[3]
    body = row[3]
    ttRaw = nltk.word_tokenize(title)
    titleTokens = []
    for t in ttRaw:
        if not t[0] in string.punctuation:
            titleTokens.append(t)
    lt = len(titleTokens)
    taggedTokens = [(t,0) for t in titleTokens]#nltk.pos_tag(titleTokens)
    for i in range(len(taggedTokens)):
        print taggedTokens[i][0]
        if taggedTokens[i][0] == 'to':
            try:
                return taggedTokens[i+1][0]
            except(IndexError):
                return None
    return None

if __name__ == "__main__":
    import readCSV
    tb = readCSV.TandB('boston2012-11-1808:46:11.720122.csv')
    for i in range(1,98):
        print 'Scanning row %d' % i
        res = scrapeDate(tb.rows[i])
        if res:
            print res
