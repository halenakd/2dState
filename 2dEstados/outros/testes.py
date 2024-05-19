import wx
import wx.glcanvas as wxgl
from wx import glcanvas
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

class MyGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1, attribList=[
            wx.glcanvas.WX_GL_RGBA,
            wx.glcanvas.WX_GL_DOUBLEBUFFER,
            wx.glcanvas.WX_GL_DEPTH_SIZE, 16,
        ])

        self.context = glcanvas.GLContext(self)

        self.points = []  # Lista para armazenar os pontos do triângulo

        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouseLeftDown)

    def onSize(self, event):
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)
        self.Refresh()

    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        self.draw()
        self.SwapBuffers()

    def draw(self):
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        # Desenhe o triângulo se houver pontos suficientes
        if len(self.points) >= 3:
            glColor3f(0, 0, 0)
            glBegin(GL_TRIANGLES)
            for point in self.points:
                print(*point)
                glVertex2f(*point)
            glEnd()

    def onMouseLeftDown(self, event):
        x, y = event.GetPosition()
        # Normaliza as coordenadas para o intervalo [-1, 1]
        x_norm = 2 * (x / self.GetClientSize().GetWidth()) - 1
        y_norm = 1 - 2 * (y / self.GetClientSize().GetHeight())
        self.points.append((x_norm, y_norm))
        self.Refresh()

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        
        self.canvas = MyGLCanvas(self)

        self.Show(True)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "Desenhar Triângulo com Mouse")
    app.MainLoop()
