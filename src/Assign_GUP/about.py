#!/usr/bin/env python

'''
show the About box
'''

import os, sys
from PyQt4 import QtCore, QtGui
import main_window
import plainTextEdit
import resources

UI_FILE = 'about.ui'
DOCS_URL = 'http://Assign_GUP.readthedocs.org'
LICENSE_FILE = 'LICENSE'


class AboutBox(QtGui.QDialog):
    '''
    a Qt GUI for the About box
    '''

    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        resources.loadUi(UI_FILE, baseinstance=self)

        self.docs_pb.clicked.connect(self.doUrl)
        self.license_pb.clicked.connect(self.doLicense)

    def doUrl(self):
        '''opening documentation URL in default browser'''
        main_window.addLog(self.__doc__)
        url = QtCore.QUrl(DOCS_URL)
        service = QtGui.QDesktopServices()
        service.openUrl(url)

    def doLicense(self):
        '''show the license'''
        main_window.addLog('opening License in new window')

        path = resources.get_forms_path()
        path = os.path.abspath(os.path.join(path, '..'))
        license_text = open(os.path.join(path, LICENSE_FILE), 'r').read()

        ui = plainTextEdit.TextWindow('LICENSE', license_text, self)
        ui.setMinimumSize(1100, 500)
        ui.show()
