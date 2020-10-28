#!/usr/bin/env python

import requests
import os

status_code = 500

while status_code != 200:
    status_code = requests.get('http://google.com').status_code

os.system('/home/pi/dev/api/launchAPI.sh')