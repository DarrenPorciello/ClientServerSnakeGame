import socket
import threading
import rsa

choice = input("Do you want to host (1) or connect (2)")
servera = "localhost"
port = 5551
if (choice == "1"):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((servera, port))
    server.listen()

    client, _ = server.accept()

elif choice == "2":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((servera, port))

else:
    exit()

def sending_messages(c):
    while True:
        message = input("")
        c.send(message.encode())
        print("You "+ message)

def receiving_messages(c):
    while True:   
        print("Partner: " + c.recv(1024).decode())

threading.Thread(target=sending_messages, args=(client,))
threading.Thread(target=receiving_messages, args=(client,))