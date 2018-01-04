from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import sys
import argparse

sys.path.append('/usr/local/lib/python2.7/site-packages')

from influxdb import InfluxDBClient

json_body = [
    {
        "measurement": "Database_Temp",
        "tags": {
            "Rack_Num": "3",
            "CRV_Num": "N/A"
               },
        "fields": {
            "value": 23.6
               }
           }
       ]

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'mydb')
client.write_points(json_body)                       
result = client.query('select * from "Database_Temp"')
print("Result: {0}".format(result))
