import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
import wx
import wx.glcanvas as wxgl

# Classe para representar um objeto gráfico
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

    def rotate_to_angle(self, angle):
        self.angle = angle

    def draw(self):
        if len(self.points) >= 1:
            #glPushMatrix()
            centerX, centerY = self.calculate_center()
            #glTranslatef(centerX, centerY, 0.0)
            #glRotatef(self.angle, 0.0, 0.0, 1.0)
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
            #glPopMatrix()

    def drawTemp(self):
        glLineWidth(self.lineWidth)
        glColor3f(self.color[0], self.color[1], self.color[2])
        #glBegin(self.style)
        glBegin(GL_LINE_STRIP)
        for p in self.points:
            #glVertex2f(p[0] - centerX, p[1] - centerY)
            glVertex2f(p[0], p[1])
        glEnd()

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
    

class Circle:
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
        glPopMatrix()