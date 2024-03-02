from socket import socket, timeout, AF_INET, SOCK_DGRAM, SOCK_STREAM
import threading
import queue
import time
import ClientClass


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


'''This function will be called if the message received is corrupted or nothing was received'''
def request_retransmission(socket, IP, port):
    header = 'R0000' # the re-transmission request message
    socket.sendto(header.encode(), (IP, port)) # sending the re-transmission request to the peer



#----------- Client to Client -----------#
#Using UDP

# The flag is to keep track of whether you have started a chat or you accepted a chat request: 
# True = you started the chat; False = you accepted a request

NAME = ""
sentCounter = 0
messages = [" "] # Made the first message empty so the indexes would correspond to the message number 
acknowledged = False


def create_Chat_Header(messageType,body,chatNo):
    """Given the type of message and the body, this method will return a header for the message
    and return the message with the header attactched"""

    # Attatching the header 
    out = messageType

    # Determining the size of the message
    arr = list(body)
    size = str(len(arr))

    # Padding if the size of the message is less than 1000 characters
    while len(size)<4:
        size = "0"+size

    # Padding if the size of the number is less than 1000
    chatNoS=""+chatNo
    while len(chatNoS)<4:
        chatNoS = "0"+chatNoS
    #Attatching the body
    out = out+size+'*'+chatNoS+'*'+body
    return out

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


def receive(user_IP, user_port):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', user_port))
    disconnect = False
    global acknowledged
    while not disconnect:
        try:
                message, _ = serverSocket.recvfrom(1024)
                message = message.decode()
                header = message[:5]
                size = int(message[1:5])
                chatNo = message[7:10]
                body = message[11:]
                # if True:
                    # We don't need to send an acknowledgement for an acknowledgement
                    # if header[:1] == 'A':
                    #     acknowledged = True
                    # else:
                    #     message = create_Chat_Header("A","",chatNo) # Sends acknowledgement for the chat number so that the sender knows which message this is for        
                    #     server.sendto(message.encode(),(SENDER_IP,6969))
                print(body)
                # else: 
                #     resendThread = threading.Thread(target=resend_Message(chatNo)) 
                #     resendThread.start()
        except:
            pass


def send(peer_IP, peer_port):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    global sentCounter
    global messages
    disconnect = False
    while not disconnect:
        message = input("")
        if message == "DISCONNECT":
            disconnect = True
            message = create_Chat_Header("C",f"{NAME} has ended the chat",chatNo)         
            clientSocket.sendto(message.encode(),(peer_IP, peer_port))
        else:
            # chatNo = str(sentCounter)
            # while len(chatNo)<4:
            #     chatNo="0"+chatNo
            sentCounter+=1
            chatNo = str(sentCounter)

            # Adding message to the messages array 
            message = create_Chat_Header("C",message,chatNo)      
            messages.append(message)
            clientSocket.sendto(message.encode(),(peer_IP, peer_port))



#def create_chat(name, IP, port, chat_request_flag):
def create_chat(peer_name, peer_IP, peer_port, user_port, user_IP):
    '''If you started the chat then you will send the first message and the user who accepted the chat request
    will have to wait to receive that message first'''
    
    peer_port = int(peer_port) # ensure port is int
    user_port = int(user_port)
    
    print("To leave the chat enter 'DISCONNECT'")

    msg = '' # Initialising the msg variable for the while loop condition
    timeout_count = 0 # Keeping track of how many times a timeout has occured
    timeout_flag = False # This flag becomes true when there have been 3 timeouts and the connection is terminated

    recThread = threading.Thread(target=receive, args=(user_IP, user_port))
    sendThread = threading.Thread(target=send, args=(peer_IP, peer_port))

    recThread.start()
    sendThread.start()
    print("threads have started")

    '''
    # If you started the chat then you send the first message
    # This is just to send the initial message, all messages thereafter will be sent in the while loop
    if chat_request_flag:
        msg = input('You: ') # The message to send to the other client
        msg_with_header = create_Header('C', msg) # Adding the header to the message
        chatSocket.sendto(msg_with_header.encode(), (IP, port)) # sending the message with the header to the peer

    while msg.upper() != 'DISCONNECT': # The upper() method is used to make the condition case insensitive

        try:
            # Receive data from the socket
            response, peerAddress = chatSocket.recvfrom(2048) # saving the response from the peer to response, peerAddress is not used
            header = response.decode()[:5] # saving just the header

            # If data is received before timeout
            if header[:1] == 'C': # The response is a chat message
                modifiedMessage = response.decode()[5:] # taking off the header
                print(name + ': ' + modifiedMessage) # Showing the response from the peer
                msg = input('You: ') # Next message
                continue
            elif header[:1] == 'A': # This is not the response from the peer but just an acknowledgement 
                continue
            elif header[:1] == 'R': # This means the chat message was not sent or was corrupted and the peer has requested you to re-send it
                chatSocket.sendto(msg_with_header.encode(), (IP, port)) # re-sending the message
                continue

            msg_with_header = create_Header('C', msg) # Adding the header to the message
        
            chatSocket.sendto(msg_with_header.encode(), (IP, port)) # sending the message with the header to the peer

            start_time = time.time()
            chatSocket.settimeout(30)  # 30 seconds timeout

        except timeout:
            # If timeout occurs
            timeout_count += 1 # Increasing the timeout counter
            if timeout_count == 3:
                print("Peer unresponsive, terminating connection")
                timeout_flag = True # Too many timeouts have occured so the connection must be terminated
                break # Breaking out of the loop so that the connection is terminated   
            elapsed_time = time.time() - start_time
            print("Timeout occurred after", elapsed_time, "seconds") # Telling the user that a timeout has occurred

            # After timeout occurs then a request is sent to the peer to resend the message
            request_retransmission(chatSocket, IP, port)
            print("Re-transmission request has been sent")


    if timeout_flag == False:
        # This message must not be printed if the connection is being terminated because there were too many timeouts
        chatSocket.sendto(('Peer has left the chat').encode(), (IP, port))
    chatSocket.close() # Terminate the connection to the peer
    '''
