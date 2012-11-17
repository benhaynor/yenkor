import request
import posting

if __name__ == '__main__':
    rawPostings = request.readQuery('test') 
    posting.ParsedPostings.parseAndPickle(rawPostings,'seattle30.pickle',30)
