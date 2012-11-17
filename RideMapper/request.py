'''
Responsible for making requests of craigslist
and returning strings
'''
import urllib
from posting import Posting
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
        shortDescription = item.getElementsByTagName('description')[0].childNodes[0].wholeText
        postings.append(Posting(city,title,permalink,shortDescription,postingDate))
        print postings[i].__repr__()
    return domItems

if __name__ == '__main__':
    items = readQuery('test')
