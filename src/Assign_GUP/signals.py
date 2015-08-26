
r'''
Custom Qt4 signals
'''


import datetime
import os, sys
from PyQt4 import QtCore

class CustomSignals(QtCore.QObject):
    '''custom signals'''

    checkBoxGridChanged = QtCore.pyqtSignal()
    closed = QtCore.pyqtSignal()                # topics_editor
    topicValueChanged = QtCore.pyqtSignal(str, str, float)
