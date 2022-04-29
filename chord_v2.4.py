#! /usr/bin/python3
# v0.1.0
import socket
from chord_tools import *
import random
import sys

class Node:
    def __init__(self,ip_, port_, id_):
        self._Port = port_
        self._Ip = ip_
        self._Id = id_





def get():
    global json_data
    global _Suivant
    global Vget
    global Vgeti
    Key = json_data["key"] 
    Ip = json_data["ip"]
    Port = json_data["port"]
    print("-Get-\t","Key :",Key,"Ip :",Ip,"Port",Port)

    if Key >= _Id and (Key < _Suivant._Id or _Id > _Suivant._Id or _Id == _Suivant._Id):
        toSend = None
        if Key in data:
            toSend = data[Key]
        json_data = {
            "type"  : 'res',
            "key"   : Key,
            "val"   : toSend
        }
        json_send(Ip, Port, json_data)
        Vget += 1
    else:
        json_send(_Suivant._Ip, _Suivant._Port, json_data)
        Vgeti += 1


def update():
    global json_data
    global data
    global Vupd
    global Vgeti
    Key = json_data["key"]
    Val = json_data["val"]


    if Key >= _Id and (Key < _Suivant._Id or _Id > _Suivant._Id or _Id == _Suivant._Id):#si c'est a moi de gerer
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
    else:
        json_send(_Suivant._Ip, _Suivant._Port, json_data)
        Vgeti += 1

def quit():# Ip Port Id Vget Vupd Vgeti 
    global json_data
    global ProgramStop
    global Vget
    global Vupd
    global Vgeti
    if json_data["id"] == None:
        json_data["id"] = _Id
        json_data["vget"] = 0
        json_data["vupd"] = 0
        json_data["vgeti"] = 0
        json_send(_Suivant._Ip, _Suivant._Port, json_data)
    elif json_data["id"] != _Id:
        json_data["vget"] += Vget
        json_data["vupd"] += Vupd
        json_data["vgeti"] += Vgeti
        json_send(_Suivant._Ip, _Suivant._Port, json_data)
        ProgramStop = True
    else:
        json_data["vget"] += Vget
        json_data["vupd"] += Vupd
        json_data["vgeti"] += Vgeti
        json_send(json_data["ip"], json_data["port"], json_data)
        ProgramStop = True


def join():#join Id Ip Port
    global json_data
    global data
    global _Suivant
    global Vgeti
    Id = json_data["id"]
    Ip = json_data["ip"]
    Port = json_data["port"]

    if Id == _Id:
        json_data = {
            "type"  : 'nok'
        }
        #print(_Id,"nok id invalide")
        print(_Id,"send",json_data)
        json_send(Ip, Port, json_data)
    elif Id > _Id and (_Id == _Suivant._Id or Id < _Suivant._Id or _Suivant._Id < _Id):
        data2send = {}
        newdata = {}
        for key_ in data:
            if key_< Id:
                newdata[key_] = data[key_]
            else:
                data2send[key_] = data[key_]
        data = newdata
        # data2send = data[Id-_Id:]
        # data = data[:Id-_Id]
        json_data = {
            "type"  : 'ok',
            "ipp"   : _Ip,
            "portp" : _Port,
            "idp"   : _Id,
            "ips"  : _Suivant._Ip,
            "ports" : _Suivant._Port,
            "ids"   : _Suivant._Id,
            "data"  : data2send
        }#ok Ipp Portp ips Ports Data
        _Suivant = Node(Ip,Port,Id)
        #print(_Id,"ok add id",Id,_Suivant._Id)
        print(_Id,"send",json_data)
        json_send(Ip, Port, json_data)
    else:
        print(_Id,"send",json_data)
        json_send(_Suivant._Ip, _Suivant._Port, json_data)
    Vgeti += 1


