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

class SquareState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.tempSquare = Object("square", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)


    # ========================================================
    # CALLBACK - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        global currentState, currentPoints
        quadrado = Object("square", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)

        if event.LeftDown():
            pass

        elif event.LeftUp():

            if currentState == States.INIT_DRAW:
                # primeiro ponto
                currentPoints.append((x, y))

                currentState = States.FINISH_DRAW
            elif currentState == States.FINISH_DRAW:
                pTemp = (x, y) # guardando o terceiro ponto

                # segundo ponto
                lado = pTemp[0] - currentPoints[0][0]
                currentPoints.append((pTemp[0], currentPoints[0][1]))

                # terceiro ponto
                currentPoints.append(pTemp)

                # quarto ponto
                currentPoints.append((currentPoints[0][0], currentPoints[2][1]))

                # todos os pontos
                quadrado.points = currentPoints
                quadrado.selected = True
                self.objects.append(quadrado)
                self.tempSquare.points = []

                currentState = States.INIT_DRAW

                currentPoints = []

                self.manageStates.setState(self.manageStates.getIdleState())

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        #print("Movendo pressionado")
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        #print("Movendo solto")

        global currentState, currentPoints

        if currentState == States.FINISH_DRAW:
            tempPoints = currentPoints.copy()

            pTemp = (x, y)
            
            tempPoints.append((pTemp[0], tempPoints[0][1]))

            tempPoints.append(pTemp)

            tempPoints.append((tempPoints[0][0], tempPoints[2][1]))

            self.tempSquare.points = tempPoints


    
    def draw(self):
        super().draw()
        self.tempSquare.draw()

