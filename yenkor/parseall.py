import os
import glob
import sys
from parsing import classifydata
import argparse

if __name__ == '__main__':
    '''
    Parses all the csv files in a folder of clrequests.
    creates an identical folder in parsed clrequests with the same name.
    Parses 
    '''
    dirs = os.path.dirname(sys.argv[1])
    indir = os.path.split(dirs)[1] 
    outdir = os.path.join('parsedclrequests',indir)   
    os.mkdir(outdir)
    for f in glob.glob(sys.argv[1] + "/*.csv"):
        print 'parsing ' + f.__str__()
        classifydata.classifyData(f,outdir)
