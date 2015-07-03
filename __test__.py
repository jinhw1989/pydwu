# -*- coding: utf-8 -*-


import urllib2

content = urllib2.urlopen("http://ipinfo.io/json").read()
with open("ipinfo.json", "w") as outfile:
    outfile.write(content)

