# http://www.java2s.com/Tutorial/Python/0380__wxPython/extendswxgridPyGridTableBase.htm

import wx
import wx.grid

class GenericTable(wx.grid.PyGridTableBase):
    def __init__(self, data, rowLabels=None, colLabels=None):
        wx.grid.PyGridTableBase.__init__(self)
        self.data = data
        self.rowLabels = rowLabels
        self.colLabels = colLabels
        
    def GetNumberRows(self):
        return len(self.data)

    def GetNumberCols(self):
        return len(self.data[0])

    def GetColLabelValue(self, col):
        if self.colLabels:
            return self.colLabels[col]
        
    def GetRowLabelValue(self, row):
        if self.rowLabels:
            return self.rowLabels[row]
        
    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        return self.data[row][col]

    def SetValue(self, row, col, value):
        pass         


data = (("A", "B"), 
        ("C", "D"), 
        ("E", "F"), 
        ("G", "G"),
        ("F", "F"), 
        ("Q", "Q"))
            
colLabels = ("Last", "First")
rowLabels = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
                   

class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent):
        wx.grid.Grid.__init__(self, parent, -1)
        tableBase = GenericTable(data, rowLabels, colLabels)
        self.SetTable(tableBase)                   

class TestFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "A Grid", size=(275, 275))
        grid = SimpleGrid(self)

app = wx.PySimpleApp()
frame = TestFrame(None)
frame.Show(True)
app.MainLoop()
