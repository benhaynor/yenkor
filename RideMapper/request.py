'''
Responsible for making requests of craigslist
and returning strings
'''
import sys
import urllib
import re
from posting import Posting, Postings
from xml.dom.minidom import parse, parseString
import datetime

def __query(city):
    '''
    Opens an http request with a particular city, and returns the results
    as a string.

    Args:
    city: A string of the city to query

    Returns:
    Craigslist xml for that city
    '''
    requestURL = "http://" + city + ".craigslist.org/rid/index.rss"
    httpConnection = urllib.urlopen(requestURL)
    xmlstring = httpConnection.read(httpConnection)
    return xmlstring

def __parseQuery(city):
    '''
    Queries a city and parses the results as a minidom
    object.

    Args: 
    city:A string representation of the city
    
    Returns: A parsed version of the Craigslist xml resonse
    
    '''
    response = __query(city)
    return parseString(response)

def readQuery(city,queryEmail):
    '''
    Queries a city, and parses the result into a list
    of Posting objects.

    Args:
    city: A string representation of the city to query
    queryEmaiL: a boolean whether to search for the reply_to e-mail
    associated with each post.  This (unfortunately) is quite slow.

    returns:
    postingsObject: A list of postings.  
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
        if (queryEmail):
            print i
            permalinkPage = urllib.urlopen(permalink)
            permalinkHTML = permalinkPage.read()
            permalinkPage.close()
            match = re.search('(mailto:)([^?]+)',permalinkHTML)
            if match:
                mailToLink = match.group(2)
            else:
                mailToLink = "emailnotfound"
        else:
            mailToLink = "emailnotfound"
        shortDescription = item.getElementsByTagName('description')[0].childNodes[0].wholeText
        postings.append(Posting(city,title,permalink,shortDescription,postingDate,mailToLink))
    postingsObject = Postings(postings)
    return postingsObject

if __name__ == '__main__':
    items = readQuery(sys.argv[1],True)
    items.writeToCSV((sys.argv[1] + datetime.datetime.now().__str__() + '.csv').replace(' ',''))

