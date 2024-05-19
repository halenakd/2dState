# Autor: Halena Kulmann Duarte
# Data: 27/02/2024
# Versão: 12/03/2024
# Descrição: Programa com menu seletor(botão direito do mouse) para escolher um 
#            dos três desenhos pedidos na lista 1: círculo (questão 1), triângulo
#            com círculos (questão 3) ou espiral (questão 4). Além disso, é possível
#            dar zoomIn com a tecla p e zoomOut com a tecla o (questão 2).

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import numpy as np
from enum import Enum

# ========================================================
# VARIÁVEIS GLOBAIS
# ========================================================

PONTOS = 36

left = -30.0
right = 30.0
bottom = -30.0
top = 30.0

zoom = 0.0

triangle_points = []
circle_points = []
square_points = []
polygon_points = []

# ========================================================
# CONTROLE DO MENU (click direito do mouse)
# ========================================================

class Shapes(Enum):
    CIRCLE = 1
    TRIANGLE = 2
    SQUARE = 3
    POLYGON = 4

def shape_menu(value):
    global selected_shape
    if value == 1:
        selected_shape = Shapes.CIRCLE
    elif value == 2:
        selected_shape = Shapes.TRIANGLE
    elif value == 3:
        selected_shape = Shapes.SQUARE
    elif value == 4:
        selected_shape = Shapes.POLYGON

    glutPostRedisplay()

selected_shape = Shapes.CIRCLE

# ========================================================
# FUNÇÃO DISPLAY
# ========================================================

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
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    draw() # CHAMADA DOS DESENHOS NA TELA

    glutSwapBuffers()


class Shape:
    def __init__(self, points):
        self.points = points

    def draw(self):
        if len(self.points) >= 1:
            glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_LINE_LOOP)
            for point in self.points:
                glVertex2f(point[0], point[1])
            glEnd()

class ShapeManager:
    def __init__(self):
        self.shapes = []

    def add_shape(self, shape):
        self.shapes.append(shape)

    def draw_shapes(self):
        for shape in self.shapes:
            shape.draw()

    def clear_shapes(self):
        self.shapes = []

# Inicialize o gerenciador de formas
shape_manager = ShapeManager()

# ========================================================
# FUNÇÕES DE ZOOM
# ========================================================

def zoomIn():
    global zoom
    if keyStates[ord('p')]:
        zoom += 1
        #print("ZoomIn: ", zoom)
        #glutPostRedisplay()

def zoomOut():
    global zoom
    if keyStates[ord('o')]:
        zoom -= 1
        #print("ZoomOut: ", zoom)
        #glutPostRedisplay()


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
# CALLBACK - MOUSE
# ========================================================

def Dist(a, b):
    x1, x2 = a[0], b[0]
    y1, y2 = a[1], b[1]

    dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    return dist


# click do mouse quando pressiona e quando solta
def MouseClick(button, state, x, y):
    global circle_points
    global triangle_points
    global square_points
    global polygon_points
    global selected_shape
    global centro

    coordsWorld = getWorldCoords(x, y)

    if selected_shape == Shapes.CIRCLE:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            centro = (coordsWorld[0], coordsWorld[1])
        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            raio = Dist(coordsWorld, centro)
            draw_circle(centro[0], centro[1], raio)
            shape_manager.add_shape(Shape(circle_points))
            circle_points = []  # limpa a lista de pontos do círculo

    elif selected_shape == Shapes.TRIANGLE:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            triangle_points.append(coordsWorld)
        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            triangle_points.append(coordsWorld)
            distance = triangle_points[1][0] - triangle_points[0][0]
            third_point_x = triangle_points[0][0] - distance
            third_point_y = triangle_points[1][1]
            triangle_points.append((third_point_x, third_point_y))
            shape_manager.add_shape(Shape(triangle_points))
            triangle_points = []  # limpa a lista de pontos do triângulo

    elif selected_shape == Shapes.SQUARE:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            square_points.append(coordsWorld)
        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            draw_square(coordsWorld)
            shape_manager.add_shape(Shape(square_points))
            square_points = []  # limpa a lista de pontos do triângulo

    elif selected_shape == Shapes.POLYGON:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            polygon_points.append(coordsWorld)
        elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
            if (Dist(polygon_points[0], coordsWorld) < 5) and (len(polygon_points) > 0):
                shape_manager.add_shape(Shape(polygon_points))
                polygon_points = []  # limpa a lista de pontos do polígono
            else:
                polygon_points.append(coordsWorld)
                draw_line(polygon_points[-1], coordsWorld)
                #shape_manager.add_shape(Shape(square_points))

