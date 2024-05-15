import pygame, sys, random
from network import Network
import threading
from player import Player
 
#Khoi tao
pygame.init()
clock=pygame.time.Clock()

#Cua so
screen_width = pygame.display.Info().current_w * 85 / 100
screen_height = pygame.display.Info().current_h * 85 / 100
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Ping Pong")

#Mau
bg_color = pygame.Color('black')
white = pygame.Color('white')
black = pygame.Color('black')
red = pygame.Color('red')

#Rect
ball_size = 20
bar_width = 10
bar_height = 100
bar_space = 60

ball = pygame.Rect(screen_width/2-ball_size/2,screen_height/2-ball_size/2,ball_size,ball_size)
player_right = pygame.Rect(screen_width-bar_space,screen_height/2-bar_height/2,bar_width,bar_height)
player_left = pygame.Rect(bar_space,screen_height/2-bar_height/2,bar_width,bar_height)

#Thong so trong game
menu = True
finding = False
game_start = False
game_over = False
ball_pause = True
speed_ball = 10
speed_ball_x = speed_ball * random.choice((-1,1))
speed_ball_y = speed_ball * random.choice((-1,1))
speed_player = 10
speed_player_right_y = 0
speed_player_left_y = 0

#Diem
game_font = pygame.font.Font("Striger.ttf",50)
score_left = 0
score_right = 0

def ball_mover():
    global speed_ball_x,speed_ball_y,score_left,score_right, ball_pause
    if not ball_pause:
        ball.x += speed_ball_x
        ball.y += speed_ball_y
                    
    if ball.top <= 0 or ball.bottom >= screen_height:
        speed_ball_y *= -1
    if ball.left <= 0:
        score_right += 1
        ball_reset()
    if ball.right >= screen_width:
        score_left += 1
        ball_reset()
    if ball.colliderect(player_left) or ball.colliderect(player_right):
        speed_ball_x *= -1

def player_right_mover():
    player_right.y += speed_player_right_y
    if player_right.top <= 0:
        player_right.top = 0
    if player_right.bottom >= screen_height:
        player_right.bottom = screen_height

def player_left_mover():
    player_left.y += speed_player_left_y
    if player_left.top <= 0:
        player_left.top = 0
    if player_left.bottom >= screen_height:
        player_left.bottom = screen_height

def bot_mover():
    if player_left.top < ball.y:
        player_left.top += speed_player*1.25
    if player_left.bottom > ball.y:
        player_left.top -= speed_player*1.25

    if player_left.top <= 0:
        player_left.top = 0
    if player_left.bottom >= screen_height:
        player_left.bottom = screen_height

def ball_reset():
    global speed_ball_x,speed_ball_y,speed_ball,ball_pause
    ball_pause = True
    ball.center = (screen_width/2,screen_height/2)
    speed_ball_x *= random.choice((-1,1))
    speed_ball_y *= random.choice((-1,1))
    
def match_reset():
    global score_left,score_right
    score_left = 0
    score_right = 0
    player_left.y = screen_height/2 - bar_height/2
    player_right.y = screen_height/2 - bar_height/2

def create_button(text,x,y,width,height):
    global red,white,black
    font = pygame.font.Font("Striger.ttf",50)
    button_text = font.render(text,True,white)
    button = pygame.Rect(x,y,width,height)
    a,b = pygame.mouse.get_pos()
    if button.x <= a <= button.x + width and button.y <= b <= button.y +height:
        pygame.draw.rect(screen,red,button)
    else:
        pygame.draw.rect(screen,black,button)
    screen.blit(button_text,(button.x+5,button.y+5))
    return button

