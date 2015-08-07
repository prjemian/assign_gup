
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
import qt_utils
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

        self.details_panel.save_pb.clicked.connect(self.onSaveButton)
        self.details_panel.revert_pb.clicked.connect(self.onRevertButton)

    def eventFilter(self, listView, event):
        NAVIGATOR_KEYS = (QtCore.Qt.Key_Down, QtCore.Qt.Key_Up)
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in NAVIGATOR_KEYS:
                prev = listView.currentIndex()
                listView.keyPressEvent(event)
                curr = listView.currentIndex()
                self.selectProposalByIndex(curr, prev)
                return True
        return False
    
    def onSaveButton(self, value):
        # TODO: handle self.save_pb here
        history.addLog("save_pb pressed")
        self.details_panel.modified = False
        self.details_panel.save_pb.setEnabled(False)
        self.details_panel.revert_pb.setEnabled(False)
        qt_utils.setButtonBackground(self.details_panel.save_pb)

    def onRevertButton(self, value):
        # TODO: handle self.revert_pb here
        history.addLog("revert_pb pressed")
        self.details_panel.modified = False
        self.details_panel.save_pb.setEnabled(False)
        self.details_panel.revert_pb.setEnabled(False)
        qt_utils.setButtonBackground(self.details_panel.save_pb)

    def on_item_clicked(self, index):
        '''
        called when changing the selected Proposal in the list
        '''
        if index == self.prior_selection_index:   # clicked on the current item
            return False
        self.selectProposalByIndex(index, self.prior_selection_index)
    
    def canChangeProposal(self):
        '''OK to select a different proposal now?'''
        return not self.details_panel.modified

    def selectProposal(self, prop_id, prev_prop_index):
        '''
        select Proposal for editing as referenced by ID number
        '''
        if not self.canChangeProposal():
            # must save or revert before changing proposals
            self.listView.setCurrentIndex(prev_prop_index)
            return
            
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
        self.prior_selection_index = self.listView.currentIndex()
        self.details_panel.modified = False
        history.addLog('selected proposal: ' + str(prop_id))
    
    def index_to_ID(self, index):
        '''convert QListView index to GUP ID string'''
        return str(index.data().toPyObject())

    def selectProposalByIndex(self, curr, prev):
        '''
        select Proposal for editing as referenced by QListView index
        
        :param index curr: GUP ID string of current selected proposal
        :param index prev: QListView index of previously selected proposal
        '''
        prop_id = self.index_to_ID(curr)
        self.selectProposal(prop_id, prev)
        
    def setModel(self, model):
        self.proposals = model
        self.proposals_model = prop_mvc_model.AGUP_Proposals_Model(self.proposals, parent=self)
        self.listView.setModel(self.proposals_model)

        # select the first item in the list
        pt = QtCore.QPoint(0,0)
        idx = self.listView.indexAt(pt)
        self.listView.setCurrentIndex(idx)
        self.prior_selection_index = idx
        self.selectProposalByIndex(idx, None)
    
    def isProposalListModified(self):
        # TODO: support proposal editing
        return self.details_panel.modified


def main():     # development only
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = AGUP_Proposals_View()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
