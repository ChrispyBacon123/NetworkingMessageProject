def start_chat(connectionSocket):
    """Lists the available clients & client can choose a peer to start chat with
    & it returns the address of the chosen client"""
    
    counter = 1
    availClient = "Available:\n"
    for item in clientsList:
        availClient = availClient+str(counter)+" "+item.toString()+"\n" # list the available clients
        counter+= 1
    availClient = availClient + "Please enter the number of the person you want to chat!"
    output = create_Header("M", availClient)
    connectionSocket.send(output.encode())

    chosenOption = connectionSocket.recv(1024).decode() # get the option chosen by the user
    chosenOption = int(chosenOption)   
    chosenClient = clientsList[chosenOption - 1]

    message = "Starting a chat with " + chosenClient.getName() + " ..."
    output = create_Header("M", message)
    connectionSocket.send(output.encode())

    peerIP = chosenClient.getIP()
    peerPort = chosenClient.getPort()
    destination = {peerIP, peerPort}    # this does not work atm since clientFile
                                        # does not contain IP nor port of client

    return destination
