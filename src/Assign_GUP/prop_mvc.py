
'''
MVC for proposals - test version

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
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

        self.details = ProposalDetails.AGUP_ProposalDetails()
        layout = self.details_gb.layout()
        layout.addWidget(self.details)
    
        self.mylist = ["test1", "test2", "test3", "test4"]
        self.proposals_model = AGUP_Proposals_Model(self.mylist)
        self.listView.setModel(self.proposals_model)


class AGUP_Proposals_Model(QtCore.QAbstractListModel):
    '''
    MVC model for Proposals
    
    This is an adapter for the actual proposals data
    '''
    
    def __init__(self, data_in=[], parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.data_in = data_in

    def rowCount(self, parent):
        return len(self.data_in)

    def data(self, index, role):
        if not index.isValid():
            return None
            # For the foreground role you will need to edit this to suit your data
        elif role == QtCore.Qt.ForegroundRole:
            item = self.data_in[index.row()]
            if str(item) == "OFF":
                return QtGui.QBrush(QtCore.Qt.red)
            elif str(item) == "ON":
                return QtGui.QBrush(QtCore.Qt.green)
            else:
                return QtGui.QBrush(QtCore.Qt.black)

        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self.data_in[index.row()])

    # Use this only if you want the items in the table to be editable
    #   def setData(self, index, value, color):
    #       self.data_in[index.row()] = value
    #       self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, ''const QModelIndex &)'), index, index)
    #       return True

    #   def flags(self, index):
    #       return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


class AGUP_Proposals_list(object):
    '''
    the list of all proposals (is this needed?)
    '''
    
    def __init__(self):
        pass


class AGUP_Proposal_data(object):
    '''
    data of a single proposal
    '''
    
    def __init__(self):
        pass

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = AGUP_Proposals_View()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
