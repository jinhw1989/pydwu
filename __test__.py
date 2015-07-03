# -*- coding: utf-8 -*-

import urllib2
import json
import requests
content = urllib2.urlopen("http://ipinfo.io/json").read()
with open("ipinfo.json", "w") as outfile:
    outfile.write(content)

with open("ipinfo.json") as infile:
    data = json.load(infile)
    zipcode = data.get("postal")
print zipcode

