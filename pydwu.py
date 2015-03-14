# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import os
import sys
import re
import urllib2
import tempfile
import threading
import time
import urllib
# try:
#     from argparse import ArgumentParser as ArgParser
# except ImportError:
#     from optparse import OptionParser as ArgParser

__version__ = '0.0.1'

usage = \
"""
usage pydwu [OPTIONS] --start=<YYYY-MM-DD> --end=<YYYY-MM-DD> --location=( ZIP | City | Airport )
    -h, --help  Display this usage message
    -w          Folder to store downloadereqdb.wmo=99999d file
    -z ZIP      Download zip code
    --version   Display version
Example:
    Usage:
    pydwu --start=2010-01-02 --end-2010-02-01 --location=60616
"""

def get_history_using_HTTP(START_DATE, END_DATE, AIRPORT):
    '''
    Get Historical Weather Data through HTTP
    '''
    try:
        num_days = (END_DATE - START_DATE).days
        work_day = START_DATE

        # @TODO: use multi thread to download weather data if possible.
        for i in range(num_days):
            y = work_day.year
            m = "%02d" % work_day.month
            d = "%02d" % work_day.day
            address = "http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html?format=1".format(AIRPORT,
                y, m, d)
            try:
                os.mkdir(os.path.join(working_dir, AIRPORT))
            except OSError:
                pass
            filename = os.path.join(
                working_dir, AIRPORT, "wunderground_{}_{}_{}.csv".format(y, m, d))
            urllib.urlretrieve(address, filename)
            outfile = ""
            with open(filename, "r") as infile:
                infile.readline()
                for line in infile:
                    line = line.replace("<br />", "")
                    outfile += line
            with open(filename, "w") as inputFile:
                inputFile.write(outfile)
            work_day = work_day + timedelta(days=1)
        return True
    except IOError:
        return False

def merge_files(airport):
    work_folder = os.path.join(working_dir, airport)
    file_list = os.listdir(work_folder)
    with open(os.path.join(work_folder, "..\\merged_history.csv"), "w") as outfile:
        for line in open(os.path.join(work_folder, file_list[0])):
            outfile.write(line)
        print "write the first line"
        for i in range(1, len(file_list)):
            with open(os.path.join(work_folder, file_list[i])) as infile:
                infile.next()
                for line in infile:
                    outfile.write(line)

def pydwu():
    """
    """
    try:
        sd = "1991-01-01"
        ed = "1991-01-31"
        START_DATE = datetime.strptime(sd, "%Y-%m-%d")
        END_DATE = datetime.strptime(ed, "%Y-%m-%d")
        AIRPORT = "KMDW"
        status = get_history_using_HTTP(START_DATE, END_DATE, AIRPORT)
        if status is True:
            merge_files(AIRPORT)
        content = urllib2.urlopen("http://www.whereismyip.com").read()
        ip_addr = re.search(r'[0-9]+(?:\.[0-9]+){3}', content).group(0)
        print ip_addr
        print working_dir
    except KeyboardInterrupt:
        print("processing interrupted")

    pass

def main():
    """
    start
    """
    try:
        global working_dir
        working_dir = os.path.dirname(os.path.abspath(__file__))
        pydwu()
    except KeyboardInterrupt:
        print("\nCancelling download processing...")

if __name__ == '__main__':
    main()