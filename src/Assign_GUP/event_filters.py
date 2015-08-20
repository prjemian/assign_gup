
'''
event filters for certain MVC widgets such as QListView
'''

from PyQt4 import QtGui, QtCore

NAVIGATOR_KEYS = (QtCore.Qt.Key_Down, QtCore.Qt.Key_Up)


class ArrowKeysEventFilter(QtCore.QObject):
    '''
    watches for ArrowUp and ArrowDown (navigator keys) to change selection
    '''

    def eventFilter(self, listView, event):
        '''
        custom event filter
        '''
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in NAVIGATOR_KEYS:
                prev = listView.currentIndex()
                listView.keyPressEvent(event)
                curr = listView.currentIndex()
                parent = listView.parent().parent()     # FIXME: fragile!
                parent.selectProposalByIndex(curr, prev)
                return True
        return False
