#!/usr/bin/env python

'''
show the About box
'''

import os, sys
from PyQt4 import QtCore, QtGui
import history
import plainTextEdit
import resources

UI_FILE = 'about.ui'
DOCS_URL = 'http://Assign_GUP.readthedocs.org'
LICENSE_FILE = 'LICENSE'


class InfoBox(QtGui.QDialog):
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
        history.addLog('opening documentation URL in default browser')
        url = QtCore.QUrl(DOCS_URL)
        service = QtGui.QDesktopServices()
        service.openUrl(url)

    def doLicense(self):
        '''show the license'''
        history.addLog('opening License in new window')
        license_text = open(resources.resource_file('../' + LICENSE_FILE), 'r').read()
        ui = plainTextEdit.TextWindow('LICENSE', license_text, self)
        ui.setMinimumSize(700, 500)
        ui.setWindowModality(QtCore.Qt.ApplicationModal)
        ui.show()
