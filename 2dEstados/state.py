import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from geometries import Object
import wx
import wx.glcanvas as wxgl

# ========================================================
# Classe State
# ========================================================
# define a interface comum para todas as classes de estado

class State:
    def __init__(self, manageStates):
        self.manageStates = manageStates


    # ========================================================
    # CALLBACKS - MOUSE
    # ========================================================

    # click do mouse quando pressiona e quando solta
    def MouseClick(self, event, x, y):
        if event.LeftDown():
            print("State - MousePassiveMotion")
            pass
        elif event.LeftUp():
            print("State - MousePassiveMotion")
            pass

    # mouse em movimento pressionado
    def MouseMotion(self, x, y):
        pass

    # mouse em movimento solto
    def MousePassiveMotion(self, x, y):
        pass

    # roda do mouse
    def onMouseWheel(self, event):
        pass


    # ========================================================
    # DRAW - desenhos
    # ========================================================

    def draw(self):
        pass
    