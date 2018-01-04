#IMPORTING MODULES
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import sys
import argparse
sys.path.append('/usr/local/lib/python2.7/site-packages')
from influxdb import InfluxDBClient
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'mydb')

#DEFINED METHODS
def writeToInfluxBox(box_max, box_min, box_avg, box_num):
    box_json = [
        {
            "measurement": "Database_Temp",
            "tags": {
                "Spot_Num": "N/A",
                "Box_Num": str(box_num),
                "Rack_Num": "14",
                "CRV_Num": "N/A",
                "Unit": "F"
            },
            "fields": {
                "Max_Value": float(box_max),
                "Min_Value": float(box_min),
                "Avg_Value": float(box_avg)
            }
        }
    ]

    client.write_points(box_json)

def writeToInfluxSpot(spot_temp, spot_num):

    #Use this template for all individual measurements to be added to
    #influx
    spot1_json = [
        {
            "measurement": "Database_Temp",
            "tags": {
                "Spot_Num": str(spot_num),
                "Box_Num": "N/A",
                "Rack_Num": "3",
                "CRV_Num": "N/A",
                "Unit": "F"
                },
            "fields": {
                "value": float(spot_temp)
                }
            }
        ]

    client.write_points(spot1_json)
    #result = client.query('select * from "Database_Temp"')
    #print("Result: {0}".format(result))

##CONTROL PHANTOM_JS AND COLLECT DATA

#Control Variables
login_sleep = 10
interface_sleep = 30
test_num = 10
test_interval = 5
error = 0

#Browser login and initialization of intrface
driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
driver.get("http://172.31.4.49/login")
driver.find_element_by_id('login_input_username').send_keys("admin")
driver.find_element_by_id("login_input_password").send_keys("admin")
driver.find_element_by_id("button-login").click()

print "Current URL: Should be: 'http://172.31.4.49/login'"
print driver.current_url
print "Login Initiating... (" + str(login_sleep) + "s)"
time.sleep(login_sleep)
print "Current URL Below -- Should be: 'http://172.31.4.49/'"
print driver.current_url
print "~~~~~~~~~~~~~~~~~~~~"
print "Camera and Interface Initiating... (" + str(interface_sleep) + "s)"
time.sleep(interface_sleep)
print "~~~~~~~~~~~~~~~~~~~~"
print "Beginning Thermal Data Collection..."
print "Data Points: " + str(test_num)
print "Interval: " + str(test_interval) + "s"

#Data collection and call to writeToInflux
for i in range(0, test_num):

    if (i == 0):
        print "~~~~~First "+ str(test_interval) +" Seconds~~~~~"

    #Use this template for all spots
    ##SPOT 1
    try:
        spot1XPATH = driver.find_element(By.XPATH, '//*[@id="spot-bar-1"]/p')
        spot1_uncut_Temp = spot1XPATH.get_attribute('innerHTML')
        spot1_cut_Temp = spot1_uncut_Temp[:4]
        print "Spot 1: " + spot1_cut_Temp
    except:
        print "Interface not properly Initialized, logging out to prevent issues..."
        driver.find_element_by_id('header-logout').click()
        error = 1
        time.sleep(10)
        break

    if (error == 1):
        break

    ##SPOT 2
    #spot2XPATH = driver.find_element(By.XPATH, '//*[@id="spot-bar-2"]/p')
    #spot2_uncut_Temp = spot2XPATH.get_attribute('innerHTML')
    #spot2_cut_Temp = spot2_uncut_Temp[:4]
    #print "Spot 2: " + spot2_cut_Temp

    ##SPOT 3
    #spot3XPATH = driver.find_element(By.XPATH, '//*[@id="spot-bar-3"]/p')
    #spot3_uncut_Temp = spot3XPATH.get_attribute('innerHTML')
    #spot3_cut_Temp = spot3_uncut_Temp[:4]
    #print "Spot 3: " + spot3_cut_Temp

    ##SPOT 4
    #spot4XPATH = driver.find_element(By.XPATH, '//*[@id="spot-bar-4"]/p')
    #spot4_uncut_Temp = spot4XPATH.get_attribute('innerHTML')
    #spot4_cut_Temp = spot4_uncut_Temp[:4]
    #print "Spot 4: " + spot4_cut_Temp

    #Use this template for all boxes.
    ##BOX 1
    box1XPATH_max = driver.find_element(By.XPATH, '//*[@id="mbox-bar-1"]/p[1]')
    box1_cutTempMax = box1XPATH_max.get_attribute('innerHTML')[5:9]
    print "BOX 1 - MAX: " + box1_cutTempMax
    box1XPATH_min = driver.find_element(By.XPATH, '//*[@id="mbox-bar-1"]/p[2]')
    box1_cutTempMin = box1XPATH_min.get_attribute('innerHTML')[5:9]
    print "BOX 1 - MIN: " + box1_cutTempMin
    box1XPATH_avg = driver.find_element(By.XPATH, '//*[@id="mbox-bar-1"]/p[3]')
    box1_cutTempAvg = box1XPATH_avg.get_attribute('innerHTML')[5:9]
    print "BOX 1 - AVG: " + box1_cutTempAvg

    #INTERNAL TEMP
    internalXPATH = driver.find_element(By.XPATH, '//*[@id="tempsens-bar-1"]/p')
    internal_cutTemp = internalXPATH.get_attribute('innerHTML')[:4]
    print "Internal Temp: " + internal_cutTemp

    #CALL INFLUX WRITE - Spot
    writeToInfluxSpot(spot1_cut_Temp, 1)

    #Call influx write - Box
    writeToInfluxBox(box1_cutTempMax, box1_cutTempMin, box1_cutTempAvg, 1)

    time.sleep(test_interval)

    if (i != 10):
        print "~~~~~Next "+ str(test_interval) +" Sec~~~~~~"



#END SESSION
if (error != 1):
    print "Ending Session..."
    print "Logging Out... (10s)"

    driver.find_element_by_id('header-logout').click()

    time.sleep(10)
    driver.quit()
