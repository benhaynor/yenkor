import request
import datetime
for city in ['newyork','losangeles','chicago','houston','philadelphia',
             'phoenix','sanantonio','sandiego','dallas','sanjose']:
    print city
    try:
        items = request.readQuery(city,False)
        items.writeToCSV(('top10cities/' + city + datetime.datetime.now().__str__() + '.csv').replace(' ',''))
    except:
        continue