# arrasto do mouse
def MouseMotion(x, y):
    global selected_shape

    coordsWorld = getWorldCoords(x, y)

    if selected_shape == Shapes.SQUARE:
        if len(polygon_points) >= 1:
            draw_line(polygon_points[-1], coordsWorld)


# ========================================================
# FUNÇÕES DE DESENHOS JÁ DEFINIDOS
# ========================================================

def draw_line(ponto1, ponto2):
    glBegin(GL_LINES)
    glVertex2f(ponto1[0], ponto1[1])
    glVertex2f(ponto2[0], ponto2[1])
    glEnd()


def draw_triangle(points):
    # verifica se há pontos suficientes para desenhar o triângulo
    if len(points) == 3:
        # define a cor para o triângulo
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINE_LOOP)
        for point in points:
            glVertex2f(point[0], point[1])
        glEnd()


def draw_circle(x0, y0, r):
    global circle_points
    glBegin(GL_LINE_LOOP) # CÍRCULO DE LINHA
    #glBegin(GL_POINTS) # CÍRCULO DE PONTOS
    ang = 0.0
    while ang <= 360:
        x = x0 + r * math.cos(math.radians(ang))
        y = y0 + r * math.sin(math.radians(ang))
        glVertex2f(x, y)
        ang += 360/PONTOS
        circle_points.append((x, y))
    glEnd()


def draw_square(coordsWorld):
    global square_points
    second_point_x = coordsWorld[0]
    second_point_y = square_points[0][1]
    square_points.append((second_point_x, second_point_y))
    square_points.append(coordsWorld)
    forth_point_x = square_points[0][0]
    forth_point_y = square_points[2][1]
    square_points.append((forth_point_x, forth_point_y))



# ========================================================
# FUNÇÃO DE DESENHO - DEFINIÇÃO DOS DESENHOS
# ========================================================
    
def draw():
    global selected_shape

    glClear(GL_COLOR_BUFFER_BIT)

    # DESENHO DO EIXO X #
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(-20.0, 0.0)
    glVertex2f(20.0, 0.0)
    glEnd()

    # DESENHO DO EIXO Y #
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex2f(0.0, -20.0)
    glVertex2f(0.0, 20.0)
    glEnd()

    # Desenha todas as formas gerenciadas
    shape_manager.draw_shapes()


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
    glutCreateWindow(b'Lista 3') # NOME DA JANELA

    # FUNÇÕES REFERENTES AO MENU (botão direito do mouse)
    menu_id = glutCreateMenu(shape_menu) 
    glutAddMenuEntry("Circulo", Shapes.CIRCLE.value)
    glutAddMenuEntry("Triangulo", Shapes.TRIANGLE.value)
    glutAddMenuEntry("Quadrado", Shapes.SQUARE.value)
    glutAddMenuEntry("Poligono", Shapes.POLYGON.value)
    glutAttachMenu(GLUT_RIGHT_BUTTON)

    glutMouseFunc(lambda button, state, x, y: None)

    # CHAMADA DA FUNÇÃO DE DISPLAY #
    glutDisplayFunc(display)
    glutIdleFunc(display)

    # TECLADO #
    glutKeyboardFunc(keyPressed) # PRESSIONOU A TECLA
    glutKeyboardUpFunc(keyUp) # SOLTOU A TECLA

    # MOUSE #
    glutMotionFunc(MouseMotion)
    glutMouseFunc(MouseClick)

    # LOOP PRINCIPAL #
    glutMainLoop()

if __name__ == "__main__":
    main()