from socket import *
import time

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

def create_chat(name, status, IP, port):
    chatSocket = socket(AF_INET, SOCK_DGRAM)
    print("To leave the chat enter 'DISCONNECT'")
    print(name + ' is ' + status)
    msg = input('You: ') # The message to send to the other client
    timeout_count = 0 # Keeping track of how many times a timeout has occured
    timeout_flag = False # This flag becomes true when there have been 3 timeouts and the connection is terminated
    while msg.upper() != 'DISCONNECT': # The upper() method is used to make the condition case insensitive

        msg_with_header = create_Header('C', msg) # Adding the header to the message
        chatSocket.sendto(msg_with_header.encode(), (IP, port)) # sending the message with the header to the peer

        start_time = time.time()
        chatSocket.settimeout(30)  # 30 seconds timeout

        try:
            # Receive data from the socket
            response, serverAddress = chatSocket.recvfrom(2048) # saving the response from the peer to response, serverAddress is not used
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

        except socket.timeout:
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










# Main function
def main():
    #----------- Client to Server -----------#
    #Using TCP
    #serverName = socket.gethostbyname(socket.gethostname())
    serverName = '127.0.0.1'
    serverPort = 6971
    clientSocket = socket(AF_INET, SOCK_STREAM)
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
    # Example: M1024 (1024 is the number of characters in the string)


    '''This while loop is for when the client is interacting with the server'''
    while flag != True:
        start_time = time.time()
        clientSocket.timeout(30) # If the server does not respond within 30 seconds then a timeout will occur
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
                flag = True

        except socket.timeout:
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