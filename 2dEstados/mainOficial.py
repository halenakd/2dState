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

# cor atual desenho
color = (0.0, 0.0, 0.0)

# tamanho atual da linha
lineWidth = 1.0

# lista de objetos atuais
objects = []

class MyGLCanvas(glcanvas.GLCanvas):
    def __init__(self, parent, manageStates):
        glcanvas.GLCanvas.__init__(self, parent, -1, attribList=[
            wx.glcanvas.WX_GL_RGBA,
            wx.glcanvas.WX_GL_DOUBLEBUFFER,
            wx.glcanvas.WX_GL_DEPTH_SIZE, 16,
        ])

        self.manageStates = manageStates
        self.context = glcanvas.GLContext(self)

        self.manageStates.zoom = 1.0
        size = self.GetClientSize()
        #self.ortho = [self.manageStates.width/20, self.manageStates.width/20, self.manageStates.height/20, self.manageStates.height/20]
        self.ortho = [300, 300, 800, 800]
        self.left = -self.ortho[0]
        self.right = self.ortho[1]
        self.bottom = -self.ortho[2]
        self.top = self.ortho[3]
        self.ctrl_pressed = False
        self.lastMousePos = None
        self.color = (1, 1, 1)
        self.background_color = (1, 1, 1, 1.0)
        self.dragging = False

        self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.onMouse)
        self.Bind(wx.EVT_LEFT_UP, self.onMouse)
        self.Bind(wx.EVT_MOTION, self.onMotion)
        self.Bind(wx.EVT_MOUSEWHEEL, self.onMouseWheel)
        self.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.onKeyUp)
    
    # Evento de redimensionamento
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
        glOrtho(self.left, self.right, self.bottom, self.top, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glClearColor(*self.background_color)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        self.manageStates.currentState.draw()

        for obj in self.manageStates.objects:
            obj.draw()

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
        x, y = event.GetPosition()
        normalCoords = self.normalizar(x, y)
        if event.LeftDown():
            self.lastMousePos = normalCoords
        """elif event.LeftUp():
            self.dragging = False"""

        print(normalCoords[0], normalCoords[1])
        self.manageStates.currentState.MouseClick(event, normalCoords[0], normalCoords[1])
        self.Refresh()

    def onMotion(self, event):
        x, y = event.GetPosition()
        #normalCoords = event.GetPosition()
        normalCoords = self.normalizar(x, y)
        if self.lastMousePos is not None and not event.Dragging():
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
        self.left = -self.ortho[0] * self.manageStates.zoom
        self.right = self.ortho[1] * self.manageStates.zoom
        self.bottom = -self.ortho[2] * self.manageStates.zoom
        self.top = self.ortho[3] * self.manageStates.zoom

        print(self.left, self.right, self.bottom, self.top)

        """# Verifica se o zoom ultrapassa os limites mínimos
        if self.manageStates.zoom < min_zoom:
            self.manageStates.zoom = min_zoom"""

        # Verifica se os limites do ortho são válidos
        """if self.left >= self.right or self.bottom >= self.top:
            return"""

        glOrtho(self.left, self.right, self.bottom, self.top, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

    def normalizar(self, x, y):

        x_norm = 2 * (x / self.GetClientSize().GetWidth()) - 1
        y_norm = 1 - 2 * (y / self.GetClientSize().GetHeight())
        
        return x_norm, y_norm
        
class MyFrame(wx.Frame):
    # cor atual desenho
    color = (0.0, 0.0, 0.0)

    # tamanho atual da linha
    lineWidth = 1.0

    # lista de objetos atuais
    objects = []

    manageStates = None

    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        
        self.manageStates = ManageStates(color, lineWidth, objects)
        self.canvas = MyGLCanvas(self, self.manageStates)

        self.manageStates.width = 800
        self.manageStates.height = 600

        # Adiciona uma faixa para os botões na parte superior
        self.buttons_panel = wx.Panel(self)
        self.buttons_panel.SetBackgroundColour(wx.Colour(220, 220, 220))
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons_panel.SetSizer(self.button_sizer)
        
        # botão select
        # é associado ao painel buttons_panel
        # BU_EXACTFIT - o botão tem exatamente o espaço que precisa pro conteúdo
        # NO_BORDER - tira a borda ao redor do botão, fica contínuo com o fundo
        self.selectButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        # define a cor do botão
        self.selectButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        # carrega a imagem como um bitmap no formato de png
        selectIcon = wx.Bitmap("icons/cursor.png", wx.BITMAP_TYPE_PNG)
        # pega as dimensões da imagem
        width, height = selectIcon.GetSize()
        # converte pra um objeto, redimensiona e converte de volta para bitmap
        selectIcon = selectIcon.ConvertToImage().Rescale(width//12, height//12).ConvertToBitmap()
        # define o bitmap já criado como ícone do botão
        self.selectButton.SetBitmap(selectIcon)
        # associa o evento de click no botão à função de tratamento dele
        self.selectButton.Bind(wx.EVT_BUTTON, self.onSelectButtonClicked)
        # adiciona ao sizer
        self.button_sizer.Add(self.selectButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        # botão fill
        self.fillButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.fillButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        fillIcon = wx.Bitmap("icons/latatinta.png", wx.BITMAP_TYPE_PNG)
        width, height = fillIcon.GetSize()
        fillIcon = fillIcon.ConvertToImage().Rescale(width//18, height//20).ConvertToBitmap()
        self.fillButton.SetBitmap(fillIcon)
        self.fillButton.Bind(wx.EVT_BUTTON, self.onFillButtonClicked)
        self.button_sizer.Add(self.fillButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # botão triangulo
        self.triangleButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.triangleButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        triangleIcon = wx.Bitmap("icons/triangulo.png", wx.BITMAP_TYPE_PNG)
        width, height = triangleIcon.GetSize()
        triangleIcon = triangleIcon.ConvertToImage().Rescale(width//4, height//4).ConvertToBitmap()
        self.triangleButton.SetBitmap(triangleIcon)
        self.triangleButton.Bind(wx.EVT_BUTTON, self.onTriangleButtonClicked)
        self.button_sizer.Add(self.triangleButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # botão quadrado
        self.squareButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.squareButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        squareIcon = wx.Bitmap("icons/quadrado.png", wx.BITMAP_TYPE_PNG)
        width, height = squareIcon.GetSize()
        squareIcon = squareIcon.ConvertToImage().Rescale(width//4, height//4).ConvertToBitmap()
        self.squareButton.SetBitmap(squareIcon)
        self.squareButton.Bind(wx.EVT_BUTTON, self.onSquareButtonClicked)
        self.button_sizer.Add(self.squareButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # botão circulo
        self.circleButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.circleButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        circleIcon = wx.Bitmap("icons/circulo.png", wx.BITMAP_TYPE_PNG)
        width, height = circleIcon.GetSize()
        circleIcon = circleIcon.ConvertToImage().Rescale(width//4, height//4).ConvertToBitmap()
        self.circleButton.SetBitmap(circleIcon)
        self.circleButton.Bind(wx.EVT_BUTTON, self.onCircleButtonClicked)
        self.button_sizer.Add(self.circleButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # botão polígono
        self.polygonButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.polygonButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        polygonIcon = wx.Bitmap("icons/poligono.png", wx.BITMAP_TYPE_PNG)
        width, height = polygonIcon.GetSize()
        polygonIcon = polygonIcon.ConvertToImage().Rescale(width//8, height//8).ConvertToBitmap()
        self.polygonButton.SetBitmap(polygonIcon)
        self.polygonButton.Bind(wx.EVT_BUTTON, self.onPolygonButtonClicked)
        self.button_sizer.Add(self.polygonButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Adiciona um controle de escolha para a grossura da linha
        self.lineThicknessChoice = wx.Choice(self.buttons_panel, choices=["1", "2", "3", "4", "5"])
        self.lineThicknessChoice.Bind(wx.EVT_CHOICE, self.onLineThicknessChoice)
        self.button_sizer.Add(self.lineThicknessChoice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # Adiciona um controle de escolha para o estilo de linha
        self.lineStyleChoice = wx.Choice(self.buttons_panel, choices=["Contínuo", "Tracejado", "Pontilhado"])
        self.lineStyleChoice.Bind(wx.EVT_CHOICE, self.onLineStyleChoice)
        self.button_sizer.Add(self.lineStyleChoice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # botão para abrir a caixa de diálogo de seleção de cores
        self.colorsButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.colorsButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        colorsIcon = wx.Bitmap("icons/cores.png", wx.BITMAP_TYPE_PNG)
        width, height = colorsIcon.GetSize()
        colorsIcon = colorsIcon.ConvertToImage().Rescale(40, 40).ConvertToBitmap()
        self.colorsButton.SetBitmap(colorsIcon)
        self.colorsButton.Bind(wx.EVT_BUTTON, self.onColorsButtonClicked)
        self.button_sizer.Add(self.colorsButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.buttons_panel, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.Show(True)

    # Função de manipulador de eventos para o botão Select
    def onSelectButtonClicked(self, event):
        print("Botão Select clicado!")
        self.manageStates.setState(self.manageStates.getIdleState())

    def onFillButtonClicked(self, event):
        print("Botão Select clicado!")
        self.manageStates.style = "Preenchido"
        for obj in self.manageStates.objects:
            if(obj.selected == True):
                obj.style = "Preenchido"
        self.Refresh()

    def onTriangleButtonClicked(self, event):
        print("Botão Triangle clicado!")
        """for obj in self.manageStates.objects:
                obj.selected = False"""
        self.manageStates.setState(self.manageStates.getTriangleState())

    def onSquareButtonClicked(self, event):
        print("Botão Square clicado!")
        """for obj in self.manageStates.objects:
                obj.selected = False"""
        self.manageStates.setState(self.manageStates.getSquareState())

    def onCircleButtonClicked(self, event):
        print("Botão Circle clicado!")
        """for obj in self.manageStates.objects:
                obj.selected = False"""
        self.manageStates.setState(self.manageStates.getCircleState())

    def onPolygonButtonClicked(self, event):
        print("Botão Polygon clicado!")
        """for obj in self.manageStates.objects:
                obj.selected = False"""
        self.manageStates.setState(self.manageStates.getPolygonState())

    def onLineThicknessChoice(self, event):
        """for obj in self.manageStates.objects:
                obj.selected = False"""
        selected_thickness = int(self.lineThicknessChoice.GetStringSelection())
        print(f"Grossura selecionada: {selected_thickness}")
        self.manageStates.lineWidth = selected_thickness
        for obj in self.manageStates.objects:
            if(obj.selected == True):
                obj.lineWidth = selected_thickness
        self.Refresh()

    def onLineStyleChoice(self, event):
        """for obj in self.manageStates.objects:
                obj.selected = False"""
        selected_style = self.lineStyleChoice.GetStringSelection()
        print(selected_style)
        print(f"Grossura selecionada: {selected_style}")
        self.manageStates.style = selected_style
        for obj in self.manageStates.objects:
            if(obj.selected == True):
                obj.style = selected_style
        self.Refresh()

    def onColorsButtonClicked(self, event):
        # Abra o diálogo de seleção de cores
        dlg = wx.ColourDialog(self)
        if dlg.ShowModal() == wx.ID_OK:
            # Obtenha a cor selecionada
            colorData = dlg.GetColourData()
            color = colorData.GetColour().Get()
            print("Cor selecionada:", color)
            r = color[0]/255
            g = color[1]/255
            b = color[2]/255
            self.manageStates.color = (r, g, b)
            for obj in self.manageStates.objects:
                if(obj.selected == True):
                    obj.color = (r, g, b)
            self.Refresh()

        dlg.Destroy()

    def onClose(self, event):
        self.Destroy()

        
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "OpenGL Canvas com WXPython e Botões")
    app.MainLoop()
