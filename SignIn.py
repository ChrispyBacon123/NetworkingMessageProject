# returns True when signed in, False if it is not an existing account
def sign_in(connectionSocket):
    # asks client for a username
    message = "USERNAME: "
    message =create_Header("M",message)
    connectionSocket.send(message.encode())

    # gets the username
    username = connectionSocket.recv(1024).decode()

    userFound = False
    
    for client in clientsList:
        if client.getName == username:
            message = "PASSWORD: "
            message =create_Header("M",message)
            connectionSocket.send(message.encode())
            password = connectionSocket.recv(1024).decode()

            if client.getPassword == password:
                return True
            
            userFound = True
            break
        
    if userFound == False:
        message = "Account not found. Create Datcord account :D\n"
        connectionSocket.send(message.encode())
        return False
    
'''
Add this in handle_client

    if option == "1":
        if (sign_in(connectionSocket)) ## if it is an existing account, it returns True
        ## proceed to menu

    else:
            # it is not an existing account, do something

'''
