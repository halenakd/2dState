import wx
from myFrame import MyFrame

# ========================================================
# Main - onde o app e o quadro são criados e chamados
# ========================================================
# deve ser rodado para iniciar o programa

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, "Ambiente 2D Interativo")
    frame.Show()
    app.MainLoop()
