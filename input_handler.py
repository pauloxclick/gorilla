import pygame
from . import game_state
import math # Para cálculos trigonométricos (cos, sin)


def process_player_input(event):
    """Processa o input do teclado do jogador para ângulo e força."""
    if game_state.game_phase == "GAME_OVER":
        if event.type == pygame.KEYDOWN: # Processa 'R' para reiniciar ou 'Q' para sair
            if event.key == pygame.K_r:
                game_state.reset_game()
            elif event.key == pygame.K_q:
                game_state.quit_requested = True # Sinaliza que o jogador quer sair
        return # Não processa mais nada se for game over
    elif game_state.game_phase != "INPUT": # Se não for INPUT nem GAME_OVER, não faz nada
        return 

    if event.type == pygame.KEYDOWN:
        current_text_field = None
        # Determina qual campo de input está ativo
        if game_state.active_input_field == "angle":
            current_text_field = game_state.current_angle_input_str
        elif game_state.active_input_field == "force":
            current_text_field = game_state.current_force_input_str

        if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
            if game_state.active_input_field == "angle":
                # Processa input de ângulo
                try:
                    # Validação básica, pode ser melhorada
                    val = float(game_state.current_angle_input_str)
                    if 0 <= val <= 180: # Gorila 1 (esquerda) atira para direita (0-90), Gorila 2 (direita) atira para esquerda (90-180)
                                        # Simplificando por agora: 0-180 para ambos. Ajustaremos a direção do tiro depois.
                        game_state.player_angle = val
                        game_state.active_input_field = "force"
                        print(f"Player {game_state.current_player} Angle set to: {game_state.player_angle}")
                    else:
                        print("Angle must be between 0 and 180.")
                        game_state.current_angle_input_str = "" # Limpa input inválido
                except ValueError:
                    print("Invalid angle input.")
                    game_state.current_angle_input_str = "" # Limpa input inválido
            elif game_state.active_input_field == "force":
                # Processa input de força
                try:
                    val = float(game_state.current_force_input_str)
                    if 0 < val <= 200: # Força entre 1 e 200 (arbitrário)
                        game_state.player_force = val
                        print(f"Player {game_state.current_player} Force set to: {game_state.player_force}")
                        print(f"Player {game_state.current_player} ready to throw! Angle: {game_state.player_angle}, Force: {game_state.player_force}")
                                     
                        # Iniciar o arremesso da banana
                        game_state.banana_active = True
                        angle_rad = 0
                        # Ajustar o ângulo para a direção correta e converter para radianos
                        if game_state.current_player == 1: # Jogador 1 (esquerda) atira para a direita
                            # Ângulo 0 é para cima, 90 para a direita.
                            # O input do jogador é 0-90 para direita, 90-180 para esquerda (relativo ao gorila)
                            # Para o jogador 1, o ângulo de 0-90 é o que queremos.
                            angle_rad = math.radians(game_state.player_angle)
                            game_state.banana_x = game_state.PLAYER1_POS_X + game_state.GORILLA_WIDTH / 2 # Posição inicial da banana
                            game_state.banana_y = game_state.PLAYER1_POS_Y - game_state.GORILLA_HEIGHT / 2
                        else: # Jogador 2 (direita) atira para a esquerda
                            # Para o jogador 2, um ângulo de "0" (para ele) seria 180 graus no sistema de coordenadas.
                            # Um ângulo de "90" (para ele, para cima) seria 90 graus.
                            # Então, o ângulo real é 180 - player_angle
                            angle_rad = math.radians(180 - game_state.player_angle)
                            game_state.banana_x = game_state.PLAYER2_POS_X - game_state.GORILLA_WIDTH / 2
                            game_state.banana_y = game_state.PLAYER2_POS_Y - game_state.GORILLA_HEIGHT / 2
                        game_state.banana_vx = game_state.player_force * math.cos(angle_rad) / 15 # Aumentado o divisor para reduzir velocidade
                        game_state.banana_vy = -game_state.player_force * math.sin(angle_rad) / 15 # Aumentado o divisor para reduzir velocidade
                        game_state.game_phase = "THROWING"
                        if game_state.sound_throw:
                            game_state.sound_throw.play()
                        # TODO: Lógica para trocar de jogador ou iniciar o arremesso
                    else:
                        print("Force must be between 1 and 200.")
                        game_state.current_force_input_str = ""
                except ValueError:
                    # Input de força inválido
                    print("Invalid force input.")
                    game_state.current_force_input_str = ""
        # Lógica para backspace e digitação de números/ponto
        elif event.key == pygame.K_BACKSPACE:
            current_text_field = current_text_field[:-1]
        elif event.unicode.isdigit() or (event.unicode == '.' and '.' not in current_text_field):
            current_text_field += event.unicode

        # Atualiza o game_state com o texto modificado
        if game_state.active_input_field == "angle":
            game_state.current_angle_input_str = current_text_field
        elif game_state.active_input_field == "force":
            game_state.current_force_input_str = current_text_field