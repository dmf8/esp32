from socket import *
import network
import time
from machine import Timer
from machine import Pin

t0 = Timer(0)
led = Pin(2, Pin.OUT)


def pin_op(t):
    led.value(1-led.value())


def blink(half_period):
    t0.init(mode=Timer.PERIODIC, period=half_period, callback=pin_op)


def stop():
    t0.deinit()


def statusName(status):
    if network.STAT_IDLE == status:
        return "idle"
    elif network.STAT_CONNECTING == status:
        return "connecting"
    elif network.STAT_WRONG_PASSWORD == status:
        return "wrong password"
    elif network.STAT_NO_AP_FOUND == status:
        return "no ap found"
    elif network.STAT_CONNECT_FAIL == status:
        return "connect fail"
    elif network.STAT_GOT_IP == status:
        return "got ip"
    else:
        return "unknown status"


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('sniper_office', 'sniper9017')

for i in range(5):
    if wlan.isconnected():
        break
    else:
        print("current status:", statusName(wlan.status()))
        time.sleep(1)

if wlan.isconnected():
    print(wlan.ifconfig())
    blink(500)
else:
    print("connect failed")
    print(statusName(wlan.status()))

tcp_skt = socket(AF_INET, SOCK_STREAM)
tcp_server = ("192.168.28.185", 4321)
tcp_skt.connect(tcp_server)
message = 'test msg '
i = 0


def sendMsg(t):
    global i
    global tcp_skt
    global message
    tcp_skt.send(message+str(i))
    i = i+1


t1 = Timer(1)
t1.init(mode=Timer.PERIODIC, period=1000, callback=sendMsg)


# for j in range(10400):
#     msg = str(j)
#     tcp_skt.send("%-16s" % msg)
