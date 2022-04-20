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

if len(sys.argv) == 3:
    _Ip = sys.argv[1]
    _Port = int(sys.argv[2])
    _Id = 0
elif len(sys.argv) == 4:
    _Ip = 'localhost' #sys.argv[1]
    _Port = int(sys.argv[2])
    _Id = int(sys.argv[3])
else:
    _Port = 8001
    _Ip = 'localhost'
    _Id = 0

_N = 20
data = [None]*_N; 
for i in range(0,len(data)):
    data[i]=i
_Suivant = Node(_Ip,_Port,_Id)

defaultNode = Node('localhost', 8001, None)
print("ip:",_Ip,"port:",_Port,"id:",_Id)




def get():
    global json_data
    global _Suivant
    Key = json_data["key"] 
    Ip = json_data["ip"]
    Port = json_data["port"]
    print("-Get-\t","Key :",Key,"Ip :",Ip,"Port",Port)

    if Key >= _Id and (Key < _Suivant._Id or _Id > _Suivant._Id):
        json_data = {
            "type"  : 'resP',
            "key"   : Key,
            "val"   : data[Key-_Id]
        }
        json_send('localhost', Port, json_data)
    else:
        json_send(_Suivant._Ip, _Suivant._Port, json_data)


def update():
    global json_data
    global data
    Key = json_data["key"]
    Val = json_data["val"]


    if Key >= _Id and (Key < _Suivant._Id or _Id > _Suivant._Id):#si c'est a moi de gerer
        data[Key-_Id] = Val
        if(len(json_data) >3):
            Ip = json_data["ip"]
            Port = json_data["port"]
            print("-Update-","key :",Key,"val :",Val,"ip :",Ip,"port :",Port)

            json_data = {
                "type"  : 'respUpdateAck',
                "key"   : Key
            }

            json_send('localhost', Port, json_data)
        else:
            print("-Update-","key :",Key,"val :",Val)
    else:
        json_send(_Suivant._Ip, _Suivant._Port, json_data)
    #   ---- 

    # if Key < _Id or Key > _Suivant._Id-1:
    #     json_send(_Suivant._Ip, _Suivant._Port, json_data)
    
    # data[Key-_Id] = Val
    
    # if(len(json_data) >3):
    #     Ip = json_data["ip"]
    #     Port = json_data["port"]
    #     print("-Update-","key :",Key,"val :",Val,"ip :",Ip,"port :",Port)

    #     json_data = {
    #         "type"  : 'respUpdateAck',
    #         "key"   : Key
    #     }

    #     json_send('localhost', Port, json_data)
    # else:
    #     print("-Update-","key :",Key,"val :",Val)


def joind():#joind Id Ip Port
    global json_data
    global data
    global _Suivant
    Id = json_data["id"]
    Ip = json_data["ip"]
    Port = json_data["port"]

    if Id == _Id:
        json_data = {
            "type"  : 'nok'
        }
        #print(_Id,"nok id invalide")
        print(_Id,"send",json_data)
        json_send('localhost', Port, json_data)
    elif Id > _Id and (_Id == _Suivant._Id or Id < _Suivant._Id or _Suivant._Id < _Id):
        data2send = data[Id-_Id:]
        data = data[:Id-_Id]
        json_data = {
            "type"  : 'ok',
            "ipp"   : _Ip,
            "portp" : _Port,
            "ipps"  : _Suivant._Ip,
            "ports" : _Suivant._Port,
            "data"  : data2send
        }#ok Ipp Portp Ipps Ports Data
        _Suivant = Node(Ip,Port,Id)
        #print(_Id,"ok add id",Id,_Suivant._Id)
        print(_Id,"send",json_data)
        json_send(Ip, Port, json_data)
    else:
        print(_Id,"send",json_data)
        json_send(_Suivant._Ip, _Suivant._Port, json_data)


def ok():
    global json_data
    global _N
    global _Suivant
    global data
    data = json_data["data"]
    print("ok",_Id,len(data),_Id+len(data),(_Id+len(data))%_N)
    _Suivant = Node(json_data["ipps"],json_data["ports"],(_Id+len(data))%_N)
    print("ok2",_Suivant._Id)
    json_data = {
        "type" : 'plop',
        "id" : _Id,
        "ip" : _Ip,
        "port" : _Port
    }#Plop Id Ip Port   
    print(_Id,"send",json_data)
    json_send(_Suivant._Ip, _Suivant._Port, json_data)


def nok():
    global _Id
    _Id = random.randrange(_N)
    #print("ip:",_Ip,"port:",_Port,"id:",_Id)
    #joind Id Ip Port
    json_data = {
        "type" : 'joind',
        "id" : _Id,
        "ip" : _Ip,
        "port" : _Port
    }
    print(_Id,"send",json_data)
    json_send(defaultNode._Ip, defaultNode._Port, json_data)
#Plop Id Ip Port    
def plop():
    global json_data
    global _Suivant
    Id = json_data["id"]
    #print("plop id",Id,_Id)
    if _Suivant._Id == Id:
        _Suivant = Node(json_data["ip"],json_data["port"],Id)
    elif Id > _Id and Id < _Suivant._Id:
        _Suivant = Node(json_data["ip"],json_data["port"],Id)
    else:
        print(_Id,"send",json_data)
        json_send(_Suivant._Ip, _Suivant._Port, json_data)  


14


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((_Ip, _Port))
    serversocket.listen(5)
    print('listening on port:', serversocket.getsockname()[1])

    if _Ip != defaultNode._Ip or _Port != defaultNode._Port:
        print("connect to default")
        json_data = {
            "type" : 'joind',
            "id" : _Id,
            "ip" : _Ip,
            "port" : _Port
        }
        print(_Id,"send",json_data)
        json_send(defaultNode._Ip, defaultNode._Port, json_data)

    while True:
        (clientsocket, address) = serversocket.accept()
        json_data = json_recv(clientsocket)

        commande = json_data["type"]
        print("data :",json_data)    
        if(commande == 'get'):
            get()
        elif(commande == 'update'):
            update()
        elif(commande == 'joind'):
            joind()
        elif(commande == 'ok'):
            ok()
        elif(commande == 'nok'):
            nok()
        elif(commande == 'plop'):
            plop()
        else:
            print("invalid")
        

        print(_Id,len(data),data)
        print("suivant",_Suivant._Id)
