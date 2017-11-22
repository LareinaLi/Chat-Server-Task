# -*- coding: utf-8 -*-
"""
@author: lix9
"""

import socket
import threading
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
#server = '10.62.0.116'

sock.bind((server, 5550))

sock.listen(5)
serverip = str(socket.gethostbyname(server))
print('Server', serverip, 'listening ...')

userdict = dict()
userrefdict = dict()
userlist = list()
userid = 0

roomdict = dict()
roomrefdict = dict()
roomlist = list()
roomid = 0

roomuser = dict()

conlist = list()
condict = dict()

# send 'whatToSay' to everyone except exceptNum
def broadcast(exceptNum, whatToSay, chatroomNum):
    for con in conlist:
        for c in roomuser[chatroomNum]:
            if con.fileno() == condict[c] and con.fileno() != exceptNum:
                try:
                    con.send(whatToSay.encode())
                except:
                    pass

def subThreadIn(myconnection, connNumber):
    conlist.append(myconnection)
    while True:
        try:
            recvedMsg = connection.recv(4086).decode()
            
            print(recvedMsg)
            
            if recvedMsg == 'HELO text':
                ip = str(myconnection.getsockname()[0])
                helomsg = 'HELO text\nIP: ' + ip + '\nPort: 5550\nStudentID: 17303493\n'
                myconnection.send(helomsg.encode())
            
            elif recvedMsg == 'KILL_SERVICE':
                myconnection.send(b'Service is terminated.')
                myconnection.close()
               
            else:
                if re.match(r'JOIN_CHATROOM:', recvedMsg):
                    info = recvedMsg.split('\\n',3)
                    try:
                        if re.match(r'CLIENT_IP', info[1]) and re.match(r'PORT', info[2]) and re.match(r'CLIENT_NAME', info[3]):
                            roomname = info[0].split()[1]
                            nickname = info[3].split()[1]
                            print(roomname, nickname)
                            if roomname != None and nickname != None:
                                if roomname in roomlist:
                                    pass
                                else:
                                    roomlist.append(roomname)
                                    roomref = roomid + 1
                                    roomuser[roomref] = []
                                    roomdict[roomname] = roomref
                                    roomrefdict[roomref] = roomname
                                if nickname in userdict:
                                    pass
                                else:
                                    userlist.append(nickname)
                                    userref = userid + 1
                                    userdict[nickname] = userref
                                    userrefdict[userref] = nickname
                                condict[userdict[nickname]] = myconnection.fileno()
                                roomuser[roomdict[roomname]].append(userdict[nickname])
                                joinmsg = 'JOINED_CHATROOM: ' + roomname + '\nSERVER_IP: ' + serverip + '\nPORT: 5550\nROOM_REF: ' + str(roomdict[roomname]) + '\nJOIN_ID: ' + str(userdict[nickname]) + '\n'
                                myconnection.send(joinmsg.encode())
                                broadcast(connNumber, '[Syetem info: ' + nickname + ' entered.]\n', roomdict[roomname])

                    except:
                        errormsg = 'ERROR_CODE:001\nERROR_DESCRIPTION: CANNOT JOIN THE CHATROOM!\n'
                        myconnection.send(errormsg.encode())
                        print(errormsg)
                                                
                elif re.match(r'LEAVE_CHATROOM:', recvedMsg):
                    info = recvedMsg.split('\\n', 2)
                    if re.match(r'JOIN_ID', info[1]) and re.match(r'CLIENT_NAME', info[2]):
                        roomref = info[0].split()[1]
                        userref = info[1].split()[1]
                        if roomref in roomrefdict and userref in userrefdict:
                            leftmsg = 'LEFT_CHATROOM: ' + roomref + '\nJOIN_ID: ' + userref + '\n'
                            roomuser[roomref].remove(userref)
                            myconnection.send(leftmsg.encode())
                            broadcast(connNumber, '[Syetem info: ' + userrefdict[userref] + ' left.]\n', roomref)
                        
                elif re.match(r'DISCONNECT:', recvedMsg):
                    info = recvedMsg.split('\\n', 2)
                    if re.match(r'PORT', info[1]) and re.match(r'CLIENT_NAME', info[2]):
                        username = info[2].split()[1]
                        myconnection.send(b'Service is terminated.')
                        for room in roomuser:
                            if userdict[username] in roomuser[room]:
                                broadcast(connNumber, '[Syetem info: ' + username + ' left.]\n', room)
                        myconnection.close()
                            
                elif re.match(r'CHAT:', recvedMsg):
                    info = recvedMsg.split('\\n', 3)
                    if re.match(r'JOIN_ID', info[1]) and re.match(r'CLIENT_NAME', info[2]) and re.match(r'MESSAGE', info[3]):
                        roomref = info[0].split()[1]
                        userref = info[2].split()[1]
                        username = info[2].split()[1]
                        message = info[3].split()[1]
                        if roomref in roomrefdict and userref in userrefdict:
                            if userref in roomuser[roomref]:
                                chatmsg = 'CHAT: ' + roomref + '\nCLIENT_NAME: '+ username + '\nMESSAGE: ' + message + '\n\n'
                                myconnection.send(chatmsg.encode())
                                broadcast(connNumber, chatmsg, roomref)
                            else:
                                myconnection.send(b'Sorry, you are not in this chatroom!')
        except (OSError, ConnectionResetError):
            try:
                conlist.remove(myconnection)
            except:
                pass
            return

while True:
    connection, addr = sock.accept()
  
    try:
        connection.send(b'Connection Successful for host 10.62.0.116 on port 5550.')
        
        mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
        mythread.setDaemon(True)
        mythread.start()

    except Exception as e:
        print(e.message)
        pass  
