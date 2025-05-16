import pygame
import random # Precisamos para a aleatoriedade das janelas
from . import game_state # Usando import relativo para pegar as constantes

# Fonte para UI (será inicializada no main.py)
UI_FONT = None

def draw_sky(screen):
    """Desenha o céu."""
    screen.fill(game_state.BLUE_SKY)

def draw_ground(screen):
    """Desenha o chão."""
    pygame.draw.rect(screen, game_state.GREEN_GRASS, (0, game_state.SCREEN_HEIGHT - game_state.GROUND_HEIGHT, game_state.SCREEN_WIDTH, game_state.GROUND_HEIGHT))

def draw_buildings(screen):
    """Desenha os prédios."""
    # Desenha os prédios e suas janelas
    for x, y_top, width, height, color, window_lit_pattern in game_state.BUILDINGS:
        window_pattern_idx = 0 # Índice para percorrer o padrão de janelas
        # Desenha o retângulo principal do prédio
        pygame.draw.rect(screen, color, (x, y_top, width, height))

        # Calcula a área onde as janelas podem ser desenhadas (excluindo margens)
        window_area_x_start = x + game_state.WINDOW_MARGIN_X
        window_area_y_start = y_top + game_state.WINDOW_MARGIN_Y
        window_area_width = width - 2 * game_state.WINDOW_MARGIN_X
        window_area_height = height - 2 * game_state.WINDOW_MARGIN_Y

        # Desenha as janelas APENAS se houver espaço suficiente
        if window_area_width >= game_state.WINDOW_WIDTH and window_area_height >= game_state.WINDOW_HEIGHT:
            # Itera pelas posições possíveis das janelas
            for current_window_y in range(window_area_y_start, y_top + height - game_state.WINDOW_MARGIN_Y - game_state.WINDOW_HEIGHT + 1, game_state.WINDOW_HEIGHT + game_state.WINDOW_MARGIN_Y):
                for current_window_x in range(window_area_x_start, x + width - game_state.WINDOW_MARGIN_X - game_state.WINDOW_WIDTH + 1, game_state.WINDOW_WIDTH + game_state.WINDOW_MARGIN_X):
                    if window_pattern_idx < len(window_lit_pattern): # Garante que não estouramos o índice
                        if window_lit_pattern[window_pattern_idx]:
                            color_to_use = game_state.WINDOW_LIT_COLOR
                        else:
                            color_to_use = game_state.WINDOW_UNLIT_COLOR
                        # Desenha a janela com a cor escolhida
                        pygame.draw.rect(screen, color_to_use, (current_window_x, current_window_y, game_state.WINDOW_WIDTH, game_state.WINDOW_HEIGHT))
                        window_pattern_idx += 1
                    # else: # Opcional: logar se o número de janelas desenhadas não bate com o padrão
                        # print("Aviso: Padrão de janelas menor que o número de janelas desenhadas.")

def draw_gorilla(screen, player_number, position):
    """Desenha a imagem do gorila."""
    # position[0] é o centro X do gorila
    # position[1] é o Y do topo do prédio onde o gorila está
    # O gorila é desenhado de forma que sua base esteja em position[1]
    
    image_to_draw = None
    if player_number == 1 and game_state.gorilla_image:
        image_to_draw = game_state.gorilla_image
    elif player_number == 2 and game_state.gorilla_image_flipped:
        image_to_draw = game_state.gorilla_image_flipped

    if image_to_draw:
        gorilla_rect_x = position[0] - image_to_draw.get_width() // 2
        gorilla_rect_y = position[1] - image_to_draw.get_height() # Y do topo do gorila
        screen.blit(image_to_draw, (gorilla_rect_x, gorilla_rect_y))
    else: # Fallback para o retângulo se a imagem não carregou
        fallback_color = game_state.BROWN_GORILLA
        gorilla_rect_x = position[0] - game_state.GORILLA_WIDTH // 2
        gorilla_rect_y = position[1] - game_state.GORILLA_HEIGHT 
        pygame.draw.rect(screen, fallback_color, (gorilla_rect_x, gorilla_rect_y, game_state.GORILLA_WIDTH, game_state.GORILLA_HEIGHT))

