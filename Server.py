import socket
import threading
import os
import time 
from ClientClass import *
#import Client.py

clientsList =[]
folderPath = "/Users/CrispyBacon/Desktop/Disscord Clients"
IP = socket.gethostbyname(socket.gethostname())
PORT = 6984
ADDR = (IP, PORT)
DISCONNECT_MSG = "!DISCONNECT"


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


def unique_Username(name, clients):
    """Given the name, this method checks if the username is already taken by some else
        If the name is taken, the method will return true, otherwise it will return false"""
    flag = False

    # Looping through the array of clients
    for client in clients:
        if client.getName() == name:
            flag = True
            return flag
    return flag



def delete_Client(fileName):
    """Deletes the file of the client"""
    fileName = fileName+".txt"
    folderPath = "/Users/CrispyBacon/Desktop/Disscord Clients/"
    try:
        # Iterate through all files in the folder
        for file in os.listdir(folderPath):
            filePath = os.path.join(folderPath, file)

            # Makes sure that the right file is deleted
            if os.path.isfile(filePath) and filePath.endswith(fileName):
                # Delete the file
                os.remove(filePath)
    except Exception as e:
        print("Can not delete the file",filePath)


def initialize_Clients():
    """Creates an array of clients to be manipulated in the server"""
    clients = []
    global folderPath
    for file in os.listdir(folderPath):
        if file.endswith(".txt"):
            with open(os.path.join(folderPath,file), "r") as f:
                data = f.readlines()
                client = Client(data[0].strip(),data[1].strip(),data[2].strip())
                clients.append(client)
    return clients


def save_Client(client):
    """Saves the clients details into a text file on the server"""
    global folderPath
    try:
        # File path to save details of the client
        file_name = folderPath+client.getName()+".txt"
        print(file_name)
        file = open(file_name,"w")

        # Writing data to client's file
        print(client.getName(),file=file)
        print(client.getPassword(),file=file)
        print(client.getStatus(),file=file)
        file.close()

    except IOError:
        print("The Client could not be saved")


def sign_in(connectionSocket,addr):
    """This method handles the process of signing in a client to the server"""
    global clientsList
    message = "Please enter your Username:\n"
    message =create_Header("M",message)
    connectionSocket.send(message.encode())

    # gets the username
    username = connectionSocket.recv(1024).decode()

    correctPassword = False
    counter = 0
    # Ensures that the username exists
    for client in clientsList:
        if client.getName == username:
            break
        counter+=1
    
    # Ensures client enteres the correct password
    while not correctPassword:
        message = f"Please enter your Password {username}:\n "
        message =create_Header("M",message)
        connectionSocket.send(message.encode())
        password = connectionSocket.recv(1024).decode()

        # Base case and setting the IP and port adresses so clients can connect to eachother
        if client.getPassword == password:
            clientsList[counter].setIP(addr[0])
            clientsList[counter].setPort(addr[1])
            return -1
    
    # Recursive case to ensure that the client enters a username that results in a username that is registered
    message = "Account not found\n"
    message = create_Header("M",message)
    connectionSocket.send(message.encode())
    return sign_in(connectionSocket,addr)

    
'''
Add this in handle_client

    if option == "1":
        if (sign_in(connectionSocket)) ## if it is an existing account, it returns True
        ## proceed to menu

    else:
            # it is not an existing account, do something

'''


def sign_up(connectionSocket,addr):
    """This method handles the process of signing up a new account to the server"""
    global clientsList
    #Generating username prompt
    message = "Please enter your Username:"
    message = create_Header("M",message)
    connectionSocket.send(message.encode())

    username = connectionSocket.recv(1024).decode()


    # Look up username in the clients list to ensure that the username is unique
    while (unique_Username(username, clientsList)):   # if username taken
        username = input()
        message = "DUPLICATE. ENTER ANOTHER USERNAME:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())
        username = connectionSocket.recv(1024).decode()
    

    # Determining password for client
    message = "Please enter your Password:"
    message = create_Header("M",message)
    connectionSocket.send(message.encode())

    password = connectionSocket.recv(1024).decode()

    # Error handling for if client tries to not have password
    while(password == ""):
        message = "You can not have an empty password\nPlease enter your Password:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())

        password = connectionSocket.recv(1024).decode()


    aClient = Client(username, password, "ONLINE")    # create new instance of client
    # Generates text file of client
    save_Client(aClient)
    # Modifies the client's details so other clients can talk to clients 
    aClient.setIP(addr[0])
    aClient.setPort(addr[1])
    clientsList.append(aClient)

    # Letting client know that they have been sucessfully registered
    message = "You have been sucessfully registered, please enjoy Datcord\n\n"
    message = create_Header("I",message)
    connectionSocket.send(message.encode())

