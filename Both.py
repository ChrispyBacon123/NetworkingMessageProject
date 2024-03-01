import socket
import threading
import queue
import ClientClass


messages =queue.Queue()
# Makes port
ipSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ipSocket.connect(("8.8.8.8", 80))
ipAddress = ipSocket.getsockname()[0]
IP = ipAddress
print(IP)
server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.bind(('127.0.0.1',6969))


def create_Header(messageType,body,chatNo):
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
    # Padding if the size of the number is less than 1000
    while (len(chatNo)<4):
        chatNoS = "0"+chatNo
    #Attatching the body
    out = out+size+'*'+chatNoS+'*'+body
    return out

def letter_Counter_Validation(size,body):
    """Given the body of the message and the supposed number of characters in the message,
    This method checks if the two correspond
    This method will return true if the message passes the validation check"""
    messageList = list(body)
    if size == len(messageList):
        return True
    else:
        return False

def recieve():
   while True:
        try:
            message, _ = server.recvfrom(1024)
            message = message.decode()
            # header = message[:5]
            # chatNo = message[7:10]
            # body = message[11:]
            print(message)
            # print(body)
            # print(chatNo)
            # print(header)
            #print(letter_Counter_Validation())
        except:
            pass

def send():
    while True:
        message = input("")
        if message == "!q":
            exit()  
        else:
            message = "cnsdMin: "+message
            message = create_Header("C",message)
            # server.sendto(f"{name}: {message}".encode(),("192.168.101.250",6969))
            server.sendto(message.encode(),("192.168.101.250",6969))


# def resend_Request()

def main():
    t1 = threading.Thread(target=recieve)
    t2 = threading.Thread(target=send)

    t1.start()
    t2.start()
    print("threads have started")

if __name__=="__main__":
    main()
