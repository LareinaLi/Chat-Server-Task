import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', 5550))

def sendThreadFunc():
    while True:
        try:
            myword = input()
            sock.send(myword.encode())
            # print(sock.recv(1024).decode())

            if myword.upper() == "KILL_SERVICE":
                break

        except ConnectionAbortedError:
            print('Server closed this connection!')
        except ConnectionResetError:
            print('Server is closed! Please close the window.')
            pass

def recvThreadFunc():
    while True:
        try:
            otherword = sock.recv(1024)
            if otherword:
                print(otherword.decode())
            else:
                pass
        except ConnectionAbortedError:
            print('Server closed this connection!')

        except ConnectionResetError:
            print('Server is closed! Please close the window.')
            pass


th1 = threading.Thread(target=sendThreadFunc)
th2 = threading.Thread(target=recvThreadFunc)
threads = [th1, th2]

for t in threads:
    t.setDaemon(True)
    t.start()
t.join()
