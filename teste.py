import pygame
import sys
import random
from pygame.locals import *

import warnings
warnings.filterwarnings("ignore", category=Warning)

# Definição de algumas constantes
WIDTH = 800
HEIGHT = 600
FPS = 60

# Inicialização do Pygame
pygame.init()

# Criação da janela
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Shooter')
pygame.mouse.set_visible(False)

# Inicialização do Clock para controle de FPS
fpsClock = pygame.time.Clock()

# # Carregamento dos sons
# shot_sound = pygame.mixer.Sound('res/shot.ogg')
# hit_sound = pygame.mixer.Sound('res/hit.ogg')
# miss_sound = pygame.mixer.Sound('res/miss.ogg')
# reload_sound = pygame.mixer.Sound('res/reload.ogg')

# Carregamento das imagens
crosshair_img = pygame.image.load('res/crosshair_white_large.png')
bg_img = pygame.image.load('res/bg_blue.png')
target_img = pygame.image.load('res/target_red2.png')
bullet_hole_img = pygame.image.load('res/bg_blue.png')


# Classe para o alvo
class Target(pygame.sprite.Sprite):
    def __init__(self, pos, vel):
        super().__init__()
        self.image = target_img.copy()
        self.rect = self.image.get_rect(center=pos)
        self.vel = vel

    def update(self):
        self.rect.move_ip(self.vel)
        if self.rect.right < 0:
            self.kill()


# Classe para o buraco de bala
class BulletHole(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = bullet_hole_img.copy()
        self.rect = self.image.get_rect(center=pos)


# Classe para o jogo
class Game:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.targets = pygame.sprite.Group()
        self.bullet_holes = pygame.sprite.Group()
        self.crosshair = pygame.sprite.Sprite()
        self.crosshair.image = crosshair_img
        self.crosshair.rect = self.crosshair.image.get_rect()
        self.crosshair_group = pygame.sprite.Group(self.crosshair)
        self.background = pygame.sprite.Sprite()
        self.background.image = pygame.Surface((WIDTH, HEIGHT))
        self.background.rect = self.background.image.get_rect()
        self.background_group = pygame.sprite.Group(self.background)
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.targets_per_level = 5
        self.targets_left = self.targets_per_level

    def start(self):
        self.targets_left = self.targets_per_level
        self.add_target()  # adiciona o primeiro alvo
        self.update_score()
        self.update_level()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            fpsClock.tick(FPS)

    def add_target(self):
        if self.targets_left > 0:
            # Adiciona um novo alvo à tela com uma posição e velocidade aleatórias
            pos = (random.randint(100, WIDTH - 100),
                   random.randint(100, HEIGHT - 100))
            vel = (random.randint(-3, 3), random.randint(-3, 3))
            target = Target(pos, vel)
            self.targets.add(target)
            self.targets_left -= 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.shoot(pygame.mouse.get_pos())
            elif event.type == KEYDOWN:
                if event.key == K_r:
                    self.reload()

    def update(self):
        self.background_group.update()
        self.crosshair_group.update()
        self.targets.update()
        self.bullet_holes.update()
        self.crosshair.rect.center = pygame.mouse.get_pos()

        if len(self.targets) == 0 and self.targets_left == 0:
            self.level += 1
            self.targets_left = self.targets_per_level
            self.add_target()
            self.update_level()

    def update_score(self):
        score_text = self.font.render(
            'Score: {}'.format(self.score), True, (255, 255, 255))
        self.background_group.add(pygame.sprite.Sprite())
        self.background_group.sprites()[-1].image = score_text
        self.background_group.sprites(
        )[-1].rect = score_text.get_rect(top=10, right=WIDTH-10)

    def update_level(self):
        level_text = self.font.render(
            'Level: {}'.format(self.level), True, (255, 255, 255))
        self.background_group.add(pygame.sprite.Sprite())
        self.background_group.sprites()[-1].image = level_text
        self.background_group.sprites(
        )[-1].rect = level_text.get_rect(top=10, left=10)

    def draw(self):
        self.background_group.draw(DISPLAYSURF)
        self.targets.draw(DISPLAYSURF)
        self.bullet_holes.draw(DISPLAYSURF)
        self.crosshair_group.draw(DISPLAYSURF)
        pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.start()
