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

# if len(sys.argv) == 3:
#     _Ip = sys.argv[1]
#     _Port = int(sys.argv[2])
#     _Id = 0
# elif len(sys.argv) == 4:
#     _Ip = 'localhost' #sys.argv[1]
#     _Port = int(sys.argv[2])
#     _Id = int(sys.argv[3])
# else:
#     _Port = 8001
#     _Ip = 'localhost'
#     _Id = 0
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


data = {}; 
# for i in range(0,len(data)):
#     data[i]=i
_Suivant = Node(_Ip,_Port,_Id)
_Precedant = Node(_Ip,_Port,_Id)


_Table = {}
# i_=1
# nv_ = (_Id+(1<<i_))%_N
# stop_ = False

# while not stop_:
#     _Table[nv_] = _Id
#     nv_ = (_Id+(1<<i_))%_N
#     # print(_Id+(1<<i_))
#     # print(_N)
#     # print(nv_)
#     # print(2%32)
#     i_+=1
#     stop_ = nv_ == _Id
# print("table :", _Table,"N :",_N)





print("ip:",_Ip,"port:",_Port,"id:",_Id)

def initTable():
    global _Table
    global _Suivant
    _Table = {_Id+1:{"id":_Suivant._Id,"ip":_Suivant._Ip,"port":_Suivant._Port}}
    i_=1
    nv_ = (_Id+(1<<i_))%_N
    stop_ = False


    while not stop_:
        if _Suivant._Id != _Id:# or nv_ < _Suivant._Id:
            if((nv_ > _Precedant._Id and nv_ <= _Id)
                or (_Id < _Precedant._Id and (nv_ > _Precedant._Id or nv_ <= _Id))):
            #if(nv_>= _Id and (nv_ < _Suivant._Id or _Id > _Suivant._Id)):
                _Table[nv_] = {"id":_Id,"ip":_Ip,"port":_Port}
            else:
                _Table[nv_] = {"id":_Suivant._Id,"ip":_Suivant._Ip,"port":_Suivant._Port}
                json_data = {
                    "type"  : 'holder_req',
                    "key"   : nv_,
                    "ip"   : _Ip,
                    "port"  : _Port
                }
                print(_Id,"send",json_data)
                json_send(_Suivant._Ip, _Suivant._Port, json_data)
        else:
            _Table[nv_] = {"id":_Id,"ip":_Ip,"port":_Port}
        nv_ = (_Id+(1<<i_))%_N
        i_+=1
        stop_ = nv_ == _Id
    print("table :", _Table,"N :",_N,"-------------------------------------------------------")

# def majTable():
#     global _Table
#     global _Suivant
#     _Table = {_Id+1:{"id":_Suivant._Id,"ip":_Suivant._Ip,"port":_Suivant._Port}}
#     i_=1
#     nv_ = (_Id+(1<<i_))%_N
#     stop_ = False
#     #print("avant boucle")
#     while not stop_:
#         #print("boucle")
#         if _Suivant._Id != _Id or nv_ < _Suivant._Id:
#             json_data = {
#                 "type"  : 'holder_req',
#                 "key"   : nv_,
#                 "ip"   : _Ip,
#                 "port"  : _Port
#             }
#             #print(_Id,"send",json_data)
#             #holder_req()
#             json_send(_Ip, _Port, json_data)
#         else:
#             _Table[nv_] = {"id":_Id,"ip":_Ip,"port":_Port}
#         nv_ = (_Id+(1<<i_))%_N
#         i_+=1
#         stop_ = nv_ == _Id
#         print(nv_, _Id)
#     print("fin boucle")

