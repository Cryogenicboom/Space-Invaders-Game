# distance formula: D = sqroot([x2-x1]^2 + [y2-y1]^2)

import pygame
import random
import math

# music class 
from pygame import mixer

# initilize pygame 
pygame.init()

# create a screen and store its parameters in var (width (xaxis), height(yaxis))
# origin of screen is at "top left corner" [4th quadrant]
screen = pygame.display.set_mode((800, 600))

# background image 
background = pygame.image.load('background.png')

# background_sound 
mixer.music.load('background.wav')
# to keep playing music on loop, use -1
mixer.music.play(-1)


# window title
pygame.display.set_caption("Space Invaders")

# save image in a var and use that image as our window's logo
# ICONS AND CAPTIONS 
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 480
# moving player 
playerX_change = 0

# enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):

    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40)

# bullet, fire- bullet is moving, ready - at rest
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480  #same as spaceship
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# score 
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX =10
textY =10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def showscore(x,y):
    score = font.render("Score: "+ str(score_value), True, (255, 255, 255))
    screen.blit(score, (x,y))

def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200,250))

def player(x,y):
    # blit: draws image on window, with taking x-y coodn
    screen.blit(playerimg, (x, y))

def enemy(x,y, i):
    screen.blit(enemyimg[i] , (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    xdiff = enemyX-bulletX
    ydiff = enemyY-bulletY
    distance = math.sqrt((math.pow(xdiff, 2)) + (math.pow(ydiff, 2)))

    if distance < 27:
        return True
    else:
        return False

# event: any activity that happens inside our window 
running = True

# when running == false, that means "X" is being pressed and user quits program
while running:
    # changing background (R,G,B)
    screen.fill((0,0,0))

    # background image 
    screen.blit(background, (0,0))

    # windows remain running until player presses exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # check whether key pressed or not, if pressed then which right or left
        # KEYDOWN : pressing key, KEYUP : releasing key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("left key pressed")
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                # print("right key pressed")
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # storing player's coodn as bullet starting point in a variable, we didnt used player's location directly to avoid bullet following player after it is released
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("keyhas been released")
                playerX_change = 0

    playerX += playerX_change

    # if player crosses boundary 
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736 

    # enemy movement
    for i in range(num_of_enemy):

        #  how much close enemy should get
        if enemyY[i] > 480:
            for j in range(num_of_enemy):
                # after game over enemies goes out of window
                enemyY[j] = 2000
            game_over_text(200, 250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.2
            # when enemy hit edges it comes down
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2 
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i] , enemyY[i] , bulletX, bulletY)
        if collision:

            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()

            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i]  = random.randint(0,735)
            enemyY[i]  = random.randint(50,150)
        
        enemy(enemyX[i] , enemyY[i] , i)
    
    # bullet movement 
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    

    # calling player 
    player(playerX, playerY) 
    # enemy(enemyX, enemyY)
    showscore(textX, textY)

    # now we have changed the background color, but we need to update it 
    pygame.display.update()
 