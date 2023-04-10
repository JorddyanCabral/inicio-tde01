        # atualização da posição do alvo
        update_target()

        # limpeza da tela
        screen.fill(BLACK)

        # desenho do alvo e das informações do jogador
        draw_target()
        draw_info()

        # atualização da tela
        pygame.display.flip()