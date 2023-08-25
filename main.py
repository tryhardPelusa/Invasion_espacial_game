import pygame
import random
import math
from pygame import mixer
import time
import io


def fuente_bytes(fuente):
    # Abre el archivo TTF en modo lectura binaria
    with open(fuente, "rb") as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


# Iniciamos el Juego
pygame.init()

clock = pygame.time.Clock()
FPS = 60  # Número de fotogramas por segundo objetivo

# Creamos la pantalla
pantalla = pygame.display.set_mode((800, 600))
fondo = pygame.image.load("fondo.png")

# Título e icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("icon.png")
pygame.display.set_icon(icono)

# Musica de fondo
mixer.music.load("MusicaFondo.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.5)

# Jugador
img_jugador = pygame.image.load("navePrincipal.png")
jugador_x = 368
jugador_x_cambio = 0
jugador_y = 500
# jugador_y_cambio = 0

# Enemigo 1
img_enemigo1 = []
enemigo1_x = []
enemigo1_x_cambio = []
enemigo1_y = []
enemigo1_y_cambio = []
cantidad_enemigos1 = 4

for e in range(cantidad_enemigos1):
    img_enemigo1.append(random.choice([pygame.image.load("enemigo1.png"), pygame.image.load("enemigo2.png")]))
    enemigo1_x.append(random.randint(0, 736))
    enemigo1_x_cambio.append(5)
    enemigo1_y.append(random.randint(50, 200))
    enemigo1_y_cambio.append(50)

# Bala laser
balas = []
img_bala_laser = pygame.image.load("bala_laser.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 13
bala_visible = False
tiempo_entre_disparos = 0.5  # Tiempo mínimo en segundos entre disparos
ultimo_disparo_tiempo = 0.0  # Tiempo en que se disparó la última bala

# puntuacion
puntuacion = 0
fuente_como_bytes = fuente_bytes("freesansbold.ttf")
fuente = pygame.font.Font(fuente_como_bytes, 32)
texto_x = 10
texto_y = 10

# Texto final de juego
fuente_final = pygame.font.Font(fuente_como_bytes, 40)


def texto_final():
    mi_fuente_final = fuente_final.render(f"HAS PERDIDO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (280, 280))


# Funcion mostrar puntuacion
def mostrar_puntuacion(x, y):
    texto = fuente.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Generamos la imagen del jugador en su posición correcta
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Generamos la imagen del enemigo 1 en su posición correcta
def enemigo1(x, y, enemigo):
    pantalla.blit(img_enemigo1[enemigo], (x, y))


# Funcion disparar bala
def disparar(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala_laser, (x + 22, y + 10))


# Funcion para detectar colisiones
def haycolision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow((x_2 - x_1), 2) + math.pow((y_2 - y_1), 2))
    if distancia < 27:
        return True
    else:
        return False


# Eventos del juego
encendido = True
while encendido:

    clock.tick(FPS)  # Limitamos la velocidad de fotogramas

    pantalla.blit(fondo, (0, 0))

    # Leemos los eventos generados
    for evento in pygame.event.get():
        # Comprobamos si se cierra el juego
        if evento.type == pygame.QUIT:
            encendido = False
            continue

        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -10
            elif evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 10
            elif evento.key == pygame.K_UP:
                jugador_y_cambio = -7
            elif evento.key == pygame.K_DOWN:
                jugador_y_cambio = 7
            elif evento.key == pygame.K_SPACE:
                tiempo_actual = time.time()
                if tiempo_actual - ultimo_disparo_tiempo >= tiempo_entre_disparos:
                    ultimo_disparo_tiempo = tiempo_actual
                    bala_x = jugador_x
                    sonido_bala = mixer.Sound("disparo.mp3")
                    sonido_bala.play()
                    nueva_bala = {
                        "x": jugador_x,
                        "y": jugador_y,
                        "velocidad": -5
                    }
                    balas.append(nueva_bala)

        # Detenemos el movimiento del jugador
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
            if evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                jugador_y_cambio = 0

    # Llamada al jugador
    jugador_x += jugador_x_cambio

    # Mantener jugador dentro de los límites
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    if jugador_y <= 0:
        jugador_y = 0
    elif jugador_y >= 536:
        jugador_y = 536

    # movimiento bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala_laser, (bala["x"] + 22, bala["y"] + 10))
        if bala["y"] <= -64:
            balas.remove(bala)

    # Llamada al enemigo 1
    for e in range(cantidad_enemigos1):
        # Fin del juego
        if enemigo1_y[e] > 450:
            for k in range(cantidad_enemigos1):
                enemigo1_y[k] = 1000
            texto_final()
            balas.clear()
            break

        enemigo1_x[e] += enemigo1_x_cambio[e]

        # Mantener enemigo 1 dentro de los límites
        if enemigo1_x[e] <= 0:
            enemigo1_x_cambio[e] = 5
            enemigo1_y[e] += enemigo1_y_cambio[e]
        elif enemigo1_x[e] >= 736:
            enemigo1_x_cambio[e] = -5
            enemigo1_y[e] += enemigo1_y_cambio[e]

        # colision
        for bala in balas:
            colision1 = haycolision(enemigo1_x[e], enemigo1_y[e], bala["x"], bala["y"])
            if colision1:
                sonido_impacto = mixer.Sound("Golpe.mp3")
                sonido_impacto.play()
                bala_y = 500
                bala_visible = False
                puntuacion += 1
                enemigo1_x[e] = random.randint(0, 736)
                enemigo1_y[e] = random.randint(50, 200)

        enemigo1(enemigo1_x[e], enemigo1_y[e], e)

    jugador(jugador_x, jugador_y)

    # Mostrar puntuacion
    mostrar_puntuacion(texto_x, texto_y)

    # Actualizamos la pantalla
    pygame.display.update()
