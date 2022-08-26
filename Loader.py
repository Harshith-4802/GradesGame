import pygame
from main import player


class Loader(pygame.sprite.Sprite):
    def __init__(self):
        super(Loader, self).__init__()
        self.val = 1
        self.surf = pygame.Surface((self.val, 10))
        self.surf.fill((100, 0, 0))
        self.rect = self.surf.get_rect(
            center=(player.rect.centerx+40, player.rect.centery+40))

    def update(self):
        self.val += 1
        self.surf = pygame.Surface((self.val, 10))
        self.surf.fill((100, 0, 0))
        self.rect = self.surf.get_rect(
            center=(player.rect.centerx+40, player.rect.centery+40))
