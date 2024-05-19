import wx
import wx.glcanvas as wxgl
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLU import *
from geometries import Object
from geometries import Circle
from state import State
from manageStates import ManageStates

# cor atual desenho
color = (0.0, 0.0, 0.0)

# tamanho atual da linha
lineWidth = 1.0

# lista de objetos atuais
objects = []

manageStates = ManageStates(color, lineWidth, objects)

# Classe de canvas OpenGL
class MyGLCanvas(wxgl.GLCanvas):
    def __init__(self, parent, manageStates):
        wxgl.GLCanvas.__init__(self, parent, -1)

        self.manageStates = manageStates
        self.context = glcanvas.GLContext(self)
        self.SetCurrent(self.context)  # Define o contexto OpenGL atual

        self.manageStates.zoom = 1.0
        self.ortho = [30, 30, 30, 30]
        self.ctrl_pressed = False
        self.lastMousePos = None
        
        self.InitGL()  # Inicializa OpenGL agora que o contexto está definido
        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouse)
        self.Bind(wx.EVT_LEFT_UP, self.onMouse)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)

    # Método de inicialização OpenGL
    def InitGL(self):
        glClearColor(1, 1, 1, 1)  # Cor de fundo
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-self.ortho[0], self.ortho[1], -self.ortho[2], self.ortho[3], -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

    # Evento de redimensionamento
    def onSize(self, event):
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)
        self.Refresh()

    # Evento de pintura
    def onPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        self.draw()
        self.SwapBuffers()

    # Método para desenhar na tela
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Desenha os eixos
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_LINES)
        glVertex3f(-30.0, 0.0, 0.0)
        glVertex3f(30.0, 0.0, 0.0)
        glVertex3f(0.0, -30.0, 0.0)
        glVertex3f(0.0, 30.0, 0.0)
        glEnd()

        self.manageStates.currentState.draw()
        for obj in objects:
            obj.draw()

        self.Refresh()


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


    def onMouse(self, event):
        if event.LeftDown():
            self.dragging = True
            self.lastMousePos = event.GetPosition()

        x, y = event.GetPosition()
        self.manageStates.currentState.MouseClick(event, x, y)
        self.Refresh()

    # Evento de movimento do mouse
    def onMotion(self, event):
        if event.Dragging():
            mousePos = event.GetPosition()
            dx = mousePos.x - self.lastMousePos.x
            dy = mousePos.y - self.lastMousePos.y

            # Atualiza a posição do objeto (ou outra lógica de interação desejada)
            # Aqui, apenas imprime a diferença de posição do mouse
            print(f"Mouse moveu: dx={dx}, dy={dy}")

            self.lastMousePos = mousePos

            self.manageStates.currentState.MousePassiveMotion(mousePos.x, mousePos.y)
            self.Refresh()

    def onMouseWheel(self, event):
        if self.ctrl_pressed:
            rotation = event.GetWheelRotation()
            # Invertendo a direção do zoom
            self.manageStates.zoom -= rotation / event.GetWheelDelta() * 0.1
            # Limitando o zoom para garantir que não ultrapasse os limites mínimos
            if self.manageStates.zoom < 0.01:
                self.manageStates.zoom = 0.01
            self.updateProjection()
            self.Refresh()


    def updateProjection(self):
        self.SetCurrent(self.context)
        size = self.GetClientSize()
        glViewport(0, 0, size.width, size.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        # Define limites mínimos para o zoom
        min_zoom = 0.1

        # Calcula os novos limites do ortho
        left = -self.ortho[0] * self.manageStates.zoom
        right = self.ortho[1] * self.manageStates.zoom
        bottom = -self.ortho[2] * self.manageStates.zoom
        top = self.ortho[3] * self.manageStates.zoom

        # Verifica se o zoom ultrapassa os limites mínimos
        if self.manageStates.zoom < min_zoom:
            self.manageStates.zoom = min_zoom

        # Verifica se os limites do ortho são válidos
        if left >= right or bottom >= top:
            return

        glOrtho(left, right, bottom, top, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)


# Classe de frame principal
class MyFrame(wx.Frame):
    def __init__(self, parent, title, manageStates):
        wx.Frame.__init__(self, parent, title=title, size=(800, 600))

        self.manageStates = manageStates
        self.canvas = MyGLCanvas(self, self.manageStates)
        
        # Adiciona uma faixa para os botões na parte superior
        self.buttons_panel = wx.Panel(self)
        self.buttons_panel.SetBackgroundColour(wx.Colour(220, 220, 220))
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons_panel.SetSizer(self.button_sizer)
        
        # Adiciona botões à faixa de botões
        self.selectButton = wx.Button(self.buttons_panel, label="Select")
        self.triangleButton = wx.Button(self.buttons_panel, label="Triangle")
        self.button_sizer.Add(self.selectButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.button_sizer.Add(self.triangleButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        # Adicione a função de manipulador de eventos ao botão 1
        self.selectButton.Bind(wx.EVT_BUTTON, self.onSelectButtonClicked)
        self.triangleButton.Bind(wx.EVT_BUTTON, self.onTriangleButton1Clicked)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.buttons_panel, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.onClose)

    def onClose(self, event):
        self.Destroy()

    # Função de manipulador de eventos para o botão 1
    def onSelectButtonClicked(self, event):
        print("Botão Select clicado!")
        self.manageStates.setState(self.manageStates.getIdleState())

    # Função de manipulador de eventos para o botão 2
    def onTriangleButton1Clicked(self, event):
        print("Botão Triangle clicado!")
        self.manageStates.setState(self.manageStates.getTriangleState())


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(None, "Paint com wxPython e OpenGL", manageStates)
    frame.Show(True)
    app.MainLoop()
