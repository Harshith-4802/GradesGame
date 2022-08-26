import pygame
import os
from consts import *
from Bullet import Bullet

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load(os.getcwd() + "/pics/uday.png").convert()
        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
    # Move the sprite based on user keypresses

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.rect.move_ip(0, -player_speed)
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.rect.move_ip(0, player_speed)
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.rect.move_ip(-player_speed, 0)
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.rect.move_ip(player_speed, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def dash(self, x, y):
        self.rect.center = (x, y)

    def shoot(self):
        Bullet(self.rect.center)
