class Posting:
    
    def __init__(self,postingFrom,title,permalink,shortDescription,
                 postingDate):
        '''
        An object which stores information relevant to a posting.
        
        Keyword arguments:
        title: the title of the post
        postingFrom: the city from which to go
        permalink: a link to the posting page, where I can later look for the full post
        shortDescription: the incomplete body of the post available from the xml feed
        postingDate: the date when the post went online
        '''
        self.title = title
        self.postingFrom = postingFrom
        self.permalink = permalink
        self.shortDescription = shortDescription
        self.postingDate = postingDate

    def __str__(self):
        return 'Posting from: %s\nTitle: %s\n' % (self.postingFrom, self.title)

    def __repr__(self):
        return ('Posting\nPosting from: %s\nTitle: %s\nShort Description: %s\nPermalink: %s\n' 
                'Post date: %s\n' % (self.postingFrom, self.title,self.shortDescription, self.permalink, self.postingDate))
