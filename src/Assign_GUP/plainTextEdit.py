#!/usr/bin/env python

'''
show text in a GUI window
'''

from PyQt4 import QtGui
import qt_form_support

UI_FILE = 'plainTextEdit.ui'

class TextWindow(QtGui.QDialog):
    '''
    show text in a GUI window
    '''

    def __init__(self, title, text, parent=None):
        QtGui.QDialog.__init__(self, parent)
        qt_form_support.loadUi(UI_FILE, baseinstance=self)
        self.setWindowTitle(title)
        self.plainTextEdit.setPlainText(text)
