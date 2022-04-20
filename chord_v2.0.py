#! /usr/bin/python3
# v0.1.0
import socket
from chord_tools import *


_Port = 8001
_Ip = 'localhost'
_Id = 0



class Node:
    def __init__(self,ip, port, id):
        self._Port = ip
        self._Ip = port
        self._Id = id
    # def Node(ip,port,id):
    #     _Port = port
    #     _Ip = ip
    #     _Id = id


def get(json_data):
    Key = json_data["key"] 
    Ip = json_data["ip"]
    Port = json_data["port"]
    print("-Get-\t","Key :",Key,"Ip :",Ip,"Port",Port)

    
    if Key in data:
        json_data = {
            "type"  : 'resP',
            "key"   : Key,
            "val"   : data[Key]
        }
    else:
        json_data = {
            "type"  : 'resP',
            "key"   : Key,
            "val"   : 'null'
        }
    json_send('localhost', Port, json_data)

    return
def update(json_data):
    Key = json_data["key"]
    Val = json_data["val"]

    data[Key] = Val
    
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
    return



# def joind(json_data):
#     Id = json_data["id"]
#     Ip = json_data["ip"]
#     Port = json_data["port"]

#     if Id == _Id:
#         json_data = {
#             "type"  : 'nok'
#         }
#         json_send('localhost', Port, json_data)
#     elif (_Id > Id and (_Precedant._Id < Id or _Precedant._Id > _Id or _Id == _Precedant._Id)) or 
#         (_Id < Id and (_Precedant._Id < Id or _Id == _Suivanta._Id)):
#         #si me precede et suit mon predeceseur 
#         #si me precede et mon predeceseur est le plus grand id 
#         #si me precede et je n'ai pas de predecesseur
#         #si plus grand que moi et suit mon predeceseur
#         #si me suis et que je n'ai pas de suivant
#             newip = json_data["ip"]
#             newport = json_data["port"]
#             newid = json_data["id"]
#             print(_Id,"a rajouter apres moi")
#             data2send = dict(list(data.items())[len(dico)//2:])
#             data = dict(list(data.items())[:len(dico)//2])
#             json_data = {
#                 "type"  : 'ok',
#                 "ipp"   : _Precedant._Ip,
#                 "portp" : _Precedant._Port,
#                 "idp"   : _Precedant._Id,
#                 "ipps"  : _Ip,
#                 "ports" : _Port,
#                 "ids"   : _Id,
#                 "data"  : data2send
#             }#ok Ipp Portp Ipps Ports Data
#             _Precedant = Node(newip,newport,newid)
#             if(_Suivant._Id == _Id):
#                 _Suivant = Node(newip,newport,newid)
#     else:
#         print(_Id,"au suivant de le traiter")
#         json_send(_Suivant._Ip, _Suivant._Port, json_data)
#     return

# def ok(json_data):
#     _Suivant = Node(json_data["ipps"],json_data["ports"],)
#     _Precedant = Node(_Ip,_Port,_Id)
#     data = 

data = {}

_Suivant = Node(_Ip,_Port,_Id)
_Precedant = Node(_Ip,_Port,_Id)
# TableSuivant = {"ip" : "null","port" : -1,"id":-1,"empty":True}
# TablePrecedant = {"ip" : "null","port" : -1,"id":-1,"empty":True}


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((_Ip, _Port))
    serversocket.listen(5)
    print('listening on port:', serversocket.getsockname()[1])
    while True:
        (clientsocket, address) = serversocket.accept()
        json_data = json_recv(clientsocket)

        commande = json_data["type"]
        print("data :",json_data)    
        if(commande == 'get'):
            get(json_data)
        elif(commande == 'update'):
            update(json_data)
        else:
            print("invalid")
        

        print(data)
