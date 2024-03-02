import socket
import threading
import queue
import ClientClass
import time

# USER_IP = '127.0.0.1'
# SENDER_IP = '192.168.101.250'
# NAME = ""

SENDER_IP = '127.0.0.1'
USER_IP = '192.168.101.250'
NAME = ""
sentCounter = 0
messages = [" "] # Made the first message empty so the indexes would correspond to the message number 
acknowledged = False
# Makes port
ipSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ipSocket.connect(("8.8.8.8", 80))
ipAddress = ipSocket.getsockname()[0]
IP = ipAddress
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind((USER_IP,6969))


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


# def letter_Counter_Validation(size,body):
#     """Given the body of the message and the supposed number of characters in the message,
#     This method checks if the two correspond
#     This method will return true if the message passes the validation check"""
#     messageList = list(body)
#     if size == len(messageList):
#         return True
#     else:
#         return False

# def check_Message(message,size,body,chatNo):
#     """This method applies all the checks as per the protocol to ensure that
#     the entire message has been delivered uncorrupted it will return true if the message is correct"""
#     global recievedCounter
#     correct = False
#     # Checks to see if header got corrupted
#     print("We got to 83")
#     if message[:1] not in "MISXARP":
#         mssg = create_Header("R",num)
#         correct=False
    
#     print("We got to 88")
#     # Checks to see if message number did not get corrupted
#     if message[11]!= "*" and message[:1]=="C":
#         correct=False
#         # mssg = create_Header("R",num)
#         # server.sendto(mssg.encode(),(SENDER_IP,6969))
#     # Checks to see if any messages were lost in their entirety
#     print("We got to 95")
#     if recievedCounter!=chatNo and recievedCounter<chatNo:
#         correct = False
#         for i in range(recievedCounter,chatNo):
#             num = str(i)
#             while len(num)<4:
#                 num= "0"+num
#             # mssg= create_Header("R",num)
#             # server.sendto(mssg.encode(),(SENDER_IP,6969))

#     print("We got to 105")
#     # Checks to see if the body of the message was corrupted
#     if not letter_Counter_Validation(size,body):
#         # mssg = create_Header("R",chatNo)
#         # server.sendto(mssg.encode(),(SENDER_IP,6969))
#         correct = False
    
#     return correct


# Fix Resend Header
def resend_Message(number):
    """This method handles a resend message request, it takes the number of the message that needs to be resent and tries to resend the data"""
    global acknowledged
    global messages
    found = False
    counter =0
    for i in range(3):
        messages[number]
        # Header is already included in the message 
        message = message.getMessage()
        server.sendto(message.encode(),((SENDER_IP,6969)))

        # Message will always be found as the number will always be at most 1 less than the number of messages sent
        time.sleep(3)
        if acknowledged:
            break
        else:
            counter+=1
        if counter==3:
            print("Failed to deliver message")
    

def recieve():
    disconnect = False
    global acknowledged
    while not disconnect:
        try:
                message, _ = server.recvfrom(1024)
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

def send():
    global sentCounter
    global messages
    disconnect = False
    while not disconnect:
        message = input("")
        if message == "DISCONNECT":
            disconnect = True
            message = create_Chat_Header("C",f"{NAME} has ended the chat",chatNo)         
            server.sendto(message.encode(),(SENDER_IP,6969))
        else:
            # chatNo = str(sentCounter)
            # while len(chatNo)<4:
            #     chatNo="0"+chatNo
            sentCounter+=1
            chatNo = str(sentCounter)

            # Adding message to the messages array 
            message = create_Chat_Header("C",message,chatNo)      
            messages.append(message)
            server.sendto(message.encode(),(SENDER_IP,6969))


def main():
    recThread = threading.Thread(target=recieve)
    sendThread = threading.Thread(target=send)

    recThread.start()
    sendThread.start()
    print("threads have started")

if __name__=="__main__":
    main()