from player import Player
from ball import Ball
import pygame,random

class Game:
    def __init__(self, id):
        self.ready = False
        self.id = id
        self.wins = [0,0]
        self.screen_width = 1161.1
        self.screen_height = 652.8
        self.players = [Player(60,self.screen_height/2 - 50,pygame.Color('red')),Player(self.screen_width-60,self.screen_height/2 - 50,pygame.Color('red'))]
        self.ball = Ball(self.screen_width/2 - 10,self.screen_height/2 -10,pygame.Color('red'),random.choice((-1,1)),random.choice((-1,1)))
        
    def connected(self):
        return self.ready
    
    def checkwin(self):
        if self.wins[0] == 10 or self.wins[1] == 10:
            return True
        return False

    def winner(self):
        if self.wins[0] == 10:
            return 0
        else:
            return 1