def ok():#ok Ipp Portp ips Ports Data
    global json_data
    global _N
    global _Suivant
    global _Precdant
    global data
    global Vgeti
    data = json_data["data"]
    #print("ok",_Id,len(data),_Id+len(data),(_Id+len(data))%_N)
    _Suivant = Node(json_data["ips"],json_data["ports"],json_data["ids"])
    _Precdant = Node(json_data["ipp"],json_data["portp"],json_data["idp"])
    print("ok2",_Suivant._Id)
    json_data = {
        "type" : 'new',
        "id" : _Id,
        "ip" : _Ip,
        "port" : _Port
    }#new Id Ip Port   
    print(_Id,"send",json_data)
    json_send(_Precdant._Ip, _Precdant._Port, json_data)
    Vgeti += 1


def nok():
    global _Id
    global Vgeti
    _Id = random.randrange(_N)
    #print("ip:",_Ip,"port:",_Port,"id:",_Id)
    #join Id Ip Port
    json_data = {
        "type" : 'join',
        "id" : _Id,
        "ip" : _Ip,
        "port" : _Port
    }
    print(_Id,"send",json_data)
    json_send(defaultNode._Ip, defaultNode._Port, json_data)
    Vgeti += 1
#new Id Ip Port    
def new():
    # global json_data
    # global _Suivant
    # Id = json_data["id"]
    # #print("new id",Id,_Id)
    # if _Suivant._Id == Id:
    #     _Suivant = Node(json_data["ip"],json_data["port"],Id)
    # elif Id > _Id and Id < _Suivant._Id:
    #     _Suivant = Node(json_data["ip"],json_data["port"],Id)
    # else:
    #     print(_Id,"send",json_data)
    #     json_send(_Suivant._Ip, _Suivant._Port, json_data)  
    global json_data
    global _Precdant
    _Precdant = Node(json_data["ip"],json_data["port"],json_data["id"])

_N = 1<<5
defaultNode = Node('localhost', 8001, None)
if(len(sys.argv) == 1):
    _Ip = '127.0.0.1'
    _Port = 8001
    _Id = 0
if len(sys.argv) == 2:
    _Ip = '127.0.0.1'
    _Port = int(sys.argv[1])
    _Id = 0
elif len(sys.argv) == 4:
    _Ip = '127.0.0.1'
    _Port = int(sys.argv[1])
    _Id = random.randrange(_N)
    defaultNode = Node(sys.argv[2], int(sys.argv[3]), None)
elif len(sys.argv) == 5:
    _Ip = '127.0.0.1'
    _Port = int(sys.argv[1])
    _Id = int(sys.argv[2])
    defaultNode = Node(sys.argv[3], int(sys.argv[4]), None)


data = {}; 

Vget = 0
Vupd = 0
Vgeti = 0
ProgramStop = False

_Suivant = Node(_Ip,_Port,_Id)
_Precedant = Node(_Ip,_Port,_Id)

print("ip:",_Ip,"port:",_Port,"id:",_Id)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((_Ip, _Port))
    serversocket.listen(5)
    print('listening on port:', serversocket.getsockname()[1])

    if len(sys.argv) == 4 or len(sys.argv) == 5:
        print("connect to default")
        json_data = {
            "type" : 'join',
            "id" : _Id,
            "ip" : _Ip,
            "port" : _Port
        }
        print(_Id,"send",json_data)
        json_send(defaultNode._Ip, defaultNode._Port, json_data)

    while not ProgramStop:
        (clientsocket, address) = serversocket.accept()
        json_data = json_recv(clientsocket)

        commande = json_data["type"]
        print("data :",json_data)    
        if(commande == 'get'):
            get()
        elif(commande == 'update'):
            update()
        elif(commande == 'join'):
            join()
        elif(commande == 'ok'):
            ok()
        elif(commande == 'nok'):
            nok()
        elif(commande == 'new'):
            new()
        elif(commande == 'quit'):
            quit()
        else:
            print("invalid")
        

        print(_Id,len(data),data)
        print("suivant",_Suivant._Id)