def get():
    global json_data
    global _Suivant
    Key = json_data["key"] 
    Ip = json_data["ip"]
    Port = json_data["port"]
    print("-Get-\t","Key :",Key,"Ip :",Ip,"Port",Port)

    #if Key >= _Id and (Key < _Suivant._Id or _Id > _Suivant._Id or _Id == _Suivant._Id):
    if  (Key <= _Id and Key > _Precedant._Id) or (_Id < _Precedant._Id and (Key > _Precedant._Id or Key <= _Id)) or (_Id == _Suivant._Id and _Id == _Precedant._Id):
        toSend = None
        if Key in data:
            toSend = data[Key]
        json_data = {
            "type"  : 'resP',
            "key"   : Key,
            "val"   : toSend
        }
        json_send('localhost', Port, json_data)
    else:
        stop = False
        i=0
        v = _Id
        nv = (v+(1<<i))%_N
        while not stop:
            if (Key >= v and (Key < nv or nv < v)):#envoie au prochain
                stop = True
                # json_data = {
                #     "type" : 'holder_res',
                #     "key" : Key,
                #     "id" : _Table[v]["id"],
                #     "ip" : _Table[v]["ip"],
                #     "port" : _Table[v]["port"]
                # }#holder_res Key Id Ip Port 
                print(_Id,"send",json_data)
                if(_Table[v]["id"] != _Id):
                    json_send(_Table[v]["ip"], _Table[v]["port"], json_data)
                else:
                    json_send(_Suivant._Ip, _Suivant._Port, json_data)
            else:
                v=nv
                nv = (v+(1<<i))%_N
                i+=1
                stop = v == _Id



def update():
    global json_data
    global data
    Key = json_data["key"]
    Val = json_data["val"]


    #if Key >= _Id and (Key < _Suivant._Id or _Id > _Suivant._Id or _Id == _Suivant._Id):#si c'est a moi de gerer
    if (Key <= _Id and Key > _Precedant._Id) or (_Id < _Precedant._Id and (Key > _Precedant._Id or Key <= _Id)) or (_Id == _Suivant._Id and _Id == _Precedant._Id):
        data[Key] = Val
        if(len(json_data) >3):
            Ip = json_data["ip"]
            Port = json_data["port"]
            print("-Update-","key :",Key,"val :",Val,"ip :",Ip,"port :",Port)

            json_data = {
                "type"  : 'respUpdateAck',
                "key"   : Key
            }
            print(_Id,"send","client",json_data)
            json_send('localhost', Port, json_data)
        else:
            print("-Update-","key :",Key,"val :",Val)
    else:
        stop = False
        i=0
        v = _Id
        nv = (v+(1<<i))%_N
        while not stop:
            if (Key >= v and (Key < nv or nv < v)):#envoie au prochain
                stop = True
                # json_data = {
                #     "type" : 'holder_res',
                #     "key" : Key,
                #     "id" : _Table[v]["id"],
                #     "ip" : _Table[v]["ip"],
                #     "port" : _Table[v]["port"]
                # }#holder_res Key Id Ip Port 
                
                if(_Table[v]["id"] != _Id):
                    print(_Id,"send",_Table[v]["id"],json_data)
                    json_send(_Table[v]["ip"], _Table[v]["port"], json_data)
                else:
                    print(_Id,"send",_Suivant._Id,json_data)
                    json_send(_Suivant._Ip, _Suivant._Port, json_data)
            else:
                v=nv
                nv = (v+(1<<i))%_N
                i+=1
                stop = v == _Id




