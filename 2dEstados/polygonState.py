import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from state import State
from geometries import Object
import wx

# ========================================================
# PolygonState - ESTADO DE DESENHAR POLÍGONO
# ========================================================
# possibilita desenhar um polígono e ver o desenho em tempo real
# no fim, o polígono é adicionado à lista de objetos do programa

class PolygonState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.tempPolygon = Object("polygon", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)


    # ========================================================
    # CALLBACKS - mouse
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        global currentState, currentPoints
        poligono = Object("polygon", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)

        if event.LeftDown():
            print("PolygonState - MouseClick(LeftDown)")

        elif event.LeftUp():
            print("PolygonState - MouseClick(LeftUp)")

            if len(currentPoints) > 2:
                if (np.sqrt((currentPoints[0][0] - x)**2 + (currentPoints[0][1] - y)**2)) < 0.1:
                    poligono.points = currentPoints
                    poligono.selected = True
                    self.manageStates.objects.append(poligono)
                    currentPoints = []
                    self.manageStates.setState(self.manageStates.getIdleState())
                else:
                    currentPoints.append((x, y))
            else:
                currentPoints.append((x, y))

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        print("PolygonState - MouseMotion")
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        print("PolygonState - MousePassiveMotion")

        global currentState, currentPoints

        tempPoints = currentPoints.copy()

        tempPoints.append((x, y))

        self.tempPolygon.points = tempPoints

    # roda do mouse
    def onMouseWheel(self, event):
        print("PolygonState - onMouseWheel")
        if self.ctrl_pressed:
            rotation = event.GetWheelRotation()
            self.manageStates.zoom -= rotation / event.GetWheelDelta() * 0.1


    # ========================================================
    # DRAW - desenhos
    # ========================================================

    def draw(self):
        print("PolygonState - draw")
        super().draw()
        self.tempPolygon.drawTemp()

