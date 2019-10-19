#!/usr/bin/env python3
# coding=utf-8

import requests
import json
from datetime import datetime

response = requests.get("192.168.1.30:8082/test/SANVICENTEDELPALACIO")    # make a get http request
print(response)