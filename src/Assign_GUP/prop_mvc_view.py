
'''
MVC View for proposals - test version

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
:see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/
'''

import os, sys
from PyQt4 import QtGui, QtCore
import history
import prop_mvc_data
import prop_mvc_model
import proposal_details
import resources
from topics import Topics

UI_FILE = 'proposals_listview.ui'
PROPOSALS_TEST_FILE = os.path.join('project', '2015-2', 'proposals.xml')


class AGUP_Proposals_View(QtGui.QWidget):
    '''
    Manage the list of proposals, including assignments of topic weights and reviewers
    '''
    
    def __init__(self, parent=None, proposals=None, topics=None):
        self.parent = parent
        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)

        self.details_panel = proposal_details.AGUP_ProposalDetails(self)
        layout = self.details_gb.layout()
        layout.addWidget(self.details_panel)

        if topics is None:       # developer use
            topics = Topics()
            for key in 'bio chem phys'.split():
                topics.add(key)
        self.topics = topics

        if proposals is None:       # developer use
            if not os.path.exists(PROPOSALS_TEST_FILE):
                raise IOError, 'File not found: ' + PROPOSALS_TEST_FILE
            proposals = prop_mvc_data.AGUP_Proposals_List()
            proposals.importXml(PROPOSALS_TEST_FILE)

        for topic in topics:
            proposals.addTopic(topic)
            self.details_panel.addTopic(topic, 0.0)

        self.setModel(proposals)

        self.listView.clicked.connect(self.on_item_clicked)
        self.listView.entered.connect(self.on_item_clicked)
        self.listView.installEventFilter(self)      # for keyboard events

    def eventFilter(self, listView, event):
        NAVIGATOR_KEYS = (QtCore.Qt.Key_Down, QtCore.Qt.Key_Up)
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in NAVIGATOR_KEYS:
                listView.keyPressEvent(event)
                index = listView.currentIndex()
                self.selectProposalByIndex(index)
                return True
        return False

    def on_item_clicked(self, index):
        '''
        called when changing the selected Proposal in the list
        '''
        if index == self.prior_selection:
            return False
        # TODO: check the "modified" flag here before proceeding
        self.prior_selection = index
        self.selectProposalByIndex(index)

    def selectProposal(self, prop_id):
        '''
        select Proposal for editing as referenced by ID number
        '''
        proposal = self.proposals.proposals[str(prop_id)]
        self.details_panel.setAll(
                                  proposal.db['proposal_id'], 
                                  proposal.db['proposal_title'], 
                                  proposal.db['review_period'], 
                                  proposal.db['spk_name'], 
                                  proposal.db['first_choice_bl'], 
                                  proposal.db['subjects'],
                                  )
        # TODO: proposal.setTopic(topic, assigned_value)
        # set reviewers
        history.addLog('selected proposal: ' + str(prop_id))

    def selectProposalByIndex(self, index):
        '''
        select Proposal for editing as referenced by QListView index
        '''
        prop_id = str(index.data().toPyObject())
        self.selectProposal(prop_id)
        
    def setModel(self, model):
        self.proposals = model
        self.proposals_model = prop_mvc_model.AGUP_Proposals_Model(self.proposals, parent=self)
        self.listView.setModel(self.proposals_model)

        # select the first item in the list
        pt = QtCore.QPoint(0,0)
        idx = self.listView.indexAt(pt)
        self.listView.setCurrentIndex(idx)
        self.prior_selection = idx
        self.selectProposalByIndex(idx)


def main():     # development only
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = AGUP_Proposals_View()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
