# Need to fix
#def main_Menu(option,connectionSocket):
def main_Menu(connectionSocket):
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
        start_chat(connectionSocket) # this must return peer's address
        #return False
    
    if option == "2":
        output = "Setting:\n1.Change Password\n2.Change Status"

        #return False

    # The user has decided to log off
    if option == "3":
        output = "Thank you for using Disscord, Logging you off now!\nHave a nice day :)"
        output = create_Header("X",output)
        connectionSocket.send(output.encode())
        connectionSocket.close()
        #return False
 
