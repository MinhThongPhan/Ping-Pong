import pygame,random

class Ball():
    def __init__(self,x,y,color,speed_x,speed_y):
        self.start_x = x
        self.start_y = y
        self.speed = 210 * pygame.time.Clock().tick(60)/1000.0
        self.x = x
        self.speed_x = speed_x * self.speed
        self.y = y
        self.speed_y = speed_y * self.speed
        self.color = color
        self.size = 20
        self.rect = (x,y,self.size,self.size)

    def draw(self,screen):
        pygame.draw.ellipse(screen,self.color,self.rect)

    def move(self,screen_width,screen_height,player_left,player_rigth,wins):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.y <=0 or self.y + self.size >= screen_height:
            self.speed_y *= -1
        if pygame.Rect(self.x,self.y,self.size,self.size).colliderect(player_left) or pygame.Rect(self.x,self.y,self.size,self.size).colliderect(player_rigth):
            self.speed_x *= -1
        
        if self.x <= 0:
            wins[1] +=1
            self.reset()
        if self.x + self.size >= screen_width:
            wins[0] +=1
            self.reset()

        self.update()

    def update(self):
        self.rect = (self.x,self.y,self.size,self.size)
    
    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.speed_x *= random.choice((-1,1))
        self.speed_y *= random.choice((-1,1))