def letter_Counter_Validation(size,body):
    """Given the body of the message and the supposed number of characters in the message,
    This method checks if the two correspond
    This method will return true if the message passes the validation check"""
    messageList = list(body)
    if size == len(messageList):
        return True
    else:
        return False
    
def send_Reply(correct, counter, connectionSocket):
    """This method sends either a confirmation message that the full message was delivered,
      or it sends a resend message based on the boolean parameter
      This method also ensures that if the resend request has been sent 3 times,
      then a message faliure option will be printed"""
    
    # If the message recieved was correct and decoded
    if correct:
        output = "A0000"
        connectionSocket.send(output.encode())
    
    # Recursive case to send requests to resend the message 
    elif not correct and counter<3:
        output = "R0000"
        connectionSocket.send(output.encode())
        counter+=1

        # Give the server time to resend the message
        time.sleep(6)
        message = connectionSocket.recv(1024)
        decodedMessage = message.decode()
        size = decodedMessage[1:5]
        body = decodedMessage[:5]
        correct = letter_Counter_Validation(int(size),body)

        send_Reply(correct,counter,connectionSocket)

    # Base case
    else:
        print("The message failed to deliver and the sender is being stingy with its resends :(")
        connectionSocket.close()
        return ""


# Need to fix
#def main_Menu(option,connectionSocket):
def main_Menu(connectionSocket):
    """This method handles the main menu and all of its cases.
       It returns true if the method needs to be called again"""
    
    #Creating Header for the string

    # Creating the main menu String
    #menu = menu +"\t\tMain menu:\n"
    menu = "\t\tMain menu\n=======================================\n"
    menu = menu +"1. Start a chat "
    menu = menu +"2. Settings "
    menu = menu +"3. Log Out"

    ## send this menu to client-side ##
    print(menu)     # display the menu
    #connectionSocket.sendto(menu.encode(), 

    option = input()    ## user chooses an option
    
    # Option to send first time
    if option == "":    # if nothing selected, display menu again
        connectionSocket.send(menu.encode())
        return True

    if option not in "123":
        output = "Please choose option 1, 2 or 3\n"+menu
        output = create_Header("M",output)
        connectionSocket.send(output.encode())
        return True
    
    # Printing the list of all the clients
    if option == "1":
        counter = 1
        output = ""
        for item in clientsList:
            output = output+counter+" "+item.toString()+"\n"
            counter+= 1
        output = create_Header("M",output)
        connectionSocket.send(output.encode())
        return False
    
    if option == "2":
        output = "Setting:\n1.Change Password\n2.Change Status"

        return False

    # The user has decided to log off
    if option == "3":
        output = "Thank you for using Disscord, Logging you off now!\nHave a nice day :)"
        output = create_Header("X",output)
        connectionSocket.send(output.encode())
        connectionSocket.close()
        return False
    

def handle_client(connectionSocket, addr):
    """Code that each thread does"""
    print(f"[NEW CONNECTION] {addr} connected.")
    global clientsList
    message = "Welcome to Datcord!\n1. Sign In\n2. Sign up"
    message = create_Header("M",message)
    connectionSocket.send(message.encode())

    # Getting option from client
    optionM = connectionSocket.recv(1024).decode()
    option = str(optionM)  

    # Making sure user actually enters one of the perscribed options
    while option not in '12':
        message = "Please select an option by entering the corresponding number\nWelcome to Datcord!\n1. Sign In\n2. Sign up"
        message =create_Header("M",message)
        connectionSocket.send(message.encode())

        optionM = connectionSocket.recv(1024).decode()
        option = str(optionM)
    
    if option == "1":
        sign_in(connectionSocket,addr)
    
    else:
        sign_up(connectionSocket,addr)


    # Display menu on client-side
    
    
    connectionSocket.close()

def main():
    # Starting up server
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    # Makes a list of clients so that the server can access them 
    global clientsList
    clientsList = initialize_Clients()
    # Lets us know that the server is operational
    print(f"[LISTENING] Server is listening on {IP}:{PORT}") 


    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

        
        
if __name__ == "__main__":
    main()