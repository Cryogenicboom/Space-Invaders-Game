import pygame
import random
import math

from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background.png')

mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerimg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullets (infinite)
bulletimg = pygame.image.load('bullet.png')
bullets = []  # Each bullet is a dict: {'x': ..., 'y': ...}
bulletY_change = 1

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def showscore(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerimg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))

def fire_bullet(x, y):
    screen.blit(bulletimg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    xdiff = enemyX - bulletX
    ydiff = enemyY - bulletY
    distance = math.sqrt((math.pow(xdiff, 2)) + (math.pow(ydiff, 2)))
    return distance < 27

running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                # Add a new bullet at the player's position
                bullets.append({'x': playerX, 'y': playerY})

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement and collision
    for i in range(num_of_enemy):
        if enemyY[i] > 480:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text(200, 250)
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Check collision with all bullets
        for bullet in bullets:
            if isCollision(enemyX[i], enemyY[i], bullet['x'], bullet['y']):
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
                bullet['y'] = -1000  # Move bullet off screen

        enemy(enemyX[i], enemyY[i], i)

    # Move and draw all bullets
    for bullet in bullets:
        if bullet['y'] > 0:
            fire_bullet(bullet['x'], bullet['y'])
            bullet['y'] -= bulletY_change

    # Remove bullets that are off screen
    bullets = [b for b in bullets if b['y'] > 0]

    player(playerX, playerY)
    showscore(textX, textY)
    pygame.display.update()
