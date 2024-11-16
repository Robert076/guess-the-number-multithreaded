import socket, struct, threading, random

threads = []
winnerThread = -1
serverNumber = random.randint(0, 10)
clientCount = 0
mylock = threading.Lock()
e = threading.Event()
notGuessed = True

def worker(cs):
    global winnerThread, serverNumber, clientCount, mylock, e, notGuessed
    curTries = 0
    curCount = clientCount
    print(f"Starting with client {curCount}")
    while notGuessed:
        print(f"Client #{clientCount} is on try {curTries}")
        num = struct.unpack("!I", cs.recv(4))[0]
        print(num)        
        if num == serverNumber and notGuessed:
            mylock.acquire()
            winnerThread = threading.get_ident()
            e.set()
            notGuessed = False
            mylock.release()
        cs.sendall(b'C')
        curTries += 1
    if winnerThread == threading.get_ident():
        print(f"Thread {curCount} has won after {curTries} try(tries)")
        cs.sendall(b'W')
    else:
        cs.sendall(b'L')
    cs.close()

def resetSrv(cs):
    pass

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 1234))
    s.listen(5)
    print("Server started...")
    while True:
        clientSocket, clientAddress = s.accept()
        print(f'New connection from {clientAddress[0]}:{clientAddress[1]}')
        t = threading.Thread(target = worker, args=(clientSocket,))
        t.start()
    


