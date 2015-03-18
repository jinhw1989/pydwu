import threading
import time
import urllib
from datetime import datetime, timedelta
import os
exitFlag = 0

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter = 5, year = 1900):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.year = year
    def run(self):
        print "Starting " + self.name
        # print_time(self.name, self.counter, 5)
        retrieve_data(self.name, self.year)
        print "Exiting " + self.name

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1
CURRENT_FOLDER = os.path.dirname(os.path.realpath(__file__))
def retrieve_data(threadName, year):
    START_DATE = datetime.strptime(str(year)+"-01-01", "%Y-%m-%d")
    END_DATE = datetime.strptime(str(year+1)+"-01-01", "%Y-%m-%d")
    num_days = (END_DATE - START_DATE).days
    work_day = START_DATE
    work_folder = os.path.join(CURRENT_FOLDER, str(year))
    # work_folder = os.mkdir(os.path.join(CURRENT_FOLDER, str(year)))
    for i in range(num_days):
        y = work_day.year
        m = "%02d" % work_day.month
        d = "%02d" % work_day.day
        address = "http://www.wunderground.com/history/airport/KORD/{}/{}/{}/DailyHistory.html?format=1".format(
            y, m, d)
        # filename = os.path.join(
        #     META_DATA_FOLDER, "wunderground_{}_{}_{}.csv".format(y, m, d))
        filename = os.path.join(work_folder, "wunderground_{}_{}_{}.csv".format(y, m, d))    
        urllib.urlretrieve(address, filename)
        outFile = ""
        with open(filename, "r") as inFile:
            inFile.readline()
            for line in inFile:
                line = line.replace("<br />", "")
                outFile += line
        with open(filename, "w") as inputFile:
            inputFile.write(outFile)
        work_day = work_day + timedelta(days=1)
# Create new threads
# thread1 = myThread(1, "1991", 5, year=1991)
# thread2 = myThread(2, "1992", 5, year=1992)
# thread3 = myThread(3, "Thread-3", 1)
# thread4 = myThread(4, "Thread-4", 1)
# thread5 = myThread(5, "Thread-5", 1)
# thread6 = myThread(6, "Thread-6", 1)
# thread7 = myThread(7, "Thread-7", 1)
# thread8 = myThread(8, "Thread-8", 1)
# Start new Threads
# thread1.start()
# thread2.start()
# thread3.start()
# thread4.start()
# thread5.start()
# thread6.start()
# thread7.start()
# thread8.start()
for i in range(1991, 1992):
    myThread(i, name = str(i), year = i).start()
print "Exiting Main Thread"