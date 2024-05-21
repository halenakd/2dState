import wx
import wx.glcanvas as wxgl
from wx import glcanvas
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from geometries import Object
from geometries import Circle
from state import State
from manageStates import ManageStates

# ========================================================
# MyGLCanvas
# ========================================================
# operações referentes ao canvas do openGL
# desenho, eventos (mouse, teclado), zoom, resize, etc...

class MyGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent, manageStates):
        glcanvas.GLCanvas.__init__(self, parent, -1, attribList=[
            wx.glcanvas.WX_GL_RGBA,
            wx.glcanvas.WX_GL_DOUBLEBUFFER,
            wx.glcanvas.WX_GL_DEPTH_SIZE, 16,
        ])

        self.parent = parent
        self.manageStates = manageStates
        self.context = glcanvas.GLContext(self)

        # ========================================================
        # VARIÁVEIS NECESSÁRIAS PARA O CONTROLE DO PROGRAMA
        # ========================================================

        self.manageStates.zoom = 1.0 # zoom atual do programa
        self.ortho = [300, 300, 400, 400]
        self.left = -self.ortho[0]
        self.right = self.ortho[1]
        self.bottom = -self.ortho[2]
        self.top = self.ortho[3]
        self.ctrl_pressed = False # para dar zoom com a rodinha do mouse
        self.lastMousePos = None # última posição do mouse utilizada em algumas operações com o mouse
        self.background_color = (1, 1, 1, 1.0) # cor de fundo - branca
        self.dragging = False # para o movimento do mouse pressionado ou solto

        # ========================================================
        # EVENTOS
        # ========================================================

        # ligando as funções de tratamento à cada evento
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouse)
        self.Bind(wx.EVT_LEFT_UP, self.onMouse)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
    
    # ========================================================
    # onSize - resize
    # ========================================================

    def onSize(self, event):
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)
        self.Refresh()

    # ========================================================
    # FUNÇÕES DE DESENHO - onPaint e draw
    # ========================================================

    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        self.draw()
        self.SwapBuffers()

    def draw(self):
        glViewport(0, 0, *self.GetSize())
        aspect_ratio = self.GetSize()[0] / self.GetSize()[1]
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if aspect_ratio > 1:
            glOrtho(-aspect_ratio, aspect_ratio, -1, 1, -1.0, 1.0)
        else:
            glOrtho(-1, 1, -1/aspect_ratio, 1/aspect_ratio, -1.0, 1.0)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.manageStates.currentState.draw()

        for obj in self.manageStates.objects:
            obj.draw()

        self.updateSelectedObjectInfo()


    # ========================================================
    # updateSelectedObjectInfo - chama as funções de cálculo de área e perímetro para fazer a atualização
    # ========================================================

    def updateSelectedObjectInfo(self):
        for obj in self.manageStates.objects:
            if obj.selected:
                area = obj.calculateArea()
                perimeter = obj.calculatePerimeter()
                self.parent.updateInfoDisplay(area, perimeter)
            else:
                self.parent.updateInfoDisplay(0, 0)


    # ========================================================
    # CALLBACKS - teclado
    # ========================================================

    # Evento de tecla pressionada
    def onKeyDown(self, event):
        if event.GetKeyCode() == wx.WXK_CONTROL:
            self.ctrl_pressed = True
        event.Skip()

    # Evento de tecla liberada
    def onKeyUp(self, event):
        if event.GetKeyCode() == wx.WXK_CONTROL:
            self.ctrl_pressed = False
        event.Skip()


    # ========================================================
    # CALLBACKS - mouse
    # ========================================================

    def onMouse(self, event):
        x, y = event.GetPosition()
        normalCoords = self.normalizar(x, y)
        if event.LeftDown():
            self.lastMousePos = normalCoords

        self.manageStates.currentState.MouseClick(event, normalCoords[0], normalCoords[1])
        self.Refresh()

    def onMotion(self, event):
        x, y = event.GetPosition()
        normalCoords = self.normalizar(x, y)
        if self.lastMousePos is not None:
            dx = normalCoords[0] - self.lastMousePos[0]
            dy = normalCoords[1] - self.lastMousePos[1]

            self.lastMousePos = normalCoords

            self.manageStates.currentState.MousePassiveMotion(normalCoords[0], normalCoords[1])
            self.Refresh()
            
        if self.lastMousePos is not None and event.Dragging():
            self.manageStates.currentState.MouseMotion(normalCoords[0], normalCoords[1])
            self.Refresh()
    
    def onMouseWheel(self, event):
        self.manageStates.currentState.onMouseWheel(event)
        self.Refresh()


    # ========================================================
    # normalizar - normaliza as coordenadas ([-1, 1])
    # ========================================================

    def normalizar(self, x, y):
        width, height = self.GetSize()
        aspect_ratio = width / height
        x_norm = 2 * ((x / width) - 0.5) * aspect_ratio
        y_norm = 1 - 2 * (y / height)
        return x_norm, y_norm