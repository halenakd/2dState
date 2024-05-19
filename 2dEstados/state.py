import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from geometries import Object
import wx
import wx.glcanvas as wxgl

class State:
    def __init__(self, manageStates):
        self.manageStates = manageStates
        self.color = manageStates.color
        self.lineWidth = manageStates.lineWidth
        self.objects = manageStates.objects
        self.ctrl_pressed = False


    # ========================================================
    # CALLBACK - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        if event.LeftDown():
            print("Clicou")
        elif event.LeftUp():
            print("Soltou")

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        print("Movendo pressionado")

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        print("Movendo solto")


    def draw(self):
        pass


    # ========================================================
    # DISTÂNCIA ENTRE PONTOS
    # ========================================================

    def Dist(self, a, b):
        x1, x2 = a[0], b[0]
        y1, y2 = a[1], b[1]

        dist = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        
        return dist
    