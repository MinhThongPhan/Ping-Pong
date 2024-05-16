import socket,pygame,random
from _thread import *
import pickle
from game import Game
from player import Player
from ball import Ball

server = "0.0.0.0"
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))
    
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if data == "player":
                        if p == 0:
                            reply = games[gameId].players[0]
                        elif p == 1:
                            reply = games[gameId].players[1]
                        conn.sendall(pickle.dumps(reply))
                    elif data == "get" :
                        conn.sendall(pickle.dumps(game))
                    elif data == "ball":
                        conn.sendall(pickle.dumps(games[gameId].ball))
                        games[gameId].ball.move(games[gameId].screen_width,games[gameId].screen_height,games[gameId].players[0],games[gameId].players[1],games[gameId].wins)
                    else:
                        games[gameId].players[p] = data
                        if p == 0:
                            reply = games[gameId].players[1]
                        elif p == 1:
                            reply = games[gameId].players[0]
                        conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    
    print("Lost connection")    
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr= s.accept()
    print("Connected to: ",addr)
    idCount+=1
    p =0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("creating new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client,(conn, p ,gameId))