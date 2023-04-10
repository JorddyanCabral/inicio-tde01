import pygame
import math


class Crosshair(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            "res/crosshair_white_large.png")
        self.rect = self.image.get_rect()

        self.fire = pygame.mixer.Sound('')
        self.reload_sound = pygame.mixer.Sound('')

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def shot_fire(self):
        self.fire.play()

    def reload(self):
        self.reload_sound.play()


class Background (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface([800, 600])
        self.bg_image = pygame.image.load("res/bg_blue.png")
        self.rect = self.image.get_rect()

    def update(self):
        tiles = math.ceil(800 / self.bg_image.get_width())
        size = self.bg_image.get_width()
        for i in range(tiles):
            for j in range(tiles):
                self.image.blit(self.bg_image, (j * size, i * size))
