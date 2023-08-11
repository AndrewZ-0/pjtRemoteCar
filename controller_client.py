import socket as sock

client = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
client.connect(("raspberrypi.local", 10000))

print(client.recv(1024).decode("utf-8"))

message = ""
while message != "CLOSE_CONNECTION":
    message = input("Send:: ")
    client.send(message.encode("utf-8"))
