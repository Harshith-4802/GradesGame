import pygame
import random
import numpy as np
from consts import *
from common import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, y_movement):
        super(Enemy, self).__init__()
        rand_idx = random.randint(0, 4)
        enemy_pic = enemy_pics[rand_idx]
        self.surf = pygame.image.load("pics/"+enemy_pic).convert()
        self.score = 0
        if(enemy_pic == "a.png"):
            self.score = 10
        elif(enemy_pic == "b.png"):
            self.score = 8
        elif(enemy_pic == "c.png"):
            self.score = 6
        elif(enemy_pic == "d.png"):
            self.score = 4

        self.surf.set_colorkey((255, 255, 255), pygame.RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(20, SCREEN_HEIGHT-20),
            )
        )
        self.xspeed = random.randint(
            enemy_speed_range[0], enemy_speed_range[1]) * np.exp(frame/(400*num_college_days))
        self.yspeed = 0
        if y_movement:
            self.yspeed = random.randint(-2, 2) * \
                np.exp(frame/(800*num_college_days))

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(round(-self.xspeed), round(self.yspeed))
        if self.rect.right < 0 or self.rect.bottom <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            enemies.remove(self)
            self.kill()

    def slowdown(self):
        self.xspeed /= 10
        self.yspeed /= 10

    def speedup(self):
        self.xspeed *= 10
        self.yspeed *= 10
