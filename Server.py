from socket import *
serverPort = 6969

serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
                   
serverSocket.listen(3)
print("Skippy is awake and i ready to take on those messages")

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    output = "Hello and how are you?"
    connectionSocket.send(output.encode())
    connectionSocket.close()