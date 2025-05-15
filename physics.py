from . import game_state
import pygame # Para usar pygame.Rect para colisões

def update_banana_position():
    """Atualiza a posição da banana com base na física e verifica colisões simples."""
    if not game_state.banana_active:
        return

    # Aplicar gravidade à velocidade vertical
    game_state.banana_vy += game_state.GRAVITY

    # Aplicar vento à velocidade horizontal
    game_state.banana_vx += game_state.wind_speed

    # Atualizar posição da banana
    game_state.banana_x += game_state.banana_vx
    game_state.banana_y += game_state.banana_vy

    # Criar um Rect para a banana para facilitar a detecção de colisão
    # Usaremos um Rect que envolve a banana.
    banana_rect = pygame.Rect(
        game_state.banana_x - game_state.BANANA_RADIUS,
        game_state.banana_y - game_state.BANANA_RADIUS,
        2 * game_state.BANANA_RADIUS,
        2 * game_state.BANANA_RADIUS
    )

    # Definir Rects dos gorilas para detecção de colisão
    gorilla1_rect = pygame.Rect(
        game_state.PLAYER1_POS_X - game_state.GORILLA_WIDTH // 2,
        game_state.PLAYER1_POS_Y - game_state.GORILLA_HEIGHT,
        game_state.GORILLA_WIDTH,
        game_state.GORILLA_HEIGHT
    )
    gorilla2_rect = pygame.Rect(
        game_state.PLAYER2_POS_X - game_state.GORILLA_WIDTH // 2,
        game_state.PLAYER2_POS_Y - game_state.GORILLA_HEIGHT,
        game_state.GORILLA_WIDTH,
        game_state.GORILLA_HEIGHT
    )

    # Verificar colisão com prédios
    for i, building_data in enumerate(game_state.BUILDINGS): # building_data agora tem 6 elementos
        b_x, b_y_top, b_width, b_height, b_color, b_window_pattern = building_data # Desempacota o padrão
        building_rect = pygame.Rect(b_x, b_y_top, b_width, b_height)

        if banana_rect.colliderect(building_rect):
            print(f"Banana atingiu o prédio {i} em ({int(b_x)}, {int(b_y_top)})!")

            # --- Lógica de Dano ao Prédio ---
            damage_amount = 20  # Quantidade de "dano" (pixels) à altura do prédio
            new_height = b_height - damage_amount
            new_y_top = b_y_top + damage_amount # O topo do prédio "desce"

            # Garante que o prédio não fique com altura negativa ou muito pequena
            min_segment_height = 10 # Altura mínima para um segmento de prédio visível
            if new_height < min_segment_height:
                new_height = min_segment_height
                # Recalcula y_top para garantir que a base do prédio permaneça no chão
                # ou na altura mínima se o prédio for "destruído"
                new_y_top = game_state.SCREEN_HEIGHT - game_state.GROUND_HEIGHT - new_height
            
            # Mantém o padrão de janelas original ao atualizar o prédio
            game_state.BUILDINGS[i] = (b_x, new_y_top, b_width, new_height, b_color, b_window_pattern)
            print(f"Prédio {i} danificado. Nova altura: {new_height}, Novo Y_top: {new_y_top}")

            # --- Ajustar posição do gorila se ele estiver neste prédio ---
            # Gorila 1
            if b_x <= game_state.PLAYER1_POS_X < (b_x + b_width):
                game_state.PLAYER1_POS_Y = new_y_top
                print(f"Jogador 1 ajustado para Y: {new_y_top}")
            # Gorila 2
            if b_x <= game_state.PLAYER2_POS_X < (b_x + b_width):
                game_state.PLAYER2_POS_Y = new_y_top
                print(f"Jogador 2 ajustado para Y: {new_y_top}")
            # --- Fim do ajuste do gorila ---
            # --- Fim da Lógica de Dano ao Prédio ---

            # Ativa a explosão no local da banana
            game_state.explosion_x, game_state.explosion_y = game_state.banana_x, game_state.banana_y
            game_state.explosion_active = True
            game_state.explosion_start_time = pygame.time.get_ticks()
            
            game_state.banana_active = False
            if game_state.sound_explosion:
                game_state.sound_explosion.play()
            game_state.switch_player_turn() # Troca o turno após o impacto
            return # Sai da função pois a banana já colidiu

    # Verificar colisão com o gorila oponente
    opponent_gorilla_rect = gorilla2_rect if game_state.current_player == 1 else gorilla1_rect
    opponent_player_number = 2 if game_state.current_player == 1 else 1

    if banana_rect.colliderect(opponent_gorilla_rect):
        print(f"HIT! Jogador {game_state.current_player} acertou o Jogador {opponent_player_number}!")
        # Ativa a explosão no local da banana
        game_state.explosion_x, game_state.explosion_y = game_state.banana_x, game_state.banana_y
        game_state.explosion_active = True
        game_state.explosion_start_time = pygame.time.get_ticks()
        game_state.banana_active = False
        if game_state.sound_explosion:
            game_state.sound_explosion.play()
        game_state.game_phase = "VICTORY_DELAY" # Mudar para o estado de atraso
        game_state.victory_delay_start_time = pygame.time.get_ticks() # Registrar tempo de início do atraso
        game_state.winner = game_state.current_player
        return

    # Verificar colisão com os limites da tela (se não colidiu com prédio)
    if (game_state.banana_x + game_state.BANANA_RADIUS < 0 or 
        game_state.banana_x - game_state.BANANA_RADIUS > game_state.SCREEN_WIDTH or
        game_state.banana_y - game_state.BANANA_RADIUS > game_state.SCREEN_HEIGHT): # Se sair por baixo também (considerando o raio)
        print("Banana saiu da tela ou atingiu o chão (fora dos prédios).")
        game_state.banana_active = False
        game_state.switch_player_turn() # Troca o turno
        return