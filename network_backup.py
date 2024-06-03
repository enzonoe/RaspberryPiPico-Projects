import network
import socket
import time
from secrets import *

wlan = network.WLAN(network.STA_IF)

class Server:
    #host = '172.31.68.204'
    #port = 8392
    def __init__(self, host: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((host, port))
            print('Started server')
        except socket.error as e:
            print(f"Error: {e}")
            if('48' in str(e)):

                print('Could not start server.. Port[' + str(port) + '] already in use? ')
            quit()
    
    def listen(self):
        while True:
            self.socket.listen(1)
            cnt, adr = self.socket.accept()
            print("ich hasse dich")
            self.handler(adr,cnt)

    def handler(self, adr, cnt):
        html = open('index.html', 'r', encoding='utf-8')
        response = html.read()
        html.close()
        while(True):
            data = cnt.recv(1024)
            data1 = list(data)
            if len(data1) == 0:
                break
                
            decoded = bytes(data1).decode("utf-8")
            cnt.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cnt.send(response)
            
            
            if not data:
                break

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

"""
def connectable():
    html = open('index.html', 'r', encoding='utf-8')

    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
    
    addr = socket.getaddrinfo('192.168.1.101', 80)[0][-1]
    
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    
    print('listening on', addr)
    
    # Listen for connections
    while True:
        try:
            #statement = "ooooooh maaahgaaahd"
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
    
        except OSError as e:
            cl.close()
            print('connection closed')
        
do_connect()
connectable()
"""

host = '10.0.0.101'
port = 80
host=do_connect()
Server(host, port).listen()