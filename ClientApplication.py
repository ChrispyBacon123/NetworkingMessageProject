from socket import *

def create_Header(messageType,body):
    """Given the type of message and the body, this method will return a header for the message
    and return the message with the header attactched"""

    # Attatching the header 
    out = messageType

    # Determining the size of the message
    arr = list(body)
    size = str(len(arr))

    # Padding if the size of the message is less than 1000 characters
    while(len(size)<4):
        size = "0"+size
    #Attatching the body
    out = out+size+body
    return out




#----------- Client to Client -----------#
#Using UDP

def create_chat(name, status, IP, port):
    chatSocket = socket(AF_INET, SOCK_DGRAM)
    chatSocket.connect(IP, port)
    msg = input('You: ') # The message to send to the other client
    while msg != 'DISCONNECT':
        chatSocket.sendto(msg.encode(), (IP, port))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)












#----------- Client to Server -----------#
#Using TCP
#serverName = socket.gethostbyname(socket.gethostname())
serverName = '192.168.101.250'
serverPort = 6969
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
flag = False # Flag used to exit the loop

# Header Key:
# M = Menu
# I = Information
# S = Start chat
# X = Exit current process
# C = Chat message
# A = Acknowledgement
# R = Re-transmission request
# Example: M1024 (1024 is the number of characters in the string)


'''This while loop is for when the client is interacting with the server'''
while flag != True:
    modifiedSentence = clientSocket.recv(1024) 
    header = modifiedSentence.decode()[:5] # Slicing the received string to get the header from the message
    msg = ''
    if len(modifiedSentence.decode()) > 5:
        msg = modifiedSentence.decode()[5:]

    # Handling the message based on the header
    if header[:1] == 'M': # The message is a Menu
        print (msg) # The menu/options given by the server
        sentence = input("Choose an option:\n") # Choosing one of the options the server presents to the client
        clientSocket.send(sentence.encode())
        continue
    elif header[:1] == 'I': # Information
        print(msg) # Display the message
        continue
    elif header[:1] == 'X': # Exit
        '''Since this loop is for when the client is interacting with the server an exit message 
        would mean that the user wants to log out of the server and therefore the program would end'''
        clientSocket.close()# Terminate connection with server
        break
    elif header[:1] == 'A': # Acknowledgment
        continue
    elif header[:1] == 'R': # Re-transmission request
        clientSocket.send(sentence.encode())
        continue
    elif header[:1] == 'S':
        # splitting the message into an array to access each piece of the user data
        user_data = msg.split() #[name, status, IP, port number]
        peer_name = user_data[0]
        peer_status = user_data[1]
        peer_IP = user_data[2]
        peer_port = user_data[3]
        create_chat(peer_name, peer_status, peer_IP, peer_port)
        continue
    else:
        print('Invalid message') # In case the message does not have a valid header
    
# Exits the loop when the user logs out of the server