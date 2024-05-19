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

class IdleState(State):
    def __init__(self, manageStates):
        super().__init__(manageStates)


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
    # CALLBACK - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        if event.LeftDown():
            print("Clicou")   

        elif event.LeftUp():
            print("Soltou")
            self.selectObject(x, y)

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        #print("Movendo pressionado")
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        #print("Movendo solto")

        # Redesenha a cena
        #self.manageStates.canvas.Refresh()
        pass

    def onMouseWheel(self, event):
        if self.ctrl_pressed:
            rotation = event.GetWheelRotation()
            # Invertendo a direção do zoom
            self.manageStates.zoom -= rotation / event.GetWheelDelta() * 0.1
            """# Limitando o zoom para garantir que não ultrapasse os limites mínimos
            if self.manageStates.zoom < 0.01:
                self.manageStates.zoom = 0.01"""

    def draw(self):
        super().draw()
    