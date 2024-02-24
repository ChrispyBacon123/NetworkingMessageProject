# simple UDP client program from textbook pg.186
# 20 Feb 2024


from socket import *

serverName = "127.0.0.1"
serverPort = 10001
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = input("Input lowercase sentence: ")
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
