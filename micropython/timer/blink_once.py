from machine import Timer
from machine import Pin

t0=Timer(0)
led = Pin(2, Pin.OUT)

def blink_once(on_time):
    led.on()
    t0.init(mode=Timer.ONE_SHOT,period=on_time,callback=lambda t: led.off())