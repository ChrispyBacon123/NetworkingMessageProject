import socket
import threading
import os
import time 
from ClientClass import *

# # List containing all the client details
clientsList =[]
# Lock to synchronize clientsList
lock = threading.Lock()
FOLDER_PATH = "/Users/Elijah/Documents/BbuSc_ComSci/CSC3002F/Networks_Assignment_1/Client_Files"
ipSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ipSocket.connect(("8.8.8.8", 80))
ipAddress = ipSocket.getsockname()[0]
IP = ipAddress
PORT = 6969
ADDR = (IP, PORT)
DISCONNECT_MSG = "!DISCONNECT"


# Functions relating to messaging
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



# Functions relating to the list of clients
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

def get_Client_Index(name):
    """Given a client name, this function will return the index of the client in the clientsList list"""
    clientsList
    counter=0
    for client in clientsList:
        if client.getName()==name:
            return counter
        counter +=1

def update_Client(fileName):
    """Deletes the file of the client"""
    fileName = fileName+".txt"
    FOLDERPATH = "/Users/Elijah/Documents/BbuSc_ComSci/CSC3002F/Networks_Assignment_1/Client_Files"
    try:
        # Iterate through all files in the folder
        for file in os.listdir(FOLDERPATH):
            filePath = os.path.join(FOLDERPATH, file)

            # Makes sure that the right file is deleted
            if os.path.isfile(filePath) and filePath.endswith(fileName):
                # Delete the file
                os.remove(filePath)
    except Exception as e:
        print("Can not delete the file",filePath)

def initialize_Clients():
    """Creates an array of clients to be manipulated in the server
    It does this by scanning all the textfiles in the folder, extracting the data
    and generating a list of clients"""
    clients = []
    for file in os.listdir(FOLDER_PATH):
        if file.endswith(".txt"):
            with open(os.path.join(FOLDER_PATH,file), "r") as f:
                data = f.readlines()
                # There is no guarantee that the client is online at this moment
                if data[2].strip() == "ONLINE":
                    data[2] = "OFFLINE"
                client = Client(data[0].strip(),data[1].strip(),data[2].strip())
                clients.append(client)

    return clients

def save_Client(client):
    """Saves the clients details into a text file stored on the server machine"""
    FOLDER_PATH
    try:
        # File path to save details of the client
        file_name = FOLDER_PATH+client.getName()+".txt"
        print(file_name)
        SystemExit()
        file = open(file_name,"w")

        # Writing data to client's file
        print(client.getName(),file=file)
        print(client.getPassword(),file=file)
        print(client.getStatus(),file=file)
        file.close()

    except IOError:
        print("The Client could not be saved")

def print_Clients():
    """This function returns a string list of the list of clients registred on the server"""
    global clientsList
    counter = 1
    availClient = "Available:\n"
    for item in clientsList:
        availClient = availClient+str(counter)+" "+item.toString()+"\n" # list the available clients
        counter+= 1
    availClient = availClient + "Please enter the number of the person you want to chat!"
    return availClient

# Functions to be used Signing in Menus
def first_Option(connectionSocket,addr):
    for i in clientsList:
        print(i.toString())
    message = "\tWelcome to Datcord!\n=======================================\n1. Sign In\n2. Sign up"
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
        clientIndex = sign_in(connectionSocket,addr)
        return clientIndex
    
    else:
        clientIndex = sign_up(connectionSocket,addr)
        return clientIndex


