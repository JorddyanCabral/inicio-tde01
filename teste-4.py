import pygame
import sys
import random
from pygame.locals import *

pygame.init()

FPS = 60
SCREEN_X = 800
SCREEN_Y = 600

BLUE = "#1562BA"
BLUE_HOVER = "#46BEEC"
WHITE = "#FFFFFF"
RED = (255, 0, 0)
BLACK = (0, 0, 0)


font_large = pygame.font.Font("./res/joystix.otf", 48)
font = pygame.font.Font("./res/joystix.otf", 24)
small_font = pygame.font.Font("./res/joystix.otf", 18)

fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((SCREEN_X, SCREEN_Y))

# criação da tela
screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
pygame.display.set_caption("Jogo do Alvo")

# Configuração das Imagens de Fundo
bg_game_menu = pygame.transform.scale(
    pygame.image.load('./res/bg_main_menu.png'), (SCREEN_X, SCREEN_Y))
bg_game = pygame.transform.scale(
    pygame.image.load('./res/bg_game.png'), (SCREEN_X, SCREEN_Y)
)
bg_option = pygame.transform.scale(
    pygame.image.load('./res/bg_options.png'), (SCREEN_X, SCREEN_Y)
)
bg_about = pygame.transform.scale(
    pygame.image.load('./res/bg_credits.png'), (SCREEN_X, SCREEN_Y)
)


def draw_text(text, font, color, surface, position):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = position
    surface.blit(textobj, textrect)


def main_menu():
    scroll = SCREEN_X
    DISPLAYSURF.blit(bg_game_menu, (0, 0))
    while True:
        scroll -= 0.2
        DISPLAYSURF.blit(bg_game_menu, (scroll - SCREEN_X, 0))
        DISPLAYSURF.blit(bg_game_menu, (scroll, 0))

        if scroll <= 0:
            scroll = SCREEN_X

        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect((SCREEN_X/3*0) + 60, 500, 150, 50)
        button_2 = pygame.Rect((SCREEN_X/3*1) + 60, 500, 150, 50)
        button_3 = pygame.Rect((SCREEN_X/3*2) + 60, 500, 150, 50)

        pygame.draw.rect(DISPLAYSURF, BLUE, button_1, 0, 10)
        pygame.draw.rect(DISPLAYSURF, BLUE, button_2, 0, 10)
        pygame.draw.rect(DISPLAYSURF, BLUE, button_3, 0, 10)

        click = pygame.mouse.get_pressed()

        if button_1.collidepoint(mx, my):
            pygame.draw.rect(DISPLAYSURF, BLUE_HOVER, button_1, 0, 10)
            if click[0]:
                game()
        if button_2.collidepoint(mx, my):
            pygame.draw.rect(DISPLAYSURF, BLUE_HOVER, button_2, 0, 10)
            if click[0]:
                options()
        if button_3.collidepoint(mx, my):
            pygame.draw.rect(DISPLAYSURF, BLUE_HOVER, button_3, 0, 10)
            if click[0]:
                about()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        draw_text("Nigth's Adventures", font_large,
                  WHITE, DISPLAYSURF, [400, 150])
        draw_text("The Game", font_large, WHITE, DISPLAYSURF, [400, 250])

        draw_text("Start", font, WHITE, DISPLAYSURF, button_1.center)
        draw_text("Options", font, WHITE, DISPLAYSURF, button_2.center)
        draw_text("About", font, WHITE, DISPLAYSURF, button_3.center)

        pygame.display.update()
        fpsClock.tick(FPS)


def game():
    global SCREEN_X, SCREEN_Y

    global target_x, target_y, target_speed
    # definição das variáveis do jogo
    player_score = 0
    player_level = 1
    level_threshold = 5
    target_radius = 20
    target_speed = 5
    target_x = random.randint(target_radius, SCREEN_X - target_radius)
    target_y = random.randint(target_radius, SCREEN_Y - target_radius)
    max_errors = 10
    error_count = 0

    # carrega o som de acerto do alvo
    # hit_sound = pygame.mixer.Sound("hit_sound.wav")
    # carrega o som de erro
    # error_sound = pygame.mixer.Sound("error_sound.wav")

    # função para atualizar o alvo

    def update_target():
        global target_x, target_y, target_speed
        target_x += random.randint(-target_speed, target_speed)
        target_y += random.randint(-target_speed, target_speed)
        target_x = max(target_radius, min(target_x, SCREEN_X - target_radius))
        target_y = max(target_radius, min(target_y, SCREEN_Y - target_radius))
        if player_score % 5 == 0 and target_speed > 1:
            target_speed -= 1

    # função para desenhar o alvo

    def draw_target():
        pygame.draw.circle(screen, WHITE, (target_x, target_y), target_radius)

    # função para desenhar o score e o level do jogador

    def draw_info():
        score_text = font.render("Score: " + str(player_score), True, WHITE)
        level_text = small_font.render(
            "Level " + str(player_level), True, WHITE)
        error_text = small_font.render(
            "Errors: " + str(error_count) + "/" + str(max_errors), True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(error_text, (10, 90))

    # loop principal do jogo
    running = True
    while running:
        # tratamento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # verificação de acerto no alvo
                dist = ((event.pos[0] - target_x)**2 +
                        (event.pos[1] - target_y)**2)**0.5
                if dist <= target_radius:
                    player_score += 1
                    if player_score % level_threshold == 0:
                        player_level += 1
                        target_speed += 1
                        target_radius = max(10, target_radius - 2)
                    target_x = random.randint(
                        target_radius, SCREEN_X - target_radius)
                    target_y = random.randint(
                        target_radius, SCREEN_Y - target_radius)
                    # hit_sound.play()
                else:
                    error_count += 1
                    if error_count >= max_errors:
                        running = False
                    # error_sound.play()

        # atualização da posição do alvo
        update_target()

        # limpeza da tela
        screen.fill(BLACK)

        # desenho do alvo e das informações do jogador
        draw_target()
        draw_info()

        # atualização da tela
        pygame.display.flip()


def options():
    running = True
    while running:
        DISPLAYSURF.blit(bg_option, (0, 0))
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    DISPLAYSURF.blit(bg_game_menu, (0, 0))
                    running = False
        pygame.display.update()
        fpsClock.tick(60)


def about():
    running = True
    scroll = SCREEN_Y

    while running:
        DISPLAYSURF.blit(bg_about, (0, 0))
        scroll -= 1
        draw_text("Jorddyan", font, WHITE,
                  DISPLAYSURF, (400, scroll - SCREEN_Y))
        draw_text("Jorddyan", font, WHITE,
                  DISPLAYSURF, (400, scroll))
        draw_text("Breno", font, WHITE,
                  DISPLAYSURF, (400, scroll - SCREEN_Y))
        draw_text("Breno", font, WHITE,
                  DISPLAYSURF, (400, scroll + 20))
        draw_text("Caetano", font, WHITE,
                  DISPLAYSURF, (400, scroll - SCREEN_Y))
        draw_text("Caetano", font, WHITE,
                  DISPLAYSURF, (400, scroll + 100))
        if scroll <= 0:
            scroll = SCREEN_Y
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    DISPLAYSURF.blit(bg_game_menu, (0, 0))
                    running = False
        pygame.display.update()
        fpsClock.tick(60)


main_menu()
