# Dimensões da tela
import random
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cores (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_SKY = (135, 206, 235)
GREEN_GRASS = (34, 139, 34)
GRAY_BUILDING = (128, 128, 128)
BROWN_GORILLA = (139, 69, 19)
YELLOW_BANANA = (255, 255, 0)

# Paleta de cores para os prédios
BUILDING_COLORS = [
    (100, 100, 100), (110, 110, 110), (120, 120, 120),
    (130, 130, 130), (140, 140, 140), (90, 90, 90),
    (105, 105, 125), (115, 100, 100) # Tons levemente azulados ou avermelhados
]

# Constantes para as Janelas
WINDOW_LIT_COLOR = (255, 255, 100) # Amarelo claro para janelas acesas
WINDOW_UNLIT_COLOR = (60, 60, 80)   # Cinza escuro azulado para janelas apagadas
WINDOW_LIT_PROBABILITY = 0.3        # 30% de chance de uma janela estar acesa

WINDOW_WIDTH = 9
WINDOW_HEIGHT = 12
WINDOW_MARGIN_X = 5 # Espaço horizontal entre a borda do prédio e as janelas, e entre janelas
WINDOW_MARGIN_Y = 8 # Espaço vertical entre o topo/base do prédio e as janelas, e entre janelas

# Constantes do jogo
GORILLA_WIDTH = 50
GORILLA_HEIGHT = 50
GROUND_HEIGHT = 50
GRAVITY = 0.2  # Ajuste conforme necessário para a "sensação" do jogo

# Posições X e Y finais dos gorilas, calculadas após a geração dos prédios
PLAYER1_POS_X = 0
PLAYER1_POS_Y = 0
PLAYER2_POS_X = 0
PLAYER2_POS_Y = 0

# Estado do turno e input
current_player = 1  # 1 ou 2

# Valores de input atuais (como string, enquanto o jogador digita)
current_angle_input_str = ""
current_force_input_str = ""

# Valores finais de ângulo e força para o jogador atual
player_angle = 0.0
player_force = 0.0

active_input_field = "angle"  # "angle" ou "force"
game_phase = "TITLE_SCREEN"  # Novo estado inicial: "TITLE_SCREEN", "INPUT", "THROWING", "VICTORY_DELAY", "GAME_OVER"
victory_delay_start_time = 0
VICTORY_SOUND_DELAY_MS = 700 # Atraso de 700 milissegundos (0.7 segundos)
winner = 0 # 0: Ninguém, 1: Jogador 1, 2: Jogador 2

# Placar
player1_score = 0
player2_score = 0

# Estado da Banana
banana_active = False
banana_x = 0.0
banana_y = 0.0
banana_vx = 0.0 # Velocidade horizontal
banana_vy = 0.0 # Velocidade vertical
BANANA_RADIUS = 5

# Lista para armazenar os dados dos prédios: [(x, y_topo, largura, altura, cor), ...]
BUILDINGS = []

# Caminhos para os arquivos de som (relativos à raiz do projeto, as sumindo que main.py está em gorilla_game)
# Ajuste os nomes dos arquivos se os seus forem diferentes.
SOUND_FILE_THROW = "assets/sounds/throw.wav"
SOUND_FILE_EXPLOSION = "assets/sounds/explosion.wav"
SOUND_FILE_VICTORY = "assets/sounds/victory.wav"

# Variáveis para armazenar os objetos de som carregados
sound_throw = None
sound_explosion = None
sound_victory = None

# Caminhos para os arquivos de imagem
IMAGE_FILE_GORILLA = "assets/images/gorilla.png"
IMAGE_FILE_BANANA = "assets/images/banana.png"
IMAGE_FILE_EXPLOSION = "assets/images/explosion.png" # Carregaremos, mas não usaremos ainda

# Variáveis para armazenar os objetos de imagem carregados
gorilla_image = None
gorilla_image_flipped = None # Para o jogador 2
banana_image = None
explosion_image = None # Para uso futuro
explosion_image_scaled = None # Imagem da explosão escalonada

# Estado da Explosão
explosion_active = False
explosion_x, explosion_y = 0, 0
explosion_start_time = 0
EXPLOSION_DURATION_MS = 300 # Duração da explosão em milissegundos (0.3 segundos)
# Estado do Jogo (Controle de Fluxo)
quit_requested = False # Flag para sinalizar que o jogador quer sair

# Estado do Vento
wind_speed = 0.0  # Positivo para direita, negativo para esquerda
MAX_WIND_SPEED = 0.05 # Quão forte o vento pode ser (afeta a aceleração da banana)
MIN_WIND_FOR_DISPLAY = 0.01 # Velocidade mínima para mostrar o vento

def generate_buildings():
    """Gera prédios aleatórios para o cenário."""
    global BUILDINGS
    BUILDINGS = []
    current_x = 0
    min_width, max_width = 50, 100
    min_height, max_height = 50, SCREEN_HEIGHT - GROUND_HEIGHT - 100 # Deixa espaço para o céu

    while current_x < SCREEN_WIDTH:
        width = random.randint(min_width, max_width)
        if current_x + width > SCREEN_WIDTH: # Garante que o último prédio não ultrapasse a tela
            width = SCREEN_WIDTH - current_x
        height = random.randint(min_height, max_height)
        y_top = SCREEN_HEIGHT - GROUND_HEIGHT - height
        color = random.choice(BUILDING_COLORS)

        # Gera o padrão de janelas acesas/apagadas para este prédio
        window_lit_pattern = []
        # Calcula a área e itera como em graphics.py para saber quantas janelas cabem
        # e gerar um estado (acesa/apagada) para cada uma.
        window_area_x_start_gs = current_x + WINDOW_MARGIN_X
        window_area_y_start_gs = y_top + WINDOW_MARGIN_Y

        if (width - 2 * WINDOW_MARGIN_X >= WINDOW_WIDTH and
            height - 2 * WINDOW_MARGIN_Y >= WINDOW_HEIGHT):
            for _wy in range(window_area_y_start_gs, y_top + height - WINDOW_MARGIN_Y - WINDOW_HEIGHT + 1, WINDOW_HEIGHT + WINDOW_MARGIN_Y):
                for _wx in range(window_area_x_start_gs, current_x + width - WINDOW_MARGIN_X - WINDOW_WIDTH + 1, WINDOW_WIDTH + WINDOW_MARGIN_X):
                    window_lit_pattern.append(random.random() < WINDOW_LIT_PROBABILITY)
        
        BUILDINGS.append((current_x, y_top, width, height, color, window_lit_pattern))

        current_x += width

def place_gorillas_on_buildings():
    """Coloca os gorilas no topo de prédios selecionados."""
    global PLAYER1_POS_X, PLAYER1_POS_Y, PLAYER2_POS_X, PLAYER2_POS_Y

    if not BUILDINGS:
        print("Aviso: Nenhum prédio gerado para posicionar os gorilas.")
        return

    num_buildings = len(BUILDINGS)

    # Seleciona prédio para o Jogador 1
    # Tenta colocar no segundo prédio, ou no primeiro se houver poucos.
    p1_building_index = 1 if num_buildings > 1 else 0
    if p1_building_index >= num_buildings: # Fallback para o último se o índice for inválido
        p1_building_index = num_buildings -1
        
    b1_x, b1_y_top, b1_width, _, _, _ = BUILDINGS[p1_building_index] # Ignora altura, cor e padrão de janelas
    PLAYER1_POS_X = b1_x + b1_width // 2
    PLAYER1_POS_Y = b1_y_top

    # Seleciona prédio para o Jogador 2
    # Tenta colocar no penúltimo prédio, ou no último se houver poucos.
    p2_building_index = num_buildings - 2 if num_buildings > 1 else num_buildings - 1
    if p2_building_index < 0 : # Fallback para o primeiro se o índice for inválido
         p2_building_index = 0
    if p2_building_index == p1_building_index and num_buildings > 1: # Evita mesmo prédio se possível
        p2_building_index = (p1_building_index + 1) % num_buildings

    b2_x, b2_y_top, b2_width, _, _, _ = BUILDINGS[p2_building_index] # Ignora altura, cor e padrão de janelas
    PLAYER2_POS_X = b2_x + b2_width // 2
    PLAYER2_POS_Y = b2_y_top

def generate_new_wind():
    """Gera uma nova velocidade de vento aleatória."""
    global wind_speed
    # Gera um valor entre -MAX_WIND_SPEED e MAX_WIND_SPEED
    wind_speed = random.uniform(-MAX_WIND_SPEED, MAX_WIND_SPEED)
    print(f"Novo vento gerado: {wind_speed:.3f}")

def switch_player_turn():
    """Alterna o jogador atual e reseta o estado para o novo turno."""
    global current_player, current_angle_input_str, current_force_input_str, active_input_field, game_phase
    
    current_player = 2 if current_player == 1 else 1
    current_angle_input_str = ""
    current_force_input_str = ""
    active_input_field = "angle"
    game_phase = "INPUT" # Volta para INPUT após trocar o turno
    generate_new_wind() # Gera novo vento a cada turno
    print(f"--- Trocando para o turno do Jogador {current_player} ---")

def reset_game():
    """Reseta o estado do jogo para uma nova partida."""
    global current_player, current_angle_input_str, current_force_input_str
    global active_input_field, game_phase, winner, banana_active, victory_delay_start_time, explosion_active, quit_requested

    print("--- Reiniciando o Jogo ---")
    generate_buildings()
    place_gorillas_on_buildings()
    current_player = 1
    current_angle_input_str = ""
    current_force_input_str = ""
    active_input_field = "angle"
    game_phase = "INPUT" # Volta para INPUT após reiniciar
    winner = 0
    banana_active = False
    victory_delay_start_time = 0
    explosion_active = False
    quit_requested = False # Reseta a flag de sair
    generate_new_wind()