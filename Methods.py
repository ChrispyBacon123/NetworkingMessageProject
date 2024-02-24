import os

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