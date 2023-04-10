from sprites import *
import pygame
import sys
from pygame.locals import *

pygame.init()

FPS = 60

fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Shooter')
pygame.mouse.set_visible(False)

crosshair = Crosshair()
background = Background()

crosshair_group = pygame.sprite.Group()
background_group = pygame.sprite.Group()


crosshair_group.add(crosshair)
background_group.add(background)

while True:
    DISPLAYSURF.fill((0, 0, 128))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
          crosshair.shot_fire()
        if event.type == KEYDOWN:
          if event.key ==K_r:
            crosshair.reload()

    background_group.draw(DISPLAYSURF)
    background_group.update()

    crosshair_group.draw(DISPLAYSURF)
    crosshair_group.update()

    pygame.display.update()
    fpsClock.tick(FPS)