def draw_scene(screen):
    """Desenha todos os elementos da cena."""
    draw_sky(screen)
    draw_buildings(screen) 
    draw_ground(screen) 

    # Desenha os gorilas em suas posições calculadas nos prédios
    player1_actual_pos = (game_state.PLAYER1_POS_X, game_state.PLAYER1_POS_Y)
    player2_actual_pos = (game_state.PLAYER2_POS_X, game_state.PLAYER2_POS_Y)
    draw_gorilla(screen, 1, player1_actual_pos) # Passa o número do jogador
    draw_gorilla(screen, 2, player2_actual_pos) # Passa o número do jogador

def draw_input_ui(screen):
    """Desenha a UI para entrada de ângulo e força."""
    if not UI_FONT:
        return # Fonte não inicializada

    if game_state.game_phase == "INPUT":
        player_text = f"Player {game_state.current_player}'s Turn"
        angle_prompt = "Angle (0-180): "
        force_prompt = "Force (1-200): "

        if game_state.active_input_field == "angle":
            angle_val_text = game_state.current_angle_input_str + "_" # Adiciona cursor piscante (simples)
            force_val_text = game_state.current_force_input_str
        else: # active_input_field == "force"
            angle_val_text = game_state.current_angle_input_str
            force_val_text = game_state.current_force_input_str + "_"

        text_player = UI_FONT.render(player_text, True, game_state.BLACK)
        text_angle = UI_FONT.render(angle_prompt + angle_val_text, True, game_state.BLACK)
        text_force = UI_FONT.render(force_prompt + force_val_text, True, game_state.BLACK)

        screen.blit(text_player, (10, 10))
        screen.blit(text_angle, (10, 30))
        screen.blit(text_force, (10, 50))

