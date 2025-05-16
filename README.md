## Gorilla Game (Pygame)

Um jogo simples no estilo clássico Gorilla.bas, implementado em Python usando a biblioteca Pygame.

Os jogadores se revezam atirando bananas em prédios, tentando acertar o gorila adversário. O vento afeta a trajetória da banana, e os prédios podem ser danificados.

### Como Rodar

1.  **Pré-requisitos:** Certifique-se de ter o Python instalado (versão 3.6+ recomendada).
2.  **Instalar Pygame:** Se você ainda não tem o Pygame, instale-o:
    ```bash
    pip install pygame
    ```
3.  **Navegar até o diretório do projeto:**
    ```bash
    cd ~/games/
    ```
4.  **Executar o jogo:**
    ```bash
    python -m gorilla.main
    ```

### Como Jogar

-   O jogo começa na tela inicial. Pressione qualquer tecla para iniciar.
-   Na sua vez, insira o **ângulo** (0-180) e a **força** (1-200) do seu arremesso quando solicitado na parte inferior da tela.
-   Pressione `Enter` após digitar cada valor.
-   Observe o indicador de vento no canto superior direito, ele afeta a trajetória da banana!
-   O primeiro jogador a acertar o gorila adversário vence.
-   Pressione `R` na tela de fim de jogo para reiniciar.

### Estrutura do Projeto

+-   `main.py`: Ponto de entrada principal, loop do jogo, inicialização.
+-   `game_state.py`: Armazena todas as variáveis de estado do jogo (posições, turno, fase, vento, prédios, etc.).
+-   `graphics.py`: Funções para desenhar todos os elementos na tela.
+-   `input_handler.py`: Processa eventos de input do jogador.
+-   `physics.py`: Lógica de física (gravidade, vento, movimento da banana, detecção de colisão).
+-   `assets/`: Diretório para recursos (sons, imagens).
+    -   `sounds/`: Arquivos `.wav` ou `.ogg` para efeitos sonoros.
+    -   `images/`: Arquivos `.png` para sprites.
+

### Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

*(Certifique-se de que os assets na pasta `assets/` também podem ser redistribuídos sob uma licença compatível, como CC0 ou CC BY.)*
