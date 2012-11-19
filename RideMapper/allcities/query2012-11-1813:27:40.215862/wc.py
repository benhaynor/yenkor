import glob,os
for f in glob.glob("*.csv"):
    p = os.popen('cat %s | wc' % f)
    print p.read()
