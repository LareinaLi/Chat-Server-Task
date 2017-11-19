import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 5550))

sock.listen(5)
serverip = str(socket.gethostbyname('localhost'))
print('Server', serverip, 'listening ...')

userdict = dict()
userlist = list()

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
    roomname = connection.recv(1024).decode()
    if roomname != None:
        if roomname in roomlist:
            pass
        else:
            roomlist.append(roomname)
            roomdict[roomname] = roomid + 1
        
        connection.send(b"Please enter your nickname: ")
        nickname = myconnection.recv(1024).decode()
        userdict[myconnection.fileno()] = nickname
        
        ip = str(myconnection.getsockname()[0])
        helomsg = 'HELO text\nIP: ' + ip + '\nPort: 5550\nStudentID: 17303493\n'
        leftmsg = 'LEFT_CHATROOM: ' + str(roomdict[roomname]) + '\nJOIN_ID: ' + str(connNumber) + '\n'
        termsg = 'DISCONNECT: 0\nPORT: 0\nCLIENT_NAME: ' + userdict[connNumber] + '\n'
        
        print('JOIN_CHATROOM: ' + roomname + '\nCLIENT_IP: 0\nPORT: 0\nCLIENT_NAME: ', nickname, '\n')
        joinmsg = 'JOINED_CHATROOM: ' + roomname + '\nSERVER_IP: ' + serverip + '\nPORT: 5550\nROOM_REF: ' + str(roomdict[roomname]) + '\nJOIN_ID: ' + str(connNumber) + '\n'
        
        myconnection.send(joinmsg.encode())
        userlist.append(myconnection)
        #print('Connection', connNumber, ' has nickname :', nickname, '\n')
        broadcast(connNumber, '[Syetem info: ' + userdict[connNumber] + ' entered.]\n')
        while True:
            try:
                recvedMsg = myconnection.recv(1024).decode()
                if recvedMsg:
                    smsg = 'CHAT: ' + roomname + '\nJOIN_ID: ' + str(connNumber) + '\nCLIENT_NAME: ' + userdict[connNumber] + '\nMESSAGE: ' + recvedMsg + '\n'
                    print(smsg)
                    bmsg = 'CHAT: ' + roomname + '\nCLIENT_NAME: ' + userdict[connNumber] + '\nMESSAGE: ' + recvedMsg + '\n'
                    myconnection.send(bmsg.encode())
                    broadcast(connNumber, bmsg)
                if recvedMsg == 'HELO text':
                    myconnection.send(helomsg.encode())
                elif recvedMsg == 'KILL_SERVICE':
                    print('LEAVE_CHATROOM: ', str(roomdict[roomname]), '\nJOIN_ID: ', str(connNumber), '\nCLIENT_NAME: ', userdict[connNumber], '\n')
                    broadcast(connNumber, leftmsg)
                    myconnection.close()
    
            except (OSError, ConnectionResetError):
                try:
                    userlist.remove(myconnection)
                except:
                    pass

                print(termsg)
                broadcast(connNumber,termsg)
                myconnection.close()
                return


while True:
    connection, addr = sock.accept()

    try:
        # connection.settimeout(5)
        connection.send(b"Please enter chatroom name: ")
        
        mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
        mythread.setDaemon(True)
        mythread.start()

    except Exception as e:
        errmsg = 'ERROR_CODE: \nERROR_DESCRIPTION: ' + str(e.message) + '\n'
        print(errmsg)
        pass  
