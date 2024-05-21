import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from state import State
from geometries import Object
from geometries import Circle
import wx
import wx.glcanvas as wxgl

# ========================================================
# SelectedState - ESTADO DE OBJETO SELECIONADO
# ========================================================
# desenha handles em torno do objeto selecionado
# permite transladar, escalar, rotacionar, etc. objetos

class Handle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.x - 0.02, self.y - 0.02)
        glVertex2f(self.x + 0.02, self.y - 0.02)
        glVertex2f(self.x + 0.02, self.y + 0.02)
        glVertex2f(self.x - 0.02, self.y + 0.02)
        glEnd()

class SelectedState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.handles = []
    
    def selectObject(self, x, y):
        for obj in self.manageStates.objects:
            N_int = 0
            for i in range(len(obj.points)):
                
                if(i == len(obj.points)-1):
                    iMaisUm = 0
                else:
                    iMaisUm = i + 1
                
                if obj.points[i][1] != obj.points[iMaisUm][1]:
                    x_int = (y - obj.points[i][1]) * (obj.points[iMaisUm][0] - obj.points[i][0]) / (obj.points[iMaisUm][1] - obj.points[i][1]) + obj.points[i][0]
                    y_int = y
                    if x_int == x:
                        obj.selected = True
                        print(obj.selected)
                        self.manageStates.setState(self.manageStates.getSelectedState())
                        break
                    else:
                        if x_int > x and y_int > min(obj.points[i][1], obj.points[iMaisUm][1]) and y_int <= max(obj.points[i][1], obj.points[iMaisUm][1]):
                            N_int += 1
                else:
                    if y == obj.points[i][1] and x >= min(obj.points[i][0], obj.points[iMaisUm][0]) and x <= max(obj.points[i][0], obj.points[iMaisUm][0]):
                        obj.selected = True
                        print(obj.selected)
                        self.manageStates.setState(self.manageStates.getSelectedState())
                        break

            if (N_int % 2) != 0:
                obj.selected = True
                print(obj.selected)
                self.manageStates.setState(self.manageStates.getSelectedState())
            else:
                obj.selected = False

    def Translate(self, x, y):
        for obj in self.manageStates.objects:
            if obj.selected:
                # diferença entre o x e o y da primeira posição e da próxima
                dx = x - obj.primeiro[0]
                dy = y - obj.primeiro[1]

                # atualizando a posição de todos os pontos
                for i in range(len(obj.points)):
                    obj.points[i] = (obj.points[i][0] + dx, obj.points[i][1] + dy)
                
                # atualiza os pontos para as próximas iterações
                obj.primeiro = (x, y)
                obj.previousPoints = obj.points

    def MouseClick(self, event, x, y):
        if event.LeftDown():
            self.handles = []
            for obj in self.manageStates.objects:
                if obj.selected:
                    self.calculate_handles(obj)
                    obj.primeiro = (x, y)
        
        elif event.LeftUp():
            self.selectObject(x, y)

    def MouseMotion(self, x, y):
        for obj in self.manageStates.objects:
                if obj.selected:
                    self.Translate(x, y)

    def calculate_handles(self, obj):
        # Calcula o centro da forma
        center_x, center_y = obj.calculate_center()
        # Adiciona handles nos cantos da forma
        for point in obj.points:
            self.handles.append(Handle(point[0], point[1]))
        # Adiciona handles nos pontos médios dos lados da forma
        for i in range(len(obj.points)):
            next_point = obj.points[(i + 1) % len(obj.points)]
            midpoint_x = (obj.points[i][0] + next_point[0]) / 2
            midpoint_y = (obj.points[i][1] + next_point[1]) / 2
            self.handles.append(Handle(midpoint_x, midpoint_y))

    def drawHandles(self):
        for handle in self.handles:
            handle.draw()

    def draw(self):
        super().draw()
        for obj in self.manageStates.objects:
                if obj.selected:
                    self.calculate_handles(obj)
        self.drawHandles()