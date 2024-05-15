import pygame

class Player():
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 100
        self.color = color
        self.rect = (x,y,self.width,self.height)
        self.speed = 700 * pygame.time.Clock().tick(60)/1000.0

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,self.rect)

    def move(self,screen):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.speed
        
        if keys[pygame.K_s]:
            self.y += self.speed
        
        self.limitscreen(screen)
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

    def limitscreen(self,screen):
        if self.y <=0:
            self.y = 0
        if self.y + self.height >= screen:
            self.y = screen - self.height