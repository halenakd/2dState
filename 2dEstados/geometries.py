import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
import wx
import wx.glcanvas as wxgl

# ========================================================
# Classe Geometries - representa objetos gráficos
# ========================================================
# possibilita construir objetos(formas), de diferentes quantidades de pontos
# guarda variáveis/informações sobre os objetos
# desenha os objetos e responde a alterações no estilo e na grossura das linhas
# cálcula área, perímetro, centro, etc

class Object:
    def __init__(self, type, color, style, lineWidth):
        self.type = type
        self.color = color
        self.style = style
        self.lineWidth = lineWidth
        self.selected = False
        self.points = []
        self.previousPoints = self.points
        self.primeiroClick = None
        self.angle = 0
        self.center = (0, 0)

    # ========================================================
    # DRAW - desenhos
    # ========================================================

    def draw(self):
        if len(self.points) >= 1:
            glColor3f(self.color[0], self.color[1], self.color[2])
            glLineWidth(self.lineWidth)
            if self.style == "Contínuo":
                glBegin(GL_LINE_LOOP)
                for p in self.points:
                    glVertex2f(p[0], p[1])
                glEnd()
            elif self.style == "Tracejado":
                glLineStipple(6, 0xAAAA)
                glEnable(GL_LINE_STIPPLE)
                glBegin(GL_LINE_LOOP)
                for p in self.points:
                    glVertex2f(p[0], p[1])
                glEnd()
                glDisable(GL_LINE_STIPPLE)
            elif self.style == "Pontilhado":
                glLineStipple(2, 0xAAAA)
                glEnable(GL_LINE_STIPPLE)
                glBegin(GL_LINE_LOOP)
                for p in self.points:
                    glVertex2f(p[0], p[1])
                glEnd()
                glDisable(GL_LINE_STIPPLE)
            elif self.style == "Preechido":
                glBegin(GL_POLYGON)
                for p in self.points:
                    glVertex2f(p[0], p[1])
                glEnd()

    def drawTemp(self):
        glLineWidth(self.lineWidth)
        glColor3f(self.color[0], self.color[1], self.color[2])
        glBegin(GL_LINE_STRIP)
        for p in self.points:
            glVertex2f(p[0], p[1])
        glEnd()

    # ========================================================
    # FUNÇÕES DE CÁLCULO
    # ========================================================

    def calculate_center(self):
        total_x = 0
        total_y = 0
        num_points = len(self.points)

        for point in self.points:
            total_x += point[0]
            total_y += point[1]

        center_x = total_x / num_points
        center_y = total_y / num_points

        return (center_x, center_y)
    
    def calculate_area(self):
        if self.type == "triangle":
            dx = self.points[1][0] - self.points[2][1]
            dy = self.points[1][0] - self.points[2][1]
            base = np.sqrt(dx**2 + dy**2)
            altura = abs(self.points[0][1] - self.points[1][1])
            area = (base * altura) / 2
        elif self.type == "square":
            dx = abs(self.points[0][0] - self.points[2][0])
            dy = abs(self.points[0][1] - self.points[2][1])
            area = dx * dy
        elif self.type == "polygon":
            area = 0
        elif self.type == "circle":
            area = 0
            #base = np.sqrt(dx**2 + dy**2)
            #altura = abs(self.points[0][1] - self.points[1][1])
            #area = dx * dy
        return area
    
    def calculate_perimeter(self):
        perimeter = 0
        num_points = len(self.points)
        for i, point in enumerate(self.points):
            if i < num_points - 1:
                next_point = self.points[i + 1]
            else:
                next_point = self.points[0]

            dx = next_point[0] - point[0]
            dy = next_point[1] - point[1]
            perimeter += math.sqrt(dx**2 + dy**2)

        return perimeter
    

"""class Circle:
    def __init__(self, center, radius, segments):
        self.center = center
        self.radius = radius
        self.segments = segments
        self.rotation_angle = 0  # Inicializa o ângulo de rotação acumulado como 0

    def set_rotation_angle(self, angle):
        self.rotation_angle = angle

    def rotate(self, angle):
        self.rotation_angle += angle

    def draw(self):
        glPushMatrix()
        glTranslatef(self.center[0], self.center[1], 0.0)
        glRotatef(math.degrees(self.rotation_angle), 0, 0, 1)  # Rotaciona em torno do eixo Z
        glBegin(GL_LINE_LOOP)
        for i in range(self.segments):
            theta = 2.0 * math.pi * i / self.segments
            x = self.radius * math.cos(theta)
            y = self.radius * math.sin(theta)
            glVertex2f(x, y)
        glEnd()
        glPopMatrix()"""