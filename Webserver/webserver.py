import network
import time
from machine import Pin
from microWebSrv import MicroWebSrv

# Connect to Wi-Fi
ssid = '...'
password = '...'

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)

while not sta_if.isconnected():
    time.sleep(1)

print('Connected to Wi-Fi')
print('Network config:', sta_if.ifconfig())

# Define functions to be called when buttons are pressed
def toggle_led1():
    led_pin=Pin('LED', machine.Pin.OUT)
    led_pin.toggle()
    return "LED 1 Toggled"

def printConsole():
    print("Print Console active")
    return "Successfull print"

# Define web server request handlers
@MicroWebSrv.route('/')
def index(httpClient, httpResponse):
    content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MicroPython Web Server</title>
    </head>
    <body>
        <h1>MicroPython Web Server</h1>
        <button onclick="location.href='/led1'">Toggle LED</button>
        <br>
        <button onclick="location.href='/printConsole'">Print in Console</button>
    </body>
    </html>
    """
    httpResponse.WriteResponseOk(headers=None, contentType="text/html", contentCharset="UTF-8", content=content)

@MicroWebSrv.route('/led1')
def led1_route(httpClient, httpResponse):
    result = toggle_led1()
    httpResponse.WriteResponseOk(headers=None, contentType="text/html", contentCharset="UTF-8", content="<p>{}</p><a href='/'>Back</a>".format(result))

@MicroWebSrv.route('/printConsole')
def printConsole_route(httpClient, httpResponse):
    result = printConsole()
    httpResponse.WriteResponseOk(headers=None, contentType="text/html", contentCharset="UTF-8", content="<p>{}</p><a href='/'>Back</a>".format(result))

# Start the web server
srv = MicroWebSrv(webPath='/www')
srv.Start()

# Keep the main program running
while True:
    time.sleep(1)
