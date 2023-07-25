from bluetooth import BLE
from bluetooth import UUID
from machine import Timer
from machine import Pin

t0=Timer(0)
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
    blink(200)

def handler(event, data):
    if 1 == event:
        print("connect")
        stop()
        led.on()
    if 2 == event:
         print("disconnect")
         led.off()

def buildCharacter(uuid, flags):
    return (UUID(uuid), flags)

def buildService(uuid, chars):
    return (UUID(uuid), chars)

def regServices(ble):
    char1 = buildCharacter(0xabcd,0x2|0x8)
    serv1 = buildService(0xbcde, [char1])
    ble.gatts_register_services([serv1])

ble2=activeBle()
regServices(ble2)
adBle(ble2)
ble2.irq(handler)