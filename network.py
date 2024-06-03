import network
import socket
import time
from secrets import *

wlan = network.WLAN(network.STA_IF)

def handle_websocket_message(client_socket, message):
    parsed_message = ujson.loads(message)
    if 'action' in parsed_message:
        action = parsed_message['action']
        if action == 'on':
            light_pin.value(1)  # Turn on the light
        elif action == 'off':
            light_pin.value(0)  # Turn off the light
        else:
            print("Invalid action:", action)

def handle_websocket_disconnect(client_socket):
    clients.remove(client_socket)
    print("WebSocket client disconnected")


def do_connect():
    #wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    accesspoints = wlan.scan()
    print("Access Points:")
    for ap in accesspoints:
        print(ap)
    wlan.connect(secrets['ssid'],secrets['password'])
    # False on first
    print("Connected:",wlan.isconnected())

    # Wait for connect or fail
    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('wifi connection failed')
    else:
        print('connected')
        ip=wlan.ifconfig()[0]
        print('network config: ', ip)
        return ip

def connectable():
    html = open('index.html', 'r', encoding='utf-8')

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    #Prints the current ip address of the pico
    print(wlan.ifconfig())
    
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
    
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('HTTP server started')
    print('listening on', addr)
    
    # Listen for connections
    while True:
        try:
            #cl = Client Socket"
            cl, addr = s.accept()
            print('client connected from', addr)
            request = cl.recv(1024)
            
            print(request)
            
            request = str(request)
            response = html.read()

            # Sends information
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            
            #for cl in range(1):
            #    try:
            #        message = s.receive(cl)
            #        if message is not None:
            #            handle_websocket_message(cl, message)
            #        else:
            #            handle_websocket_disconnect(cl)
            #    except OSError:
            #        handle_websocket_disconnect(cl)
    
            except OSError as e:
                cl.close()
                print('connection closed')

do_connect()
connectable()