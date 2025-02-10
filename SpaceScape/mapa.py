import pygame
import sys
from coin import Coin  
from enemigo import Enemigo

# Inicializa Pygame
pygame.init()
pygame.mixer.init()
game_sound = pygame.mixer.music.load('sonidos/The Room 8 Bit Theme.mp3')
pygame.mixer.music.play(-1)  # -1 para reproducir en bucle
coin_sound = pygame.mixer.Sound('sonidos/blip-131856.mp3')  
game_over_sound = pygame.mixer.Sound('sonidos/ouch-116112.mp3')  
victorySound = pygame.mixer.Sound('sonidos/victory.mp3')

# Dimensiones de la pantalla
screen_width = 1920
screen_height = 1080

# Tamaño de cada tile y sprite
tile_size = 60
sprite_width = 64  # Ancho de cada cuadro de animación del sprite (ajustado)
sprite_height = 64  # Altura de cada cuadro de animación del sprite (ajustado)

# Crear la ventana
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mapa 1")

# Cargar la imagen del piso cuadriculado
floor_tile = pygame.image.load("sprites/piso.jpg").convert()

# Cargar la imagen de la pared
wall_tile = pygame.image.load("sprites/tile_wall.png").convert()

# Crear un mapa con varias habitaciones y pasillos
game_map = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WWWWWWWWWFFFFFFFFFFFFFFFFFFFFWWWWWWWWWWWWWWWWW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WWWWWWWWWFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WWWWWWWWWFFFFFFFFFFFFFFFFFFFFWWWWWWWWWWWWWWWWW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WWWWWWWWWFFFFFFFFFFFFFFFFFFFFWFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFW",
    "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
]

# Cargar la imagen del sprite
sprite_sheet = pygame.image.load("sprites/personaje.png").convert_alpha()
enemigo_sprite_sheet_original = pygame.image.load("sprites/alien.png").convert_alpha()

sprite_size = 64
frame_count = 4
directions_count = 4
enemigo_sprite_sheet = pygame.Surface((sprite_size * frame_count, sprite_size * directions_count), pygame.SRCALPHA)
for row in range(directions_count):
    for col in range(frame_count):
        sprite = enemigo_sprite_sheet_original.subsurface(pygame.Rect(col * 128, row * 128, 128, 128))
        sprite = pygame.transform.scale(sprite, (sprite_size, sprite_size))
        enemigo_sprite_sheet.blit(sprite, (col * sprite_size, row * sprite_size))

# Cargar la imagen de fondo
background_image = pygame.image.load("sprites/background.jpg").convert()

# Definir el personaje
player = pygame.Rect(800, 800, sprite_width, sprite_height)

# Velocidad de movimiento del personaje
player_speed = 5

# Posición inicial de la cámara
camera_x = 0
camera_y = 0

# Animación del personaje
directions = {
    'down': 0,
    'left': 1,
    'right': 2,
    'up': 3
}
current_direction = 'down'
current_frame = 0
animation_speed = 0.2
frame_count = 4

# Lista de monedas
coins = [
    Coin(100, 100),
    Coin(500, 500),
    Coin(800, 300),
    Coin(1500, 700),
    Coin(1700, 900)
]

enemigos = [
    Enemigo(200, 200, 2, enemigo_sprite_sheet, frame_count, 0.2, sprite_size=sprite_size),
    Enemigo(600, 400, 2, enemigo_sprite_sheet, frame_count, 0.2, sprite_size=sprite_size),
    Enemigo(1000, 800, 2, enemigo_sprite_sheet, frame_count, 0.2, sprite_size=sprite_size)
]

# Contador de monedas recolectadas
collected_coins = 0

# Caja para depositar las monedas
box_rect = pygame.Rect(30, 30, 60, 60)  # Caja situada en la esquina superior izquierda

# Cargar los sprites de la caja (cerrada y abierta)
box_closed_sprite = pygame.image.load("sprites/box.png").convert_alpha()
box_closed_sprite = pygame.transform.scale(box_closed_sprite, (60, 60))
box_open_sprite = pygame.image.load("sprites/box_open.png").convert_alpha()
box_open_sprite = pygame.transform.scale(box_open_sprite, (60, 60))

# Función para dibujar el mapa
def draw_map(surface, camera_x, camera_y):
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 'W':
                surface.blit(wall_tile, (x * tile_size - camera_x, y * tile_size - camera_y))
            else:
                surface.blit(floor_tile, (x * tile_size - camera_x, y * tile_size - camera_y))

# Función para dibujar el personaje
def draw_player(surface, x, y):
    global current_frame
    row = directions[current_direction]
    col = int(current_frame) % frame_count
    sprite = sprite_sheet.subsurface(pygame.Rect(col * sprite_width, row * sprite_height, sprite_width, sprite_height))
    surface.blit(sprite, (x, y))

# Función para dibujar la caja
def draw_box(surface, camera_x, camera_y):
    if player.colliderect(box_rect):
        surface.blit(box_open_sprite, (box_rect.x - camera_x, box_rect.y - camera_y))
    else:
        surface.blit(box_closed_sprite, (box_rect.x - camera_x, box_rect.y - camera_y))

