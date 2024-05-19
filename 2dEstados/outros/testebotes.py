import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(300, 200))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Criando um botão com um ícone
        button_with_icon = wx.Button(panel, style=wx.BU_EXACTFIT)
        icon = wx.Bitmap("icons/triangulo.png", wx.BITMAP_TYPE_PNG)  # Substitua "triangulo.png" pelo caminho para o seu ícone

        # Redimensionando o ícone para torná-lo menor
        width, height = icon.GetSize()
        icon = icon.ConvertToImage().Rescale(width//4, height//4).ConvertToBitmap()
        button_with_icon.SetBitmap(icon)

        # Definindo o tamanho mínimo do botão
        #button_with_icon.SetMinSize((width//3, height//3))

        sizer.Add(button_with_icon, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(sizer)
        self.Center()
        self.Show()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "Botão com Ícone")
    app.MainLoop()
