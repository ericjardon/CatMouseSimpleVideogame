#Autor: Eric Andrés Jardón Chao, A10376748
#Descripción: Código fuente para el minijuego: Cat&Mouse
#todo Agregar botón replay, botón Menu, colisión con paredes dx se vuelve cero; o con base en valor de move si choca, ignora comando.
#Preguntar: GetWidth? Loop canción?
import pygame   # Librería de pygame
import random

# PANTALLA
ANCHO = 800
ALTO = 600
# COLORES
BLANCO = (255, 255, 255)  # R,G,B en el rango [0,255], 0 ausencia de color, 255 toda la intensidad
VERDE_BANDERA = (27, 94, 32)    # un poco de rojo, más de verde, un poco de azul
ROJO = (255, 0, 0)      # solo rojo, nada de verde, nada de azul
AZUL = (0, 0, 255)      # nada de rojo, ni verde, solo azul
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

def dibujarMenu(ventana,btnJugar,fondoMenu,btnPuntajes):
    ventana.blit(fondoMenu, (0, 0))
    ventana.blit(btnJugar, (306,270))
    ventana.blit(btnPuntajes,(ANCHO//2-150,400))

def dibujarFondo(ventana,imgFondo):
    ventana.blit(imgFondo,(0,0))

def dibujarRaton(ventana,spriteRaton,move):
    ventana.blit(spriteRaton.image, spriteRaton.rect)
    velocidadRaton = 7
    dX = calcularDeltaX(move)
    dY = calcularDeltaY(move)
    choca=""
    for pared in listaParedes:
        if spriteRaton.rect.colliderect(pared):
            if dX > 0 and spriteRaton.rect.right+dX < pared.rect.right and spriteRaton.rect.right+dX>pared.rect.left: #si se mueve a la derecha chocando con la pared
                choca="right"
            elif dX < 0 and spriteRaton.rect.left+dX < pared.rect.right and spriteRaton.rect.left+dX>pared.rect.left: #Si se mueve a la izquierda y choca con la pared
                choca="left"
            elif dY > 0 and spriteRaton.rect.bottom+dY < pared.rect.bottom and spriteRaton.rect.bottom+dY>pared.rect.top: #Si va hacia abajo y choca con la pared x arriba
                choca="down"
            elif dY < 0 and spriteRaton.rect.top+dY < pared.rect.bottom and spriteRaton.rect.top+dY>pared.rect.top:
                choca ="up"
            else:
                choca=""
    if move == "right":
        if move==choca:
            pass
        else:
            spriteRaton.rect.left += velocidadRaton
    if move == "left":
        if move == choca:
            pass
        else:
            spriteRaton.rect.left -= velocidadRaton
    if move == "up":
        if move == choca:
            pass
        else:
            spriteRaton.rect.top -= velocidadRaton
    if move == "down":
        if move == choca:
            pass
        else:
            spriteRaton.rect.top +=velocidadRaton

def calcularDeltaX(move):
    if move == "right":
        return 1
    elif move == "left":
        return -1
    else:
        return 0
def calcularDeltaY(move):
    if move == "up":
        return -1
    elif move == "down":
        return 1
    else:
        return 0


def dibujarGato(ventana, spriteGato, spriteRaton):
    ventana.blit(spriteGato.image, spriteGato.rect)
    velocidadGato = 2
    if spriteRaton.rect.left < spriteGato.rect.left:
        spriteGato.rect.left -= velocidadGato
    else:
        spriteGato.rect.left += velocidadGato
    if spriteRaton.rect.top < spriteGato.rect.top:
        spriteGato.rect.top -= velocidadGato
    else:
        spriteGato.rect.top += velocidadGato

def dibujarQueso(ventana,spriteQueso):
    ventana.blit(spriteQueso.image, spriteQueso.rect)
    #Aquí no podría incluir a aparición y reaparición, sería más bien afuera

def dibujarlistaParedes(ventana):
    for pared in listaParedes:
        ventana.blit(pared.image, pared.rect)
        #pygame.draw.rect(ventana, SADDLEBROWN,(pared.rect))

def verificarAtrapaGatoRaton(spriteGato,spriteRaton):
    if spriteGato.rect.colliderect(spriteRaton): #usar subsprites para mejorar experiencia
            return True
    return False

def verificarQuesoComido(spriteRaton,spriteQueso):
    if spriteRaton.rect.colliderect(spriteQueso):
            return True
    return False

def dibujarPantallaFin(ventana,fuente2,score, contadorQuesos,muere,btnPuntajes):
    if muere == "hambre":
        texto = fuente2.render("¡MORISTE DE HAMBRE!", 1, ROJO)
    elif muere == "comido":
        texto = fuente2.render("¡FUISTE COMIDO!", 1, ROJO)
    puntajeFinal = fuente2.render("Score: %d " %(int(score*100)), 1, ROJO) #Dejar el multiplicador * 10 o por 100?
    totalDeQuesos = fuente2.render("Total Quesos Comidos: %d" %(contadorQuesos), 1, ROJO)
    ventana.blit(texto,(100,100))
    ventana.blit(puntajeFinal, (100, 200))
    ventana.blit(totalDeQuesos, (100,300))
    ventana.blit(btnPuntajes, (ANCHO//2-150,400))


def obtenerCoordenada(eje):
    if eje == "x":
        aleatoria=random.randint(anchoQueso,ANCHO-anchoQueso)
        return aleatoria
    elif eje == "y":
        aleatoria=random.randint(altoQueso,ALTO-anchoQueso)
        return aleatoria


def dibujarBarra(ventana, fuente1, vida):
    texto = fuente1.render("Score", 1, ROJO)
    ventana.blit(texto,(20,ALTO-20))
    pygame.draw.rect(ventana, ROJO, (20, ALTO-40, vida+2, 10)) #Sumo 2 a vida por razones estéticas: no debe llegar a crecer al lado izquierdo

def obtenerPuntajes():
    lista = []
    entrada = open("Puntajes", "r", encoding = "UTF-8")
    puntajes = entrada.readlines()
    for i in range(3): #no lee la última línea que está vacía
        datos = puntajes[i].split(" ")
        lista.append(datos[1]) #Agrega la puntuación a la lista
    entrada.close()
    return lista

def calcularNuevosPuntajes(listaPuntajes,scoreActual):
    primer = int(listaPuntajes[0])
    segundo = int(listaPuntajes[1])
    tercer = int(listaPuntajes[2])

    if scoreActual > primer: #Si es mayor que el primer, es el nuevo primer lugar y se recorren todos, borrando el anterior tercer
        tercer=segundo
        segundo=primer
        primer = scoreActual
    elif scoreActual < primer and scoreActual > segundo: #Si no es mayor que el primer pero es mayor que el segundo, es el nuevo segundo lugar y se recorren.
            tercer = segundo
            segundo = scoreActual
    elif scoreActual < segundo and scoreActual > tercer: #Si no es mayor que el segundo pero sí mayor que el tercero, es el nuevo tercer lugar.
                tercer=scoreActual
        #Si no es mayor que ninguno, no hay ningún cambio
    nuevaLista = [] #Crea una nueva lista con los puntajes actualizados
    nuevaLista.append(str(primer))
    nuevaLista.append(str(segundo))
    nuevaLista.append(str(tercer))
    guardarNuevosPuntajes(nuevaLista)
    return nuevaLista

def guardarNuevosPuntajes(lista):
    archivo=open("Puntajes","w", encoding = "UTF-8")
    counter=1
    for i in lista:
        archivo.write("%d %s\n"%(counter,i))
        counter +=1

    archivo.close() #Quedan 4 líneas de las cuales las 3 primeras contienen los puntajes

def dibujarPuntajes(ventana,fuente1,lista,btnReplay):
    titulo = fuente1.render("HIGH SCORES",1,AZUL)
    ventana.blit(titulo,(ANCHO//2-150,20))
    for i in range(len(lista)):
        linea = fuente1.render("%d %s" %(i+1,lista[i]), 1, AZUL)
        ventana.blit(linea, (100,100+i*80)) #(en y aumenta 70 pixeles cada iteración)
        #ventana.blit(btnReplay, (ANCHO//2-135, ALTO//2+100))

def verificarDentroPantalla(spriteRaton):
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
    btnReplay = pygame.image.load("PlayAgain.png")

    #SPRITES
    spriteGato = pygame.sprite.Sprite()
    spriteGato.image=gato
    spriteRaton = pygame.sprite.Sprite()
    spriteRaton.image = raton
    spriteQueso = pygame.sprite.Sprite()
    spriteQueso.image=queso

    #PAREDES SPRITE
    #a partir de aquí es NUEVO
    #crearParedesSprite()
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
    #hasta acá

    #Coordenadas rect
    spriteGato.rect = gato.get_rect()
    spriteRaton.rect = raton.get_rect()
    spriteQueso.rect = queso.get_rect()

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

    #Paredes
    #pared1 = (170, 90, 20, 200)
    #pared2 = (630, 340, 20, 200)
    #pared3 = (ANCHO//2 - 100, ALTO // 2 - 10, 200, 20)
    listaParedes.append(pared1)
    listaParedes.append(pared2)
    listaParedes.append(pared3)

    #Texto:
    fuente1=pygame.font.SysFont("Boulder", 30)
    fuente2=pygame.font.SysFont("Uni Sans", 72)
    fuente3 = pygame.font.SysFont("Boulder", 70)
    score = 100
    vida = score

    #ESTADOS
    MENU = 1
    JUGANDO = 2
    GAMEOVER = 3
    PUNTAJES = 4
    estado = MENU
    move="quieto"

    #AUDIOS
    pygame.mixer.init()
    maullido = pygame.mixer.Sound("miau.wav") #NO lo reproduce, sólo lo carga. Lo reproducimos imperativamente en el evento que presione espacio.
    #sonido corto: WAv. Sonido largo: MP3
    pygame.mixer.music.load("SonicMusic.mp3") #Se carga una sola cancion
    pygame.mixer.music.play()
    contadorQuesos = 0
    muere = ""
    while not termina:  # Ciclo principal, MIENTRAS la variable termina sea False, el ciclo se repite automáticamente
        # Procesa los eventos que recibe
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # El usuario hizo click en el botón de salir
                termina = True      # Queremos terminar el ciclo
                #Para el botón de Play:
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                xMouse, yMouse = pygame.mouse.get_pos()
                if estado == MENU: #(306,270) #boton 189x142;
                    if xMouse >= 306 and xMouse <= 505 and yMouse >= 270 and yMouse <= 412:
                        xMouse = -1
                        # CAMBIA EL ESTADO
                        estado = JUGANDO  # PASA A JUGAR
                    elif xMouse >= (ANCHO//2-150) and xMouse <= (ANCHO//2 +150) and yMouse >= 400 and yMouse <= 465:
                        estado = PUNTAJES
                if estado == GAMEOVER:
                    if xMouse >= (ANCHO//2-150) and xMouse <=ANCHO//2+150 and yMouse>=400 and yMouse <=465:
                        estado = PUNTAJES
            elif evento.type == pygame.KEYDOWN:  #Interacción usuario-teclado
                if evento.key == pygame.K_RIGHT:
                    move="right"
                elif evento.key == pygame.K_LEFT:  # Tecla flecha derecha
                    move ="left"
                elif evento.key == pygame.K_UP:  # Tecla flecha derecha
                    move="up"
                elif evento.key == pygame.K_DOWN:  # Tecla flecha derecha
                    move = "down"
            elif evento.type != pygame.KEYDOWN:
                move="quieto" #no se está moviendo

        # Borrar pantalla
        ventana.fill(NEGRO)
        # Dibujar, aquí haces todos los trazos que requieras
        if estado == MENU:
            #dibujarCirculo(ventana, xMouse, yMouse) #por qué hay un círculo?
            dibujarMenu(ventana, playButton,fondoMenu,btnPuntajes)
        elif estado == JUGANDO:
            dentro=verificarDentroPantalla(spriteRaton)
            if dentro == False:
                vida -= (1)
            quesoComido=verificarQuesoComido(spriteRaton,spriteQueso)
            if quesoComido:
                vida +=35
                spriteQueso.rect.left = obtenerCoordenada("x")
                spriteQueso.rect.top = obtenerCoordenada("y")
                contadorQuesos +=1
            else:
                vida-= (1/4)
            if vida >= score:
                score = vida
            capturado = verificarAtrapaGatoRaton(spriteGato, spriteRaton)#Esta función no dibuja
            if capturado:
                maullido.play()
                muere="comido"
                estado = GAMEOVER
            if vida <=0:
                muere="hambre"
                estado = GAMEOVER

            dibujarFondo(ventana, background)
            dibujarRaton(ventana,spriteRaton,move)
            #dibujarGato(ventana, spriteGato,spriteRaton)
            dibujarlistaParedes(ventana)
            dibujarQueso(ventana,spriteQueso)
            dibujarBarra(ventana,fuente1,vida)

        elif estado == GAMEOVER:
            dibujarPantallaFin(ventana,fuente2,score,contadorQuesos,muere,btnPuntajes)
            #Aquí debe ir lo de guardar puntaje y todo eso
        elif estado == PUNTAJES:
            listaPuntajes = obtenerPuntajes() #Lista de 3 puntajes más altos registrados
            nuevaLista = calcularNuevosPuntajes(listaPuntajes,int(score*100))
            dibujarPuntajes(ventana,fuente3,nuevaLista,btnReplay)

        pygame.display.flip()  # Actualiza trazos (Si no llamas a esta función, no se dibuja)
        reloj.tick(40)  # 40 fps

    # Después del ciclo principal
    pygame.quit()  # termina pygame


# Función principal, aquí resuelves el problema
def main():
    dibujar()   # Por ahora, solo dibuja


# Llamas a la función principal
main()
def funcionDeteccionInutil(spriteRaton,pared,velocidadRaton):
    if spriteRaton.rect.left <= pared.rect.right and spriteRaton.rect.right >= pared.rect.left:  # está a la longitud de la pared
        if spriteRaton.rect.bottom + velocidadRaton > pared.rect.top:
            # deshabilitar down
            print("Toca abajo")
        elif spriteRaton.rect.top - velocidadRaton < pared.rect.bottom:
            # deshabilitar up
            print("toca arriba")
    elif spriteRaton.rect.top <= pared.rect.bottom and spriteRaton.rect.bottom >= pared.rect.top:  # Está a la latitud de la pared
        if spriteRaton.rect.right + velocidadRaton > pared.rect.left:
            print("toca derecha")
        elif spriteRaton.rect.left - velocidadRaton < pared.rect.right:
            # Deshabilitar left
            print("Toca izquierda")

def dibujarRatonProcessViejo(ventana, spriteRaton, move):  # Dibuja al ratón y lo mueve según el comando move que recibe.
        ventana.blit(spriteRaton.image, spriteRaton.rect)
        velocidadRaton = 7
        dX = velocidadRaton
        dY = velocidadRaton
        choca = ""
