
'''
Helper routines for Qt
'''

from PyQt4 import QtGui, QtCore


BACKGROUND_DEFAULT = '#efefef'


'''
            QPushButton { 
                   background-color: red;
                   color: black;
                   text-align: center;
                   }
'''

def setButtonBackground(widget, color = BACKGROUND_DEFAULT):
    css = 'background-color: %s;' % color
    widget.setStyleSheet(css)


def setWidgetBackground(widget, color = BACKGROUND_DEFAULT):
    '''
    change the background color of a Qt widget
    
    :param str color: specified as name (mintcream), hex RGB (#dea)
    '''
    if widget is not None:
        palette = QtGui.QPalette()
        palette.setColor(widget.backgroundRole(), QtGui.QColor(color))
        widget.setPalette(palette)