def sign_in(connectionSocket,addr):
    """This method handles the process of signing in a client to the server"""
    clientsList
    message = "Please enter your Username:"
    message =create_Header("M",message)
    connectionSocket.send(message.encode())

    # gets the username
    username = connectionSocket.recv(1024).decode()

    correctPassword = False
    counter = 0

    # If Client wants to go back 
    if "BACK" == username:
        clientIndex = first_Option(connectionSocket,addr)
        print(clientIndex, "Line 154")
        return clientIndex

    # Ensures that the username exists in the server's list of clients
    while (not unique_Username(username, clientsList)):   # if username does not exist
        message = "That doesn't exist.. Enter BACK to sign up.\nOtherwise please enter another username:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())
        username = connectionSocket.recv(1024).decode()

        # If Client wants to go back 
        if "BACK" == username:
            clientIndex = first_Option(connectionSocket,addr)
            print(clientIndex, "Line 168")
            return clientIndex
    
    # Requesting password from Client
    message = f"Please enter your Password {username}:"
    message =create_Header("M",message)
    connectionSocket.send(message.encode())
    password = connectionSocket.recv(1024).decode()

    # If Client wants to go back 
    if "BACK" == password:
        clientIndex = first_Option(connectionSocket,addr)
        return clientIndex
    
    # If password is incorrect
    while clientsList[get_Client_Index(username)].getPassword() != password:
            message = f"Password was incorrect\nPlease enter your Password or \"BACK\" to go back to the first menu:"
            message =create_Header("M",message)
            connectionSocket.send(message.encode())
            password = connectionSocket.recv(1024).decode()

            # If Client wants to go back 
            if "BACK" == password:
                clientIndex = first_Option(connectionSocket,addr)
                return clientIndex
    
    # Once the password is correct
    correct = False

    # Get the UDPPort
    message = f"Please enter a valid port (10000 < x < 65535) that will be used to message other clients:"
    message =create_Header("M",message)
    connectionSocket.send(message.encode())
    while not correct:        
            inputPort = connectionSocket.recv(1024).decode()
            if inputPort.isdigit():
                port = int(inputPort)

                if port>10000 and port<65535: # and isinstance(port,int):
                    correct = True
                else:
                    message = "That port number is not valid. Please enter a valid port number:"
                    message =create_Header("M",message)
                    connectionSocket.send(message.encode())

            # If Client wants to go back 
            elif inputPort == "BACK":
                clientIndex = first_Option(connectionSocket,addr)
                return clientIndex
            else:
                message = "Please enter an integer for the port NUMBER:"
                message =create_Header("M",message)
                connectionSocket.send(message.encode())
       
            
    #  If all the data entered is correct
    if clientsList[get_Client_Index(username)].getPassword() == password and correct:
        # Setting the client's details
        counter = get_Client_Index(username)
        clientsList[counter].setIP(addr[0])
        clientsList[counter].setPort(addr[1])
        clientsList[counter].setUDPPort(int(port))
        if clientsList[counter].getStatus() == "OFFLINE":
            clientsList[counter].setStatus("ONLINE")


        for i in clientsList:
            print(i.toString())
        return counter

                      
def sign_up(connectionSocket,addr):
    """This method handles the process of signing up a new account to the server"""
    global clientsList
    #Generating username prompt
    message = "Please enter your Username:"
    message = create_Header("M",message)
    connectionSocket.send(message.encode())

    # Getting username from client
    username = connectionSocket.recv(1024).decode()

    # If Client wants to go back 
    if "BACK" == username:
        clientIndex = first_Option(connectionSocket,addr)
        return clientIndex

    # Look up username in the clients list to ensure that the username is unique
    while (unique_Username(username, clientsList)):   # if username taken
        message = "That username is already taken. Enter BACK to cancel.\nOtherwise please enter another username:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())
        username = connectionSocket.recv(1024).decode()
        # If Client wants to go back 
        if "BACK" == username:
            clientIndex = first_Option(connectionSocket,addr)
            return clientIndex
    
    # Determining password for client
    message = "Please make your Password:"
    message = create_Header("M",message)
    connectionSocket.send(message.encode())

    password = connectionSocket.recv(1024).decode()

    # Allowing user to go back to first menu
    if password=="BACK":
        clientIndex = first_Option(connectionSocket,addr)
        return clientIndex

    # Error handling for if client tries to not have password
    while(password == ""):
        message = "You can not have an empty password. Enter BACK to cancel.\nOtherwise please enter your Password:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())
        password = connectionSocket.recv(1024).decode()
        # Allowing user to go back to first menu
        if password =="BACK":
            clientIndex = first_Option(connectionSocket,addr)
            return clientIndex
    # Get the UDPPort
        
    correct = False

    # Get the UDPPort
    message = f"Please enter a valid port (10000 < x < 65535) that will be used to message other clients:"
    message =create_Header("M",message)
    connectionSocket.send(message.encode())
    while not correct:        
            inputPort = connectionSocket.recv(1024).decode()
            if inputPort.isdigit():
                port = int(inputPort)

                if port>10000 and port<65535: # and isinstance(port,int):
                    correct = True
                else:
                    message = "That port number is not valid. Please enter a valid port number:"
                    message =create_Header("M",message)
                    connectionSocket.send(message.encode())

            # If Client wants to go back 
            elif inputPort == "BACK":
                clientIndex = first_Option(connectionSocket,addr)
                return clientIndex
            else:
                message = "Please enter an integer for the port NUMBER:"
                message =create_Header("M",message)
                connectionSocket.send(message.encode())
       

    # Data that has been validated
    aClient = Client(username, password, "ONLINE")    # create new instance of client
    # Generates text file of client
    save_Client(aClient)
    # Modifies the client's details so other clients can talk to clients 
    
    clientsList.append(aClient)
    clientsList = initialize_Clients()
    clientsList[len(clientsList)-1].setIP(addr[0])
    clientsList[len(clientsList)-1].setUDPPort(port)
    clientsList[len(clientsList)-1].setPort(addr[1])
    clientsList[len(clientsList)-1].setStatus("ONLINE")
    # Letting client know that they have been sucessfully registered
    message = "You have been sucessfully registered, please enjoy Datcord\n\n"
    message = create_Header("I",message)
    connectionSocket.send(message.encode())
    return len(clientsList)-1


