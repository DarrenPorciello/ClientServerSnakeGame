import numpy as np
import socket
from _thread import *
import pickle
from snake import SnakeGame
import uuid
import time
import math
import random
import json
import rsa



server = "localhost"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Generate key pair
#server_public_key, server_private_key = generate_keypair(8)

counter = 0
rows = 20

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for connections, Server Started")

game = SnakeGame(rows)
game_state = ""
last_move_timestamp = time.time()
interval = 0.2
moves_queue = set()

rgb_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 165, 0),
}
rgb_colors_list = list(rgb_colors.values())

def broadcast(message):
    for client in clients:
        client.send(message.encode())

def game_thread():
    global game, moves_queue, game_state, last_move_timestamp
    while True:
        last_move_timestamp = time.time()
        game.move(moves_queue)
        moves_queue = set()
        game_state = game.get_state()
        while time.time() - last_move_timestamp < interval:
            time.sleep(0.1)


def client_thread(conn, addr):
    global game, moves_queue, game_state
    unique_id = str(uuid.uuid4())
    color = rgb_colors_list[np.random.randint(0, len(rgb_colors_list))]
    game.add_player(unique_id, color=color)

    start_new_thread(game_thread, ())

    while True:
        #Need to tell nto to decode ahead of time

        data = conn.recv(500).decode()
        #print(data)
        conn.send(game_state.encode())

        move = None
        if not data:
            print("No data received from client")
            break
        elif data == "get":
            #print("Received get")
            pass
        elif data == "quit":
            print("Received quit")
            game.remove_player(unique_id)
            break
        elif data == "reset":
            game.reset_player(unique_id)
        elif data in ["up", "down", "left", "right"]:
            move = data
            moves_queue.add((unique_id, move))

        elif 'Control' in data:
            #print("control received")
            data2 = conn.recv(500)
            messagetosend = rsa.decrypt(data2, private_key)
            #broadcast(decrypteddata)
            #print(messagetosend.decode())
            checker = messagetosend.decode()
            if "Congr" in checker:
                print("hi")
                #messagetosend = rsa.decrypt(data2, private_key)
                #print(messagetosend)
                broadcast(checker)
            elif "works" in checker:
                #messagetosend = rsa.decrypt(data2, private_key)
                #print(messagetosend)
                broadcast(checker)
            elif "Ready" in checker:
                #messagetosend = rsa.decrypt(data2, private_key)
                #print(messagetosend)
                broadcast(checker)
        
        else:
            print("Invalid data received from client:", data)

        
            

    conn.close()


if __name__ == "__main__":
    clients = []
    client_public_keys = []
    public_key, private_key = rsa.newkeys(1024)
    #print("PrivateKey: ", private_key)
    #print("PublicKey: ", public_key)
    
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        
        public_partner = False
        #clientPublicKey = conn.recv(500).decode()
        #print(clientPublicKey)
        clientPublicKey = conn.recv(500).decode()
        #print("RECEIVED CLIENT PUBLIC KEY", clientPublicKey)

        # Convert the string back to a tuple
        #restored_tuple = json.loads(data)
        client_public_keys.append(clientPublicKey)
        
        #Send the client the servers public key
        #tuple_as_string = json.dumps(server_public_key) 
        conn.send(public_key.save_pkcs1("PEM"))
        
        #print("Connected to:", addr)
        start_new_thread(client_thread, (conn, addr))
