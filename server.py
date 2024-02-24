import socket
import threading


IP = socket.gethostbyname(socket.gethostname())
PORT = 6969
ADDR = (IP, PORT)
DISCONNECT_MSG = "!DISCONNECT"

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(1024).decode()
        if msg == DISCONNECT_MSG:
            connected = False

        print(f"[{addr}] {msg}")
        # msg = f"Msg received: {msg}"
        
        conn.send(msg.encode)

    conn.close()


def sign_in():
    username = input("USERNAME: ")
    password = input("PASSWORD: ")

    # look up username in the user file
    # check whehter it is correct password
    # if correct, sign in
    # else, ask for password again
    #       after 3 tries, cancel


def sign_up():
    username = input("USERNAME: ")
    password = input("PASSWORD: ")



def main():
    print("[STARTING] Server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server is listening on {IP}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

if __name__ == "__main__":
    main()
