import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Brick Breaker")

# Función para mostrar la pantalla de inicio
def pantalla_inicio():
    inicio = True
    while inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if 400 <= pos[0] <= 600 and 300 <= pos[1] <= 350:
                    inicio = False
                if 400 <= pos[0] <= 600 and 400 <= pos[1] <= 450:
                    # Botón de "Salir" presionado
                    pygame.quit()
                    sys.exit()

        screen.fill((0, 0, 0))  # Fondo negro
        font = pygame.font.Font(None, 36)
        mensaje = font.render("Presiona el botón para comenzar", True, (255, 255, 255))
        screen.blit(mensaje, (300, 200))

        # Dibuja el botón de "Comenzar"
        pygame.draw.rect(screen, (185, 225, 185), (400, 300, 200, 44))
        font = pygame.font.Font(None, 32)
        mensaje = font.render("Comenzar", True, (0, 0, 0))
        screen.blit(mensaje, (450, 312))

        # Dibuja el botón de "Salir"
        pygame.draw.rect(screen, (185, 0, 0), (400, 400, 200, 44))
        mensaje = font.render("Salir", True, (255, 255, 255))
        screen.blit(mensaje, (470, 412))

        pygame.display.flip()

pantalla_inicio()

# Musica Fondo
BackgrounMusic = pygame.mixer.Sound('sounds/spacesong.mp3')
BackgrounMusic.play(-1)
# Cargar el sonido para cuando la pelota golpee la raqueta
sound_pelota_raqueta = pygame.mixer.Sound('sounds/golpe.mp3')

# Colores de raqueta, pelota
raqueta = (196, 188, 238)
pelota = (0, 208, 238)

# Cargar la imagen de fondo
background = pygame.image.load('img/Space.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
angle = 0  # Ángulo de rotación inicial

# Configuración de la raqueta
paddle_width = 140
paddle_height = 15
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height

# Restringir los límites de movimiento de la raqueta
paddle_speed = 10

# Configuración de la pelota
ball_radius = 10
ball_x = random.randint(ball_radius, screen_width - ball_radius)
ball_y = paddle_y - 2 * ball_radius
ball_speed_x = 6
ball_speed_y = -6

# Restringir los límites de movimiento de la pelota
ball_speed_limit = 9

# Configuración de los ladrillos
brick_width = 80
brick_height = 20
bricks = []

# Función para generar colores RGB aleatorios
def generate_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Función para generar ladrillos aleatorios
def generar_ladrillos():
    shuffle_bricks()
    bricks.clear()  # Borra todos los ladrillos existentes
    for row in range(5):
        for col in range(12):
            brick_x = col * (brick_width + 5)
            brick_y = row * (brick_height + 5)
            brick_color = generate_random_color()
            bricks.append([brick_x, brick_y, brick_color])

# Game loop
clock = pygame.time.Clock()
game_over = False

def shuffle_bricks():
    random.shuffle(bricks)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= paddle_speed
        # Restringir la raqueta para que no salga de la pantalla
        paddle_x = max(0, paddle_x)
    if keys[pygame.K_RIGHT]:
        paddle_x += paddle_speed
        # Restringir la raqueta para que no salga de la pantalla
        paddle_x = min(screen_width - paddle_width, paddle_x)

    # Actualizar la posición de la pelota
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Comprobar colisiones con la pared izquierda y derecha
    if ball_x <= ball_radius or ball_x >= screen_width - ball_radius:
        ball_speed_x = -ball_speed_x

    # Comprobar colisión con la pared superior
    if ball_y <= ball_radius:
        ball_speed_y = -ball_speed_y

    # Comprobar colisión con la raqueta
    if (
        ball_y + ball_radius >= paddle_y
        and paddle_x - ball_radius <= ball_x <= paddle_x + paddle_width + ball_radius
    ):
        # Cambiar solo la dirección vertical hacia arriba
        ball_speed_y = -ball_speed_y

    # Reproducir el sonido al golpear la raqueta
    sound_pelota_raqueta.play()

    # Verificar colisiones con los ladrillos
    for brick in bricks:
        if (
            brick[0] <= ball_x <= brick[0] + brick_width
            and brick[1] <= ball_y <= brick[1] + brick_height
        ):
            ball_speed_y = -ball_speed_y
            bricks.remove(brick)

    # Limpiar la pantalla
    screen.fill((0, 0, 0))  # Limpia la pantalla con un fondo negro

    # Dibujar la raqueta
    pygame.draw.rect(screen, raqueta, (paddle_x, paddle_y, paddle_width, paddle_height))

    # Dibujar la pelota
    pygame.draw.circle(screen, pelota, (ball_x, ball_y), ball_radius)

    # Dibujar los ladrillos restantes
    for brick in bricks:
        pygame.draw.rect(screen, brick[2], (brick[0], brick[1], brick_width, brick_height))

    pygame.display.flip()
    # Hace que la bolita se mueva a velocidad
    clock.tick(60)

    # Condición de victoria
    if len(bricks) == 0: 
        generar_ladrillos()

    # Condición de derrota 
    if ball_y > screen_height:
        pantalla_inicio()

# Cerrar Pygame
pygame.quit()
sys.exit()
