
'''
MVC View for proposals - test version

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
:see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/
'''

import os, sys
from PyQt4 import QtGui, QtCore
import event_filters
import history
import general_mvc_model
import proposal_details
import qt_utils
import resources
import topics

UI_FILE = 'listview.ui'
PROPOSALS_TEST_FILE = os.path.join('project', '2015-2', 'proposals.xml')


class AGUP_Proposals_View(QtGui.QWidget):
    '''
    Manage the list of proposals, including assignments of topic weights and reviewers
    '''
    
    def __init__(self, parent=None, proposals=None, topics_object=None):
        self.parent = parent
        self.topics = topics_object or topics.Topics()

        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)
        
        self.setWindowTitle('Assign_GUP - Proposals')
        self.listview_gb.setTitle('Proposals')
        self.details_gb.setTitle('Proposal Details')

        self.details_panel = proposal_details.AGUP_ProposalDetails(self)
        layout = self.details_gb.layout()
        layout.addWidget(self.details_panel)

        for topic in self.topics:
            self.details_panel.addTopic(topic, topics.DEFAULT_TOPIC_VALUE)

        if proposals is not None:
            self.setModel(proposals)
            if len(proposals) > 0:
                prop_id = proposals.keyOrder()[0]
                self.editProposal(prop_id, None)
                self.selectFirstListItem()

        self.listView.clicked.connect(self.on_item_clicked)
        self.listView.entered.connect(self.on_item_clicked)
        self.details_panel.custom_signals.topicValueChanged.connect(self.onTopicValueChanged)

        self.arrowKeysEventFilter = event_filters.ArrowKeysEventFilter()
        self.listView.installEventFilter(self.arrowKeysEventFilter)

    def on_item_clicked(self, index):
        '''
        called when changing the selected Proposal in the list
        '''
        if index == self.prior_selection_index:   # clicked on the current item
            return False
        self.selectModelByIndex(index, self.prior_selection_index)

    def onTopicValueChanged(self, prop_id, topic, value):
        '''
        called when user changed a topic value in the details panel
        '''
        self.proposals.setTopicValue(str(prop_id), str(topic), value)
        self.details_panel.modified = True
    
    def details_modified(self):
        '''OK to select a different proposal now?'''
        return self.details_panel.modified

    def editProposal(self, prop_id, prev_prop_index):
        '''
        select Proposal for editing as referenced by ID number
        '''
#         if self.details_modified():
#             # TODO: get values from details panel and store in main
#             history.addLog('need to save modified proposal details')
#             pass
            
        if prop_id is None:
            return
        proposal = self.proposals.getProposal(str(prop_id))
        self.details_panel.setAll(
                                proposal.db['proposal_id'], 
                                proposal.db['proposal_title'], 
                                proposal.db['review_period'], 
                                proposal.db['spk_name'], 
                                proposal.db['first_choice_bl'], 
                                proposal.db['subjects'],
                                )
        topics_list = proposal.getTopicList()
        for topic in topics_list:
            value = proposal.getTopic(topic)
            self.details_panel.setTopic(topic, value)
        # set reviewers
        self.prior_selection_index = self.listView.currentIndex()
        self.details_panel.modified = False
        history.addLog('selected proposal: ' + str(prop_id))
    
    def selectFirstListItem(self):
        idx = self.listView.indexAt(QtCore.QPoint(0,0))
        self.listView.setCurrentIndex(idx)
        return idx
    
    def index_to_ID(self, index):
        '''convert QListView index to GUP ID string'''
        obj = index.data().toPyObject()
        if obj is None:
            return obj
        return str(obj)

    def selectModelByIndex(self, curr, prev):
        '''
        select Proposal for editing as referenced by QListView index
        
        :param index curr: GUP ID string of current selected proposal
        :param index prev: QListView index of previously selected proposal
        '''
        prop_id = self.index_to_ID(curr)
        if prop_id is None:
            return
        self.editProposal(prop_id, prev)
        
    def setModel(self, model):
        self.proposals = model
        self.proposals_model = general_mvc_model.AGUP_MVC_Model(self.proposals, parent=self)
        self.listView.setModel(self.proposals_model)

        # select the first item in the list
        idx = self.selectFirstListItem()
        self.prior_selection_index = idx
        self.selectModelByIndex(idx, None)
    
    def isProposalListModified(self):
        # TODO: support proposal editing
        return self.details_panel.modified
