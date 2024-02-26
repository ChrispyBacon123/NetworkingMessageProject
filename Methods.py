import os
from socket import *
import time

# Text file manipulation and client registering methods
def unique_Username(name, clients):
    """Given the name, this method checks if the username is already taken by some else
        If the name is taken, themethod will return true, otherwise it will return falsex"""
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
    clients=[]
    folderPath = "/Users/CrispyBacon/Desktop/Disscord Clients/"
    for file in os.listdir(folderPath):
        with open(os.path.join(folderPath,file), "r") as f:
            details = f.readlines()
            client = Client(details[0],details[1],details[2])
            clients.append(client)
    return clients         

def save_Client(client):
    """Saves the clients details into a text file on the server"""
    try:
        # File path to save details of the client
        file_name = "/Users/CrispyBacon/Desktop/Disscord Clients/"+client.getName()+".txt"
        file = open(file_name,"w")

        # Writing data to client's file
        print(client.getUsername(),file=file)
        print(client.getPassword(),file=file)
        print(client.getStatus(),file=file)
        file.close()

    except IOError:
        print("The Client could not be saved")







# Need to fix
def main_Menu(option,connectionSocket):
    """This method handles the main menu and all of it's cases.
       It returns true if the method needs to be called again"""
    
    #Creating Header for the string

    # Creating the main menu String
    menu = menu +"\t\tMain menu:\n"
    menu = menu +"1. Start a chat"
    menu = menu +"2. Settings"
    menu = menu +"3. Log Out"

    # Option to send first time
    if option == "":
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




# Message Header methods 
def letter_Counter_Validation(size,body):
    """Given the body of the message and the supposed number of characters in the message,
    This method checks if the two correspond
    This method will return true if the message passes the validation check"""
    messageList = list(body)
    if size == len(messageList):
        return True
    else:
        return False
    
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
 
 # Functions to be used Signing in Menus
def first_Option(connectionSocket,addr):
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

def sign_in(connectionSocket,addr):
    """This method handles the process of signing in a client to the server"""
    global clientsList
    message = "Please enter your Username:"
    message =create_Header("M",message)
    connectionSocket.send(message.encode())

    # gets the username
    username = connectionSocket.recv(1024).decode()

    correctPassword = False
    counter = 0

    # If Client wants to go back 
    if "BACK" == username:
        first_Option(connectionSocket,addr)
        return -1

    # Ensures that the username exists in the server's list of clients
    while (not unique_Username(username, clientsList)):   # if username does not exist
        message = "That doesn't exist..\nPlease enter another username:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())
        username = connectionSocket.recv(1024).decode()

        # If Client wants to go back 
        print(username)
        if "BACK" == username:
            first_Option(connectionSocket,addr)
            return -1
    
    # Requesting password from Client
    message = f"Please enter your Password {username}:"
    message =create_Header("M",message)
    connectionSocket.send(message.encode())
    password = connectionSocket.recv(1024).decode()

    # If Client wants to go back 
    if "BACK" == password:
        first_Option(connectionSocket,addr)
        return -1

    if clientsList[get_Client_Index(username)].getPassword() == password:
            clientsList[counter].setIP(addr[0])
            clientsList[counter].setPort(addr[1])
            return -1
    else:
    
        # Ensures client enteres the correct password
        while not correctPassword:
            message = f"Password was incorrect\nPlease enter your Password or \"BACK\" to go back to the first menu:"
            message =create_Header("M",message)
            connectionSocket.send(message.encode())
            password = connectionSocket.recv(1024).decode()

            #  If the client enters the correct password
            if clientsList[get_Client_Index(username)].getPassword() == password:
                clientsList[counter].setIP(addr[0])
                clientsList[counter].setPort(addr[1])
                return -1
            
            # If Client wants to go back 
            if "BACK" == password:
                first_Option(connectionSocket,addr)
                return -1

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
        first_Option(connectionSocket,addr)
        return -1


    # Look up username in the clients list to ensure that the username is unique
    while (unique_Username(username, clientsList)):   # if username taken
        message = "That username is already taken.\nPlease enter another username:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())
        username = connectionSocket.recv(1024).decode()
        # If Client wants to go back 
        if "BACK" == username:
            first_Option(connectionSocket,addr)
            return -1
    

    # Determining password for client
    message = "Please enter your Password:"
    message = create_Header("M",message)
    connectionSocket.send(message.encode())

    password = connectionSocket.recv(1024).decode()

    # Allowing user to go back to first menu
    if password=="BACK":
        first_Option(connectionSocket,addr)
        return-1

    # Error handling for if client tries to not have password
    while(password == ""):
        message = "You can not have an empty password\nPlease enter your Password:"
        message = create_Header("M",message)
        connectionSocket.send(message.encode())
        password = connectionSocket.recv(1024).decode()
        # Allowing user to go back to first menu
        if password =="BACK":
            first_Option(connectionSocket,addr)
            return-1


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



    

def main():
    menu = "\t\tMain menu:\n"
    menu = menu +"1. Start a chat"
    menu = menu +"2. Settings"
    menu = menu +"3. Log Out"

    tear = list(menu)
    print(len(tear))

    size = "1049"

    while(len(size)<4):
        size = "0"+size
    print(size)
    number = int(size)
    print(number)
    print("this is needed for a git")


if __name__ == "__main__":
    main()