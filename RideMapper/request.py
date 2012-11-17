'''
Responsible for making requests of craigslist
and returning strings
'''
import urllib
import re
from posting import Posting, Postings
from xml.dom.minidom import parse, parseString

def __query(city):
    '''
    Opens an http request with a particular city, and returns the results
    as a string.
    '''
    requestURL = "http://" + city + ".craigslist.org/rid/index.rss"
    httpConnection = urllib.urlopen(requestURL)
    xmlstring = httpConnection.read(httpConnection)
    return xmlstring

def __parseQuery(city):
    '''
    Queries a city and parses the results as a minidom
    object.
    '''
    response = __query(city)
    return parseString(response)

def readQuery(city):
    '''
    Queries a city, and parses the result into a list
    of Posting objects.
    '''
    if city == 'test':
        #A stored xml file
        city = 'seattle'
        f = open('files/seattle.xml')
        minneapolisString = f.read()
        f.close()
        dom = parseString(minneapolisString)
    else:
        dom = __parseQuery(city)

    domItems = dom.getElementsByTagName('item')
    postings = []
    for i,item in enumerate(domItems):
        title = item.getElementsByTagName('title')[0].childNodes[0].wholeText
        postingDate = item.getElementsByTagName('dc:date')[0].childNodes[0].wholeText
        permalink = item.getElementsByTagName('link')[0].childNodes[0].wholeText
        #Get the reply to field
        #Currently commented out, due to speed issues.
        #TODO: Change this to work
        if (False):
            permalinkPage = urllib.urlopen(permalink)
            permalinkHTML = permalinkPage.read()
            permalinkPage.close()
            match = re.search('(mailto:)([^?]+)',permalinkHTML)
            if match:
                mailToLink = match.group(2)
            else:
                mailToLink = "emailnotfound"
        else:
            mailToLink = "emailnofound"
        shortDescription = item.getElementsByTagName('description')[0].childNodes[0].wholeText
        postings.append(Posting(city,title,permalink,shortDescription,postingDate,mailToLink))
    postingsObject = Postings(postings)
    return postingsObject

if __name__ == '__main__':
    items = readQuery('test')
