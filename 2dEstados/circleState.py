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
center = (0, 0)

class States(Enum):
    INIT_DRAW = 1
    FINISH_DRAW = 2

currentState = States.INIT_DRAW

class CircleState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.tempCircle = Object("circle", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)


    # ========================================================
    # CALLBACK - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        global currentState, currentPoints, center
        circulo = Object("circle", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)

        if event.LeftDown():
            pass

        elif event.LeftUp():

            if currentState == States.INIT_DRAW:
                # centro
                center = (x, y)
                print("centro:", circulo.center, center)

                currentState = States.FINISH_DRAW
            elif currentState == States.FINISH_DRAW:
                # raio
                raio = np.sqrt((center[0] - x)**2 + (center[1] - y)**2)

                ang = 0.0
                PONTOS = 100
                while ang <= 360:
                    xc = center[0] + raio * math.cos(math.radians(ang))
                    yc = center[1] + raio * math.sin(math.radians(ang))
                    ang += 360/PONTOS
                    currentPoints.append((xc, yc))

                # todos os pontos
                circulo.points = currentPoints
                circulo.center = center
                circulo.selected = True
                self.objects.append(circulo)
                self.tempCircle.points = []

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

            tempPoints = currentPoints.copy()

            raio = np.sqrt((center[0] - x)**2 + (center[1] - y)**2)

            ang = 0.0
            PONTOS = 36
            while ang <= 360:
                x = center[0] + raio * math.cos(math.radians(ang))
                y = center[1] + raio * math.sin(math.radians(ang))
                ang += 360/PONTOS
                tempPoints.append((x, y))

            # Atualize os pontos do triângulo temporário
            self.tempCircle.points = tempPoints

    def draw(self):
        super().draw()
        self.tempCircle.draw()

