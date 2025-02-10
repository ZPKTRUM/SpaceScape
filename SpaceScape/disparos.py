import pygame
import random
import sys
from fractions import Fraction

# Inicializar Pygame
pygame.init()
pygame.mixer.music.load('sonidos/battle.mp3')  # Música en bucle
sonido_game_over = pygame.mixer.Sound('sonidos/ouch-116112.mp3')
sonido_disparo = pygame.mixer.Sound('sonidos/laser-gun-81720.mp3')
sonido_victoria = pygame.mixer.Sound('sonidos/victory.mp3')

# Iniciar la música en bucle
pygame.mixer.music.play(-1)

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Dimensiones de la ventana
ventana_ancho = 1920
ventana_alto = 1080
ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))
pygame.display.set_caption("Shooter con problemas matemáticos")
fondo = pygame.image.load("sprites/hola.png").convert() 
fondo = pygame.transform.scale(fondo, (ventana_ancho, ventana_alto))

# Jugador
jugador_ancho = 50
jugador_alto = 50
jugador_x = ventana_ancho // 2 - jugador_ancho // 2
jugador_y = ventana_alto - 100 - jugador_alto
jugador_velocidad = 5
jugador_salto = False
jugador_visible = True
jugador_rect = pygame.Rect(jugador_x, jugador_y, jugador_ancho, jugador_alto)
jugador_vida = 100
velocidad_vertical_jugador = 0
gravedad = 0.5
velocidad_salto = -10
tamaño_enemigo_ancho = int(jugador_ancho * 3.0)
tamaño_enemigo_alto = int(jugador_alto * 3.0)
jugador_derecha = pygame.image.load('sprites/monito_derecha.png').convert_alpha()
jugador_izquierda = pygame.transform.flip(jugador_derecha, True, False)
enemigo_derecha = pygame.image.load('sprites/otromonobonito.png').convert_alpha()
enemigo_derecha = pygame.transform.scale(enemigo_derecha, (tamaño_enemigo_ancho, tamaño_enemigo_alto))
enemigo_izquierda = pygame.transform.flip(enemigo_derecha, True, False)

# Enemigos
enemigo_ancho = 55
enemigo_alto = 55
velocidad_enemigo = 2
enemigos = []

# Disparos
disparo_ancho = 20
disparo_alto = 20
disparo_velocidad = 10
disparos = []
enemigo_disparos = []
direccion_disparo = 1
disparo_enemigo_velocidad = 7
tiempo_espera_disparo_enemigo = 0
tiempo_espera_max_disparo_enemigo = 50
bala_sprite = pygame.image.load('sprites/bala.png').convert_alpha()
bala_sprite = pygame.transform.scale(bala_sprite, (disparo_ancho, disparo_alto))

# Rondas
ronda = 1

# Función para dibujar la barra de vida
def dibujar_barra_vida(surface, x, y, vida, color):
    longitud_barra = 100
    altura_barra = 10
    if vida < 0:
        vida = 0
    longitud_vida = (vida / 100) * longitud_barra
    pygame.draw.rect(surface, NEGRO, (x, y, longitud_barra, altura_barra), 0)
    pygame.draw.rect(surface, color, (x, y, longitud_vida, altura_barra), 0)

