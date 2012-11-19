import glob
import sys
import classifyData
sys.path.append('/home/benhaynor/Documents/FunProjects/RideMapper/rawListingCSVs')

if __name__ == '__main__':
    '''
    Parses all in the files in directory sys.argv[1]
    placing them in sys.argv[2]
    '''
    for files in glob.glob(sys.argv[1] + "/*.csv"):
        print 'parsing ' + files.__str__()
        classifyData.classifyData(files,sys.argv[2])
