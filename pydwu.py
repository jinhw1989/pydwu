# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import os
import re
import shutil
import sys
import tempfile
import threading
import time
import urllib
import urllib2
import pandas as pd
import getopt


__version__ = '0.0.1'
__author__ = 'Hongwei Jin'

usage = \
    """
    Pydwu version {}
    : a Python package to download observed data from WeatherUnderground without using API.

    usage pydwu [OPTIONS] -s <YYYY-MM-DD> -e <YYYY-MM-DD> -l <AirportCode>
        -h, --help  Display this usage message
        -s          Start date: YYYY-MM-DD
        -e          End date: YYYY-MM-DD
        -l          Location by airport code: e.g. KLAX
        -v, --version   Display version
    Example:
        Usage:
            pydwu -s 2010-01-02 -e 2010-02-01 -l KLAX
    """.format(__version__)


def get_history_using_HTTP(START_DATE, END_DATE, AIRPORT):
    ''' Get Historical Weather Data through HTTP

    :return status: True if downloaded successfully
    :rtype: boolean
    '''
    try:
        num_days = (END_DATE - START_DATE).days
        work_day = START_DATE
        # @TODO: use multi thread to download weather data if possible.
        for i in range(num_days):
            y = work_day.year
            m = "%02d" % work_day.month
            d = "%02d" % work_day.day
            address = "http://www.wunderground.com/history/airport/{}/{}/{}/{}/DailyHistory.html?format=1".format(
                AIRPORT, y, m, d)
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
    """ Merge the data in local folder into a single one

    :param airport: airport code
    :type airport: string
    """
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
    # replace files
    shutil.copyfile(os.path.join(working_dir, 'merged_history.csv'), "merged_history.csv")
    # remove temp file
    # os.remove(os.path.join(working_dir, "merged_history.csv"))


def remove_lines():
    """
    Remove those lines which have no weather recorded.

    Note: It may results in the majority rule. When filling with minutes data,
        whose missing values may considered as incorrectly.
    """
    with open(os.path.join(working_dir, "merged_history.csv"), "w") as outfile:
        with open(os.path.join(working_dir, "merged_history.csv")) as infile:
            outfile.write(infile.next())
            for line in infile:
                if line[0].isdigit():
                    outfile.write(line)
    # replace files
    shutil.copyfile(os.path.join(working_dir, 'merged_history.csv'), os.path.join(
        working_dir, "merged_history.csv"))
    # remove temp file
    os.remove(os.path.join(working_dir, "merged_history.csv"))


def pydwu(start_date, end_date, airport):
    """
    """
    try:
        sd = start_date
        ed = end_date
        START_DATE = datetime.strptime(sd, "%Y-%m-%d")
        END_DATE = datetime.strptime(ed, "%Y-%m-%d") + timedelta(days=1)
        AIRPORT = airport
        status = get_history_using_HTTP(START_DATE, END_DATE, AIRPORT)
        if status is True:
            merge_files(AIRPORT)
            remove_lines()
        else:
            print "Connection failed, please try again"
            sys.exit()
        content = urllib2.urlopen("http://www.whereismyip.com").read()
        ip_addr = re.search(r'[0-9]+(?:\.[0-9]+){3}', content).group(0)
        print ip_addr
        print working_dir
    except KeyboardInterrupt:
        print("processing interrupted")

    pass


def main(argv):
    """
    start
    """
    try:
        global working_dir
        # tf = tempfile.TemporaryFile(suffix='.csv')
        # tf.close()
        # print tf.name
        # working_dir = os.path.dirname(os.path.abspath(__file__))
        working_dir = tempfile.gettempdir()
        try:
            # print getopt.getopt(argv, "s:e:l:", ["start", "end", 'location'])
            opts, args = getopt.getopt(argv, "hvs:e:l:", ["help", "version", "start", "end", 'location'])
        except getopt.GetoptError as err:
            print str(err)
            print usage
            sys.exit()
        for o, a in opts:
            if o.lower() in ('-h', '--help'):
                print usage
                sys.exit()
            elif o.lower() in ("-v", "--version"):
                print "Pydwu with version {}".format(__version__)
                sys.exit()
            elif o in ("-s", "--start"):
                start_date = a
            elif o in ("-e", "--end"):
                end_date = a
            elif o in ("-l", "--location"):
                location = a
        try:
            start_date
        except NameError:
            print "Please specify the start date"
            print usage
            sys.exit()
        try:
            end_date
        except NameError:
            print "Please specify the end date"
            print usage
            sys.exit()
        try:
            location
        except NameError:
            print "Please specify the location"
            print usage
            sys.exit()
        pydwu(start_date, end_date, location)
    except KeyboardInterrupt:
        print("\nCancelling download processing...")

if __name__ == '__main__':
    main(sys.argv[1:])
