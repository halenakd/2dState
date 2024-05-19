import sys
import math
import numpy as np
from enum import Enum
from OpenGL.GL import *
from OpenGL.GLU import *
from triangleState import TriangleState
from idleState import IdleState
from selectedState import SelectedState
from squareState import SquareState
from circleState import CircleState
from polygonState import PolygonState
import wx
import wx.glcanvas as wxgl

class ManageStates:
    def __init__(self, color, lineWidth, objects):
        self.color = (0, 0, 0)
        self.lineWidth = 1
        self.style = "Contínuo"
        self.objects = objects
        self.canvas = None
        self.zoom = 1.0
        self.width = 800
        self.height = 600

        # iniciando estados
        self.idleState = IdleState(self)
        self.selectedState = SelectedState(self)
        self.triangleState = TriangleState(self)
        self.squareState = SquareState(self)
        self.circleState = CircleState(self)
        self.polygonState = PolygonState(self)

        self.currentState = self.idleState
    
    def setState(self, state):
        self.currentState = state

    def getIdleState(self):
        return self.idleState

    def getSelectedState(self):
        return self.selectedState

    def getTriangleState(self):
        return self.triangleState
    
    def getSquareState(self):
        return self.squareState
    
    def getCircleState(self):
        return self.circleState
    
    def getPolygonState(self):
        return self.polygonState