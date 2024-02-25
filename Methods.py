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