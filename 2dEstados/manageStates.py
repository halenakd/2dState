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
from deleteState import DeleteState
import wx
import wx.glcanvas as wxgl

# ========================================================
# Classe ManageStates 
# ========================================================
# faz o gerenciamento dos estados
# guarda o estado atual e tem as funções necessárias para trocar de estado (setState e gets)
# também guarda algumas variáveis utilizadas no programa todos

class ManageStates:
    def __init__(self, color, lineWidth, objects):
        self.color = (0, 0, 0)
        self.lineWidth = 1
        self.style = "Contínuo"
        self.objects = objects
        self.canvas = None
        self.zoom = 1.0
        self.ctrl_pressed = False

        # iniciando estados
        self.idleState = IdleState(self)
        self.selectedState = SelectedState(self)
        self.triangleState = TriangleState(self)
        self.squareState = SquareState(self)
        self.circleState = CircleState(self)
        self.polygonState = PolygonState(self)
        self.deleteState = DeleteState(self)

        # setando o estado inicial como estado atual
        self.currentState = self.idleState

    # função que seta o estado passado como parâmetro como o estado atual
    def setState(self, state):
        self.currentState = state

    # funções de get dos estados - retornam o estado desejado
    # seus retornos são utilizados como parâmetro na função setState
    # ex.: setState(getTriangleState())
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
    
    def getDeleteState(self):
        return self.deleteState