# Add some way to get back to menu

# Main function
def main():
    #----------- Client to Server -----------#
    #Using TCP 
    serverName = '192.168.101.250'
    serverPort = 6969
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    flag = False # Flag used to exit the loop
    timeout_count = 0 # Keeping track of how many times a timeout has occured
    timeout_flag = False # This flag becomes true when there have been 3 timeouts and the connection is terminated

    # Header Key:
    # M = Menu (Any message that requires an input from the client)
    # I = Information
    # S = Start chat
    # X = Exit current process
    # C = Chat message
    # A = Acknowledgement
    # R = Re-transmission request
    # P = (Please) Request to start a chat with another client
    # Example: M1024 (1024 is the number of characters in the string)


    '''This while loop is for when the client is interacting with the server'''
    while flag != True:
        start_time = time.time()
        clientSocket.settimeout(10800) # If the server does not respond within 3 hours then a timeout will occur
        try:
            modifiedSentence = clientSocket.recv(1024) 
            header = modifiedSentence.decode()[:5] # Slicing the received string to get the header from the message
            msg = ''

            if len(modifiedSentence.decode()) > 5:
                msg = modifiedSentence.decode()[5:]

            # Handling the message based on the header
            if header[:1] == 'M': # The message is a Menu
                print (msg) # The menu/options given by the server
                sentence = input() # Giving the server the required data
                clientSocket.send(sentence.encode())
                continue
            elif header[:1] == 'I': # Information
                print(msg) # Display the message
                acknowledge = 'A0000'
                clientSocket.send(acknowledge.encode()) # This is to tell the server that the message has been received
                continue
            elif header[:1] == 'X': # Exit
                '''Since this loop is for when the client is interacting with the server an exit message 
                would mean that the user wants to log out of the server and therefore the program would end'''
                print(msg)
                clientSocket.close()# Terminate connection with server
                break
            elif header[:1] == 'A': # Acknowledgment
                continue
            elif header[:1] == 'R': # Retransmission request
                clientSocket.send(sentence.encode())
                continue
            elif header[:1] == 'S': # Start chat
                # splitting the message into an array to access each piece of the user data
                user_data = msg.split() #[name, IP, port number]
                peer_name = user_data[0]
                peer_IP = user_data[1]
                peer_port = user_data[2]
                user_port = user_data[3]
                user_IP = user_data[4]
                create_chat(peer_name, peer_IP, peer_port, user_port, user_IP)
                #create_chat(peer_name, peer_IP, peer_port, True)
                continue
            elif header[:1] == 'P': # Request for new chat
                # P####PeerName IP Port
                user_data = msg.split() #[name, IP, port number]
                peer_name = user_data[0]
                peer_IP = user_data[1]
                peer_port = user_data[2]
                #print(msg + ' wants to start a chat:\n')
                #print('1. Accept')
                #print('2. Decline\n')
                #choice = input() # Whether the user chooses to accept or deny the request

                #if choice == 1: # Accept the request
                create_chat(peer_name, peer_IP, peer_port, False)
                continue
                # elif choice == 2: # Decline the request
                #     request_response = 'User has delcined the request to chat.'
                #     clientSocket.send((create_Header('I', request_response)).encode()) # Send a response to the peer telling them their request was denied
                #     continue
            else:
                print('Invalid message') # In case the message does not have a valid header
                flag = True

        except timeout:
            # If timeout occurs
            timeout_count += 1 # Increasing the timeout counter
            if timeout_count == 3:
                print("Server unresponsive, terminating connection")
                clientSocket.close() # Terminating the connection with the server
                break # Breaking out of the loop because the connection has been terminated  
            elapsed_time = time.time() - start_time
            print("Timeout occurred after", elapsed_time, "seconds") # Telling the user that a timeout has occurred

            # After timeout occurs then a request is sent to the peer to resend the message
            request_retransmission(clientSocket, serverName, serverPort)
            print("Re-transmission request has been sent")


        
    # Exits the loop when the user logs out of the server
            


if __name__ == "__main__":
    main()