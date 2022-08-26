from random import random
import pygame
import pygame_menu
import numpy as np
from Player import Player
from Enemy import Enemy
from consts import *
from common import *
from spritesheet import SpriteSheet


def check_collisions(player, enemies):
    for enemy in enemies:
        if pygame.sprite.collide_rect(player, enemy):
            return enemy
    return None


# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def set_difficulty(value, difficulty):
    global y_movement
    if difficulty == 2:
        y_movement = True
    else:
        y_movement = False


def set_char(value, char):
    global char_idx
    char_idx = char


# Variable to keep the main loop running
running = True


def start_the_game():
    menu.disable()


# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

pygame.init()

menu = pygame_menu.Menu('The CGPA', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

# menu.add.text_input('Name :', default='John Doe')
menu.add.button('Play', start_the_game)
menu.add.selector(
    'Difficulty :', [('Easy', 1), ('Hard', 2)], onchange=set_difficulty)
menu.add.selector(
    'Character :', [('Uday', 0), ('Yagneek', 1)], onchange=set_char)
menu.add.button('Quit', pygame_menu.events.EXIT)

ok_sound = pygame.mixer.Sound("sounds/ok.wav")
dash_sound = pygame.mixer.Sound("sounds/dash.wav")
shoot_sound = pygame.mixer.Sound("sounds/book.wav")
slowed_sound = pygame.mixer.Sound("sounds/zaworld.wav")
# uday_pic = pygame.image.load('pics/uday.jpg').convert()
# uday_sad_pic = pygame.image.load('pics/uday_sad.png').convert()
# yag_pic = pygame.image.load('pics/yag.png').convert()
# yag_sad_pic = pygame.image.load('pics/yag_sad.png').convert()
uday_sprite_sheet_pic = pygame.image.load(
    'pics/uday_animated.png').convert()
uday_sad_sprite_sheet_pic = pygame.image.load(
    'pics/uday_sad_animated.png').convert()
yag_sprite_sheet_pic = pygame.image.load(
    'pics/yag_animated.png').convert()
yag_sad_sprite_sheet_pic = pygame.image.load(
    'pics/yag_sad_animated.png').convert()

uday_sprite_sheet = SpriteSheet(uday_sprite_sheet_pic)
uday_sad_sprite_sheet = SpriteSheet(uday_sad_sprite_sheet_pic)
yag_sprite_sheet = SpriteSheet(yag_sprite_sheet_pic)
yag_sad_sprite_sheet = SpriteSheet(yag_sad_sprite_sheet_pic)
font = pygame.font.SysFont("comicsansms", 72)

char_sheets = [uday_sprite_sheet, yag_sprite_sheet]
char_sad_sheets = [uday_sad_sprite_sheet, yag_sad_sprite_sheet]

shootText = pygame.font.SysFont("comicsansms", 20).render(
    "Shoot Ready", True, (255, 150, 150))
shootText.set_alpha(50)
shootTextRect = shootText.get_rect()
shootTextRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)

dashText = pygame.font.SysFont("comicsansms", 20).render(
    "Dash Ready", True, (150, 150, 255))
dashText.set_alpha(50)
dashTextRect = dashText.get_rect()
dashTextRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
# enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
menu.enable()
# Main loop
while running:
    frame += 1

    if menu.is_enabled():
        menu.mainloop(screen)

    # Fill the screen with BLACK
    screen.fill((0, 0, 0))

    if not shootable and pygame.time.get_ticks() > prev_shot_time+shoot_cooldown:
        shootable = True

    if cgpa >= 9 and not dashable and pygame.time.get_ticks() > prev_dash_time+dash_cooldown-1500:
        dashable = True

    if not dashable and pygame.time.get_ticks() > prev_dash_time+dash_cooldown:
        dashable = True

    if slowed:
        if pygame.time.get_ticks() > prev_slowed_time + slow_cooldown:
            slowed = False
            # loader = Loader()
            for enemy in enemies:
                enemy.speedup()
            bullet_speed *= 10
            pygame.time.set_timer(ADDENEMY, 250)
        # else:
        #     loader.update()

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == pygame.KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == pygame.K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == pygame.QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy(y_movement)
            enemies.append(new_enemy)
            all_sprites.add(new_enemy)

    if count == num_college_days:
        running = False
        game_over = True

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    if shootable and pressed_keys[pygame.K_SPACE]:
        prev_shot_time = pygame.time.get_ticks()
        shootable = False
        shoot_sound.play()
        player.shoot()

    if dashable and pressed_keys[pygame.K_e]:
        prev_dash_time = pygame.time.get_ticks()
        dashable = False
        pos = pygame.mouse.get_pos()
        dashline = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.draw.line(dashline, (0, 0, 100), pos, player.rect.center, 7)
        screen.blit(dashline, dashline.get_rect())
        dash_sound.play()
        player.dash(pos[0], pos[1])

    if not slowed and pressed_keys[pygame.K_q]:
        prev_slowed_time = pygame.time.get_ticks()
        slowed = True
        slowed_sound.play()
        for enemy in enemies:
            enemy.slowdown()
        bullet_speed /= 10
        pygame.time.set_timer(ADDENEMY, 0)

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Draw all sprites
    for enemy in enemies:
        enemy.update()
        screen.blit(enemy.surf, enemy.rect)

    for bullet in bullets:
        bullet.update(bullet_speed)
        screen.blit(bullet.surf, bullet.rect)

    if(count == 0 or cgpa >= 7):
        player.surf = char_sheets[char_idx].get_image(frame % 8, 62, 45)
        topper = True
    else:
        if topper:
            topper = False
            ok_sound.play()
        player.surf = char_sad_sheets[char_idx].get_image(frame % 8, 62, 45)

    screen.blit(player.surf, player.rect)

    cgpaText = font.render(str(np.round(cgpa, 4)), True, (255, 255, 255))
    cgpaText.set_alpha(50)
    cgpaTextRect = cgpaText.get_rect()
    cgpaTextRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(cgpaText, cgpaTextRect)

    if shootable:
        screen.blit(shootText, shootTextRect)

    if dashable:
        screen.blit(dashText, dashTextRect)
    # if slowed:
    #     screen.blit(loader.surf, loader.rect)

    # Check if any enemies have collided with the player
    collided_enemy = check_collisions(player, enemies)
    if collided_enemy:
        collided_enemy.kill()
        enemies.remove(collided_enemy)
        count += 1
        if(count > 0):
            total += collided_enemy.score
            cgpa = total/count

    for bullet in bullets:
        killed_enemy = check_collisions(bullet, enemies)
        if killed_enemy:
            killed_enemy.kill()
            enemies.remove(killed_enemy)
            bullet.kill()
            bullets.remove(bullet)

    pygame.display.flip()

    clock.tick(frame_rate)

if game_over:
    for sprite in all_sprites:
        sprite.kill()
while game_over:
    for event in pygame.event.get():
        screen.fill((0, 0, 0))
        # Did the user hit a key?
        if event.type == pygame.KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == pygame.K_ESCAPE:
                game_over = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == pygame.QUIT:
            game_over = False

    text = font.render(("College Over, CGPA = "+str(np.round(cgpa, 3))),
                       True, (250, 200, 200))
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.blit(text, textRect)

    pygame.display.flip()
