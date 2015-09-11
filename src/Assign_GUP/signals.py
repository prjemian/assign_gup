
r'''
Custom Qt4 signals

====================  ===============  =====================
signal                args             comments
====================  ===============  =====================
checkBoxGridChanged                    reviewer assignment
closed                                 topics_editor
recalc                                 dot?Product
topicValueChanged    str, str, float   reviewer or proposal
====================  ===============  =====================

'''


import datetime
import os, sys
from PyQt4 import QtCore

class CustomSignals(QtCore.QObject):
    '''custom signals'''

    checkBoxGridChanged = QtCore.pyqtSignal()
    closed = QtCore.pyqtSignal()                # topics_editor
    recalc = QtCore.pyqtSignal()
    topicValueChanged = QtCore.pyqtSignal(str, str, float)
