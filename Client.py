import socket



serverName = socket.gethostbyname(socket.gethostname())
#serverName = '196.24.144.227'
serverPort = 6969
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


sentence = input("Enter in a massage:\n")
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print ("Skippy says:", modifiedSentence.decode())
clientSocket.close()
