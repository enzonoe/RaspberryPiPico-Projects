import utime
import machine
from machine import Pin

while True:
    led_pin=Pin('LED', machine.Pin.OUT)
    led_pin.value(1)
    utime.sleep(1)
    led_pin.value(0)
    utime.sleep(1)