def aftermatch(text):
    global screen,game_font
    run = True
    while run:
        screen.fill(bg_color)
        screen.blit(text,(screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
        btn_rematch = create_button('REMATCH',screen_width/2 - 90,screen_height/2 + 65,220,55)
        btn_mainmenu = create_button('CANCEL',screen_width/2 - 90,screen_height/2 + 120,175,55)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_mainmenu.collidepoint(event.pos):
                    run = False
                if btn_rematch.collidepoint(event.pos):
                    run = False
                    onlinematch()
        pygame.display.update()
    

def onlinematch():
    global screen,game_font
    run = True
    start = 6500
    try:
        n = Network()
        player = int(n.getP())
        p = n.send("player")
        print(f"you are player {player}")
        while run:
            clock.tick(60)
            game = n.send("get")
            screen.fill(bg_color)
            
            if not(game.connected()):
                font = pygame.font.SysFont("Striger.ttf", 80)
                text = font.render("Waiting for Player...", 1, (255,0,0), True)
                screen.blit(text, (screen_width/2 - text.get_width()/2, screen_height/2 - text.get_height()/2))
                btn_cancel = create_button('CANCEL',screen_width/2 - 90,screen_height/2 + 65,175,55)
                
                start-=1

                if start==0:
                    n.close()
                    run= False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if btn_cancel.collidepoint(event.pos):
                            n.close()
                            run = False
            else:
                pygame.draw.aaline(screen,red,(screen_width/2,0),(screen_width/2,screen_height))
                
                p.draw(screen)
                p.move(screen_height)

                o = n.send(p)
                o.draw(screen)

                b = n.send("ball")
                b.draw(screen)
                

                left_score = game_font.render(f"{game.wins[0]}",False,red)
                right_score = game_font.render(f"{game.wins[1]}",False,red)
                
                
                screen.blit(left_score,(screen_width/2 - 125,50))
                screen.blit(right_score,(screen_width/2 + 100,50))

                if game.checkwin():
                    if game.winner() == player:
                        text_aftermatch = game_font.render(f"YOU WIN!!!",False,red)
                    else:
                        text_aftermatch = game_font.render(f"YOU LOSE!!!",False,red)
                    aftermatch(text_aftermatch)
                    n.close()
                    break
                    


                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        n.close()
                        pygame.quit()
                        sys.exit()

            pygame.display.update()
        
    except:
        run = False
        print("Cannot connect to server")
    

while True:
    screen.fill(bg_color)
    #Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.MOUSEBUTTONDOWN and btn_quit.collidepoint(event.pos)):
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if menu:
                if btn_play.collidepoint(event.pos):
                    match_reset()
                    menu = False
                    game_start = True
                if btn_online.collidepoint(event.pos):
                    onlinematch()
            if game_over:
                if btn_replay.collidepoint(event.pos):
                    match_reset()
                    game_over = False
                    game_start = True
                if btn_menu.collidepoint(event.pos):
                    game_over = False
                    menu = True
            
        #Bam space de phat bong
        if event.type == pygame.KEYDOWN and game_start:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                ball_pause = False
        #nguoi choi phai
        if game_start:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    speed_player_right_y += speed_player
                if event.key == pygame.K_UP:
                    speed_player_right_y -= speed_player
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    speed_player_right_y -= speed_player
                if event.key == pygame.K_UP:
                    speed_player_right_y += speed_player
        #nguoi choi trai
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    speed_player_left_y += speed_player
                if event.key == pygame.K_w:
                    speed_player_left_y -= speed_player
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    speed_player_left_y -= speed_player
                if event.key == pygame.K_w:
                    speed_player_left_y += speed_player
        
    if menu:
        title_font = pygame.font.Font("Striger.ttf",50)
        text_title = game_font.render(f'PING PONG',False,red)
        screen.blit(text_title,(screen_width/2-110,200))

        btn_play = create_button('PLAY',screen_width/2 - 60,screen_height/2 - 55,120,55)
        btn_quit = create_button('QUIT',screen_width/2 - 55,screen_height/2 + 110, 105,55)
        btn_online = create_button('ONLINE',screen_width/2 - 80,screen_height/2 + 25 ,160 , 55)
    
    

    if game_start:
        ball_mover()
        player_right_mover()
        player_left_mover()
    
        #Draw
        pygame.draw.rect(screen,red,player_left)
        pygame.draw.rect(screen,red,player_right)
        pygame.draw.ellipse(screen,red,ball)
        pygame.draw.aaline(screen,red,(screen_width/2,0),(screen_width/2,screen_height))

        left_score_text = game_font.render(f"{score_left}",False,red)
        right_score_text = game_font.render(f"{score_right}",False,red)
        screen.blit(left_score_text,(screen_width/2 - 125,50))
        screen.blit(right_score_text,(screen_width/2 + 100,50))

        if score_left >= 10 or score_right >= 10:
            game_start = False
            game_over = True
    
    if game_over:
        left_score_text = game_font.render(f"{score_left}",False,red)
        right_score_text = game_font.render(f"{score_right}",False,red)
        left_win_text = game_font.render(f"PLAYER 1 WON",False,red)
        right_win_text = game_font.render(f"PLAYER 2 WON",False,red)
        screen.blit(left_score_text,(screen_width/2 - 125,50))
        screen.blit(right_score_text,(screen_width/2 + 100,50))
        if score_left > score_right:
            screen.blit(left_win_text,(screen_width/2 - 140,screen_height/2-150))
        else:
            screen.blit(right_win_text,(screen_width/2 - 140,screen_height/2-150))
        btn_replay = create_button('REPLAY',screen_width/2 - 80,screen_height/2,170,55)
        btn_menu = create_button('MAIN MENU',screen_width/2 - 115,screen_height/2+100,245,55)

    pygame.display.flip()
    clock.tick(60)


