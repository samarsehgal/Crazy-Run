import pygame, random
from pygame.locals import *

WIDTH,HEIGHT=800,800
NUM_PLAYERS=2
PLAYER_WIDTH,PLAYER_HEIGHT=30,30
JUMP_COUNT=200

font = "QUIGLEYW.ttf"
white=(255,255,255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)

clock=pygame.time.Clock()


def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
 
    return newText

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super(Player,self).__init__()
        self.jumpcount=JUMP_COUNT
        self.is_jumping=False
        self.is_falling=False
        self.surf=pygame.Surface((PLAYER_WIDTH,PLAYER_HEIGHT))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()
        self.rect.y=HEIGHT-HEIGHT/4
        

    def jump(self):
        if self.is_jumping is False and self.is_falling is False:
            self.is_jumping=True

    def update(self):
        if self.is_jumping is True:
            if self.jumpcount<=0:
                self.is_falling=True
                self.is_jumping=False
            
            self.rect.move_ip(-5,0)
            self.jumpcount=self.jumpcount-5
            
        if self.is_falling is True:
            if self.jumpcount>=JUMP_COUNT:
                self.is_falling=False
            
            self.rect.move_ip(5,0)
            self.jumpcount=self.jumpcount+5

class Left(Player):
    def __init__(self):
        super(Left,self).__init__()
        self.rect.x=WIDTH-PLAYER_WIDTH-WIDTH/NUM_PLAYERS
            
class Right(Player):
    def __init__(self):
        super(Right,self).__init__()
        self.rect.x=WIDTH-PLAYER_WIDTH

class Middle(Player):
    def __init__(self):
        super(Middle,self).__init__()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy,self).__init__()
        self.enemy_width=random.randint(30,90)
        self.enemy_height=random.randint(30,60)
        self.surf=pygame.Surface((self.enemy_width,self.enemy_height))
        self.surf.fill((255,255,255))
        self.rect=self.surf.get_rect()
        self.rect.x=WIDTH-self.enemy_width
        self.rect.y=0
        self.speed=random.randint(3,9)

    def update(self):
        self.rect.move_ip(0,self.speed)
        if(self.rect.y==HEIGHT-30):
            self.kill()

class Left_Enemy(Enemy):
    def __init__(self):
        super(Left_Enemy,self).__init__()
        self.rect.x=WIDTH-self.enemy_width-WIDTH/NUM_PLAYERS

pygame.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))

def menu():
    selected="start"
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        twoPGame()
                    if selected=="quit":
                        pygame.quit()
                        quit()
 
        # Main Menu UI
        screen.fill((0,0,0))
        title=text_format("Crazy Run",font, 90, yellow)
        # title="Crazy Run"

        if selected=="start":
            text_start=text_format("START",font,  75, white)
            # text_start="Start"

        else:
            text_start = text_format("START",font,  75, black)
            # text_start = "Start"

        if selected=="quit":
            text_quit = text_format("QUIT",font,  75, white)
            # text_quit="Quit"
        else:
            text_quit = text_format("QUIT",font,  75, black)
            # text_quit="Quit"

 
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
 
        # Main Menu Text
        screen.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 300))
        screen.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(120)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")


def twoPGame():
    ADD_ENEMY=pygame.USEREVENT+1
    pygame.time.set_timer(ADD_ENEMY,2000)
    player=Right()
    player2=Left()
    enemies=pygame.sprite.Group()
    all_sprites=pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(player2)
    running=True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key==K_ESCAPE:
                    running=False

            elif event.type==QUIT:
                running=False

            elif event.type==ADD_ENEMY:
                left_enemy=Left_Enemy()
                right_enemy=Enemy()
                enemies.add(left_enemy)
                enemies.add(right_enemy)
                all_sprites.add(left_enemy)
                all_sprites.add(right_enemy)
        clock.tick(120)
        pressed_keys=pygame.key.get_pressed()
        
        if pressed_keys[K_RIGHT]:
            player.jump()
        if pressed_keys[K_LEFT]:
            player2.jump()
        player.update()
        player2.update()
        enemies.update()
        screen.fill((0,0,0))
        pygame.draw.line(screen,(255,255,255),(WIDTH/2,0),(WIDTH/2,HEIGHT))
        for entity in all_sprites:
            screen.blit(entity.surf,entity.rect)

        if pygame.sprite.spritecollideany(player,enemies):
            player.kill()
            running=False
        if pygame.sprite.spritecollideany(player2,enemies):
            player2.kill()
            running=False    

        pygame.display.flip()

menu()
