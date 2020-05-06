import random
import math
import pygame
from pygame import mixer

# Initialising the game
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# Background Image
backgroundImg = pygame.image.load("background1.png")

# Title and Icon
display = pygame.display.set_caption("Space Invader By Suman")

# Player
playerImg = pygame.image.load("shuttle.png")
playerX_cord = 370
playerY_cord = 480
playerx_change = 0

# Enemy
# For Multiple Enemies
enemyImg = []
enemy_X_cord = []
enemy_Y_cord = []
enemy_x_change = [4]
enemy_y_change = [40]
num_of_enemies = 6

# Enemies Loop
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("invader.png"))
    enemy_X_cord.append(random.randint(0, 734))
    enemy_Y_cord.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# UFO
ufoImg = pygame.image.load("ufo.png")
ufoY = 150
ufoX = 0
ufoX_change = 10
ufoY_change = 4


# Bullet

# ready: bullet cant be seen
# fire: bullet is moving
bulletImg = pygame.image.load("bullet.png")
bullet_X_cord = 0
bullet_Y_cord = 480
bullet_x_change = 0
bullet_y_change = 12
bullet_state = "ready"

# Collision Image
CollisionImg = pygame.image.load("blast.png")

# Font
# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game Over Text
over_font = pygame.font.Font("freesansbold.ttf", 64)
over_font_xcord = 400
over_font_ycord = 300

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 2,55))
    screen.blit(score, (textX, textY))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def show_high_score():
    high_score_text = high_score_font.render("HIGH SCORE:" + str(high_score_value), True, (255, 255, 255))
    screen.blit(high_score_text, (450, 10))
def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def ufo(x, y):
    screen.blit(ufoImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def is_collision(enemy_X_cord, enemy_Y_cord, bullet_X_cord, bullet_Y_cord ):
    distance = math.sqrt(math.pow(enemy_X_cord - bullet_X_cord, 2) + (math.pow(enemy_Y_cord - bullet_Y_cord, 2)))
    if distance < 27:
        screen.blit(CollisionImg, (enemy_X_cord, enemy_Y_cord))
        return True
    else:
        return False

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    # Creating Background
    screen.blit(backgroundImg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -7
            if event.key == pygame.K_RIGHT:
                playerx_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_X_cord = playerX_cord
                    fire_bullet(bullet_X_cord, bullet_Y_cord)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
    # Player
    playerX_cord += playerx_change
    player(playerX_cord, playerY_cord)

    #UFO
    ufoX += ufoX_change
    ufoY += ufoY_change
    ufo(ufoX, ufoY)

    # Player Border Checking
    if playerX_cord >= 736:
        playerX_cord = 736
    elif playerX_cord <= 0:
        playerX_cord = 0

    # Enemy Border Checking and Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemy_Y_cord[i] > 440:
            for j in range(num_of_enemies):
                enemy_Y_cord[j] = 3000
                bullet_state = "ready"
            game_over_text()
            break

        enemy_X_cord[i] += enemy_x_change[i]
        if enemy_X_cord[i] >= 736:
            enemy_x_change[i] = -6
            enemy_Y_cord[i] += enemy_y_change[i]
        elif enemy_X_cord[i] <= 0:
            enemy_x_change[i] = 6
            enemy_Y_cord[i] += enemy_y_change[i]
            # Collison
        collision = is_collision(enemy_X_cord[i], enemy_Y_cord[i], bullet_X_cord, bullet_Y_cord)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bullet_Y_cord = 480
            bullet_state = "ready"
            score_value += 10
            enemy_X_cord[i] = random.randint(0, 734)
            enemy_Y_cord[i] = random.randint(50, 150)

        enemy(enemy_X_cord[i], enemy_Y_cord[i], i)

        # Bullet Movement
    if bullet_Y_cord <= 0:
        bullet_Y_cord = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_X_cord, bullet_Y_cord)
        bullet_Y_cord -= bullet_y_change

    if ufoX > 1200:
        ufoX = 0
    if ufoY > 1200:
         ufoY = 0



    show_score(textX, textY)
    player(playerX_cord, playerY_cord)
    pygame.display.update()
