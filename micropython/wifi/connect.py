import network
import time

def statusName(status):
    if network.STAT_IDLE ==status:
        return "idle"
    elif network.STAT_CONNECTING ==status:
        return "connecting"
    elif network.STAT_WRONG_PASSWORD  ==status:
        return "wrong password"
    elif network.STAT_NO_AP_FOUND  ==status:
        return "no ap found"
    elif network.STAT_CONNECT_FAIL  ==status:
        return "connect fail"
    elif network.STAT_GOT_IP  ==status:
        return "got ip"
    else:
        return "unknown status"

wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('sniper_office', 'sniper9017')

for i in range(5):
    if wlan.isconnected():
        break
    else:
        print("current status:",statusName(wlan.status()))
        time.sleep(1)

if wlan.isconnected():
    print(wlan.ifconfig())
else:
    print("connect failed")
    print(statusName(wlan.status()))





