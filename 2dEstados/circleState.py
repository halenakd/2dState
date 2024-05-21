import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from state import State
from geometries import Object
import wx

# controle de estados dentro do estado de círculo
class States(Enum):
    INIT_DRAW = 1
    FINISH_DRAW = 2

# estado inicial de desenho
currentState = States.INIT_DRAW

currentPoints = []
center = (0, 0)

# ========================================================
# CircleState - ESTADO DE DESENHAR CÍRCULO
# ========================================================
# possibilita desenhar um círculo e ver o desenho em tempo real
# no fim, o círculo é adicionado à lista de objetos do programa

class CircleState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)
        self.tempCircle = Object("circle", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)


    # ========================================================
    # CALLBACKS - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        global currentState, currentPoints, center
        circulo = Object("circle", self.manageStates.color, self.manageStates.style, self.manageStates.lineWidth)

        if event.LeftDown():
            print("CircleState - MouseClick(LeftDown)")
            pass

        elif event.LeftUp():
            print("CircleState - MouseClick(LeftUp)")
            if currentState == States.INIT_DRAW:
                center = (x, y)

                currentState = States.FINISH_DRAW
            elif currentState == States.FINISH_DRAW:
                raio = np.sqrt((center[0] - x)**2 + (center[1] - y)**2)

                ang = 0.0
                PONTOS = 100
                while ang <= 360:
                    xc = center[0] + raio * math.cos(math.radians(ang))
                    yc = center[1] + raio * math.sin(math.radians(ang))
                    ang += 360/PONTOS
                    currentPoints.append((xc, yc))

                circulo.points = currentPoints
                circulo.center = center
                circulo.selected = True
                self.manageStates.objects.append(circulo)
                self.tempCircle.points = []

                currentState = States.INIT_DRAW

                currentPoints = []

                self.manageStates.setState(self.manageStates.getIdleState())

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        print("CircleState - MouseMotion")
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        print("CircleState - MousePassiveMotion")

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

            self.tempCircle.points = tempPoints

    # roda do mouse
    def onMouseWheel(self, event):
        print("CircleState - onMouseWheel")
        if self.ctrl_pressed:
            rotation = event.GetWheelRotation()
            self.manageStates.zoom -= rotation / event.GetWheelDelta() * 0.1


    # ========================================================
    # DRAW - desenhos
    # ========================================================

    def draw(self):
        print("CircleState - Draw") 
        super().draw()
        self.tempCircle.draw()

