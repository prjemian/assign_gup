
'''
MVC Model for proposals - test version

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
:see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/
'''

import os, sys
from PyQt4 import QtGui, QtCore


class AGUP_Proposals_Model(QtCore.QAbstractListModel):
    '''
    MVC model for Proposals
    
    This is an adapter for the actual proposals data object: proposal_dict
    '''
    
    def __init__(self, proposals=[], headerdata=None, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.proposals = proposals

    def columnCount(self, parent):
        #return len(self.headerdata)     # table
        return 1        # list

    def rowCount(self, parent):
        return len(self.proposals)

    def data(self, index, role):
        if not index.isValid():
            return None
            # For the foreground role you will need to edit this to suit your data
        row = index.row()
        if role == QtCore.Qt.ForegroundRole:
            item = self.proposals.getByIndex(row)
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return self.proposals.getByIndex(row)

    # Use this only if you want the items in the table to be editable
    #   def setData(self, index, value, color):
    #       self.proposals.getByIndex(row) = value
    #       self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, ''const QModelIndex &)'), index, index)
    #       return True

    #   def flags(self, index):
    #       return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
