import wx
import wx.glcanvas as wxgl
from wx import glcanvas
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from geometries import Object
from state import State
from manageStates import ManageStates
from myGLCanvas import MyGLCanvas

# variáveis e valores necessários para inicilização

# cor atual desenho
color = (0.0, 0.0, 0.0)

# tamanho atual da linha
lineWidth = 1.0

# lista de objetos atuais
objects = []

manageStates = None


# ========================================================
# MyFrame - interface
# ========================================================
# canvas do openGl, desenho dos botões, com ícones, resposta aos eventos, etc

class MyFrame(wx.Frame):
    def __init__(self, parent, title):

        wx.Frame.__init__(self, parent, title=title, size=(800, 600))
        
        self.manageStates = ManageStates(color, lineWidth, objects)
        self.canvas = MyGLCanvas(self, self.manageStates)


        # ========================================================
        # PAINEL DE BOTÕES
        # ========================================================

        # faixa para os botões na parte superior
        self.buttons_panel = wx.Panel(self)
        self.buttons_panel.SetBackgroundColour(wx.Colour(220, 220, 220))
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons_panel.SetSizer(self.button_sizer)
        

        # ========================================================
        # BOTÕES
        # ========================================================

        # BOTÃO SELECIONAR
        # é associado ao painel buttons_panel
        # BU_EXACTFIT - o botão tem exatamente o espaço que precisa pro conteúdo
        # NO_BORDER - tira a borda ao redor do botão, fica contínuo com o fundo
        self.selectButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        # define a cor do botão
        self.selectButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        # carrega a imagem como um bitmap no formato de png
        selectIcon = wx.Bitmap("C:/Users/halen/Downloads/ComputacaoGrafica/2dEstados/icons/cursor.png", wx.BITMAP_TYPE_PNG)
        # pega as dimensões da imagem
        width, height = selectIcon.GetSize()
        # converte pra um objeto, redimensiona e converte de volta para bitmap
        selectIcon = selectIcon.ConvertToImage().Rescale(width//2, height//2).ConvertToBitmap()
        # define o bitmap já criado como ícone do botão
        self.selectButton.SetBitmap(selectIcon)
        # associa o evento de click no botão à função de tratamento dele
        self.selectButton.Bind(wx.EVT_BUTTON, self.onSelectButtonClicked)
        # adiciona ao sizer
        self.button_sizer.Add(self.selectButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # BOTÃO BORRACHA
        self.eraserButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.eraserButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        eraserIcon = wx.Bitmap("C:/Users/halen/Downloads/ComputacaoGrafica/2dEstados/icons/borracha.png", wx.BITMAP_TYPE_PNG)
        width, height = eraserIcon.GetSize()
        eraserIcon = eraserIcon.ConvertToImage().Rescale(width//2, height//2).ConvertToBitmap()
        self.eraserButton.SetBitmap(eraserIcon)
        self.eraserButton.Bind(wx.EVT_BUTTON, self.onEraserButtonClicked)
        self.button_sizer.Add(self.eraserButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        
        # BOTÃO PREENCHER
        self.fillButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.fillButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        fillIcon = wx.Bitmap("C:/Users/halen/Downloads/ComputacaoGrafica/2dEstados/icons/latatinta.png", wx.BITMAP_TYPE_PNG)
        width, height = fillIcon.GetSize()
        fillIcon = fillIcon.ConvertToImage().Rescale(width//2, height//2).ConvertToBitmap()
        self.fillButton.SetBitmap(fillIcon)
        self.fillButton.Bind(wx.EVT_BUTTON, self.onFillButtonClicked)
        self.button_sizer.Add(self.fillButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # BOTÃO TRIÂNGULO
        self.triangleButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.triangleButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        triangleIcon = wx.Bitmap("C:/Users/halen/Downloads/ComputacaoGrafica/2dEstados/icons/triangulo.png", wx.BITMAP_TYPE_PNG)
        width, height = triangleIcon.GetSize()
        triangleIcon = triangleIcon.ConvertToImage().Rescale(width//2, height//2).ConvertToBitmap()
        self.triangleButton.SetBitmap(triangleIcon)
        self.triangleButton.Bind(wx.EVT_BUTTON, self.onTriangleButtonClicked)
        self.button_sizer.Add(self.triangleButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # BOTÃO QUADRADO
        self.squareButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.squareButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        squareIcon = wx.Bitmap("C:/Users/halen/Downloads/ComputacaoGrafica/2dEstados/icons/quadrado.png", wx.BITMAP_TYPE_PNG)
        width, height = squareIcon.GetSize()
        squareIcon = squareIcon.ConvertToImage().Rescale(width//2, height//2).ConvertToBitmap()
        self.squareButton.SetBitmap(squareIcon)
        self.squareButton.Bind(wx.EVT_BUTTON, self.onSquareButtonClicked)
        self.button_sizer.Add(self.squareButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # BOTÃO CÍRCULO
        self.circleButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.circleButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        circleIcon = wx.Bitmap("C:/Users/halen/Downloads/ComputacaoGrafica/2dEstados/icons/circulo.png", wx.BITMAP_TYPE_PNG)
        width, height = circleIcon.GetSize()
        circleIcon = circleIcon.ConvertToImage().Rescale(width//2, height//2).ConvertToBitmap()
        self.circleButton.SetBitmap(circleIcon)
        self.circleButton.Bind(wx.EVT_BUTTON, self.onCircleButtonClicked)
        self.button_sizer.Add(self.circleButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # BOTÃO POLÍGONO
        self.polygonButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.polygonButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        polygonIcon = wx.Bitmap("C:/Users/halen/Downloads/ComputacaoGrafica/2dEstados/icons/poligono.png", wx.BITMAP_TYPE_PNG)
        width, height = polygonIcon.GetSize()
        polygonIcon = polygonIcon.ConvertToImage().Rescale(width//2, height//2).ConvertToBitmap()
        self.polygonButton.SetBitmap(polygonIcon)
        self.polygonButton.Bind(wx.EVT_BUTTON, self.onPolygonButtonClicked)
        self.button_sizer.Add(self.polygonButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # CONTROLE DE ESCOLHA PARA A GROSSURA DE LINHA
        self.lineThicknessChoice = wx.Choice(self.buttons_panel, choices=["1", "2", "3", "4", "5"])
        self.lineThicknessChoice.Bind(wx.EVT_CHOICE, self.onLineThicknessChoice)
        self.button_sizer.Add(self.lineThicknessChoice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # CONTROLE DE ESCOLHA PARA O ESTILO DE LINHA
        self.lineStyleChoice = wx.Choice(self.buttons_panel, choices=["Contínuo", "Tracejado", "Pontilhado"])
        self.lineStyleChoice.Bind(wx.EVT_CHOICE, self.onLineStyleChoice)
        self.button_sizer.Add(self.lineStyleChoice, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # BOTÃO PARA ABRIR A CAIXA DE DIÁLOGO DE SELEÇÃO DE CORES
        self.colorsButton = wx.Button(self.buttons_panel, style=wx.BU_EXACTFIT | wx.NO_BORDER)
        self.colorsButton.SetBackgroundColour(wx.Colour(220, 220, 220))
        colorsIcon = wx.Bitmap("C:/Users/halen/Downloads/ComputacaoGrafica/2dEstados/icons/cores.png", wx.BITMAP_TYPE_PNG)
        width, height = colorsIcon.GetSize()
        colorsIcon = colorsIcon.ConvertToImage().Rescale(60, 60).ConvertToBitmap()
        self.colorsButton.SetBitmap(colorsIcon)
        self.colorsButton.Bind(wx.EVT_BUTTON, self.onColorsButtonClicked)
        self.button_sizer.Add(self.colorsButton, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # DISPLAY DA ÁREA E DO PERÍMETRO
        self.infoDisplay = wx.StaticText(self.buttons_panel, label="Área: 0.00, Perímetro: 0.00")
        self.button_sizer.Add(self.infoDisplay, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        # sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.buttons_panel, 0, wx.EXPAND)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.Show(True)

    
    # ========================================================
    # FUNÇÕES DE EVENTO DOS BOTÕES
    # ========================================================

    # BOTÃO SELECIONAR
    def onSelectButtonClicked(self, event):
        print("Botão Select clicado!")
        self.manageStates.setState(self.manageStates.getIdleState())

    # BOTÃO APAGAR
    def onEraserButtonClicked(self, event):
        print("Botão Eraser clicado!")
        self.manageStates.setState(self.manageStates.getDeleteState())

    # BOTÃO PREENCHER
    def onFillButtonClicked(self, event):
        print("Botão Fill clicado!")
        self.manageStates.style = "Preenchido"
        for obj in self.manageStates.objects:
            if(obj.selected == True):
                obj.style = "Preenchido"
        self.Refresh()

    # BOTÃO TRIÂNGULO
    def onTriangleButtonClicked(self, event):
        print("Botão Triangle clicado!")
        self.manageStates.setState(self.manageStates.getTriangleState())

    # BOTÃO QUADRADO
    def onSquareButtonClicked(self, event):
        print("Botão Square clicado!")
        self.manageStates.setState(self.manageStates.getSquareState())

    # BOTÃO CÍRCULO
    def onCircleButtonClicked(self, event):
        print("Botão Circle clicado!")
        self.manageStates.setState(self.manageStates.getCircleState())

    # BOTÃO POLÍGONO
    def onPolygonButtonClicked(self, event):
        print("Botão Polygon clicado!")
        self.manageStates.setState(self.manageStates.getPolygonState())

    # CONTROLE DE ESCOLHA PARA A GROSSURA DE LINHA
    def onLineThicknessChoice(self, event):
        selected_thickness = int(self.lineThicknessChoice.GetStringSelection())
        print(f"Grossura selecionada: {selected_thickness}")
        self.manageStates.lineWidth = selected_thickness
        for obj in self.manageStates.objects:
            if(obj.selected == True):
                obj.lineWidth = selected_thickness
        self.Refresh()

    # CONTROLE DE ESCOLHA PARA O ESTILO DE LINHA
    def onLineStyleChoice(self, event):
        selected_style = self.lineStyleChoice.GetStringSelection()
        print(selected_style)
        print(f"Grossura selecionada: {selected_style}")
        self.manageStates.style = selected_style
        for obj in self.manageStates.objects:
            if(obj.selected == True):
                obj.style = selected_style
        self.Refresh()

    # CAIXA DE DIÁLOGO DE SELEÇÃO DE CORES
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

    # ATUALIZA DISPLAY DA ÁREA E DO PERÍMETRO
    def updateInfoDisplay(self, area, perimeter):
        self.infoDisplay.SetLabel(f"Área: {area:.2f}, Perímetro: {perimeter:.2f}")

    def onClose(self, event):
        self.Destroy()