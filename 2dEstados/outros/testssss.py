import wx
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, -1, pos=(300, 150), size=(320, 250))
        self.panel = wx.Panel(self)
        self.text = wx.StaticText(self.panel, -1, label="Left click mouse, move and release")
        self.panel.Bind(wx.EVT_LEFT_DOWN, self.OnDown)
        self.panel.Bind(wx.EVT_LEFT_UP, self.OnUp)
        self.panel.Bind(wx.EVT_MOTION, self.OnDrag)
        self.Show()

    def OnDown(self, event):
        x, y = event.GetPosition()
        print("Click coordinates: X=",x," Y=",y)

    def OnUp(self, event):
        x, y = event.GetPosition()
        print("Release coordinates: X=",x," Y=",y)

    def OnDrag(self, event):
        x, y = event.GetPosition()
        if not event.Dragging():
            event.Skip()
            return
        event.Skip()        
        #obj = event.GetEventObject()
        #sx, sy = obj.GetScreenPosition()
        #self.Move(sx+x,sy+y)
        print("Dragging position", x, y)
        

app = wx.App()
window = MyFrame()
app.MainLoop()