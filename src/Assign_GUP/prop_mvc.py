
'''
MVC for proposals - test version
'''

import os, sys
from PyQt4 import QtGui, QtCore
import resources
import ProposalDetails

UI_FILE = 'proposals_listview.ui'

# TODO: split each class into its own file

class AGUP_Proposals_View(QtGui.QWidget):
    '''
    Manage the list of proposals, including assignments of topic weights and reviewers
    '''
    
    def __init__(self, parent=None):
        self.parent = parent
        QtGui.QWidget.__init__(self, parent)
        resources.loadUi(UI_FILE, self)


class AGUP_Proposals_Model(QtCore.QAbstractListModel):
    '''
    MVC model for Proposals
    '''
    
    def __init__(self, symbList=[[]], headerdata=[], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.header = headerdata
        self.symbList = symbList

    # TODO: refactor from table to list
    def rowCount(self, parent):
        return len(self.symbList)

    # TODO: refactor from table to list
    def columnCount(self, parent):
        if len(self.symbList) > 0:
            return len(self.symbList[0])
        return 0

    # TODO: refactor from table to list
    def data(self, index, role):
        if not index.isValid():
            return None
            # For the foreground role you will need to edit this to suit your data
        elif role == QtCore.Qt.ForegroundRole:
            item = self.symbList[index.row()][index.column()]
            if str(item) == "OFF":
                return QtGui.QBrush(QtCore.Qt.red)
            elif str(item) == "ON":
                return QtGui.QBrush(QtCore.Qt.green)
            else:
                return QtGui.QBrush(QtCore.Qt.black)

        elif role != QtCore.Qt.DisplayRole:
            return None
        return self.symbList[index.row()][index.column()]

    # TODO: refactor from table to list
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None

    # Use this only if you want the items in the table to be editable
    #   def setData(self, index, value, color):
    #       self.symbList[index.row()][index.column()] = value
    #       self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, ''const QModelIndex &)'), index, index)
    #       return True

    #   def flags(self, index):
    #       return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = AGUP_Proposals_View()
    
    mylist = [["test1", "test2"], ["test3","test4"]]
    proposals_model = AGUP_Proposals_Model(mylist)
    ui.listView.setModel(proposals_model)

    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
