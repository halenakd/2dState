import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from state import State
from geometries import Object
import wx

# controle de estados dentro do estado de triângulo
class States(Enum):
    INIT_DRAW = 1
    FINISH_DRAW = 2

# estado inicial de desenho
currentState = States.INIT_DRAW

currentPoints = []

# ========================================================
# SquareState - ESTADO DE DESENHAR QUADRADO
# ========================================================
# possibilita desenhar um quadrado e ver o desenho em tempo real
# no fim, o quadrado é adicionado à lista de objetos do programa

class SquareState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.tempSquare = Object("square", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)


    # ========================================================
    # CALLBACKS - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        global currentState, currentPoints
        quadrado = Object("square", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)

        if event.LeftDown():
            print("SquareState - MouseClick(LeftDown)")
            pass

        elif event.LeftUp():
            print("SquareState - MouseClick(LeftUp)")

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
                self.manageStates.objects.append(quadrado)
                self.tempSquare.points = []

                currentPoints = []

                # se o estado geral do progama continuasse no de triângulo, 
                # o estado dentro do estado de triângulo deveria voltar ao inicial,
                # para que mais triângulos pudessem ser desenhados
                #currentState = States.INIT_DRAW

                # troca o estado geral do programa para o estado de "espera"
                self.manageStates.setState(self.manageStates.getIdleState())

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        print("SquareState - MouseMotion")
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        print("SquareState - MousePassiveMotion")

        global currentState, currentPoints

        if currentState == States.FINISH_DRAW:
            tempPoints = currentPoints.copy()

            pTemp = (x, y)
            
            tempPoints.append((pTemp[0], tempPoints[0][1]))

            tempPoints.append(pTemp)

            tempPoints.append((tempPoints[0][0], tempPoints[2][1]))

            self.tempSquare.points = tempPoints

    # roda do mouse
    def onMouseWheel(self, event):
        print("SquareState - onMouseWheel")
        if self.ctrl_pressed:
            rotation = event.GetWheelRotation()
            self.manageStates.zoom -= rotation / event.GetWheelDelta() * 0.1


    # ========================================================
    # DRAW - desenhos
    # ========================================================

    def draw(self):
        print("SquareState - Draw") 
        super().draw()
        self.tempSquare.draw()

