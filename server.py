import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(('localhost', 5550))

sock.listen(5)
print('Server', socket.gethostbyname('localhost'), 'listening ...')

userdict = dict()
userlist = list()


# send 'whatToSay' to everyone except exceptNum
def broadcast(exceptNum, whatToSay):
    for c in userlist:
        if c.fileno() != exceptNum:
            try:
                c.send(whatToSay.encode())
            except:
                pass


def subThreadIn(myconnection, connNumber):
    nickname = myconnection.recv(1024).decode()
    userdict[myconnection.fileno()] = nickname
    ip = str(myconnection.getsockname()[0])
    welmsg = 'Welcome to server, ' + nickname + '! You can send message now!'
    feedmsg = "HELO text\nIP: " + ip + "\nPort: 5550\nStudentID: 17303493"
    print(feedmsg)
    myconnection.send(welmsg.encode())
    userlist.append(myconnection)
    print('connection', connNumber, ' has nickname :', nickname)
    broadcast(connNumber, '[Syetem info: ' + userdict[connNumber] + ' entered.]')
    while True:
        try:
            recvedMsg = myconnection.recv(1024).decode()
            if recvedMsg:
                print(userdict[connNumber], ':', recvedMsg)
                broadcast(connNumber, userdict[connNumber] + ' :' + recvedMsg)
            if recvedMsg == "HELO text":
                myconnection.send(feedmsg.encode())
            elif recvedMsg == "KILL_SERVICE":
                myconnection.send(b'Service terminated! Please close the window!')
                myconnection.close()

        except (OSError, ConnectionResetError):
            try:
                userlist.remove(myconnection)
            except:
                pass
            print(userdict[connNumber], 'exit, ', len(userlist), ' person left.')
            broadcast(connNumber, '[Syetem info: ' + userdict[connNumber] + ' left.]')
            myconnection.close()
            return


while True:
    connection, addr = sock.accept()
    print('Accept a new connection', connection.getsockname(), connection.fileno())
    try:
        # connection.settimeout(5)
        connection.send(b"Please enter your nickname: ")

        mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
        mythread.setDaemon(True)
        mythread.start()

    except Exception as e:
        print(e.message)
        pass  
