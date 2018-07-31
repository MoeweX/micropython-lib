"""

This File contains almost exactly the content of my boot.py

This script will attempt to connect to any wifi specified.
If there is no connection within the specified time limit, the script will set up an access point.

"""

import machine
import pycom
import time
from network import WLAN

TIMEOUT = 15


wlan = WLAN(mode=WLAN.STA)

pycom.heartbeat(False)
pycom.rgbled(0xff0000)

class TimeoutError(Exception):
    pass

stopconn = False

def fallback_AP(alarm):
    # machine.deepsleep(2000) # uncomment, if you want to restart the wipy 3 instead of setting up your own access point.
    global stopconn
    pycom.rgbled(0x0000ff)
    time.sleep(0.5)
    stopconn = True


def connect_to_wifi(wifissid, wifipass, alarm):
    global stopconn
    print('Network found!')
    wlan.connect(ssid=wifissid, auth=(WLAN.WPA2, wifipass), timeout=5000)
    while not wlan.isconnected():
        if stopconn:
            raise TimeoutError('timed out')
        else:
            machine.idle()
    print('WLAN connection succeeded!')
    pycom.rgbled(0x00f000)
    alarm.cancel()
    return


nets = wlan.scan()
try:
    alarm = machine.Timer.Alarm(handler=fallback_AP, s=TIMEOUT)
    for net in nets:
        if net.ssid == YOUR_WIFI1_SSID:
            connect_to_wifi(wifissid = net.ssid, wifipass = YOUR_WIFI1_PW, alarm=alarm)
            break
        elif net.ssid == YOUR_WIFI2_SSID:
            connect_to_wifi(wifissid = net.ssid, wifipass = YOUR_WIFI2_PW, alarm=alarm)
            break
        elif net.ssid == YOUR_WIFI3_SSID:
            connect_to_wifi(wifissid = net.ssid, wifipass = YOUR_WIFI3_PW, alarm=alarm)
            break
    alarm.cancel()
except TimeoutError as e:
    print('Timeout while connecting to Wifi')
    print('Setting up Access Point')
    pycom.rgbled(0xff00ff)
    wlan.deinit()
    time.sleep(1)
    wlan.init(mode=WLAN.AP, ssid=YOUR_AP_SSID, auth=(WLAN.WPA2, YOUR_AP_PW), channel=1)


pycom.rgbled(0x00ff00)
time.sleep(1)
pycom.rgbled(0x000000)

# delay execution of main.py for 10 seconds to allow connecting and cancelling of execution
for i in range (10):
    pycom.rgbled(0x000000)
    time.sleep(0.5)
    pycom.rgbled(0x0b0000)
    time.sleep(0.5)
