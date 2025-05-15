import pygame
from . import graphics # Importa o módulo graphics do pacote atual
from . import game_state # Importa o módulo game_state do pacote atual
from . import input_handler # Importa o novo input_handler
from . import physics # Importa o módulo de física

def main():
    pygame.init()
    pygame.mixer.init() # Inicializa o módulo de som
    pygame.font.init() # Inicializa o módulo de fontes

    # Configura a fonte para a UI (pode ser ajustado)
    graphics.UI_FONT = pygame.font.SysFont("monospace", 18)
    
    screen = pygame.display.set_mode((game_state.SCREEN_WIDTH, game_state.SCREEN_HEIGHT))
    pygame.display.set_caption("Gorilla Game Refactor")

    # Carrega os sons
    try:
        game_state.sound_throw = pygame.mixer.Sound(game_state.SOUND_FILE_THROW)
        game_state.sound_explosion = pygame.mixer.Sound(game_state.SOUND_FILE_EXPLOSION)
        game_state.sound_victory = pygame.mixer.Sound(game_state.SOUND_FILE_VICTORY)
    except (pygame.error, FileNotFoundError) as e:
        print(f"Erro ao carregar um ou mais arquivos de som: {e}")
        print("Verifique se os arquivos .wav ou .ogg estão em gorilla_game/assets/sounds/")
        print(f"Esperado: {game_state.SOUND_FILE_THROW}")
        print(f"Esperado: {game_state.SOUND_FILE_EXPLOSION}")
        print(f"Esperado: {game_state.SOUND_FILE_VICTORY}")
        # O jogo continuará sem sons se eles não puderem ser carregados

    # Carrega as imagens
    try:
        # Gorila
        loaded_gorilla_img = pygame.image.load(game_state.IMAGE_FILE_GORILLA).convert_alpha()
        game_state.gorilla_image = pygame.transform.scale(loaded_gorilla_img, (game_state.GORILLA_WIDTH, game_state.GORILLA_HEIGHT))
        game_state.gorilla_image_flipped = pygame.transform.flip(game_state.gorilla_image, True, False) # Espelha horizontalmente

        # Banana (vamos definir um tamanho fixo para a banana por enquanto)
        banana_width, banana_height = 15, 15 # Ajuste conforme necessário
        loaded_banana_img = pygame.image.load(game_state.IMAGE_FILE_BANANA).convert_alpha()
        game_state.banana_image = pygame.transform.scale(loaded_banana_img, (banana_width, banana_height))
        # Atualiza o BANANA_RADIUS para corresponder à metade da largura da imagem da banana, para colisões
        game_state.BANANA_RADIUS = banana_width // 2

        # Explosão
        loaded_explosion_img = pygame.image.load(game_state.IMAGE_FILE_EXPLOSION).convert_alpha()
        explosion_size = 60 # Tamanho da explosão, ajuste conforme necessário
        game_state.explosion_image_scaled = pygame.transform.scale(loaded_explosion_img, (explosion_size, explosion_size))

    except (pygame.error, FileNotFoundError) as e:
        print(f"Erro ao carregar um ou mais arquivos de imagem: {e}")
        print("Verifique se os arquivos .png estão em gorilla_game/assets/images/")
        # O jogo continuará com os placeholders se as imagens não puderem ser carregadas

    # A geração de prédios, posicionamento de gorilas e vento inicial
    # foi movida para DENTRO do loop de eventos, quando se sai da TITLE_SCREEN.
    # game_state.generate_buildings()
    # game_state.place_gorilas_on_buildings()
    # game_state.generate_new_wind()
    clock = pygame.time.Clock()
    running = True

    
    while running:
        # Verifica se o jogador pediu para sair (através do input_handler)
        if game_state.quit_requested:
            running = False
            continue # Pula o resto do loop e sai
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Processa input dependendo da fase do jogo
            if game_state.game_phase == "TITLE_SCREEN":
                # Qualquer tecla pressionada inicia o jogo
                if event.type == pygame.KEYDOWN:
                    game_state.generate_buildings() # Gera prédios
                    game_state.place_gorillas_on_buildings() # Posiciona gorilas
                    game_state.generate_new_wind() # Gera vento inicial
                    game_state.game_phase = "INPUT" # Muda para a fase de input
                    print("Jogo iniciado!")
            elif game_state.game_phase == "INPUT" or game_state.game_phase == "GAME_OVER":
                # Processa input normal do jogo ou input de restart
                input_handler.process_player_input(event)

        # Lógica de atualização do jogo
        if game_state.game_phase == "THROWING":
            physics.update_banana_position()
            # Se a banana se tornou inativa (colidiu, saiu da tela),
            # a função update_banana_position já mudou game_phase para "INPUT" ou "VICTORY_DELAY"
        elif game_state.game_phase == "VICTORY_DELAY":
            current_time = pygame.time.get_ticks()
            if current_time - game_state.victory_delay_start_time > game_state.VICTORY_SOUND_DELAY_MS:
                # Toca o som de vitória após o delay e muda para GAME_OVER
                if game_state.sound_victory:
                    game_state.sound_victory.play()
                game_state.game_phase = "GAME_OVER"


        # Desenho
        if game_state.game_phase == "TITLE_SCREEN":
            graphics.draw_title_screen(screen) # Desenha a tela inicial
        else: # Desenha a cena do jogo em qualquer outra fase
            graphics.draw_scene(screen) # Desenha prédios, chão, céu, gorilas
            if game_state.banana_active: # Desenha a banana apenas se estiver ativa
                graphics.draw_banana(screen)
            graphics.draw_input_ui(screen) # Desenha a UI de input (ângulo/força)
            if game_state.game_phase == "GAME_OVER":
                graphics.draw_game_over_message(screen) # Desenha a mensagem de Game Over
            if game_state.explosion_active: # Desenha a explosão se estiver ativa
                graphics.draw_explosion(screen)
            graphics.draw_wind_indicator(screen) # Desenha o indicador de vento
        
        pygame.display.flip() # Atualiza a tela inteira

        clock.tick(60) # Limita a 60 FPS

    pygame.quit()

if __name__ == '__main__':
    main()