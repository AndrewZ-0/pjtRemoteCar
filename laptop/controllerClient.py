import socket as sock
from threading import Thread
from time import sleep

class controllerClient:
    def __init__(self):
        self.connected = False
        self.createSocket()

    def createSocket(self):
        self.client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def connectToServer(self, ip, port):
        print("Connecting...")
        while not self.connected:
            try:
                self.client.connect((ip, port))

                print("Connected")
                print(self.client.recv(1024).decode("utf-8"))

                self.connected = True
                self.startHeartbeats()
            except (ConnectionRefusedError, ConnectionResetError):
                if self.connected:
                    print("Connection lost. Reconnecting...")
                    self.connected = False
                self.client.close()
                self.createSocket()

                sleep(0.5)

    def closeConnection(self):
        self.client.close()

    def sendMessage(self, message: str):
        self.client.send(message.encode("utf-8"))

    def heartbeat(self):
        while True:
            try:
                self.sendMessage("SYS HEARTBEAT")
            except:
                self.connected = False
                break
            else:
                self.connected = True
            sleep(0.5)

    def startHeartbeats(self):
        heartbeat_thread = Thread(target = self.heartbeat, daemon = False)
        heartbeat_thread.start()

if __name__ == "__main__":
    IP = "localhost"  #raspberrypi.local
    PORT = 10000

    cc = controllerClient()
    cc.connectToServer(IP, PORT)

    message = ""
    while message != "SYS CLOSE_CONNECTION":
        message = input("Send:: ")
        cc.sendMessage(message)

    cc.closeConnection()
