import request
import posting

if __name__ == '__main__':
    #rawPostings = request.readQuery('test') 
    #posting.ParsedPostings.parseAndPickle(rawPostings,'seattle30.pickle',30)
    pps = posting.ParsedPostings.load('seattle30.pickle')
    #pps = posting.ParsedPostings.testGoingTo()
    print pps.testGoingTo()
    print pps.testLeavingFrom()
    print pps.testLeavingOn()