def joind():#joind Id Ip Port
    global json_data
    global data
    global _Suivant
    global _Precedant
    Id = json_data["id"]
    Ip = json_data["ip"]
    Port = json_data["port"]
    print(_Id, "joind", "Id :",Id,"_Precedant._Id",_Precedant._Id)
    if Id == _Id:
        json_data = {
            "type"  : 'nok'
        }
        #print(_Id,"nok id invalide")
        print(_Id,"send",json_data)
        json_send('localhost', Port, json_data)
    #elif Id < _Id and (_Id == _Precedant._Id or Id < _Suivant._Id or _Suivant._Id < _Id):
    elif (Id <= _Id and Id > _Precedant._Id) or (_Id < _Precedant._Id and (Id > _Precedant._Id or Id <= _Id)) or _Id == _Precedant._Id:    
        data2send = {}
        newdata = {}
        for key_ in data:
            if key_ > Id:
                newdata[key_] = data[key_]
            else:
                data2send[key_] = data[key_]
        data = newdata
        # data2send = data[Id-_Id:]
        # data = data[:Id-_Id]
        json_data = {
            "type"  : 'ok',
            "ipp"   : _Precedant._Ip,
            "portp" : _Precedant._Port,
            "idp"   : _Precedant._Id,
            "ipps"  : _Ip,
            "ports" : _Port,
            "ids"   : _Id,
            "data"  : data2send
        }#ok Ipp Portp Ipps Ports Data
        _Precedant = Node(Ip,Port,Id)
        #print(_Id,"ok add id",Id,_Suivant._Id)
        print(_Id,"send",json_data)
        json_send(Ip, Port, json_data)
    else:
        print(_Id,"send",json_data)#modif pour parcourt table
        json_send(_Suivant._Ip, _Suivant._Port, json_data)


def ok():#ok Ipp Portp Ipps Ports Data
    global json_data
    global _N
    global _Suivant
    global _Precedant
    global data

    

    data = json_data["data"]
    #print("ok",_Id,len(data),_Id+len(data),(_Id+len(data))%_N)
    _Suivant = Node(json_data["ipps"],json_data["ports"],json_data["ids"])
    _Precedant = Node(json_data["ipp"],json_data["portp"],json_data["idp"])
    print("ok2",_Suivant._Id)
    json_data = {
        "type" : 'plop',
        "id" : _Id,
        "ip" : _Ip,
        "port" : _Port
    }#Plop Id Ip Port   
    print(_Id,"send",json_data)
    json_send(_Suivant._Ip, _Suivant._Port, json_data)

    #initTable()


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
    # global json_data
    # global _Suivant
    # Id = json_data["id"]
    # #print("plop id",Id,_Id)
    # if _Suivant._Id == Id:
    #     _Suivant = Node(json_data["ip"],json_data["port"],Id)
    # elif Id > _Id and Id < _Suivant._Id:
    #     _Suivant = Node(json_data["ip"],json_data["port"],Id)
    # else:
    #     print(_Id,"send",json_data)
    #     json_send(_Suivant._Ip, _Suivant._Port, json_data)  
    global json_data
    global _Precedant
    global _Suivant
    global _Table
    if (json_data["id"] == _Id):
        initTable()
        return
    #if((json_data["id"] < _Id and json_data["id"] > _Precedant._Id) or (_Precedant._Id >= _Id and _Precedant._Id< json_data["id"])):
    if (json_data["id"] > _Id and json_data["id"] < _Suivant._Id) or (json_data["id"] > _Id and _Suivant._Id < _Id and json_data["id"] > _Suivant._Id) or (json_data["id"] < _Id and _Suivant._Id < _Id and json_data["id"] < _Suivant._Id ) or _Id == _Suivant._Id:
        _Suivant = Node(json_data["ip"],json_data["port"],json_data["id"])
    
    Key = json_data["id"]
    #v2
    for key_ in _Table:
        #if(Key <= key_ and Key > _Table[key_]["id"]):
        print(_Id,"plop maj table","key:",Key,"oldKey:",_Table[key_]["id"],"TabKey:",key_)
        if(Key < _Id):
            val = key_
            if (key_ > _Table[key_]["id"]):
                val -= 32
            if not(val - _Table[key_]["id"] > val - Key):
                 _Table[key_] = {"id":Key,"ip":json_data["ip"],"port":json_data["port"]}
            # if (val <= Key):
            #     _Table[key_] = {"id":Key,"ip":json_data["ip"],"port":json_data["port"]}    
        elif(Key >= key_ and (Key < _Table[key_]["id"] or _Table[key_]["id"] == 0)):
            _Table[key_] = {"id":Key,"ip":json_data["ip"],"port":json_data["port"]}
    # stop = False
    # i=0
    # v = _Id
    # nv = (v+(1<<i))%_N
    # while not stop:
    #     print("ok",v)
    #     if(v!=_Id):
    #         s_dico = _Table[v]
    #         print(s_dico)
    #         if (Key <= v  and Key > _Table[v]["id"]):#envoie au prochain
    #             _Table[v] = {"id":Key,"ip":json_data["ip"],"port":json_data["port"]}
    #         # stop = True
    #         # json_data = {
    #         #     "type" : 'holder_res',
    #         #     "key" : Key,
    #         #     "id" : _Table[v]["id"],
    #         #     "ip" : _Table[v]["ip"],
    #         #     "port" : _Table[v]["port"]
    #         # }#holder_res Key Id Ip Port 
    #         # print(_Id,"send",json_data)
    #         # json_send(Ip, port, json_data)
    #     v=nv
    #     nv = (v+(1<<i))%_N
    #     i+=1
    #     stop = v == _Id
    json_send(_Suivant._Ip, _Suivant._Port, json_data)  
    #majTable()
    

