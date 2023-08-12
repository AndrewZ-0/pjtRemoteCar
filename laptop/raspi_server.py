import socket as sock

def handleConnection(clientSock, clientAddr):
    clientSock.send("Welcome to the server".encode("utf-8"))
    
    while True:
        message = clientSock.recv(1024)
        
        if message == "CLOSE_CONNECTION":
            print("Client has left server")
            break
        else:
            print(clientAddr, "::", message)
    
    
if __name__ == "__main__":
    server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    server.bind(("0.0.0.0", 10000))
    server.listen(1)
    print("[SERVER OPEN]")
    
    while True:
        clientSock, clientAddr = server.accept()
        print(clientAddr, "has connected")
        
        handleConnection(clientSock, clientAddr)
