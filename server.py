import socket
import threading
import os
from ClientClass import Client

IP = socket.gethostbyname(socket.gethostname())
PORT = 6970
ADDR = (IP, PORT)
clientFile = r"C:\Users\rlaal\Desktop\Clients\Client"      ## need to be changed on a different machine !!
folderPath = r"C:\Users\rlaal\Desktop\Clients"
clientsList =[]


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
    #folderPath = ""    
    try:
        # Iterate through all files in the folder
        for file in os.listdir(clientFile):
            #filePath = os.path.join(folderPath, file)
            filePath = os.path.join(clientFile, file)

            # Makes sure that the right file is deleted
            if os.path.isfile(filePath) and filePath.endswith(fileName):
                # Delete the file
                os.remove(filePath)
    except Exception as e:
        print("Can not delete the file",filePath)


def initialize_Clients():
    """Creates an array of clients to be manipulated in the server"""
    clients=[]
    #folderPath = r"C:\Users\rlaal\Desktop"      ## need to be changed on a different machine !!
    for file in os.listdir(folderPath):
        #with open(os.path.join(folderPath,file), "r") as f:
        with open(os.path.join(folderPath,file), "r") as f:
            details = f.readlines()
            client = Client(details[0],details[1],details[2])
            clients.append(client)
    return clients         


def save_Client(client):

    """Saves the clients details into a text file on the server"""
    try:
        # File path to save details of the client
        file_name = clientFile+client.getName()+".txt"   ## without ""clientFile+", the new file gets saved in the same directory as the codes
        file = open(file_name, "w")

        # Writing data to client's file
        print(client.getName(),file=file)
        print(client.getPassword(),file=file)
        print(client.getStatus(),file=file)
        file.close()

    except IOError:
        print("The Client could not be saved")


def sign_in():
    username = input("USERNAME: ")
    
    if (unique_Username(username, clientsList)):
        for client in clientsList:
            if username == client.getName():
                correctPassword = client.getPassword()  # get the password of the existing client
                break
        password = input("PASSWORD: ")
        if password == correctPassword:
            print("signing in stuff. make it happen beep")
            print("list of clients:")
            for client in clientsList:    # printing the list of clients
                print(client.toString())


            
        else:
            print("wrong password")
    else:
        print("You must sign up first!")



def sign_up():
    username = input("USERNAME: ")
    
    # look up username in the user file
    while (unique_Username(username, clientsList)):   # if username taken
        username = input("DUPLICATE. ENTER ANOTHER USERNAME: ")
        
    password = input("PASSWORD: ")
    aClient = Client(username, password, "ONLINE")    # create new instance of client
    save_Client(aClient)
    clientsList.append(aClient)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        #msg = conn.recv(1024).decode()


        ## menu here ??
        menu = input("Type 1 for sign up, 2 to sign in, 3 to exit: ")
        if (menu == "1"):
            sign_up()
        elif (menu == "2"):
            sign_in()
        elif (menu == "3"):
            connected = False


        
        #if msg == DISCONNECT_MSG:
           # connected = False

        #print(f"[{addr}] {msg}")
        # msg = f"Msg received: {msg}"

        
        
        #conn.send(msg.encode)
    print(f"[NEW CONNECTION] {addr} disconnected.")
    conn.close()
    

clientsList = initialize_Clients()
def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")
    #clientsList = initialize_Clients()


    print("list of clients:")
    for client in clientsList:    # printing the list of clients
        print(client.toString())
    
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
