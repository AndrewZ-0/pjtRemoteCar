import socket as sock

class raspiServer:
    def __init__(self):
        self.cmdStack = []

    def startServer(self):
        with sock.socket(sock.AF_INET, sock.SOCK_STREAM) as self.server:
            self.server.bind(("0.0.0.0", 8000))
            self.server.listen(1)
            print("[SERVER OPEN]")
            
            while True:
                self.clientSock, self.clientAddr = self.server.accept()
                self.client_ip, self.client_port = self.clientSock.getpeername()
                print(self.client_ip, "has connected on port", self.client_port)
                
                self.handleConnection()

    def handleConnection(self):
        self.clientSock.send("Welcome to the server".encode("utf-8"))
        
        try:
            while True:
                dataPackage = self.clientSock.recv(1024).decode("utf-8")

                dataType, data = self.unpackPackage(dataPackage)
                if dataType == "SYS":
                    if data == "CLOSE_CONNECTION":
                        print(f"Client {self.client_ip} has left server")
                        break
                    #data == "HEARTBEAT": --> pass
                elif dataType == "CMD":
                    self.cmdStack.append(data)

                    print(self.client_ip, "::", data)
        except ConnectionResetError:
            print(f"Client {self.client_ip} has left the server unexpectedly")
        finally:
            self.clientSock.close()
    
    def unpackPackage(self, dataPackage: str):
        dataPackets = dataPackage.split(" ", maxsplit = 1)
        return dataPackets[0], dataPackets[1]

    
if __name__ == "__main__":
    rs = raspiServer()
    rs.startServer()
