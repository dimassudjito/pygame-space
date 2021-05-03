"""
Pygame first game
"""

import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Background sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Player
playerImg = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0,740))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
# "ready": invisible, "fire": in motion
bullet_state = "ready"

# Score display
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32,)
textX = 10
textY = 10

# Game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_score(x, y):
    score = font.render(str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def player(x, y):
    # Blit = Draw
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    # Blit = Draw
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # 16 and 10 is to centralized the bullet w.r.t the spaceship
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    # Use pythagoras to determine distance
    distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
    return distance < 27


# Game loop: anything continous in the game
running = True
while running:
    # Background color (RGB)
    screen.fill((0, 0, 0))

    # Background image
    screen.blit(background, (0,0))

    # Checking every event in the program
    for event in pygame.event.get():
        # Checking if window is closed
        if event.type == pygame.QUIT:
            running = False
        # Check if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            # Moving player left and right
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            # Iniating bullet
            if event.key == pygame.K_SPACE:
                # Checking if bullet is still firing
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    # Saving initial position of the spaceship
                    bulletX = playerX
                    # Iniatiate bullet
                    fire_bullet(playerX, bulletY)
        
        # Check if keystroke is released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
        

    # Changing the position of player
    playerX += playerX_change
    # Boundary
    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736
    
    # Changing the position of enemy
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 200:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        # Boundary
        if enemyX[i] <= 0:
            enemyX_change[i] = 1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1
            enemyY[i] += enemyY_change[i]
        
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            # Reset the bullet
            bulletY = 480
            bullet_state = "ready"
            # Reset the enemy
            enemyX[i] = random.randint(0,740)
            enemyY[i]= random.randint(50,150)
            # Print score
            score_value += 1
        
        # Drawing the enemy
        enemy(enemyX[i], enemyY[i], i)
    
    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    # Initating bullet movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    

    # Drawing the surface
    player(playerX, playerY)
    show_score(textX, textY)

    # Update the surface
    pygame.display.update()
    
