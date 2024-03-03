# NetworkingMessageProject


## Overview

This python program is a networking application which allows for messaging between clients as well as a server.

The server acts as a phone book to allow for users (clients) to obtain the resources that they need to communicate 
with eachother.
The server has the following features:
 - Listing all clients and their status with the server

 - Allowing the client to obtain the details fo the other client they wish to message

 - Allowing the client to change their password and visibility status to other clients


## Usage

To run the program, follow these steps:

 1. Create a folder on your desktop to store the client details

 2. Copy that folder's path and replace the file path for the global variable <folderPath> in the Server.py program

 3. Start the Server.py Program (This can be done by running the command: `Python3 Server.py`) in your terminal 

 4. Copy the IP address and port number that the Server.py Program is listening on (the address will be printed in the format "Listening on <IP address>:<Port Number>)

 5. Paste the IP value into the variable <serverName> and the Port value into the variable <serverPort> which are found shortly after the line "#----------- Client to Server -----------#" 

 6. Run the ClientApplication.py program and proceed to follow the inputs in the terminal (This can be done by running the command: `Python3 ClientApplication.py`) in your terminal 
 

## Program Structure

The program consists of two main programs and a class :

1. `Server`: Acts as a phone book and connection hub for clients. The clients sign up or log in and can view all the other clients that the server has interracted with. Upon choosing a client to speak to, the server will send them the necessary details required to initiate a one on one connection with the client they intend to message. The server also allows the clients to change their status and password. 

2. `ClientAppication`: Allows computers to connect with the server using TCP as well as initiate one on one messaging with other clients using UDP. This program serves as the client's ability to use the server and send messages.

3. `ClientClass`: Encapsulates all the variables of a client as well as allows for the server to determine who is online and who is not.


## Notes

- This program was written on devices using Python 3.12, so please make sure you have Python 3.12 installed on your system to compile and run the program.

- This program requires Python3 at the bare minimum to run so please ensure that you have this installed.

- If quickly turning off and restarting the server, the server may produce `OSError: [Errno 48] Address already in use`
  To fix this, please choose a new port number for the variable <PORT> in the server class


## Credits

- Elijah Sherman (SHRELI006)
- Min Kim (KMXMIN010)
- Christopher Blignaut (BLGCHR003) 
