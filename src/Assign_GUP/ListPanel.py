
'''
show a lot of text in a scrolling wx window
'''

import wx


class ListPanel(wx.ScrolledWindow):
    '''
    Use this to show a lot of text in a scrolling window
    '''
    def __init__(self, parent, text):
        '''
        :param str text: text to be shown
        '''
        wx.ScrolledWindow.__init__(self, parent=parent, id=wx.ID_ANY)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.block = wx.TextCtrl(self, wx.ID_ANY, text, 
            style = wx.TE_AUTO_SCROLL | wx.TE_MULTILINE | wx.HSCROLL | wx.FIXED | wx.TE_RICH)
        self.block.SetEditable(False)

        # use a fixed size font
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.block.SetFont(font)

        sizer.Add(self.block, 1, wx.ALL | wx.GROW | wx.EXPAND, 5)
        self.SetSizer(sizer)