def reiniciar_juego():
    global player, collected_coins, enemigos
    
    # Reiniciar posición del jugador
    player.x = 800
    player.y = 800
    
    # Reiniciar monedas recolectadas
    collected_coins = 0
    
    # Reiniciar posición de los enemigos
    enemigos = [
        Enemigo(200, 200, 2, enemigo_sprite_sheet, frame_count, 0.2, sprite_size=sprite_size),
        Enemigo(600, 400, 2, enemigo_sprite_sheet, frame_count, 0.2, sprite_size=sprite_size),
        Enemigo(1000, 800, 2, enemigo_sprite_sheet, frame_count, 0.2, sprite_size=sprite_size)
    ]

    # Reiniciar otros valores según sea necesario

def pantalla_fin_juego():
    # Rellenar la pantalla con un color
    screen.fill((0, 0, 0))  # Color negro
    
    # Mostrar mensaje de juego terminado
    font = pygame.font.Font(None, 72)
    text_surface = font.render("¡Juego Terminado!", True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.mixer.music.stop()
    game_over_sound.play() 
    pygame.time.wait(2000)
    
    # Mostrar opciones para reiniciar o salir
    font_small = pygame.font.Font(None, 36)
    restart_surface = font_small.render("Presiona 'R' para reiniciar", True, (255, 255, 255))
    restart_rect = restart_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
    screen.blit(restart_surface, restart_rect)
    
    quit_surface = font_small.render("Presiona 'Q' para salir", True, (255, 255, 255))
    quit_rect = quit_surface.get_rect(center=(screen_width // 2, screen_height // 2 + 100))
    screen.blit(quit_surface, quit_rect)

    
    pygame.display.flip()

    # Bucle para manejar eventos de teclado
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.play()
                    reiniciar_juego()  # Llamar a la función de reinicio
                    return True  # Reiniciar el juego
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()  # Salir del juego

def mostrar_mensaje_nivel():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 72)
    text_surface = font.render("¡Nivel 1 desbloqueado!", True, (0, 255, 0))
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Función para desbloquear el siguiente nivel
def unlock_next_level():
    pygame.mixer.music.stop()
    victorySound.play()
    mostrar_mensaje_nivel()
    import puzzle
    puzzle.start() 

clock = pygame.time.Clock()
running = True

# Bucle principal del juego
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()

    # Mover el personaje
    old_x, old_y = player.x, player.y
    moving = False

    if keys[pygame.K_LEFT]:
        player.x -= player_speed
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            current_direction = 'left'
        moving = True
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            current_direction = 'right'
        moving = True
    if keys[pygame.K_UP]:
        player.y -= player_speed
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            current_direction = 'up'
        moving = True
    if keys[pygame.K_DOWN]:
        player.y += player_speed
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            current_direction = 'down'
        moving = True

    # Animar el personaje solo si se está moviendo
    if moving:
        current_frame += animation_speed
    else:
        current_frame = 0

    # Colisiones con las paredes
    player_collided = False
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            if tile == 'W':
                wall_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if player.colliderect(wall_rect):
                    player_collided = True
                    break
        if player_collided:
            break

    if player_collided:
        player.x, player.y = old_x, old_y

    # Detectar recolección de monedas
    for coin in coins:
        if coin.collect(player):
            collected_coins += 1
            coin_sound.play()

    # Verificar si el jugador ha recolectado las monedas necesarias y las ha depositado en la caja
    if collected_coins >= 3:
        if player.colliderect(box_rect):
            unlock_next_level()
            collected_coins = 0  # Reiniciar el conteo de monedas para el próximo nivel

    # Verificar colisiones con los enemigos
    for enemigo in enemigos:
        enemigo.mover(player)
        if enemigo.rect.colliderect(player):
            # Mostrar pantalla de fin de juego
            if pantalla_fin_juego():
                # Reiniciar juego o volver a empezar nivel
                reiniciar_juego()  # Llamar a la función de reinicio
                
    # Actualizar la posición de la cámara
    camera_x = player.x - screen_width // 2 + player.width // 2
    camera_y = player.y - screen_height // 2 + player.height // 2

    # Mantener la cámara dentro de los límites del mapa
    max_camera_x = len(game_map[0]) * tile_size - screen_width
    max_camera_y = len(game_map) * tile_size - screen_height
    if camera_x < 0:
        camera_x = 0
    if camera_y < 0:
        camera_y = 0
    if camera_x > max_camera_x:
        camera_x = max_camera_x
    if camera_y > max_camera_y:
        camera_y = max_camera_y

    # Dibujar la imagen de fondo ajustada a la posición de la cámara
    screen.blit(background_image, (-camera_x, -camera_y))

    # Dibujar el mapa y el personaje en la pantalla
    draw_map(screen, camera_x, camera_y)
    for coin in coins:
        coin.draw(screen, camera_x, camera_y)
    draw_box(screen, camera_x, camera_y)
    draw_player(screen, player.x - camera_x, player.y - camera_y)

    # Dibujar enemigos
    for enemigo in enemigos:
        enemigo.dibujar(screen, camera_x, camera_y)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de los fotogramas
    clock.tick(60)

# Salir de Pygame
pygame.quit()
