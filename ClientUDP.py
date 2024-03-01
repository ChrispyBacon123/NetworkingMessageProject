import socket
import threading
import random 

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.bind(("192.168.101.250",6969))
name = input("Nickname:\n") 

def recieve():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass

t = threading.Thread(target = recieve)
t.start()

client.sendto(f"SIGNUP_TAG:{name}".encode(), ("192.168.101.250",6969))

while True:
    message = input("")
    if message == "!q":
        exit()  
    else:
        client.sendto(f"{name}: {message}".encode(),("192.168.101.250",6969))