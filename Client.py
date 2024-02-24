import socket



#serverName = socket.gethostbyname(socket.gethostname())
serverName = "192.168.101.250"
serverPort = 6969
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


sentence = input("Connected :)\n")
clientSocket.send(sentence.encode())
#modifiedSentence = clientSocket.recv(1024)
#print ("Skippy says:", modifiedSentence.decode())
clientSocket.close()

