#! /usr/bin/python3

import socket
import threading
from chord_tools import *
import random

def printer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
        serversocket.bind(('', 9000))
        serversocket.listen(5)
        print('listening on port:', serversocket.getsockname()[1])
        while True:
            (clientsocket, address) = serversocket.accept()
            json_data = json_recv(clientsocket)
            print(json_data)

printer_thread = threading.Thread(target=printer)
printer_thread.start()

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


# while True:
#     _keyGet = input("key :")
#     data = {
#         "type"  : 'get',
#         "key"   : int(_keyGet),
#         "ip"    : '198:54:23448:6546',
#         "port"  : 9000
#     }
#     json_send('localhost', 8001, data)

# data = {
#     "type"  : 'get',
#     "key"   : 5,
#     "ip"    : '198:54:23448:6546',
#     "port"  : 9000
# }
# json_send('localhost', 8001, data)

data = {
    "type"  : 'update',
    "key"   : 5,
    "val"   : 9,
    "ip"    : '198:162:0:2',
    "port"  : 9000
}
json_send('localhost', 8001, data)

data = {
    "type"  : 'update',
    "key"   : 8,
    "val"   : 41,
    "ip"    : '198:162:0:2',
    "port"  : 9000
}
json_send('localhost', 8001, data)
data = {
    "type"  : 'update',
    "key"   : 25,
    "val"   : 0,
    "ip"    : '198:162:0:2',
    "port"  : 9000
}
json_send('localhost', 8001, data)
data = {
    "type"  : 'update',
    "key"   : 31,
    "val"   : 621,
    "ip"    : '198:162:0:2',
    "port"  : 9000
}
json_send('localhost', 8001, data)
data = {
    "type"  : 'update',
    "key"   : 16,
    "val"   : 9,
    "ip"    : '198:162:0:2',
    "port"  : 9000
}
json_send('localhost', 8001, data)
data = {
    "type"  : 'update',
    "key"   : 1,
    "val"   : 1,
    "ip"    : '198:162:0:2',
    "port"  : 9000
}
json_send('localhost', 8001, data)




data = {
    "type"  : 'get',
    "key"   : 5,
    "ip"    : '198:54:23448:6546',
    "port"  : 9000
}
json_send('localhost', 8001, data)
data = {
    "type"  : 'get',
    "key"   : 31,
    "ip"    : '198:54:23448:6546',
    "port"  : 9000
}
json_send('localhost', 8001, data)
data = {
    "type"  : 'get',
    "key"   : 8,
    "ip"    : '198:54:23448:6546',
    "port"  : 9000
}
json_send('localhost', 8001, data)
data = {
    "type"  : 'get',
    "key"   : 25,
    "ip"    : '198:54:23448:6546',
    "port"  : 9000
}
json_send('localhost', 8001, data)

for i in range(0,31):
    data = {
        "type"  : 'update',
        "key"   : i,
        "val"   : random.randrange(32),
        "ip"    : '198:162:0:2',
        "port"  : 9000
    }
    json_send('localhost', 8001, data)

data = {# Ip Port Id Vget Vupd Vgeti 
    "type"  : 'quit',
    "ip"    : 'localhost',
    "port"  : 9000,
    "id"    : None,
    "vget"  : 0,
    "vupd"  : 0,
    "vgeti" : 0
}
json_send('localhost', 8001, data)

# data = {
#     "type"  : 'update',
#     "key"   : 6,
#     "val"   : 8
# }
# json_send('localhost', 8001, data)

# data = {
#     "type"  : 'get',
#     "key"   : 5,
#     "ip"    : '198:54:23448:6546',
#     "port"  : 9000
# }
# json_send('localhost', 8001, data)

# data = {
#     "type"  : 'nop'
# }
# json_send('localhost', 8001, data)
