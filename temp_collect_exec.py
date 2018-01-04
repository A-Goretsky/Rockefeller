#IMPORTING MODULES
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import sys
import argparse
sys.path.append('/usr/local/lib/python2.7/site-packages')
from influxdb import InfluxDBClient


#Control Variables
spot_num = 6
box_num = 2
login_sleep = 10
interface_sleep = 30
error = 0
spot_temp_list = []
box_temp_list = [] #FORMAT = [max1, min1, avg1, max2, min2, avg2, etc...]
client = InfluxDBClient('localhost', 8086, 'root', 'root', 'mydb')
measurement_name = "Database_Temp"
rack_num_list_box = ['1', '6']  #Should be hardcoded to which racks boxes apply to if any.
rack_num_list_spot = ['11', 'N/A', 'N/A', '14', 'N/A', '16']  #Should be hardcoded to which racks spots apply to if any
crv_num_list_spot = ['N/A', '6', '9', 'N/A', '4', 'N/A'] #Should be hardcoded to which crv's spots apply to if any
crv_num_list_box = ['N/A', 'N/A'] #Should be hardcoded to which crv's boxes apply to if any

#DEFINED METHODS
def writeToInfluxBox():
    for i in range(0, box_num):
        #print "box: " + str(i) + "JSON"
        box_json = [
            {
                "measurement": measurement_name,
                "tags": {
                    "Spot_Num": "N/A",
                    "Box_Num": str(i + 1),
                    "Rack_Num": rack_num_list_box[i],
                    "CRV_Num": crv_num_list_box[i],
                    "Unit": "F"
                },
                "fields": {
                    "Max_Value": float(box_temp_list[(i * 3) + 0]),
                    "Min_Value": float(box_temp_list[(i * 3) + 1]),
                    "Avg_Value": float(box_temp_list[(i * 3) + 2])
                }
            }
        ]

        client.write_points(box_json)

def writeToInfluxSpot():

    #Use this template for all individual measurements to be added to
    #influx
    for i in range(0, spot_num):
        #print "spot: " + str(i) + "JSON"
        spot_json = [
            {
                "measurement": measurement_name,
                "tags": {
                    "Spot_Num": str(i + 1),
                    "Box_Num": "N/A",
                    "Rack_Num": rack_num_list_spot[i],
                    "CRV_Num": crv_num_list_spot[i],
                    "Unit": "F"
                },
                    "fields": {
                        "value": float(spot_temp_list[i])
                    }
            }
        ]

        client.write_points(spot_json)
    #result = client.query('select * from "Database_Temp"')
    #print("Result: {0}".format(result))

def writeToInfluxINTERN(intern_temp):
    #print "internJSON:"
    spot_json = [
        {
            "measurement": measurement_name,
            "tags": {
                "Spot_Num": "INTERNAL",
                "Box_Num": "N/A",
                "Rack_Num": "N/A",
                "CRV_Num": "N/A",
                "Unit": "F"
            },
                "fields": {
                    "value": float(intern_temp)
            }
        }
    ]

    client.write_points(spot_json)

##CONTROL PHANTOM_JS AND COLLECT DATA

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


##SPOT COLLECTION

for i in range(0, spot_num):
    try:
        spotXPATH = driver.find_element(By.XPATH, '//*[@id="spot-bar-' + str(i + 1) + '"]/p')
        spot_Temp = spotXPATH.get_attribute('data-value')
        #print spot_Temp
        spot_temp_list.append(spot_Temp)
        print "Spot " + str(i + 1) + ": " + spot_temp_list[i]
    except:
        print "Interface not properly Initialized, logging out to prevent issues..."
        driver.find_element_by_id('header-logout').click()
        error = 1
        time.sleep(10)
        break


##BOX COLLECTION
if (error != 1):
    for i in range(0, box_num):
        try:
            boxXPATH_max = driver.find_element(By.XPATH, '//*[@id="mbox-bar-' + str(i + 1) + '"]/p[1]')
            box_Temp_max = boxXPATH_max.get_attribute('data-value')
            box_temp_list.append(box_Temp_max)
            print "Box " + str(i + 1) + " - max: " + box_Temp_max
            boxXPATH_min = driver.find_element(By.XPATH, '//*[@id="mbox-bar-' + str(i + 1) + '"]/p[2]')
            box_Temp_min = boxXPATH_min.get_attribute('data-value')
            box_temp_list.append(box_Temp_min)
            print "Box " + str(i + 1) + " - min: " + box_Temp_min
            boxXPATH_avg = driver.find_element(By.XPATH, '//*[@id="mbox-bar-' + str(i + 1) + '"]/p[3]')
            box_Temp_avg = boxXPATH_avg.get_attribute('data-value')
            box_temp_list.append(box_Temp_avg)
            print "Box " + str(i + 1) + " - avg: " + box_Temp_avg
        except:
            print "Interface not properly Initialized, logging out to prevent issues..."
            driver.find_element_by_id('header-logout').click()
            error = 1
            time.sleep(10)
            break

##INTERNAL TEMP

if (error != 1):
    try:
        internalXPATH = driver.find_element(By.XPATH, '//*[@id="tempsens-bar-1"]/p')
        internal_uncutTemp = internalXPATH.get_attribute('innerText')
        internal_Temp = internal_uncutTemp.split()[0]
        print internal_uncutTemp
        print "Internal Temp: " + internal_Temp
    except:
        print "Interface not properly Initialized, logging out to prevent issues..."
        driver.find_element_by_id('header-logout').click()
        error = 1
        time.sleep(10)

#CALL INFLUX WRITE - Spot
if (error != 1):
    print "Writing to Spots"
    writeToInfluxSpot()
    print "Writing to Box"
    writeToInfluxBox()
    print "Writing Internal"
    writeToInfluxINTERN(internal_Temp)

#END SESSION
if (error != 1):
    print "Ending Session..."
    print "Logging Out... (10s)"

    driver.find_element_by_id('header-logout').click()

    time.sleep(10)
    driver.quit()
