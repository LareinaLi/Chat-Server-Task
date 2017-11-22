# -*- coding: utf-8 -*-
"""
@author: lix9
"""

import socket
import threading
import re

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = '10.62.0.116'

sock.bind((server, 5550))

sock.listen(5)
serverip = str(socket.gethostbyname(server))
print('Server', serverip, 'listening ...')

userdict = dict()
userlist = list()
userid = 0

roomdict = dict()
roomlist = list()
roomid = 0



# send 'whatToSay' to everyone except exceptNum
def broadcast(exceptNum, whatToSay):
    for c in userlist:
        if c.fileno() != exceptNum:
            try:
                c.send(whatToSay.encode())
            except:
                pass

def subThreadIn(myconnection, connNumber):
    
    helomsg = 'HELO text\nIP: ' + server + '\nPort: 5550\nStudentID: 17303493\n'
    termsg = 'DISCONNECT: 0\nPORT: 0\nCLIENT_NAME: ' + userdict[connNumber] + '\n'
        
    recvedMsg = connection.recv(4086).decode()
    
    if recvedMsg == 'HELO text':
        myconnection.send(helomsg.encode())
    
    elif recvedMsg == 'KILL_SERVICE':
       # print('LEAVE_CHATROOM: ', str(roomdict[roomname]), '\nJOIN_ID: ', str(connNumber), '\nCLIENT_NAME: ', userdict[connNumber], '\n')
       # broadcast(connNumber, leftmsg)
        myconnection.close()
        
    else:
        if re.match(r'JOIN_CHATROOM:', recvedMsg):
            info = recvedMsg.split('\: |\n')
            roomname = info[1]
            nickname = info[7]
            if roomname != None & nickname != None:
                if roomname in roomlist:
                    pass
                else:
                    roomlist.append(roomname)
                    roomdict[roomname] = roomid + 1
                if nickname in userdict:
                    pass
                else:
                    userlist.append(nickname)
                    userdict[nickname] = userid+1
                joinmsg = 'JOINED_CHATROOM: ' + info[1] + '\nSERVER_IP: ' + serverip + '\nPORT: 5550\nROOM_REF: ' + str(roomdict[roomname]) + '\nJOIN_ID: ' + str(userdict[nickname]) + '\n'
                myconnection.send(joinmsg.encode())
                broadcast(connNumber, '[Syetem info: ' + userdict[connNumber] + ' entered.]\n')
                
        elif re.match(r'LEAVE_CHATROOM:', recvedMsg):
            info = recvedMsg.split('\: |\n')
            leftmsg = 'LEFT_CHATROOM: ' + str(roomdict[roomname]) + '\nJOIN_ID: ' + str(connNumber) + '\n'
            
        elif re.match(r'CHAT:', recvedMsg):
            info = recvedMsg.split('\: |\n')
    
        
        #userdict[myconnection.fileno()] = nickname
        
        ip = str(myconnection.getsockname()[0])

                
                
        #print('JOIN_CHATROOM: ' + roomname + '\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: ', nickname, '\n')
        #joinmsg = 'JOINED_CHATROOM: ' + roomname + '\nSERVER_IP: ' + serverip + '\nPORT: 5550\nROOM_REF: ' + str(roomdict[roomname]) + '\nJOIN_ID: ' + str(connNumber) + '\n'
        

        while True:
            try:
                recvedMsg = myconnection.recv(4086).decode()
                if recvedMsg:
                    smsg = 'CHAT: ' + roomname + '\nJOIN_ID: ' + str(connNumber) + '\nCLIENT_NAME: ' + userdict[connNumber] + '\nMESSAGE: ' + recvedMsg + '\n'
                    #print(userdict[connNumber], ':', recvedMsg)
                    print(smsg)
                    bmsg = 'CHAT: ' + roomname + '\nCLIENT_NAME: ' + userdict[connNumber] + '\nMESSAGE: ' + recvedMsg + '\n'
                    myconnection.send(bmsg.encode())
                    broadcast(connNumber, bmsg)
                if recvedMsg == 'HELO text':
                    myconnection.send(helomsg.encode())
                elif recvedMsg == 'KILL_SERVICE':
                    print('LEAVE_CHATROOM: ', str(roomdict[roomname]), '\nJOIN_ID: ', str(connNumber), '\nCLIENT_NAME: ', userdict[connNumber], '\n')
                    #myconnection.send(b'Service terminated! Please close the window!\n')
                    #myconnection.send(leftmsg.encode())
                    broadcast(connNumber, leftmsg)
                    myconnection.close()
    
            except (OSError, ConnectionResetError):

                print(termsg)
                broadcast(connNumber,termsg)
                myconnection.close()
                return


while True:
    connection, addr = sock.accept()
  
    try:
        connection.send(b'Connection Successful for host 10.62.0.116 on port 5550.')
        
        mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
        mythread.setDaemon(True)
        mythread.start()

    except Exception as e:
        errmsg = 'ERROR_CODE: \nERROR_DESCRIPTION: ' + str(e.message) + '\n'
        print(errmsg)
        pass  
