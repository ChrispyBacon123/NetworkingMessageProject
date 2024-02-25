
# Need to fix
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
        menu =create_Header("M",menu)
        connectionSocket.send(message.encode())
        return True

    if option not in "123":
        menuResend = "Please choose option 1, 2 or 3\n"+menu
        menuResend = create_Header("M",menuResend)
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
    
