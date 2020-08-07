#Autor: Eric Andrés Jardón Chao, A10376748
#Descripción: Código fuente para el minijuego: Cat&Mouse
#Huye del gato y atrapa tantos quesos puedas. La vida del jugador decrece conforme pasa hambre sin comer un queso.
# Si se sale la pantalla su vida decrece más rápidamente.
#No se puede deslizar a lo largo de las paredes, tiene que separarse de ellas para continuar moviéndose.
#Versión 1.0 finalizada el 13 de mayo de 2019

import pygame   # Librería de pygame
import random

# PANTALLA Y VARIABLES GLOBALES
ANCHO = 800
ALTO = 600
# COLORES
BLANCO = (255, 255, 255)
VERDE_BANDERA = (27, 94, 32)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
SADDLEBROWN = (139,69,19) #Café de las paredes obstáculo
NEGRO = (0, 0, 0)
anchoGato=60
altoGato=65
anchoRaton=45
altoRaton=47
anchoQueso=51
altoQueso=anchoQueso
h=int(200)
w=int(20)

#LISTAS
listaParedes = []
listaPuntajes = []

def dibujarMenu(ventana,btnJugar,fondoMenu,btnPuntajes): #Dibuja el menú, dos botones: Jugar y Puntajes.
    ventana.blit(fondoMenu, (0, 0))
    ventana.blit(btnJugar, (306,270))
    ventana.blit(btnPuntajes,(ANCHO//2-150,400))

def dibujarFondo(ventana,imgFondo): #Dibuja la imagen de fondo en estado JUGANDO: un cuarto de caricatura.
    ventana.blit(imgFondo,(0,0))

def dibujarRaton(ventana,spriteRaton,move):
    ventana.blit(spriteRaton.image, spriteRaton.rect)
    velocidadRaton = 7 #el número de pixeles que avanza cada frame
    dX = calcularDeltaX(move) #obtiene su velocidad en el eje de las X según la flecha presionada
    dY = calcularDeltaY(move) #obtiene su velocidad en el eje de las Y según la flecha presionada
    choca=""
    for pared in listaParedes:
        if spriteRaton.rect.colliderect(pared): #Si el sprite del ratón está tocando una pared y moviéndose hacia ella lo notificamos al programa y desde qué lado.
            if dX > 0 and spriteRaton.rect.right+dX < pared.rect.right and spriteRaton.rect.right+dX>pared.rect.left:
                choca="right" #Si su velocidad es positiva a la derecha y su posición futura se empalma con la pared, sabemos que choca a la derecha del ratón
            elif dX < 0 and spriteRaton.rect.left+dX < pared.rect.right and spriteRaton.rect.left+dX>pared.rect.left: #Si se mueve a la izquierda y choca con la pared
                choca="left" #Si su velocidad es negativa a la izquierda y su posición futura se empalma con la pared, sabemos que choca la izquierda del ratón
            elif dY > 0 and spriteRaton.rect.bottom+dY < pared.rect.bottom and spriteRaton.rect.bottom+dY>pared.rect.top: #Si va hacia abajo y choca con la pared x arriba
                choca="down" #Si su velocidad es positiva hacia abajo y su posición futura se empalma con la pared, sabemos que choca con su lado inferior
            elif dY < 0 and spriteRaton.rect.top+dY < pared.rect.bottom and spriteRaton.rect.top+dY>pared.rect.top:
                choca ="up" #Si su velocidad es negativa hacia arriba y su posición futura se empalma con la pared, sabemos que choca con su lado superior
            else:
                choca="" #Si no se da ninguna de las condiciones anteriores, no se está moviendo hacia la pared y no hacemos nada.

    if move == "right": #Si la tecla presionada es derecha y está chocando con la pared del lado derecho, no se mueve. Lo mismo para los demás comando.
        if move==choca:
            pass
        else:
            spriteRaton.rect.left += velocidadRaton #El ratón se mueve a la derecha
    if move == "left":
        if move == choca:
            pass
        else:
            spriteRaton.rect.left -= velocidadRaton #Ratón se mueve a la izquierda
    if move == "up":
        if move == choca:
            pass
        else:
            spriteRaton.rect.top -= velocidadRaton #Ratón se mueve hacia arriba
    if move == "down":
        if move == choca:
            pass
        else:
            spriteRaton.rect.top +=velocidadRaton #Ratón se mueve hacia abajo

def calcularDeltaX(move): #1 positivo es que se mueve a la derecha, -1 es a la izquierda, 0 es inmóvil
    if move == "right":
        return 1
    elif move == "left":
        return -1
    else:
        return 0
def calcularDeltaY(move): #1 positivo es hacia abajo, -1 es hacia arriba, 0 es inmóvil.
    if move == "up":
        return -1
    elif move == "down":
        return 1
    else:
        return 0


def dibujarGato(ventana, spriteGato, spriteRaton,subGato):
    ventana.blit(subGato.image,subGato.rect) #Dibuja el subSprite rectangular detrás del Gato
    ventana.blit(spriteGato.image, spriteGato.rect)
    velocidadGato = 2 #pixeles que avanza el gato cada frame
    #El gato debe perseguir al ratón, por lo que su posición siempre debe tratar de acercarse a la del gato si es diferente.
    if spriteRaton.rect.left < spriteGato.rect.left:
        spriteGato.rect.left -= velocidadGato
    else:
        spriteGato.rect.left += velocidadGato
    if spriteRaton.rect.top < spriteGato.rect.top:
        spriteGato.rect.top -= velocidadGato
    else:
        spriteGato.rect.top += velocidadGato
    subGato.rect.left = spriteGato.rect.left+8 #El subsprite sigue la posición del sprite del gato, pero se dibuja 8 pixeles más abajo y más a la derecha.
    subGato.rect.top = spriteGato.rect.top+8

def dibujarQueso(ventana,spriteQueso):
    ventana.blit(spriteQueso.image, spriteQueso.rect)
    #Aquí no podría incluir a aparición y reaparición, sería más bien en la función que determina si el queso es comido.

def dibujarlistaParedes(ventana): #Dibuja las paredes con un ciclo
    for pared in listaParedes:
        ventana.blit(pared.image, pared.rect)

def verificarAtrapaGatoRaton(subGato,spriteRaton):
    if subGato.rect.colliderect(spriteRaton): #Si el subsprite del Gato colisiona con el sprite del ratón, el ratón es capturado.
            return True
    return False

def verificarQuesoComido(spriteRaton,spriteQueso): #Si el ratón y el queso colisionan, el ratón se comió un queso.
    if spriteRaton.rect.colliderect(spriteQueso):
            return True
    return False

def dibujarPantallaFin(ventana,fuente2,score, contadorQuesos,muere,btnPuntajes): #Dependiendo de cómo perdió el jugador se imprime el resultado en pantalla.
    if muere == "hambre":
        texto = fuente2.render("¡MORISTE DE HAMBRE!", 1, ROJO)
    elif muere == "comido":
        texto = fuente2.render("¡FUISTE COMIDO!", 1, ROJO)
    puntajeFinal = fuente2.render("Score: %d " %(int(score*100)), 1, ROJO) #Imprime puntaje final y quesos totales comidos.
    totalDeQuesos = fuente2.render("Total Quesos Comidos: %d" %(contadorQuesos), 1, ROJO)
    ventana.blit(texto,(100,100))
    ventana.blit(puntajeFinal, (100, 200))
    ventana.blit(totalDeQuesos, (100,300))
    ventana.blit(btnPuntajes, (ANCHO//2-150,400))


def obtenerCoordenada(eje): #Función que genera coordenadas aleatorias según el eje.
    if eje == "x":
        aleatoria=random.randint(anchoQueso,ANCHO-anchoQueso)
        return aleatoria
    elif eje == "y":
        aleatoria=random.randint(altoQueso,ALTO-anchoQueso)
        return aleatoria


def dibujarBarra(ventana, fuente1, vida,score): #Dibuja la barra de vida del ratón y el puntaje corriente.
    texto = fuente1.render("Score: %d"%(int(score*100)), 1, ROJO)
    ventana.blit(texto,(20,ALTO-20))
    pygame.draw.rect(ventana, ROJO, (20, ALTO-40, vida+2, 10)) #Sumo 2 a vida por razones estéticas: no debe llegar a crecer al lado izquierdo

def obtenerPuntajes(): #obtiene los 3 puntajes más altos del archivo de texto donde están guardados y los pone en una lista de mejor a peor.
    lista = []
    entrada = open("Puntajes", "r", encoding = "UTF-8")
    puntajes = entrada.readlines()
    for i in range(3): #no lee la última línea que está vacía
        datos = puntajes[i].split(" ")
        lista.append(datos[1]) #Agrega la puntuación a la lista
    entrada.close()
    return lista

def calcularNuevosPuntajes(listaPuntajes,scoreActual):
    #Lee la lista de puntajes y guarda los valores iniciales que se tienen en orden para compararlos con el puntaje actual.
    primer = int(listaPuntajes[0])
    segundo = int(listaPuntajes[1])
    tercer = int(listaPuntajes[2])

    if scoreActual > primer: #Si puntajeactual es mayor que el primer, es el nuevo primer lugar y se recorren todos, borrando el anterior tercer lugar
        tercer=segundo
        segundo=primer
        primer = scoreActual
    elif scoreActual < primer and scoreActual > segundo: #Si no es mayor que el primer pero es mayor que el segundo, es el nuevo segundo lugar y se recorren.
            tercer = segundo
            segundo = scoreActual
    elif scoreActual < segundo and scoreActual > tercer: #Si no es mayor que el segundo pero sí mayor que el tercero, es el nuevo tercer lugar.
                tercer=scoreActual
        #Si no es mayor que ninguno, no hay ningún cambio
    nuevaLista = [] #Crea y devuelve una nueva lista con los puntajes actualizados
    nuevaLista.append(str(primer))
    nuevaLista.append(str(segundo))
    nuevaLista.append(str(tercer))
    guardarNuevosPuntajes(nuevaLista)
    return nuevaLista

def guardarNuevosPuntajes(lista): #Abre el archivo de texto y reescribe los nuevos puntajes según la nueva lista
    archivo=open("Puntajes","w", encoding = "UTF-8")
    counter=1
    for i in lista:
        archivo.write("%d %s\n"%(counter,i))
        counter +=1

    archivo.close() #Resultan 4 líneas de las cuales las 3 primeras contienen los puntajes ennumerados.

def dibujarPuntajes(ventana,fuente1,lista,btnMenu): #Escribe los puntajes más altos en pantalla según la lista más actualizada
    titulo = fuente1.render("HIGH SCORES",1,AZUL)
    ventana.blit(titulo,(ANCHO//2-150,20))
    ventana.blit(btnMenu,(ANCHO-120,ALTO-120))
    for i in range(len(lista)):
        linea = fuente1.render("%d %s" %(i+1,lista[i]), 1, AZUL)
        ventana.blit(linea, (100,100+i*80)) #(en eje y aumenta 70 pixeles cada iteración)

def verificarDentroPantalla(spriteRaton): #Verifica si el ratón está en pantalla con una tolerancia aproximada de la mitad del spriteRaton.
    if spriteRaton.rect.left <= -20 or spriteRaton.rect.left >= ANCHO-20 or spriteRaton.rect.top <= -20 or spriteRaton.rect.top >= ALTO-20:
        return False
    else:
        return True

def dibujar():
    # Inicializa el motor de pygame
    pygame.init()
    # Crea una ventana de ANCHO x ALTO
    ventana = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana donde dibujará
    reloj = pygame.time.Clock()  # Para limitar los fps
    termina = False  # Bandera para saber si termina la ejecución, iniciamos suponiendo que no

    #IMÁGENES
    fondoMenu = pygame.image.load("Cat & Mouse.png")
    playButton = pygame.image.load("BtnJugar.png")
    background = pygame.image.load("background_CatMouse.png")
    gato = pygame.image.load("CatFace_r.png")
    raton = pygame.image.load("mouseFace_r.png")
    queso = pygame.image.load("cheese_r.png")
    btnPuntajes = pygame.image.load("ScoreButton.png")
    btnMenu = pygame.image.load("regresaMenu.png")

    #SPRITES
    spriteGato = pygame.sprite.Sprite()
    spriteGato.image=gato
    spriteRaton = pygame.sprite.Sprite()
    spriteRaton.image = raton
    spriteQueso = pygame.sprite.Sprite()
    spriteQueso.image=queso
    subGato = pygame.sprite.Sprite()
    subGato.image = pygame.Surface([40,45]) #creamos un subSprite del gato para que el "hitbox" se vea mejor para el usuario
    subGato.image.fill(NEGRO)

    #Declaración de atributos rect
    spriteGato.rect = gato.get_rect()
    spriteRaton.rect = raton.get_rect()
    spriteQueso.rect = queso.get_rect()
    subGato.rect = subGato.image.get_rect()

    #PAREDES SPRITE
    # dos paredes verticales y una pared horizontal, las tres de misma superficie.
    pared1 = pygame.sprite.Sprite()
    pared1.image = pygame.Surface([w,h])
    pared2 = pygame.sprite.Sprite()
    pared2.image = pygame.Surface([w,h])
    pared3= pygame.sprite.Sprite()
    pared3.image = pygame.Surface([h,w])
    pared1.image.fill(SADDLEBROWN)
    pared2.image.fill(SADDLEBROWN)
    pared3.image.fill(SADDLEBROWN)
    pared1.rect = pared1.image.get_rect()
    pared2.rect = pared2.image.get_rect()
    pared3.rect = pared3.image.get_rect()
    #anexamos las paredes a nuestra lista de paredes una vez que están creadas.
    listaParedes.append(pared1)
    listaParedes.append(pared2)
    listaParedes.append(pared3)

    #Establecer coordenadas iniciales
    spriteGato.rect.left = ANCHO//2 - anchoGato//2
    spriteGato.rect.top = 35
    spriteRaton.rect.left = ANCHO//2 - anchoRaton//2
    spriteRaton.rect.top = ALTO - 2*altoRaton
    spriteQueso.rect.left = obtenerCoordenada("x")
    spriteQueso.rect.top = obtenerCoordenada("y")
    pared1.rect.left = 170
    pared1.rect.top = 90
    pared2.rect.left = 630
    pared2.rect.top = 340
    pared3.rect.left = ANCHO//2 - 100
    pared3.rect.top = ALTO//2 - 10

    #Texto:
    fuente1=pygame.font.SysFont("Boulder", 30)
    fuente2=pygame.font.SysFont("Uni Sans", 72)
    fuente3 = pygame.font.SysFont("Boulder", 70)

    #Condiciones iniciales
    score = 100
    vida = score
    contadorQuesos = 0
    muere = ""
    move = "quieto"

    #ESTADOS
    MENU = 1
    JUGANDO = 2
    GAMEOVER = 3
    PUNTAJES = 4
    estado = MENU #Comienza en el menú

    #AUDIOS
    pygame.mixer.init()
    maullido = pygame.mixer.Sound("miau.wav")
    recogeQueso = pygame.mixer.Sound("PickupSound.wav")
    #sonido corto: WAv. Sonido largo: MP3
    pygame.mixer.music.load("SonicMusic.mp3") #Se carga una sola cancion
    pygame.mixer.music.play(-1)


    while not termina:  # Ciclo principal, MIENTRAS la variable termina sea False, el ciclo se repite automáticamente
        # Procesa los eventos que recibe
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # El usuario hizo click en el botón de salir
                termina = True      # Queremos terminar el ciclo
                #Para el botón de Play:
            elif evento.type == pygame.MOUSEBUTTONDOWN: #Interacción botones en pantalla
                xMouse, yMouse = pygame.mouse.get_pos()
                if estado == MENU:
                    if xMouse >= 306 and xMouse <= 505 and yMouse >= 270 and yMouse <= 412: #Botón de Jugar
                        xMouse = -1
                        estado = JUGANDO  # PASA A JUGAR
                    elif xMouse >= (ANCHO//2-150) and xMouse <= (ANCHO//2 +150) and yMouse >= 400 and yMouse <= 465: #Botón menu de puntajes
                        estado = PUNTAJES
                if estado == GAMEOVER:
                    if xMouse >= (ANCHO//2-150) and xMouse <=ANCHO//2+150 and yMouse>=400 and yMouse <=465: #Botón menu de puntajes al finalizar partida
                        estado = PUNTAJES
                if estado == PUNTAJES:
                    if xMouse >=(ANCHO-120) and xMouse <=(ANCHO-20) and yMouse >=(ALTO-120) and yMouse <=(ALTO-20): #Botón de regreso al menu
                        estado = MENU
            elif evento.type == pygame.KEYDOWN:  #Interacción usuario-teclado
                if evento.key == pygame.K_RIGHT:    # Tecla flecha derecha
                    move="right"
                elif evento.key == pygame.K_LEFT:  # Tecla flecha izquierda
                    move="left"
                elif evento.key == pygame.K_UP:  # Tecla flecha arriba
                    move = "up"
                elif evento.key == pygame.K_DOWN:  # Tecla flecha abajo
                    move="down"
            elif evento.type != pygame.KEYDOWN:
                move="quieto" #no se está moviendo

        # Borrar pantalla
        ventana.fill(NEGRO)
        # Dibujar, aquí haces todos los trazos que requieras
        if estado == MENU:
            dibujarMenu(ventana, playButton,fondoMenu,btnPuntajes)
        elif estado == JUGANDO:
            dentro=verificarDentroPantalla(spriteRaton) #prueba si está dentro
            if dentro == False:
                #Si el ratón se sale del marco de tolerancia de la pantalla su vida decrece más rápidamente
                vida -= (1)
            else:
                vida-= (1/4) #En condiciones normales la vida decrece 0.25 por frame
            quesoComido=verificarQuesoComido(spriteRaton,spriteQueso) #prueba si atrapa un queso
            if quesoComido:
                #Si el ratón atrapa un queso, suma puntos, vida, y suena. El Queso entonces reaparece con nuevas coordenadas.
                recogeQueso.play()
                vida +=35
                score += 15
                spriteQueso.rect.left = obtenerCoordenada("x")
                spriteQueso.rect.top = obtenerCoordenada("y")
                contadorQuesos +=1 #Contamos 1 queso más al total que imprimirá al final.

            capturado = verificarAtrapaGatoRaton(subGato, spriteRaton)#Prueba si el gato atrapa al ratón de acuerdo con una colisión.
            if capturado: #Si el ratón es capturado, suena un maullido y termina la partida.
                maullido.play()
                muere="comido"
                estado = GAMEOVER
            if vida <=0: #Si la vida del ratón se agota, el ratón muere de hambre y termina la partida.
                muere="hambre"
                estado = GAMEOVER

            dibujarFondo(ventana, background)
            dibujarRaton(ventana,spriteRaton,move)
            dibujarGato(ventana, spriteGato,spriteRaton,subGato)
            dibujarlistaParedes(ventana)
            dibujarQueso(ventana,spriteQueso)
            dibujarBarra(ventana,fuente1,vida,score)

        elif estado == GAMEOVER:
            dibujarPantallaFin(ventana,fuente2,score,contadorQuesos,muere,btnPuntajes)
        elif estado == PUNTAJES:
            listaPuntajes = obtenerPuntajes() #Lista de 3 puntajes más altos registrados al momento
            nuevaLista = calcularNuevosPuntajes(listaPuntajes,int(score*100)) #Toma en consideración la nueva puntuación y hace las modificaciones necesarias
            dibujarPuntajes(ventana,fuente3,nuevaLista,btnMenu) #imprime los datos tomando en cuenta la nueva lista.
            #Se reinician las condiciones iniciales por si usuario decide reiniciar partida.
            capturado = False
            spriteGato.rect.left = ANCHO // 2 - anchoGato // 2
            spriteGato.rect.top = 35
            spriteRaton.rect.left = ANCHO // 2 - anchoRaton // 2
            spriteRaton.rect.top = ALTO - 2 * altoRaton
            spriteQueso.rect.left = obtenerCoordenada("x")
            spriteQueso.rect.top = obtenerCoordenada("y")
            score = 100
            vida = score
            contadorQuesos = 0
            muere = ""
            move = "quieto"

        pygame.display.flip()  # Actualiza trazos (Si no llamas a esta función, no se dibuja)
        reloj.tick(40)  # 40 fps

    # Después del ciclo principal
    pygame.quit()  # termina pygame

# Función principal
def main():
    dibujar()   # Por ahora, solo dibuja


# Llamas a la función principal
main()