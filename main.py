import pygame
import math
import time
import os
import platform
import random
from PIL import Image


# init pygame
pygame.init()

# not required, called by pygame.init()
#pygame.display.init()

print(pygame.display.get_init())
print(pygame.display.get_driver())
full_screen_modes = pygame.display.list_modes()

#print(full_screen_modes)
index_mode = 0

while index_mode <= len(full_screen_modes) - 1:
    print(index_mode,"-", full_screen_modes[index_mode])
    index_mode += 1

# game window
# x axis => left to right
# y axis => top to bottom
# always start 0:0 (top left corner)
screen_width  = 800
screen_height = 600

# colors
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLACK = (0, 11, 0)

screen = pygame.display.set_mode(size=(screen_width, screen_height))#, flags=pygame.FULLSCREEN)
#pygame.draw.circle(screen, GREEN, [60, 250], 40)

# music in background
load_music = pygame.mixer.music.load('music/bdub.mp3')
pygame.mixer.music.play(-1)

# read image pixels
im = Image.open('rocket/rocket.png') # Can be many different formats.
pix = im.load()
rocket_pixel = im.size[1]

# set game border
rocket_pixel = 64
left_border = screen_width - rocket_pixel
right_border  = 0

background = pygame.image.load('background/galaxy.jpg')

# screen title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icons/rocket.png')
pygame.display.set_icon(icon)

score = 0

#
##
#### player
##
#
player_img = pygame.image.load('rocket/rocket.png')
player_x = (screen_width / 2 ) - 1
player_y = 518
player_x_change = 0


#
##
### enemy
##
#
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy/enemy.png'))
    enemy_pixel = 64
    enemy_x.append(random.randint(0, (799 - enemy_pixel)))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(0.3)
    enemy_y_change.append(40)

#
##
### enemy1
##
#
enemy1_img = pygame.image.load('enemy/enemy.png')
enemy1_pixel = 64
enemy1_x = random.randint(0, (799 - enemy1_pixel))
enemy1_y = random.randint(50, 150)
enemy1_x_change = 0.3
enemy1_y_change = 40

#
##
### bullet
##
#
bullet_img = pygame.image.load('bullet/bullet32.png')
bullet_pixel = 32
bullet_x = 0
bullet_y = 518
bullet_x_change = 0
bullet_y_change = 0.5
bullet_state = "ready"

#
##
### functions
##
#
def player(x, y):
    # blit = draw image of player|rocket
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    # blit = draw image of player|rocket
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))

def bullet(x, y):
    # blit = draw image of player|rocket
    screen.blit(bullet_img, (x, y))

def isCollision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y-bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False

#
##
### Game Loop
##
#
running = True
while running:

    #screen.fill((BLACK))

    screen.blit(background, (0, 0))

    # load music
    load_music
    

    #player_y -= 1
    #print(player_y)

    #if player_y == 0:
    #    running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            print("Quit was pressed")

        #else:
        #    print(event)

        # if keystroke is pressed check whether is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3
                print(player_x)
            if event.key == pygame.K_LEFT:
                player_x_change = -0.3
                print(player_x)
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    # Get the current x cordinate of the spaceship
                    bullet_x = player_x
                    fire_bullet(player_x, bullet_y)      
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_SPACE:
                player_x_change = 0
            
    
    # everything what needs to be persistent in game, background, etc...
    
    # call it after display update because screen is loaded first!!!
    player_x += player_x_change

    # checking for boundaries of spaceship so id doesn't go out of bounds
    if player_x <= right_border:
        player_x = right_border
    elif player_x >= left_border:
        player_x = left_border

    # 
    for i in range(num_of_enemies):
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= right_border:
            enemy_x_change[i] = 0.2
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= left_border:
            enemy_x_change[i] = -0.2
            enemy_y[i] += enemy_y_change[i]
        
        # Collision
        collision = isCollision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            print(score)
            enemy_pixel = 64
            enemy_x[i] = random.randint(0, (799 - enemy_pixel))
            enemy_y[i] = random.randint(50, 150)
        
        enemy(enemy_x[i], enemy_y[i], i)
    
    # bullet movement
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
    
    if bullet_y <= -1:
        bullet_y = 540
        bullet_state = "ready"
    

    player(player_x, player_y)
    
    #enemy1(enemy1_x, enemy1_y)
    # update screen game when score changing, bullets and etc...
    pygame.display.update()
    