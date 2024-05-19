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

# aqui vai ter rotação, translação, mudar de cor, etc

"""class SelectedState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.sentido = 'H'
        self.circle = Circle((0,0), 1, 20)


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

    
    def Rotate(self, ang, x, y):
        for obj in self.manageStates.objects:
            if obj.selected:
                # Calcula a diferença de posição do mouse
                deltaX = x - obj.primeiro[0]
                deltaY = y - obj.primeiro[1]

                # Calcula o ângulo de rotação com base na diferença de posição do mouse
                #angle = math.atan2(deltaY, deltaX)
                #angle = math.pi/100
                angle = math.radians(1)

                # Calcular o ponto médio dos cantos do retângulo
                centerX, centerY = obj.calculate_center()

                cosTheta = math.cos(angle)
                sinTheta = math.sin(angle)

                # Atualiza a posição de todos os pontos
                for i in range(len(obj.points)):
                    #x′ = cos θ(x − x0) − sin θ(y − y0) + x0
                    #y′ = sin θ(x − x0) + cos θ(y − y0) + y0

                    # Calcula a nova posição do ponto após a rotação
                    newX = cosTheta * (obj.points[i][0] - centerX) - sinTheta * (obj.points[i][1] - centerY) + centerX
                    newY = sinTheta * (obj.points[i][0] - centerX) + cosTheta * (obj.points[i][1] - centerY) + centerY

                    obj.points[i] = (newX, newY)

                self.circle.rotate(math.radians(ang))

                obj.primeiro = (x, y)
                    

    # ========================================================
    # CALLBACK - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        if event.LeftDown():
            print("Clicou")
            # o primeiro click é a posição inicial do deslocamento
            for obj in self.manageStates.objects:
                if obj.selected:
                    obj.primeiro = (x, y)

        elif event.LeftUp():
            print("Soltou")

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        #print("Movendo pressionado")

        #self.Translate(x, y)

        self.Rotate(1, x, y)

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        #print("Movendo solto")
        pass

    def calculate_handles(self, obj):
        handles = []

        # Calcula o ponto médio dos cantos do triângulo
        center_x, center_y = obj.calculate_center()

        # Calcula os pontos dos handles após a rotação
        for point in obj.points:
            # Calcula o vetor do centro do triângulo até o ponto
            vec_x = point[0] - center_x
            vec_y = point[1] - center_y

            # Aplica a rotação ao vetor do ponto
            rotated_x = vec_x * math.cos(self.circle.rotation_angle) - vec_y * math.sin(self.circle.rotation_angle)
            rotated_y = vec_x * math.sin(self.circle.rotation_angle) + vec_y * math.cos(self.circle.rotation_angle)

            # Adiciona o ponto do handle à lista
            handles.append((center_x + rotated_x, center_y + rotated_y))

        return handles

    def drawHandles(self):
        for obj in self.manageStates.objects:
            if obj.selected:
                if obj.type == "triangle":
                    handles = self.calculate_handles(obj)

                    # Desenha os handles
                    glPointSize(5.0)
                    glBegin(GL_POINTS)
                    for handle in handles:
                        glVertex2f(handle[0], handle[1])
                    glEnd()

                    # Desenha a circunferência
                    self.circle.center = (obj.calculate_center()[0], obj.calculate_center()[1] - 6)
                    self.circle.draw()


    def drawHandles(self):
        for obj in self.manageStates.objects:
            if obj.selected:
                if(obj.type == "triangle"):
                    # RETÂNGULO TRACEJADO EM VOLTA DO OBJETO
                    # glLineStipple(GLint factor, GLushort pattern) - configuração do tracejado
                    glLineStipple(5, 0xAAAA)
                    glEnable(GL_LINE_STIPPLE)
                    glBegin(GL_LINE_LOOP)
                    glVertex2f(obj.points[1][0], obj.points[1][1])
                    glVertex2f(obj.points[2][0], obj.points[2][1])
                    glVertex2f(obj.points[2][0], obj.points[0][1])
                    glVertex2f(obj.points[1][0], obj.points[0][1])
                    glEnd()
                    glDisable(GL_LINE_STIPPLE)

                    # HANDLES/PUIXADORES (QUADRADINHOS) NOS CANTOS E NOS MEIOS
                    glPointSize(5.0)
                    glBegin(GL_POINTS)
                    glVertex2f(obj.points[1][0], obj.points[1][1]) # canto 1
                    glVertex2f(obj.points[2][0], obj.points[2][1]) # canto 2
                    glVertex2f(obj.points[2][0], obj.points[0][1]) # canto 3
                    glVertex2f(obj.points[1][0], obj.points[0][1]) # canto 4
                    
                    # Calcula os pontos médios das linhas do retângulo
                    midpoint_x = (obj.points[1][0] + obj.points[2][0]) / 2
                    midpoint_y = (obj.points[2][1] + obj.points[0][1]) / 2
                    
                    glVertex2f(midpoint_x, obj.points[1][1]) # ponto médio entre canto 1 e canto 2
                    glVertex2f(obj.points[2][0], midpoint_y) # ponto médio entre canto 2 e canto 3
                    glVertex2f(midpoint_x, obj.points[0][1]) # ponto médio entre canto 3 e canto 4
                    glVertex2f(obj.points[1][0], midpoint_y) # ponto médio entre canto 4 e canto 1
                    glEnd()


                    self.circle.center = (obj.calculate_center()[0], obj.calculate_center()[1] - 6)
                    self.circle.draw()
                    
        self.manageStates.canvas.Refresh()

    def draw(self):
        glPushMatrix()
        glScalef(self.manageStates.zoom, self.manageStates.zoom, 1.0)  # Aplica escala de zoom

        self.drawHandles()

        super().draw()

        glPopMatrix()"""


class Handle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.x - 5, self.y - 5)
        glVertex2f(self.x + 5, self.y - 5)
        glVertex2f(self.x + 5, self.y + 5)
        glVertex2f(self.x - 5, self.y + 5)
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
            self.handles = []  # Limpa handles anteriores
            # Calcula handles para a forma selecionada
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

    def draw(self):
        #glPushMatrix()
        #glScalef(self.manageStates.zoom, self.manageStates.zoom, 1.0)
        for obj in self.manageStates.objects:
                if obj.selected:
                    self.calculate_handles(obj)
        self.drawHandles()
        super().draw()
        #glPopMatrix()