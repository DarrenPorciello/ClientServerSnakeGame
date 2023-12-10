import numpy as np
import pygame 
from network import Network
import time
import random
import math
import pickle
import json
import rsa


playerID = random.randint(1, 100000)

width = 500
height = 500
rows = 20 



rgb_colors = {
    "red" : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue" : (0, 0, 255),
    "yellow" : (255, 255, 0),
    "orange" : (255, 165, 0),
} 
rgb_colors_list = list(rgb_colors.values())

def drawGrid(w, surface):
    global rows
    sizeBtwn = w // rows

    x = 0
    y = 0
    for l in range(rows):
        x = x + sizeBtwn
        y = y +sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x, 0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0, y),(w,y))

def drawThings(surface, positions, color = None, eye = False):
    global width, rgb_colors_list
    dis = width // rows
    if color is None : 
        color = (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255))
    for pos_id, pos in enumerate(positions):
        i, j = pos

        pygame.draw.rect(surface, color , (i*dis+1,j*dis+1,dis-2,dis-2))
        if eye and pos_id == 0:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)

def draw(surface, players, snacks):
    global rgb_colors_list

    surface.fill((0,0,0))
    drawGrid(width, surface)
    for i, player in enumerate(players) : 
        color = rgb_colors_list[i % len(rgb_colors_list)]
        drawThings(surface, player, color = color, eye = True) 
    drawThings(surface, snacks, (0, 255, 0))
    pygame.display.update()


def main():
    
    win = pygame.display.set_mode((width,height))
    
    n = Network()
    #Send key to server

    # Generate key pair
    public_key, private_key = rsa.newkeys(1024)
    public_partner = False
    #print(public_key, private_key)
    #tuple_as_string = json.dumps(public_key) 

    #Send public key
    n.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(n.recv())
    print("Public partner",public_partner)
    

    #Handle recieved ServerKey

    # Convert the string back to a tuple
    #restored_tuple = json.loads(tuple_as_string)
    #print(restored_tuple)
    
    
    flag = True
    
    #Send the client public key to the server
    #n.send()
    
    while flag:
        
        events = pygame.event.get()
        pos = None 
        chat = None
        ignore = False
        if len(events) > 0 :
            
            for event in events : 
                if event.type == pygame.QUIT:
                    flag = False
                    pos = n.send("quit", receive=True) 
                    pygame.quit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pos = n.send("left", receive = True)
                    elif event.key == pygame.K_RIGHT:
                        pos = n.send("right", receive = True)
                    elif event.key == pygame.K_UP:
                        pos = n.send("up", receive = True)
                    elif event.key == pygame.K_DOWN:
                        pos = n.send("down", receive = True)
                    elif event.key == pygame.K_SPACE:
                        pos = n.send("reset", receive = True)
                    #Send messages
                    elif event.key == pygame.K_z:
                        #Alert server encrypted message is coming
                        n.send('Control')

                        chatMessage = f"Player {playerID}: Congratulations"
                        n.send(rsa.encrypt(chatMessage.encode(), public_partner))
                        #print(rsa.encrypt(chatMessage.encode(), public_partner))
                        #print(chatMessage)
                        #ignore = True

                    elif event.key == pygame.K_x:
                        n.send('Control')
                        chatMessage = f"Player {playerID}: It works!"
                        n.send(rsa.encrypt(chatMessage.encode(), public_partner))
                        #print(chatMessage)
                        #ignore = True

                    elif event.key == pygame.K_c:
                        n.send('Control')
                        chatMessage = f"Player {playerID}: Ready?"
                        n.send(rsa.encrypt(chatMessage.encode(), public_partner))
                        #print(chatMessage)
                        #ignore = True

                    
                        
                        
        else:
            if ignore == False:
                pos = n.send("get", receive = True)
        

            
        snacks, players = [], []
        
        if pos is not None and "|" in pos: 
            #print(pos)
            raw_players = pos.split("|")[0].split("**")
            raw_snacks = pos.split("|")[1].split("**")

            if raw_players == '' : 
                pass 
            else : 
                for raw_player in raw_players :
                    raw_positions = raw_player.split("*")
                    if len(raw_positions) == 0 :
                        continue
                    
                    positions = []
                    for raw_position in raw_positions :
                        if raw_position == "" :
                            continue
                        nums = raw_position.split(')')[0].split('(')[1].split(',')
                        positions.append((int(nums[0]), int(nums[1])))
                    players.append(positions)


            if len(raw_snacks) == 0 :
                continue

            for i in range(len(raw_snacks)) :
                nums = raw_snacks[i].split(')')[0].split('(')[1].split(',')
                snacks.append((int(nums[0]), int(nums[1])))

        else:
            if pos is not None:
                print(pos)
            

        draw(win, players, snacks)
    

if __name__ == "__main__":
    main()