# Functions to be used with Main Menu
def settings(connectionSocket,clientIndex):
    global clientsList
    # Sending the settings menu to the client
    menu = menu = "\tSettings\n=======================================\n"
    menu = menu +"1. Change Password\n"
    menu = menu +"2. Change Status\n"
    menu = menu +"3. Go back to Main menu\n"

    message =create_Header("M",menu)
    connectionSocket.send(message.encode())

    # Getting option back from client
    option = connectionSocket.recv(1024).decode()

    # Ensuring that the client enters a correct option 
    while option not in "123":
        output = "Please choose option 1, 2 or 3\n"+menu
        output = create_Header("M",output)
        connectionSocket.send(output.encode())
    
    # If the client chooses to change their password
    if option == "1":
        message = "Please enter in your new password:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())
        password = connectionSocket.recv(1024).decode()

        # Updating the client and saving their details 
        clientsList[clientIndex].setPassword(password)
        save_Client(clientsList[clientIndex])
        main_Menu(connectionSocket,clientIndex)


    # If the client chooses to change their status
    elif option == "2":
        menu = "Please choose and option\n1.[HIDDEN]\n2.[ONLINE]"
        message =create_Header("M",menu)
        connectionSocket.send(message.encode())

        # Getting option back from client
        option = connectionSocket.recv(1024).decode()
        
        # Ensuring that the option is one of the available option
        while option not in "12":
            output = "Please choose option 1 or 2\n"+menu
            output = create_Header("M",output)
            connectionSocket.send(output.encode())
            option = connectionSocket.recv(1024).decode()

        # If the client opted to keep their status hidden 
        if option == "1":
            clientsList[clientIndex].setStatus("HIDDEN")
            save_Client(clientsList[clientIndex])

            # Re-initialize to make sure that the details are updated
            clientsList = initialize_Clients()
            main_Menu(connectionSocket,clientIndex)
        else:
            # If the client opted to show their status  
            clientsList[clientIndex].setStatus("ONLINE")
            save_Client(clientsList[clientIndex])

            # Re-initialize to make sure that the details are updated
            clientsList = initialize_Clients()
            clientsList[clientIndex].setStatus("ONLINE")
            main_Menu(connectionSocket,clientIndex)

    else:
        main_Menu(connectionSocket,clientIndex)

