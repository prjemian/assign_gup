#!/usr/bin/env python

import wx
import Main

modules ={u'Main': [1, 'Main frame of Application', u'Main.py']}

class BoaApp(wx.App):
    '''standard Boa constructor startup code'''

    def OnInit(self):
        self.main = Main.Main(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True


def main():
    application = BoaApp(0)
    application.MainLoop()


if __name__ == '__main__':
    main()
