
'''
wxPanel to provide edit controls for one Reviewer instance
'''


from PyQt4 import QtGui, QtCore
import qt_form_support
# import wx
# import ui


class AGUP_ReviewerPanel(object):
    '''
    Creates a Qt GUI to provide edit controls for one Reviewer instance
    '''

    def __init__(self, parent, reviewer):
        '''
        :param parent: owner (treebook object)
        :param reviewer: instance of Reviewer object
        '''
        self.treebook = parent
        self.reviewer = reviewer
        # http://doc.qt.io/qt-4.8/qabstractslider.html
        self.ui = qt_form_support.load_form('reviewerPanel.ui')
#         self._init_tables_(self.ui.tables)


# class ReviewerPanel(wx.Panel):
#     '''
#     Creates a GUI wxPanel to provide edit controls for one Reviewer instance
#     '''
# 
#     def __init__(self, parent, reviewer):
#         '''
#         :param parent: owner (treebook object)
#         :param reviewer: instance of Reviewer object
#         '''
#         self.treebook = parent
#         self.reviewer = reviewer
#         wx.Panel.__init__(self, parent=self.treebook, id=wx.ID_ANY)
#         self._init_two_panels_()
# 
#     def _init_two_panels_(self):
#         '''
#         Make two (sub)panels.
#         Use subroutines to set up the subpanels.
#         This avoids confusion with the sizers.
#         '''
#         sizer = wx.BoxSizer(wx.HORIZONTAL)
#         
#         self.widgets = {}
#         
#         main = wx.Panel(self)
#         sizer.Add(main, 1, wx.ALL | wx.GROW | wx.EXPAND, 5)
#         self._init_main_(main)
#         
#         topics = wx.Panel(self)
#         sizer.Add(topics, 0, wx.ALL | wx.GROW | wx.EXPAND, 5)
#         self._init_topics_(topics)
#         
#         self.SetSizer(sizer)
# 
#     def _init_main_(self, panel):
#         '''
#         set up most text entry fields
#         
#         :param panel: container
#         '''
#         sizer = wx.FlexGridSizer(cols=2)
# 
#         sizer.AddGrowableCol(1, 1) 
#         # TODO Can we use a Validator() method to populate the entry widgets?
#         # See p. 286, chapter 9.3, in "wxPython in Action"
#         # page numbers and section numbers vary, section is titled
#         # "How do I use a validator to transfer data?"
#         row = -1
#         for dct in self.reviewer.TellUI():
#             if dct['set'] == 'main':
#                 row += 1
#                 dct['row'] = row
#                 self.widgets[dct['key']] = ui.make(panel, sizer, dct)
#             
#         # add another row with some buttons
#         sizer.Add(wx.StaticText(panel, wx.ID_ANY, label="", style=0), 0, wx.ALL, 5)
#         buttonPanel = wx.Panel(panel)
#         sizer.Add(buttonPanel, 1, wx.ALL | wx.GROW | wx.EXPAND, 5)
#         
#         boxSizer = wx.BoxSizer(wx.HORIZONTAL)
#         self.save_button = wx.Button(buttonPanel, label="Save")
#         self.revert_button = wx.Button(buttonPanel, label="Revert")
#         boxSizer.Add(self.save_button, 0, wx.ALL, 5)
#         boxSizer.Add(self.revert_button, 0, wx.ALL, 5)
#         self.save_button.Bind(wx.EVT_BUTTON, self.OnSaveButtonPush)
#         self.revert_button.Bind(wx.EVT_BUTTON, self.OnRevertButtonPush)
#         buttonPanel.SetSizer(boxSizer)
# 
#         panel.SetSizer(sizer)
# 
#     def _init_topics_(self, panel):
#         '''
#         set topic fields
#         
#         :param panel: container
#         '''
#         sizer = wx.FlexGridSizer(cols=2)
#         row = -1
#         for dct in self.reviewer.TellUI():
#             if dct['set'] == 'topics':
#                 row += 1
#                 dct['row'] = row
#                 self.widgets[dct['key']] = ui.make(panel, sizer, dct)
#         panel.SetSizer(sizer)
# 
#     def OnSaveButtonPush(self, event):
#         '''
#         Handle a push of the Save button
#         '''
#         liszt = []
#         for dct in self.reviewer.TellUI():
#             key = dct['key']
#             dct['entry'] = self.widgets[key].GetValue()
#             liszt.append( dct )
#         self.reviewer.SaveUI(liszt)
# 
#     def OnRevertButtonPush(self, event):
#         '''
#         Handle a push of the Revert button
#         '''
#         for dct in self.reviewer.TellUI():
#             key = dct['key']
#             value = dct['entry']
#             if value == None: value = ""
#             self.widgets[key].SetValue( str(value) )
#         ui.log('RevertEdits(%s)' % str(self.reviewer))


def AGUP_main():
    '''simple starter program to develop this code'''
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = AGUP_ReviewerPanel(None, None)
    main_window.ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    AGUP_main()
    pass
