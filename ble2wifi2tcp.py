from bluetooth import BLE
from bluetooth import UUID
from socket import *
import network
import re
from machine import Timer
from machine import Pin
import time

wlan_info=0
debug=True

t0=Timer(0) # led timer
led = Pin(2, Pin.OUT)

def pin_op(t):
    led.value(1-led.value())

def blink(half_period):
	t0.init(mode=Timer.PERIODIC,period=half_period,callback=pin_op)

def stop():
    t0.deinit()

def activeBle():
    ble = BLE()
    ble.active(True)
    return ble

def adBle(ble):
    adv_data=bytearray(b'\x0a\x09')
    adv_data+=bytearray("conn_test".encode())
    ble.gap_advertise(100,adv_data=adv_data)
    blink(100)
    print("bluetooth advertise")

def handler(event, data):
    if 1 == event:
        stop()
        led.on()
        print("bluetooth connect")

    if 2 == event:
        print("bluetooth disconnect")

    if 3 == event:
        conn_hdl, char_hdl = data
        buffer = ble.gatts_read(char_hdl)
        getWlanInfo(buffer.decode())


def buildCharacter(uuid, flags):
    return (UUID(uuid), flags)

def buildService(uuid, chars):
    return (UUID(uuid), chars)

def regServices(ble):
    char1 = buildCharacter(0xabcd,0x2|0x8)
    serv1 = buildService(0xbcde, [char1])
    ble.gatts_register_services([serv1])

def infoAck():
    led.off()
    time.sleep(0.5)
    led.on()

str_ip="192.168.28.185"
def getWlanInfo(buf):
    global wlan_info
    global str_ip
    if "ssid"==buf:
        wlan_info|=0x1
        print("ssid xxx_office")
        infoAck()
    
    if "key"==buf:
        wlan_info|=0x2
        print("key xxx9017")
        infoAck()
    
    if "port"==buf:
        wlan_info|=0x8
        print("port 4321")
        infoAck()
    
    if "info"==buf:
        wlan_info|=0xf
        infoAck()
        time.sleep(0.5)
        infoAck()
        
    if "ip"==buf:
        wlan_info|=0x4
        print("ip 192.168.28.185")
        infoAck()
    else:
        re_ret=re.match("ip\s*(\d+\.\d+\.\d+\.\d+)",buf)
        if re_ret:
            wlan_info|=0x4
            str_ip=re_ret.group(1)
            print(str_ip)
            infoAck()
    


def wifiStatusName(status):
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

# start bluetooth
if debug:
    while True:
        cmd=input("cmd: ")
        if "bt" == cmd:
            ble=activeBle()
            regServices(ble)
            adBle(ble)
            ble.irq(handler)
            break
else:
    ble=activeBle()
    regServices(ble)
    adBle(ble)
    ble.irq(handler)



# wait for wlan info
while True:
    time.sleep(1)
    if debug:
        string=input()
        if string=="wlan":
            print("get all wlan info")
            break
    else:
        if 0xf==wlan_info:
            print("get all wlan info")
            break

# connect wlan
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('xxx_office', 'xxx9017')

for i in range(10):
    if wlan.isconnected():
        break
    else:
        print("current status:",wifiStatusName(wlan.status()))
        time.sleep(1)

if wlan.isconnected():
    print(wlan.ifconfig())
    blink(500)
else:
    print("connect failed")
    print(wifiStatusName(wlan.status()))


time.sleep(2)

# wait for command
if debug:
    while True:
        string=input("tcp:")
        if string=="conn":
            print("tcp connect")
            break


# connect tcp server
tcp_skt = socket(AF_INET, SOCK_STREAM)
tcp_server = (str_ip,4321)
tcp_skt.connect(tcp_server)
blink(2000)

# heartbeat
message = 'test msg '
i=0
def sendMsg(t):
    global i
    global tcp_skt
    global message
    tcp_skt.send(message+str(i))
    i=i+1

t1=Timer(1)
t1.init(mode=Timer.PERIODIC,period=1000,callback=sendMsg)
