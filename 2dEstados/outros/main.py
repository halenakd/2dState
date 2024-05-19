import sys
import math
import numpy as np
import pygame
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from geometries import Object
from geometries import Circle
from state import State
from manageStates import ManageStates


# ========================================================
# VARIÁVEIS GLOBAIS
# ========================================================

# ortho
left = -30.0
right = 30.0
bottom = -30.0
top = 30.0

# zoom atual
zoom = 0.0

# cor atual desenho
color = (0.0, 0.0, 0.0)

# tamanho atual da linha
lineWidth = 1.0

# lista de objetos atuais
objects = []

# objeto selecionado
selected_object = None

manageStates = ManageStates(color, lineWidth, objects)


def display():

    global zoom

    # CONDIÇÃO PARA RESOLVER O PROBLEMA DE QUANDO O VALOR DE ZOOM SE TORNAVA IGUAL AOS DAS MEDIDAS
    if left + zoom >= right - zoom or bottom + zoom >= top - zoom:
        zoom -= 1
        return
    
    glViewport(0, 0, 500, 500) # TAMANHO DA VIEWPORT
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    glOrtho(left+zoom, right-zoom, bottom+zoom, top-zoom, -1.0, 1.0) # ONDE O ZOOM É APLICADO
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(1, 1, 1, 1) # COR DE FUNDO DA TELA
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw() # DESENHA NA TELA

    glutSwapBuffers()


# ========================================================
# CALLBACK - TECLADO
# ========================================================

keyStates = np.full(256, False, dtype=bool)

def keyPressed(key, x, y):
    keyStates[ord(key)] = True
    zoomIn()
    zoomOut()

def keyUp(key, x, y):
    keyStates[ord(key)] = False


# ========================================================
# FUNÇÕES DE ZOOM
# ========================================================

def zoomIn():
    global zoom
    if keyStates[ord('p')]:
        zoom += 1

def zoomOut():
    global zoom
    if keyStates[ord('o')]:
        zoom -= 1


# ========================================================
# CALLBACK - MOUSE
# ========================================================

# click do mouse quando pressiona e quando solta
def MouseClick(button, state, x, y):
    coordsWorld = getWorldCoords(x, y)
    if -20 <= coordsWorld[0] <= -15 and 25 <= coordsWorld[1] <= 28:
        manageStates.setState(manageStates.getIdleState())
    elif -10 <= coordsWorld[0] <= -5 and 25 <= coordsWorld[1] <= 28:
        manageStates.setState(manageStates.getTriangleState())
    else:
        manageStates.currentState.MouseClick(button, state, coordsWorld[0], coordsWorld[1])

# mouse em movimento pressionado
def MouseMotion(x, y):
    coordsWorld = getWorldCoords(x, y)
    manageStates.currentState.MouseMotion(coordsWorld[0], coordsWorld[1])

# mouse em movimento solto
def MousePassiveMotion(x, y):
    coordsWorld = getWorldCoords(x, y)
    manageStates.currentState.MousePassiveMotion(coordsWorld[0], coordsWorld[1])


# para gerar um texto no botão
def render_text(text, x, y, size):
    pygame.init()
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, (255, 255, 255), (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)

    glRasterPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def botaoSelect():
    glBegin(GL_QUADS)
    glColor3ub(0, 0, 0)
    glVertex2f(-20, 25)
    glVertex2f(-20, 28)
    glVertex2f(-15, 28)
    glVertex2f(-15, 25)
    glEnd()

    glLineWidth(1.0)
    glBegin(GL_LINE_LOOP)
    glColor3ub(76, 75, 74)
    glVertex2f(-20, 25)
    glVertex2f(-20, 28)
    glVertex2f(-15, 28)
    glVertex2f(-15, 25)
    glEnd()

    # renderiza o texto Resetar no centro do botão
    render_text("V", -18.1, 25.3, 25)

def botaoTriangulo():
    glBegin(GL_QUADS)
    glColor3ub(0, 0, 0)
    glVertex2f(-10, 25)
    glVertex2f(-10, 28)
    glVertex2f(-5, 28)
    glVertex2f(-5, 25)
    glEnd()

    glLineWidth(1.0)
    glBegin(GL_LINE_LOOP)
    glColor3ub(76, 75, 74)
    glVertex2f(-10, 25)
    glVertex2f(-10, 28)
    glVertex2f(-5, 28)
    glVertex2f(-5, 25)
    glEnd()

    # renderiza o texto Resetar no centro do botão
    render_text("T", -8.1, 25.3, 25)


def draw():

    glClear(GL_COLOR_BUFFER_BIT)

    # DESENHO DO EIXO X #
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(-20.0, 0.0)
    glVertex2f(20.0, 0.0)
    glEnd()

    botaoSelect()
    botaoTriangulo()

    manageStates.currentState.draw()

    for obj in objects:
        obj.draw()

    glutSwapBuffers()


# ========================================================
# PROJEÇÃO INVERSA DE COORDENADAS
# ========================================================

def getWorldCoords(x, y):
    # coordenadas do volume de visualização
    xr = right
    xl = left
    yt = top
    yb = bottom
    zn = 1.0
    zf = -1.0
    
    # matriz de projeçao (window + NDC)
    P =[
        [2/(xr-xl), 0.0, 0.0, -(xr+xl)/(xr-xl)],
        [0.0, 2/(yt-yb), 0.0, -(yt+yb)/(yt-yb)],
        [0.0, 0.0, -2/(zf-zn), -(zf+zn)/(zf-zn)],
        [0.0, 0.0, 0.0, 1.0],
    ]

    PM = np.array(P)

    # inversa da matriz de prozeção
    invP = np.linalg.inv(PM)

    # conversão das coordenadas do mouse para NDC
    viewport = glGetIntegerv(GL_VIEWPORT)
    ywin = viewport[3] - y
    xndc = (2*(x-viewport[0]))/viewport[2] -1
    yndc = (2*(ywin-viewport[1]))/viewport[3] -1
    zndc = 0
    wndc = 1
    vndc = np.array([xndc, yndc, zndc,wndc])

    # transformação de projeção inversa
    world = np.matmul(invP, vndc)

    # coordenadas no sistema WCS do OpenGL
    return world[0], world[1]


# ========================================================
# MAIN - INICIALIZAÇÕES, CHAMADA DAS OUTRAS FUNÇÕES, ETC.
# ========================================================

def main():
    global selected_shape

    glutInit()
    glutInitWindowSize(500, 500) # TAMANHO DA JANELA
    glutInitWindowPosition(430, 100) # POSIÇÃO DA JANELA (+- NO MEIO)
    glutCreateWindow(b'Ambiente 2D') # NOME DA JANELA

    """# FUNÇÕES REFERENTES AO MENU (botão direito do mouse)
    menu_id = glutCreateMenu(shape_menu) 
    glutAddMenuEntry("Circulo", Shapes.CIRCLE.value)
    glutAttachMenu(GLUT_RIGHT_BUTTON)"""

    # CHAMADA DA FUNÇÃO DE DISPLAY #
    glutDisplayFunc(display)
    glutIdleFunc(display)

    # TECLADO #
    glutKeyboardFunc(keyPressed) # PRESSIONOU A TECLA
    glutKeyboardUpFunc(keyUp) # SOLTOU A TECLA

    # MOUSE #
    glutMotionFunc(MouseMotion)
    glutPassiveMotionFunc(MousePassiveMotion)
    glutMouseFunc(MouseClick)

    # LOOP PRINCIPAL #
    glutMainLoop()

if __name__ == "__main__":
    main()