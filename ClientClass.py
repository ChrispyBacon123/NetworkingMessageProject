class Client:
    
    #Constructor to create new Client object
    def __init__(self, username, password, status):
        self.__username = username
        self.__password = password
        self.__status = status
        self.__IP_add = ''
        self.__port = 0
        self.__UDP_port = 0
        self.__chat_requests = []
        #The two leading underscores ensures the fields are private

    #Accessor to get the username
    def getName(self):
        return self.__username
    
    #Accessor to get the password
    def getPassword(self):
        return self.__password
    
    #Accessor to get the user's status
    def getStatus(self):
        return self.__status
    
    #Accessor to get the IP address
    def getIP(self):
        return self.__IP_add
    
    #Accessor to get the port
    def getPort(self):
        return self.__port
    
    #Accessor to get the UDP_port
    def getUDPPort(self):
        return self.__UDP_port

    #Accessor to get list of chat requests
    def getChatRequests(self):
        return self.__chat_requests

    #Mutator to change the IP address
    def setIP(self, newIP):
        self.__IP_add = newIP

    #Mutator to change the port of the client
    def setPort(self, newPort):
        self.__port = newPort

    #Mutator to change the UDP_Port of the client
    def setUDPPort(self, newPort):
        self.__UDP_port = newPort

    #Mutator to change the password
    def setPassword(self, new_pass):
        self.__password = new_pass

    #Mutator to change the user's visibility status
    def setStatus(self, new_status):
        self.__status = new_status

    #Mutator to add string with a Client's info (name, IP_add, UDP_port) to the list of chat requests
    def addChatRequests(self, new_chat_request):
        self.__chat_requests.append(new_chat_request)

    #Method to print out the information of a client for other clients to see
    def toString(self):
        return self.__username + ' ' + self.__status
