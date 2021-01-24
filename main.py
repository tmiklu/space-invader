import pygame
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

#while index_mode <= len(full_screen_modes):
#    print(index_mode,"-", full_screen_modes[index_mode])
#    index_mode += 1

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
#pygame.mixer.music.play(-1)

# read image pixels
im = Image.open('rocket/rocket.png') # Can be many different formats.
pix = im.load()
rocket_pixel = im.size[1]

# set game border
rocket_pixel = 64
left_border = screen_width - rocket_pixel
right_border  = 0

# screen title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('icons/rocket.png')
pygame.display.set_icon(icon)

#
##
#### player
##
#
player_img = pygame.image.load('rocket/rocket.png')
player_x = (screen_width / 2 ) - 1
player_y = 518
player_x_change = 0

def player(x, y):
    # blit = draw image of player|rocket
    screen.blit(player_img, (x, y))

#
##
### enemy
##
#
enemy_img = pygame.image.load('enemy/alien.png')
enemy_pixel = 64
enemy_x = random.randint(0, (799 - enemy_pixel))
enemy_y = random.randint(50, 150)
enemy_x_change = 0.3
enemy_y_change = 40

def enemy(x, y):
    # blit = draw image of player|rocket
    screen.blit(enemy_img, (x, y))


# Game Loop
running = True
while running:

    screen.fill((BLACK))

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

        else:
            print(event)

        # if keystroke is pressed check whether is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_x_change = 0.3
                print(player_x)
            if event.key == pygame.K_LEFT:
                    player_x_change = -0.3
                    print(player_x)        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
            
    
    # everything what needs to be persistent in game, background, etc...
    
    # call it after display update because screen is loaded first!!!
    player_x += player_x_change

    # checking for boundaries of spaceship so id doesn't go out of bounds
    if player_x <= right_border:
        player_x = right_border
    elif player_x >= left_border:
        player_x = left_border

    enemy_x += enemy_x_change

    # program border
    if enemy_x <= right_border:
        enemy_x_change = 0.2
        enemy_y += enemy_y_change
    elif enemy_x >= left_border:
        enemy_x_change = -0.2
        enemy_y += enemy_y_change

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    # update screen game when score changing, bullets and etc...
    pygame.display.update()
    