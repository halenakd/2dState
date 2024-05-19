import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from state import State
from geometries import Object
import wx

currentPoints = []

class States(Enum):
    INIT_DRAW = 1
    FINISH_DRAW = 2

currentState = States.INIT_DRAW

class TriangleState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.tempTriangle = Object("triangle", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)


    # ========================================================
    # CALLBACK - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        global currentState, currentPoints
        triangulo = Object("triangle", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)

        if event.LeftDown():
            print("Clicou tri")   

        elif event.LeftUp():
            print("Soltou tri")

            if currentState == States.INIT_DRAW:
                # primeiro ponto
                currentPoints.append((x, y))

                currentState = States.FINISH_DRAW
            elif currentState == States.FINISH_DRAW:
                # segundo ponto
                currentPoints.append((x, y))

                # terceiro ponto
                dist = currentPoints[1][0] - currentPoints[0][0]
                currentPoints.append((currentPoints[0][0] - dist, currentPoints[1][1]))

                # todos os pontos
                triangulo.points = currentPoints
                triangulo.selected = True
                self.objects.append(triangulo)
                self.tempTriangle.points = []

                currentState = States.INIT_DRAW

                currentPoints = []

                self.manageStates.setState(self.manageStates.getIdleState())

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        #print("Movendo pressionado")
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):

        global currentState, currentPoints

        if currentState == States.FINISH_DRAW:
            # Copie a lista de pontos atual para evitar modificá-la diretamente
            tempPoints = currentPoints.copy()
            # Adicione o ponto atual do mouse à lista temporária
            tempPoints.append((x, y))

            dist = tempPoints[1][0] - tempPoints[0][0]

            tempPoints.append((tempPoints[0][0] - dist, tempPoints[1][1]))

            # Atualize os pontos do triângulo temporário
            self.tempTriangle.points = tempPoints

    def draw(self):
        super().draw()
        self.tempTriangle.draw()