# Función mejorada para mostrar un mensaje en la pantalla del juego
def mostrar_mensaje(mensaje, color, tamaño, y_offset=0):
    fuente = pygame.font.Font(None, tamaño)
    texto = fuente.render(mensaje, True, color)
    texto_borde = fuente.render(mensaje, True, NEGRO)
    texto_rect = texto.get_rect()
    texto_rect.center = (ventana_ancho // 2, ventana_alto // 2 + y_offset)
    ventana.blit(texto_borde, (texto_rect.x - 2, texto_rect.y - 2))
    ventana.blit(texto_borde, (texto_rect.x + 2, texto_rect.y - 2))
    ventana.blit(texto_borde, (texto_rect.x - 2, texto_rect.y + 2))
    ventana.blit(texto_borde, (texto_rect.x + 2, texto_rect.y + 2))
    ventana.blit(texto, texto_rect)

# Función para verificar si todos los enemigos han sido derrotados
def enemigos_derrotados():
    for enemigo in enemigos:
        if enemigo['visible']:
            return False
    return True

# Función para generar una pregunta matemática
def generar_pregunta():
    if ronda == 3:
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        c = random.randint(1, 10)
        x = random.randint(1, 10)
        ecuacion = f"{a}x + {b} = {c}"
        respuesta_correcta = (c - b) / a
        return f"Resuelve la ecuación para x: {ecuacion}", respuesta_correcta
    else:
        operador = random.choice(['+', '-', '*'])
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        if operador == '+':
            respuesta = num1 + num2
        elif operador == '-':
            respuesta = num1 - num2
        else:
            respuesta = num1 * num2
        return f"{num1} {operador} {num2} =", respuesta

# Función para mostrar la pregunta matemática y verificar la respuesta
def mostrar_pregunta_y_verificar():
    pregunta, respuesta_correcta = generar_pregunta()
    entrada_usuario = ""
    intentos = 0
    while True:
        ventana.fill(NEGRO)
        mostrar_mensaje("Responde la pregunta para continuar:", BLANCO, 36, y_offset=-100)
        mostrar_mensaje(pregunta, BLANCO, 48)
        mostrar_mensaje(entrada_usuario, BLANCO, 48, y_offset=100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        respuesta_usuario = eval(entrada_usuario.replace('x', '*1'))
                        respuesta_usuario_frac = Fraction(respuesta_usuario)
                        respuesta_correcta_frac = Fraction(respuesta_correcta)
                        if respuesta_usuario_frac == respuesta_correcta_frac:
                            return True
                        else:
                            intentos += 1
                            entrada_usuario = ""
                            mostrar_mensaje("Respuesta incorrecta, intenta de nuevo.", ROJO, 36, y_offset=200)
                            pygame.display.update()
                            pygame.time.wait(2000)
                    except:
                        intentos += 1
                        entrada_usuario = ""
                        mostrar_mensaje("Entrada inválida, intenta de nuevo.", ROJO, 36, y_offset=200)
                        pygame.display.update()
                        pygame.time.wait(2000)
                elif event.key == pygame.K_BACKSPACE:
                    entrada_usuario = entrada_usuario[:-1]
                else:
                    entrada_usuario += event.unicode

# Función para iniciar una nueva ronda
def nueva_ronda(inicial=False):
    global ronda, enemigos, jugador_vida, tiempo_espera_disparo_enemigo, jugador_visible
    if not inicial:
        if not mostrar_pregunta_y_verificar():
            jugador_vida -= 20
            if jugador_vida <= 0:
                jugador_vida = 0
                jugador_visible = False
                if pantalla_fin_juego():
                    jugador_visible = True
                    nueva_ronda(inicial=True)
                    ventana.fill(NEGRO)
                    mostrar_mensaje(f"Ronda {ronda}", BLANCO, 72)
                    pygame.display.update()
                    pygame.time.wait(2000)
                else:
                    sys.exit()
        ronda += 1
    else:
        ronda = 1
    jugador_vida = 100
    tiempo_espera_disparo_enemigo = 0
    enemigos.clear()
    for _ in range(ronda):
        enemigo_x = random.randint(0, ventana_ancho - enemigo_ancho)
        enemigo_y = ventana_alto - 100 - enemigo_alto
        enemigos.append({
            'rect': pygame.Rect(enemigo_x, enemigo_y, enemigo_ancho, enemigo_alto),
            'vida': 100,
            'visible': True,
            'velocidad_vertical': 0,
            'salto': False
        })

# Inicializar la primera ronda
nueva_ronda(inicial=True)

# Mostrar mensaje "Ronda 1"
ventana.fill(NEGRO)
mostrar_mensaje(f"Ronda {ronda}", BLANCO, 72)
pygame.display.update()
pygame.time.wait(2000)

def pantalla_fin_juego():
    ventana.fill(NEGRO)
    pygame.mixer.music.stop()  # Detener la música en bucle
    sonido_game_over.play()  # Reproducir sonido de "game over"
    mostrar_mensaje("¡Juego Terminado!", ROJO, 72)
    pygame.display.update()
    pygame.time.wait(2000)
    mostrar_mensaje("Presiona 'R' para reiniciar o 'Q' para salir.", BLANCO, 36, y_offset=50)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.music.play(-1)
                    return True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        


game_over = False
clock = pygame.time.Clock()
direccion_disparo = 1  
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    
    
    ventana.blit(fondo, (0, 0))        
    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        jugador_x -= jugador_velocidad
        jugador_x = max(jugador_x, 0)
        direccion_disparo = -1
    if teclas[pygame.K_RIGHT]:
        jugador_x += jugador_velocidad
        jugador_x = min(jugador_x, ventana_ancho - jugador_ancho)
        direccion_disparo = 1

    if teclas[pygame.K_UP] and not jugador_salto:
        velocidad_vertical_jugador = velocidad_salto
        jugador_salto = True

    if teclas[pygame.K_SPACE]:
     if len(disparos) < 3:
        nuevo_disparo = pygame.Rect(jugador_x + jugador_ancho // 2 - disparo_ancho // 2, jugador_y + jugador_alto - disparo_alto, disparo_ancho, disparo_alto)
        disparos.append({'rect': nuevo_disparo, 'direccion': direccion_disparo})
        sonido_disparo.play()

    velocidad_vertical_jugador += gravedad
    jugador_y += velocidad_vertical_jugador

    if jugador_y > ventana_alto - 100 - jugador_alto:
        jugador_y = ventana_alto - 100 - jugador_alto
        velocidad_vertical_jugador = 0
        jugador_salto = False

    jugador_rect.x = jugador_x
    jugador_rect.y = jugador_y

    for enemigo in enemigos:

        if jugador_x < enemigo['rect'].x:
            enemigo['rect'].x -= velocidad_enemigo
        elif jugador_x > enemigo['rect'].x:
            enemigo['rect'].x += velocidad_enemigo

        if not enemigo['salto']:
            if random.random() < 0.05:
                enemigo['velocidad_vertical'] = velocidad_salto
                enemigo['salto'] = True

        enemigo['velocidad_vertical'] += gravedad
        enemigo['rect'].y += enemigo['velocidad_vertical']

        if enemigo['rect'].y > ventana_alto - 100 - enemigo_alto:
            enemigo['rect'].y = ventana_alto - 100 - enemigo_alto
            enemigo['velocidad_vertical'] = 0
            enemigo['salto'] = False

        if random.random() < 0.01 and tiempo_espera_disparo_enemigo >= tiempo_espera_max_disparo_enemigo:
            nuevo_disparo_enemigo = pygame.Rect(enemigo['rect'].x + enemigo_ancho // 2 - disparo_ancho // 2, enemigo['rect'].y + enemigo_alto // 2 - disparo_alto // 2, disparo_ancho, disparo_alto)
            enemigo_disparos.append({'rect': nuevo_disparo_enemigo, 'direccion': -1 if jugador_x < enemigo['rect'].x else 1})
            tiempo_espera_disparo_enemigo = 0
            sonido_disparo.play()

        # Comprobación de colisión entre enemigos
        for otro_enemigo in enemigos:
            if otro_enemigo != enemigo and enemigo['rect'].colliderect(otro_enemigo['rect']):
                if enemigo['rect'].x < otro_enemigo['rect'].x:
                    enemigo['rect'].x -= velocidad_enemigo
                    otro_enemigo['rect'].x += velocidad_enemigo
                else:
                    enemigo['rect'].x += velocidad_enemigo
                    otro_enemigo['rect'].x -= velocidad_enemigo

        # Comprobación de colisión con el jugador
        if jugador_rect.colliderect(enemigo['rect']):
            if jugador_x < enemigo['rect'].x:
                enemigo['rect'].x += velocidad_enemigo
            else:
                enemigo['rect'].x -= velocidad_enemigo

            if jugador_y < enemigo['rect'].y:
                enemigo['rect'].y += velocidad_enemigo
            else:
                enemigo['rect'].y -= velocidad_enemigo

    tiempo_espera_disparo_enemigo += 1

    for disparo in disparos:
        disparo['rect'].x += disparo_velocidad * disparo['direccion']
        if disparo['rect'].x < 0 or disparo['rect'].x > ventana_ancho:
            disparos.remove(disparo)

    for disparo_enemigo in enemigo_disparos:
        disparo_enemigo['rect'].x += disparo_enemigo_velocidad * disparo_enemigo['direccion']
        if disparo_enemigo['rect'].x < 0 or disparo_enemigo['rect'].x > ventana_ancho:
            enemigo_disparos.remove(disparo_enemigo)

    for disparo_enemigo in enemigo_disparos:
        if jugador_rect.colliderect(disparo_enemigo['rect']):
            jugador_vida -= 10
            enemigo_disparos.remove(disparo_enemigo)
            if jugador_vida <= 0:
                jugador_visible = False
                if pantalla_fin_juego():
                    jugador_visible = True
                    nueva_ronda(inicial=True)
                    ventana.fill(NEGRO)
                    mostrar_mensaje(f"Ronda {ronda}", BLANCO, 72)
                    pygame.display.update()
                    pygame.time.wait(2000)
                else:
                    game_over = True

    for disparo in disparos:
        for enemigo in enemigos:
            if enemigo['visible'] and disparo['rect'].colliderect(enemigo['rect']):
                enemigo['vida'] -= 10
                if disparo in disparos:
                    disparos.remove(disparo)
                else: 
                    print(f"Disparo {disparo} procesado epicamente .")
                if enemigo['vida'] <= 0:
                    enemigo['visible'] = False

    ventana.blit(fondo, (0, 0))

    # Dibujar jugador con el sprite adecuado
    if jugador_visible:
        if direccion_disparo == 1:
            ventana.blit(jugador_derecha, (jugador_x, jugador_y))
        else:
            ventana.blit(jugador_izquierda, (jugador_x, jugador_y))

    for enemigo in enemigos:
        if enemigo['visible']:
            if jugador_x < enemigo['rect'].x:
                ventana.blit(enemigo_izquierda, (enemigo['rect'].x, enemigo['rect'].y))
            else:
                ventana.blit(enemigo_derecha, (enemigo['rect'].x, enemigo['rect'].y))
            dibujar_barra_vida(ventana, enemigo['rect'].x, enemigo['rect'].y - 10, enemigo['vida'], ROJO)

    # Dibujar las balas del jugador con el sprite
    for disparo in disparos:
        ventana.blit(bala_sprite, (disparo['rect'].x, disparo['rect'].y))

    # Dibujar las balas de los enemigos con el sprite (si quieres usar el mismo sprite)
    for disparo_enemigo in enemigo_disparos:
        ventana.blit(bala_sprite, (disparo_enemigo['rect'].x, disparo_enemigo['rect'].y))

    dibujar_barra_vida(ventana, 10, 10, jugador_vida, VERDE)

    if enemigos_derrotados():
        if ronda >= 4:
            pygame.mixer.music.stop()
            sonido_victoria.play()
            mostrar_mensaje("¡Victoria!", VERDE, 72)
            pygame.display.update()
            pygame.time.wait(5000)
            import mapa3
            mapa3.start()

        else:
            mostrar_mensaje(f"¡Ronda {ronda} completada!", BLANCO, 48)
            pygame.display.update()
            pygame.time.wait(2000)
            nueva_ronda()
            ventana.fill(NEGRO)
            mostrar_mensaje(f"Ronda {ronda}", BLANCO, 72)
            pygame.display.update()
            pygame.time.wait(2000)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()