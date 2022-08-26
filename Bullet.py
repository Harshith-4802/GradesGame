import pygame
import os
from consts import *
from common import bullets


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Bullet, self).__init__()
        self.surf = pygame.image.load(
            os.getcwd()+"/pics/book.png").convert()
        self.rect = self.surf.get_rect(center=pos)
        bullets.append(self)

    def update(self,speed):
        self.rect.move_ip(speed, 0)
        if self.rect.right < 0 or self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            bullets.remove(self)
            self.kill()
