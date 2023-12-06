import numpy as np
import socket
from _thread import *
import pickle
from snake import SnakeGame
import uuid
import time

server = "localhost"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        data = conn.recv(500).decode()
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
        elif "Congratulations" in data:
            broadcast(data)
        elif "works" in data:
            broadcast(data)
        elif "Ready" in data:
            broadcast(data)
        else:
            print("Invalid data received from client:", data)

    conn.close()


if __name__ == "__main__":
    clients = []
    while True:
        conn, addr = s.accept()
        clients.append(conn)
        print("Connected to:", addr)
        start_new_thread(client_thread, (conn, addr))
