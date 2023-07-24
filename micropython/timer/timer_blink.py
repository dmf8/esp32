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
    

