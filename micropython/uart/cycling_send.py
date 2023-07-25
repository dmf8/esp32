from machine import Timer
from machine import UART

from machine import Pin

t0=Timer(0)
led = Pin(2, Pin.OUT)

def blink_once(on_time):
    led.on()
    t0.init(mode=Timer.ONE_SHOT,period=on_time,callback=lambda t: led.off())

uart1=UART(1,timeout=1000)

def try_read(t):
    content=uart1.read()
    if content:
        blink_once(100)


t0=Timer(0)
t0.init(mode=Timer.PERIODIC,period=1000,callback=try_read)