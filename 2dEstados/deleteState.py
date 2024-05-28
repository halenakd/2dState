import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from state import State
from geometries import Object
import wx
import wx.glcanvas as wxgl

# ========================================================
# DeleteState - ESTADO DE APAGAR OBJETOS
# ========================================================
# possibilita apagar objetos clicando em cima deles

class DeleteState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)


    # ========================================================
    # SelectObject - verifica se clico em cima do objeto e, se sim, apaga ele
    # ========================================================

    def selectObject(self, x, y):
        print("DeleteState - selectObject")
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
                        self.manageStates.objects.remove(obj)
                        break
                    else:
                        if x_int > x and y_int > min(obj.points[i][1], obj.points[iMaisUm][1]) and y_int <= max(obj.points[i][1], obj.points[iMaisUm][1]):
                            N_int += 1
                else:
                    if y == obj.points[i][1] and x >= min(obj.points[i][0], obj.points[iMaisUm][0]) and x <= max(obj.points[i][0], obj.points[iMaisUm][0]):
                        self.manageStates.objects.remove(obj)
                        break

            if (N_int % 2) != 0:
                self.manageStates.objects.remove(obj)
            else:
                obj.selected = False


    # ========================================================
    # CALLBACK - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        if event.LeftDown():
            print("DeleteState - MouseClick(LeftDown)")
            pass

        elif event.LeftUp():
            print("DeleteState - MouseClick(LeftUp)")
            self.selectObject(x, y)

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        print("DeleteState - MouseMotion")
        pass
    
    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        print("DeleteState - MousePassiveMotion")
        pass

    # roda do mouse
    def onMouseWheel(self, event):
        print("DeleteState - onMouseWheel")


    # ========================================================
    # DRAW - desenhos
    # ========================================================

    def draw(self):
        print("DeleteState - draw")
        super().draw()
    