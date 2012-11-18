import nltk
import string

def findTo(title, body):
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
