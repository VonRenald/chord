#! /usr/bin/python3
# v0.1.0
import socket
from chord_tools import *

def get(json_data):
    global Vget
    Key = json_data["key"] 
    Ip = json_data["ip"]
    Port = json_data["port"]
    print("-Get-\t","Key :",Key,"Ip :",Ip,"Port",Port)

    
    if Key in data:
        json_data = {
            "type"  : 'res',
            "key"   : Key,
            "val"   : data[Key]
        }
    else:
        json_data = {
            "type"  : 'res',
            "key"   : Key,
            "val"   : 'null'
        }
    json_send(Ip, Port, json_data)
    Vget += 1

    return
def update(json_data):
    global Vupd
    Key = json_data["key"]
    Val = json_data["val"]

    data[Key] = Val
    
    if(len(json_data) >3):
        Ip = json_data["ip"]
        Port = json_data["port"]
        print("-Update-","key :",Key,"val :",Val,"ip :",Ip,"port :",Port)
        json_data = {
                "type"  : 'respupdateack',
                "key"   : Key
            }
        json_send(Ip, Port, json_data)
    else:
        print("-Update-","key :",Key,"val :",Val)
    Vupd += 1
    return
def quit(json_data):# Ip Port Id Vget Vupd Vgeti 
    global ProgramStop
    global Vget
    global Vupd
    global Vgeti
    json_data["id"] = 0
    json_data["vget"] = Vget
    json_data["vupd"] = Vupd
    json_data["vgeti"] = Vgeti
    json_send(json_data["ip"], json_data["port"], json_data)
    ProgramStop = True


data = {}
ProgramStop = False
Vget = 0
Vupd = 0
Vgeti= 0



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind(('', 8001))
    serversocket.listen(5)
    print('listening on port:', serversocket.getsockname()[1])
    while not ProgramStop:
        (clientsocket, address) = serversocket.accept()
        json_data = json_recv(clientsocket)

        commande = json_data["type"]
        print("data :",json_data)    
        if(commande == 'get'):
            get(json_data)
        elif(commande == 'update'):
            update(json_data)
        elif(commande == 'quit'):
            quit(json_data)
        else:
            print("invalid")
        #json_send('localhost', 9000, "ack")

        print(data)
