import pygame
import random

# inicialização do pygame
pygame.init()

# dimensões da tela
screen_width = 800
screen_height = 600

# cores utilizadas no jogo
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# criação da tela
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Jogo do Alvo")

# definição das fontes utilizadas no jogo
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# definição das variáveis do jogo
player_score = 0
player_level = 1
level_threshold = 5
target_radius = 20
target_speed = 5
target_x = random.randint(target_radius, screen_width - target_radius)
target_y = random.randint(target_radius, screen_height - target_radius)
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
    target_x = max(target_radius, min(target_x, screen_width - target_radius))
    target_y = max(target_radius, min(target_y, screen_height - target_radius))
    if player_score % 5 == 0 and target_speed > 1:
        target_speed -= 1

# função para desenhar o alvo


def draw_target():
    pygame.draw.circle(screen, white, (target_x, target_y), target_radius)

# função para desenhar o score e o level do jogador


def draw_info():
    score_text = font.render("Score: " + str(player_score), True, white)
    level_text = small_font.render("Level " + str(player_level), True, white)
    error_text = small_font.render(
        "Errors: " + str(error_count) + "/" + str(max_errors), True, red)
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
                    target_radius, screen_width - target_radius)
                target_y = random.randint(
                    target_radius, screen_height - target_radius)
                # hit_sound.play()
            else:
                error_count += 1
                if error_count >= max_errors:
                    running = False
                # error_sound.play()

    # atualização da posição do alvo
    update_target()

    # limpeza da tela
    screen.fill(black)

    # desenho do alvo e das informações do jogador
    draw_target()
    draw_info()

    # atualização da tela
    pygame.display.flip()

# encerramento do pygame
pygame.quit()
