# Based on sample code provided here :
# https://www.raspberrypi.com/news/how-to-run-a-webserver-on-raspberry-pi-pico-w/

import network
import socket
import time
import urequests

ssid = 'SSID'
password = 'PASSWORD'

#Default hosted website text
html = """<!DOCTYPE html>
<html>
    <head>
    <style>
        h1 {text-align: center;}
        p {text-align: center;}
        div {text-align: center;}
    </style>
    <title>Print N Play</title> </head>
    <body> <h1>Pico W Hosted Website</h1>
        <p>%s</p>
        <a href="http://www.printnplay.ca">Print N Play Website</a>
    </body>
</html>
"""

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

connectCount = 0



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

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

# Get current time
r = urequests.get('http://worldtimeapi.org/api/ip')
result = str(r.content)
startTime = result[int(result.find("datetime")) + 11:30 + result.find("datetime")]


print('Start Time', startTime)
print('listening on', addr)

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        clientIP = addr[0]
        print('client connected from', clientIP)
        request = cl.recv(1024)
        request = str(request)
        connectCount += 1
        countText = "This site has been accessed " + str(connectCount) + " time since " + startTime

        response = html % countText

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(response)
        cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')
