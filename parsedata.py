#!/usr/bin/env python3
import json

with open('twitterData.json', 'r') as json_data:
    jsonData = json.load(json_data)

for i in jsonData:
    if "obama" in i['tweet'].lower():
        print(i)