def holder_req():#holder_req Key Ip Port
    global json_data
    Key = json_data["key"]
    Ip = json_data["ip"]
    port = json_data["port"]

    #if(Key >= _Id and Key < _Suivant._Id):#c'est moi qui gere
    if (Key <= _Id and Key > _Precedant._Id) or (_Id < _Precedant._Id and (Key > _Precedant._Id or Key <= _Id)):
        json_data = {
            "type" : 'holder_res',
            "key" : Key,
            "id" : _Id,
            "ip" : _Ip,
            "port" : _Port
        }#holder_res Key Id Ip Port 
        print(_Id,"send",json_data)
        json_send(Ip, port, json_data)
    else:
        stop = False
        i=0
        v = _Id
        nv = (v+(1<<i))%_N
        while not stop:
            if (Key >= v and (Key < nv or nv < v)):#envoie au prochain
                stop = True
                # json_data = {
                #     "type" : 'holder_res',
                #     "key" : Key,
                #     "id" : _Table[v]["id"],
                #     "ip" : _Table[v]["ip"],
                #     "port" : _Table[v]["port"]
                # }#holder_res Key Id Ip Port 
                
                if(_Table[v]["id"] != _Id):
                    print(_Id,"send",_Table[v]["id"],json_data)
                    json_send(_Table[v]["ip"], _Table[v]["port"], json_data)
                else:
                    print(_Id,"send",_Suivant._Id,json_data)
                    json_send(_Suivant._Ip, _Suivant._Port, json_data)
            else:
                v=nv
                nv = (v+(1<<i))%_N
                i+=1
                stop = v == _Id

def holder_res():#holder_res Key Id Ip Port 
    global json_data
    global _Table
    Key = json_data["key"]
    Id = json_data["id"]
    Ip = json_data["ip"]
    Port = json_data["port"]
    _Table[Key] = {"id":Id,"ip":Ip,"port":Port}
    # _Table[Key]["id"] = Id
    # _Table[Key]["ip"] = Ip
    # _Table[Key]["port"] = Port

initTable()
print("table init",_Table)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serversocket:
    serversocket.bind((_Ip, _Port))
    serversocket.listen(5)
    print('listening on port:', serversocket.getsockname()[1])

    if len(sys.argv) == 4:
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

        print(_Id,len(data),data)
        print("suivant",_Suivant._Id,"precedant",_Precedant._Id)
        print(_Id,"Table",_Table)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

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
        elif(commande == 'holder_res'):
            holder_res()
        elif(commande == 'holder_req'):
            holder_req()
        else:
            print("invalid")
        

        
