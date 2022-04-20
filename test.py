import random
import sys

_N = 32
_Id = 5
_Ip = 'none'
_Port = 621
_Table = {_Id+1:{"id":_Id,"ip":_Ip,"port":_Port}}
i_=1
nv_ = (_Id+(1<<i_))%_N
stop_ = False

if (_Id == 29 ):
    print("suivant",_Suivant._Id)

while not stop_:
    _Table[nv_] = {"id":_Id,"ip":_Ip,"port":_Port}
    nv_ = (_Id+(1<<i_))%_N
    i_+=1
    stop_ = nv_ == _Id
print(_Table)
# N = 1<<4
# i=0
# v = 5
# nv = v
# stop = False
# while not stop:
    
#     print(nv)
#     nv = (v+(1<<i))%N
#     i+=1
#     stop = nv == v


# data = [0,1,2,3]

# def test(data):
#     data[2] = 200
#     print(data)

# print(data)
# test(data)
# print(data)    

# _N = 20
# data = [None] * _N
# _id = 15
# for i in range (0,_N):
#     data[i] = i+1
# print(data[:_id-1],data[_id-1:])
# print(random.randrange(20))


# dico={}
# dico[1] = 2
# # print(dico)
# # print(3 in dico )
# # print(1 in dico)
# # print(len(dico))
# # dico[2] = 6
# # print(len(dico))
# dico[5] = 4
# dico[6] = 1
# dico[3] = 9
# dico[7] = 4
# print("dico",dico,len(dico))


# def splitData(di1,di2):
#     l = len(di1)
#     m = l/2
#     i=1
#     for key,val in di1.items():
#         if i >= m:
#             di2[key]=val
#         i += 1
#     for key in di2:
#         di1.pop(key)
# dico1 = dico.copy()
# dico2 = {}
# splitData(dico1,dico2)

# print("dico",dico)
# print("dico1",dico1)
# print("dico1V2",dict(list(dico.items())[:len(dico)//2]))
# print("dico2",dico2)
# print("dico2V2",dict(list(dico.items())[len(dico)//2:]))
# dico = dict(list(dico.items())[:len(dico)//2])
# print("dico",dico)
# # l = len(dico)
# # m= l/2
# # dico2 = {}
# # i = 1
# # for key,val in dico.items():
# #     if i >= m:
# #         dico2[key]=val
# #     print(key,val)
# #     i += 1
# # print("dico2",dico2)
# # for key in dico2:
# #     dico.pop(key)
# # print("dico",dico)
