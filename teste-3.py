# carrega o som de acerto do alvo
hit_sound = pygame.mixer.Sound("hit_sound.wav")

# loop principal do jogo
running = True
while running:
    player_score = 0
player_level = 1
level_threshold = 5
target_radius = 20
target_speed = 5
target_x = random.randint(target_radius, screen_width - target_radius)
target_y = random.randint(target_radius, screen_height - target_radius)
error_count = 0  # adiciona o contador de erros
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
                hit_sound.play()  # reproduz o som de acerto do alvo

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
