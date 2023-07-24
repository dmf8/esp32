import network
from machine import Timer
from machine import Pin
import time

wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('sniper_office', 'sniper9017')

for i in range(5):
    if wlan.isconnected():
        break
    else:
        print("connecting...")
        time.sleep(1)

if wlan.isconnected():
    print(wlan.ifconfig())
    wlan.disconnect()
else:
    print("connect failed")




