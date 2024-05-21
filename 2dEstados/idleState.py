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
# IdleState - ESTADO DE ESPERA
# ========================================================
# é o estado inicial do programa, de espera e de seleção
# permite selecionar objetos, levando ao estado de Selecionado


class IdleState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)


    # ========================================================
    # selectObject - permite saber se o click foi dentro ou fora do objeto (atualiza o status de obj.selected)
    # ========================================================

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


    # ========================================================
    # CALLBACKS - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        if event.LeftDown():
            print("IdleState - MouseClick(LeftDown)")
            pass

        elif event.LeftUp():
            print("IdleState - MouseClick(LeftUp)")
            self.selectObject(x, y)

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        print("IdleState - MouseMotion")
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        print("IdleState - MousePassiveMotion")
        pass

    # roda do mouse
    def onMouseWheel(self, event):
        print("IdleState - onMouseWheel")
        if self.ctrl_pressed:
            rotation = event.GetWheelRotation()
            # Invertendo a direção do zoom
            self.manageStates.zoom -= rotation / event.GetWheelDelta() * 0.1


    # ========================================================
    # DRAW - desenhos
    # ========================================================

    def draw(self):
        print("IdleState - draw")
        super().draw()
    