def start_chat(connectionSocket,clientIndex):
    """Lists the available clients & client can choose a peer to start chat with
    & it returns the address of the chosen client"""
    global clientsList
    # Printing list of available clients
    output = create_Header("M", print_Clients())
    connectionSocket.send(output.encode())

    chosenOption = connectionSocket.recv(1024).decode() # get the option chosen by the user
    chosenOption = int(chosenOption)   
    # Error checking
    while chosenOption<1 or chosenOption>len(clientsList):
        availClient = availClient + "That option does not exist\nPlease enter the number of the person you want to chat!\n"+print_Clients()
        output = create_Header("M", availClient)
        connectionSocket.send(output.encode())
        chosenOption = connectionSocket.recv(1024).decode() # get the option chosen by the user
        chosenOption = int(chosenOption)


    # Making sure that the client hasn't tried to start a chat with themselves 
    chosenClient = clientsList[chosenOption - 1]
    while chosenClient.getName()==clientsList[clientIndex].getName():
        message = "You can not start a chat with yourself, please choose another person\n"+print_Clients()
        output = create_Header("M", message)
        connectionSocket.send(output.encode())
        chosenOption = connectionSocket.recv(1024).decode() # get the option chosen by the user
        chosenOption = int(chosenOption)
        chosenClient = clientsList[chosenOption - 1]
        

    # If the client is offline
    if chosenClient.getStatus()=="OFFLINE":
        message = "The client is offline so you can't chat with them\n"
        output = create_Header("I", message)
        connectionSocket.send(output.encode())
        connectionSocket.recv(1024).decode() # This line is to receive the acknowledgement message sent from the client
        main_Menu(connectionSocket,clientIndex)
    
    # If the client is hidden
    elif chosenClient.getStatus()=="HIDDEN":
        message = "The client is hidden and doesn't want to talk to anyone\n"
        output = create_Header("I", message)
        connectionSocket.send(output.encode())
        connectionSocket.recv(1024).decode() # This line is to receive the acknowledgement message sent from the client

        main_Menu(connectionSocket,clientIndex)
    
    else:
        # Need to send [name, IP, port number]
        message = "Starting a chat with " + chosenClient.getName() + " ..."
        output = create_Header("I", message)
        connectionSocket.send(output.encode())

        # This line is crucial to ensure that the I message and S message are not sent together as one string
        connectionSocket.recv(1024).decode()

        peerIP = chosenClient.getIP()
        peerPort = chosenClient.getUDPPort()
        peerName = chosenClient.getName()
        message= str(peerName)+" "+str(peerIP)+" "+str(peerPort)
        output = create_Header("S",message)
        connectionSocket.send(output.encode())
        
        # Maybe implement this (bring it back to main menu after chat ends)
        # client needs send an empty string after ending a chat to come back to this point
        connectionSocket.recv(1024).decode()
        main_Menu(connectionSocket,clientIndex)


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


def log_off(clientIndex):
    """When the client logs off, their status changes to OFFLINE."""
    clientsList[clientIndex].setStatus("OFFLINE")
    save_Client(clientsList[clientIndex])   
    print(clientsList[clientIndex].toString())


def main_Menu(connectionSocket,clientIndex):
    global clientsList
    """This method handles the main menu and all of its cases.
       It returns true if the method needs to be called again"""
    
    #Creating Header for the string
    # Creating the main menu String
    #menu = menu +"\t\tMain menu:\n"
    menu = "\t\tMain menu\n=======================================\n"
    menu = menu +"1. Start a chat\n"
    menu = menu +"2. Settings\n"
    menu = menu +"3. Log Out"

    output = create_Header("M",menu)
    connectionSocket.send(output.encode())

    optionM = connectionSocket.recv(1024).decode()
    option = str(optionM) 
    
    if option not in "123":
        output = "Please choose option 1, 2 or 3\n" + menu
        output = create_Header("M",output)
        connectionSocket.send(output.encode())
        #return True
    
    # Printing the list of all the clients
    if option == "1":
        start_chat(connectionSocket,clientIndex) # this must return peer's address
        #return False
    
    if option == "2":
        settings(connectionSocket,clientIndex)
        #return False

    # The user has decided to log off
    if option == "3":
        log_off(clientIndex)
        output = "Thank you for using Datcord, Logging you off now!\nHave a nice day :)"
        # Setting to make sure that the status is updated for other clients
        if clientsList[clientIndex].getSatus()=="ONLINE":
            clientsList[clientIndex].setStatus("OFFLINE")

        output = create_Header("X",output)
        connectionSocket.send(output.encode())
        connectionSocket.close()
        #return False
 
 
# Main Funtions 
def handle_client(connectionSocket, addr):
    """Code that each thread does"""
    print(f"[NEW CONNECTION] {addr} connected.")
    clientIndex = first_Option(connectionSocket,addr)
    main_Menu(connectionSocket,clientIndex)
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
        threads = threading.active_count() - 1
        print(f"A new client has joined, we now have {threads} threads\n")

        
        
if __name__ == "__main__":
    main()
