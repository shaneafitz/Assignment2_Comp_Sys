#!/usr/bin/python
# import libraries
import blynklib #used to connect the pi to the blynk app. Blynk app will have a gps trigger
from phue import Bridge #Philips hue library and importing the bridge component for communicating with the pi
from datetime import datetime #for use in getting current time
from suntime import Sun, SunTimeException # library for calculating sunset/sunrise times
import pytz # used to make sure both timezones are in the correct timezone
import requests #used to make a request to a web page and print the response text
import json #used to work with json data
import time #used for keeping stuff running
import logging
logging.basicConfig()
# Initialise variables
#Variables for sunset/sunrise data & coordinates of current location - Limerick
latitude = 52.67
longitude = -8.69
sun = Sun(latitude, longitude)
now = datetime.now(pytz.utc) #current time of day
# Get today's sunrise and sunset in UTC
today_sr = sun.get_sunrise_time()
today_ss = sun.get_sunset_time()
#Print statements to show data for troubleshooting. Commented out now
#print(now)
#print(today_sr)
#print(today_sr>now)
#print(now>today_ss)
#print('Today in Limerick the sun rose at {} and will set at {} UTC'.
#      format(today_sr.strftime('%H:%M'), today_ss.strftime('%H:%M')))
#Variables for lights and blynk authorization
b = Bridge('192.168.1.24') #Ip address of philips hue bridge
BLYNK_AUTH = 'YGlCQBf34N0FS4oFB6tAcFSrXaPU6OD0' #authorization code for blynk app
# initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)
# register handler for virtual pin V1 write event using blynk
@blynk.handle_event('write V1')
def write_virtual_pin_handler(pin, value):
    print('GPS activated:'+ str(value))
    if value[0]=="1":
       #Change the light state
        b.set_light([2,3], 'on', True) #both lights grouped together in an array and set the status to on
        #b.set_light([2,3], 'on', False)
    else :
        b.set_light([2,3], 'on', False) #Lights turned off after leaving the gps location
def door_motion_state():
    response = requests.get('http://192.168.1.24/api/4MO2i-WHT0xtMy-dhpW39gT9PmmyZslLOVBt8C7K/sensors/4') #get request to gather sensor data
    json_data = json.loads(response.text)
    #print('State:' + str(response.text)) Commented out for now-used while troubleshooting
    #print("Door sensor activated: " + str(json_data['state']['presence'])) Commented out for now-used while troubleshooting
    if json_data['state']['presence'] == True:
        #Change the light state
        b.set_light([2,3], 'on', True)
        print("Door sensor activated. ")
        #b.set_light([2,3], 'on', False)
if (now>today_ss):
        while True:
                blynk.run()
                door_motion_state()
                time.sleep(5)
else:
        while True:
                b.set_light([2,3], 'on', False)
                print('Lights will not come on during the daylight hours')