def draw_scores(screen):
    """Desenha o placar de vitórias dos jogadores."""
    if not UI_FONT:
        return

    score_text = f"{game_state.player1_score} | {game_state.player2_score}"
    text_surface_score = UI_FONT.render(score_text, True, game_state.BLACK)

    # Centraliza o placar no topo da tela
    score_rect = text_surface_score.get_rect(centerx=game_state.SCREEN_WIDTH // 2, top=10)
    screen.blit(text_surface_score, score_rect)


def draw_banana(screen):
    """Desenha a banana se ela estiver ativa."""
    if game_state.banana_active and game_state.banana_image:
        # game_state.banana_x e game_state.banana_y são o centro da banana
        # Para blit, precisamos do canto superior esquerdo
        banana_img_width = game_state.banana_image.get_width()
        banana_img_height = game_state.banana_image.get_height()
        blit_x = int(game_state.banana_x - banana_img_width // 2)
        blit_y = int(game_state.banana_y - banana_img_height // 2)
        screen.blit(game_state.banana_image, (blit_x, blit_y))
    elif game_state.banana_active: # Fallback para o círculo se a imagem não carregou
        pygame.draw.circle(screen, game_state.YELLOW_BANANA, (int(game_state.banana_x), int(game_state.banana_y)), game_state.BANANA_RADIUS)

def draw_game_over_message(screen):
    """Desenha a mensagem de fim de jogo."""
    if not UI_FONT:
        return

    if game_state.game_phase == "GAME_OVER" and game_state.winner != 0:
        winner_text = f"Player {game_state.winner} Wins!"
        restart_text = "Press R to Restart" # Texto para reiniciar
        quit_text = "Press Q to Quit"       # Texto para sair

        text_surface_winner = UI_FONT.render(winner_text, True, game_state.BLACK, game_state.WHITE) # Texto preto com fundo branco
        text_surface_restart = UI_FONT.render(restart_text, True, game_state.BLACK, game_state.WHITE)
        text_surface_quit = UI_FONT.render(quit_text, True, game_state.BLACK, game_state.WHITE)

        # Centralizar o texto
        winner_rect = text_surface_winner.get_rect(center=(game_state.SCREEN_WIDTH // 2, game_state.SCREEN_HEIGHT // 2 - 20))
        restart_rect = text_surface_restart.get_rect(center=(game_state.SCREEN_WIDTH // 2, game_state.SCREEN_HEIGHT // 2 + 20)) # Posição para reiniciar
        quit_rect = text_surface_quit.get_rect(center=(game_state.SCREEN_WIDTH // 2, game_state.SCREEN_HEIGHT // 2 + 50)) # Posição para sair (abaixo do reiniciar)

        screen.blit(text_surface_winner, winner_rect)
        screen.blit(text_surface_restart, restart_rect)
        screen.blit(text_surface_quit, quit_rect)

def draw_explosion(screen):
    """Desenha a explosão se ela estiver ativa e dentro da sua duração."""
    if game_state.explosion_active and game_state.explosion_image_scaled:
        current_time = pygame.time.get_ticks()
        if current_time - game_state.explosion_start_time < game_state.EXPLOSION_DURATION_MS:
            # game_state.explosion_x e y são o centro da explosão
            # Para blit, precisamos do canto superior esquerdo
            img_width = game_state.explosion_image_scaled.get_width()
            img_height = game_state.explosion_image_scaled.get_height()
            blit_x = int(game_state.explosion_x - img_width // 2)
            blit_y = int(game_state.explosion_y - img_height // 2)
            screen.blit(game_state.explosion_image_scaled, (blit_x, blit_y))
        else:
            game_state.explosion_active = False # Desativa a explosão após a duração

def draw_title_screen(screen):
    """Desenha a tela inicial do jogo."""
    if not UI_FONT:
        return

    screen.fill(game_state.BLUE_SKY) # Fundo azul como o céu

    # Fonte maior para o título principal "GORILLA"
    big_title_font_size = 74
    try:
        big_title_font = pygame.font.SysFont("monospace", big_title_font_size, bold=True)
    except: # Fallback se a fonte específica não estiver disponível
        big_title_font = pygame.font.SysFont(None, big_title_font_size + 10, bold=True) # Fonte padrão um pouco maior

    main_title_text = "GORILLA"
    sub_title_text = "Game" # Mantendo o "Game" menor ou como subtítulo
    instructions_text = "Press Any Key to Start"

    text_surface_main_title = big_title_font.render(main_title_text, True, game_state.BLACK)
    text_surface_sub_title = UI_FONT.render(sub_title_text, True, game_state.BLACK) # Usando a UI_FONT normal para "Game"
    text_surface_instructions = UI_FONT.render(instructions_text, True, game_state.BLACK)

    # Centralizar o texto
    main_title_rect = text_surface_main_title.get_rect(center=(game_state.SCREEN_WIDTH // 2, game_state.SCREEN_HEIGHT // 2 - 70))
    sub_title_rect = text_surface_sub_title.get_rect(center=(game_state.SCREEN_WIDTH // 2, main_title_rect.bottom + 15)) # Abaixo do GORILLA
    instructions_rect = text_surface_instructions.get_rect(center=(game_state.SCREEN_WIDTH // 2, sub_title_rect.bottom + 40))

    screen.blit(text_surface_main_title, main_title_rect)
    screen.blit(text_surface_sub_title, sub_title_rect)
    screen.blit(text_surface_instructions, instructions_rect)

def draw_wind_indicator(screen):
    """Desenha um indicador da força e direção do vento."""
    if not UI_FONT:
        return

    # Só mostra o vento se ele for significativo
    if abs(game_state.wind_speed) < game_state.MIN_WIND_FOR_DISPLAY:
        wind_text_str = "Wind: Calm"
    else:
        direction = ">>>" if game_state.wind_speed > 0 else "<<<"
        # Multiplicamos por um fator para tornar a "força" mais legível para o jogador
        strength = int(abs(game_state.wind_speed) * 1000) # Ajuste este fator se necessário
        wind_text_str = f"Wind: {direction} {strength}"

    wind_surface = UI_FONT.render(wind_text_str, True, game_state.BLACK)
    # Posiciona no canto superior direito
    screen.blit(wind_surface, (game_state.SCREEN_WIDTH - wind_surface.get_width() - 10, 10))