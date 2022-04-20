#! /usr/bin/python3
# v0.1.0
import socket
from chord_tools import *



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind(('', 8001))
    serversocket.listen(5)
    print('listening on port:', serversocket.getsockname()[1])
    while True:
        (clientsocket, address) = serversocket.accept()
        json_data = json_recv(clientsocket)
        commande = json_data[0]
        print("data :",json_data)    
        if(commande == 'get'):
            print("get")
            Key = json_data[1] 
            Ip = json_data[2]
            Port = json_data[3]
        elif(commande == 'update'):
            print("update")
            Key = json_data[1]
            Val = json_data[2]
            print("key :",Key,"val :",Val,end='')
            if len(json_data) > 3:
                Ip = json_data[3]
                Port = json_data[4]
                print("ip :",Ip,"port :",Port,end='')
            print()
        else:
            print("invalid")
        json_send('localhost', 9000, "ack")
