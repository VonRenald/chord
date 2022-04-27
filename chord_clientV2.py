#! /usr/bin/python3

import socket
import threading
from chord_tools import *
import random
import time



def printer():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind(('', 9000))
        serversocket.listen(5)
        print('listening on port:', serversocket.getsockname()[1])
        while True:
            (clientsocket, address) = serversocket.accept()
            json_data = json_recv(clientsocket)
            print(json_data)
        



client_stop = False
printer_thread = threading.Thread(target=printer)
printer_thread.start()

time.sleep(1)
while not client_stop:
    print("connection\tget\tupdate")
    client_stop = True
    printer_thread.killed 
print("fin1")

# data = ['get', 'other test', 88]
# for _ in range(3):
#     json_send('localhost', 8001, data)

# data = {
#     "type"  : 'get',
#     "key"   : 5,
#     "ip"    : '198:54:23448:6546',
#     "port"  : 9000
# }
# json_send('localhost', 8001, data)

