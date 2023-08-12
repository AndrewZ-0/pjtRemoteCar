import socket as sock

class controllerClient:
    def __init__(self):
        self.client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)

    def start(self):
        self.client.connect(("raspberrypi.local", 10000))

        print(self.client.recv(1024).decode("utf-8"))

        self.startControlling()

        self.client.close()

    def startControlling(self):
        message = ""
        while message != "CLOSE_CONNECTION":
            message = input("Send:: ")
            self.client.send(message.encode("utf-8"))

if __name__ == "__main__":
    cc = controllerClient
    cc.start()
