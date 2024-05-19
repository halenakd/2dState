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

class PolygonState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.tempPolygon = Object("polygon", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)


    # ========================================================
    # CALLBACK - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        global currentState, currentPoints
        poligono = Object("polygon", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)

        if event.LeftDown():
            print("Clicou tri")   

        elif event.LeftUp():
            print("Soltou tri")

            if len(currentPoints) > 2:
                if (np.sqrt((currentPoints[0][0] - x)**2 + (currentPoints[0][1] - y)**2)) < 0.1:
                    poligono.points = currentPoints
                    poligono.selected = True
                    self.objects.append(poligono)
                    currentPoints = []
                    self.manageStates.setState(self.manageStates.getIdleState())
                else:
                    currentPoints.append((x, y))
            else:
                currentPoints.append((x, y))


    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        #print("Movendo pressionado")
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        global currentState, currentPoints

        tempPoints = currentPoints.copy()

        tempPoints.append((x, y))

        self.tempPolygon.points = tempPoints

    def draw(self):
        super().draw()
        self.tempPolygon.drawTemp()

