
'''
MVC View for reviewers

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
:see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/
'''

import os, sys
from PyQt4 import QtGui, QtCore
import history
import general_mvc_model
import reviewer_details
import qt_utils
import resources
from topics import Topics

UI_FILE = 'proposals_listview.ui'
NAVIGATOR_KEYS = (QtCore.Qt.Key_Down, QtCore.Qt.Key_Up)
REVIEWERS_TEST_FILE = os.path.join('project', '2015-2', 'panel.xml')


class AGUP_Reviewers_View(QtGui.QWidget):
    '''
    Manage the list of Reviewers, including assignments of topic weights
    '''
    
    def __init__(self, parent=None, reviewers=None, topics=None):
        self.parent = parent
        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)

        self.details_panel = reviewer_details.AGUP_ReviewerDetails(self)
        layout = self.details_gb.layout()
        layout.addWidget(self.details_panel)

        self.topics = reviewers.reviewers['0-Myers'].db['topics']
 
        for topic in self.topics:
#             reviewers.addTopic(topic)
            value = reviewers.reviewers['0-Myers'].db['topics'][topic]
            self.details_panel.addTopic(topic, value)

        self.setModel(reviewers)

        self.listView.clicked.connect(self.on_item_clicked)
        self.listView.entered.connect(self.on_item_clicked)
        self.details_panel.custom_signals.topicValueChanged.connect(self.onTopicValueChanged)

        self.arrowKeysEventFilter = ArrowKeysEventFilter()
        self.listView.installEventFilter(self.arrowKeysEventFilter)

    def on_item_clicked(self, index):
        '''
        called when changing the selected Reviewer in the list
        '''
        if index == self.prior_selection_index:   # clicked on the current item
            return False
        self.selectReviewerByIndex(index, self.prior_selection_index)

    def onTopicValueChanged(self, sort_name, topic, value):
        '''
        called when user changed a topic value in the details panel
        '''
        self.reviewers.setTopicValue(str(sort_name), str(topic), value)
        self.details_panel.modified = True
    
    def details_modified(self):
        '''OK to select a different reviewer now?'''
        return self.details_panel.modified

    def selectReviewer(self, sort_name, prev_index):
        '''
        select Reviewer for editing as referenced by sort_name
        '''
#         if self.details_modified():
#             # TODO: get values from details panel and store in main
#             history.addLog('need to save modified reviewer details')
#             pass
            
        panelist = self.reviewers.reviewers[str(sort_name)]

        self.details_panel.setFullName(panelist.db['full_name'])
        self.details_panel.setSortName(panelist.db['name'])
        self.details_panel.setPhone(panelist.db['phone'])
        self.details_panel.setEmail(panelist.db['email'])
        self.details_panel.setNotes(panelist.db['notes'])
        self.details_panel.setJoined(panelist.db['joined'])
        self.details_panel.setUrl(panelist.db['URL'])

        topics_dict = panelist.getTopics()
        for topic, value in topics_dict.items():
            self.details_panel.setTopic(topic, value)
        # set reviewers
        self.prior_selection_index = self.listView.currentIndex()
        self.details_panel.modified = False
        history.addLog('selected reviewer: ' + str(sort_name))
    
    def index_to_ID(self, index):
        '''convert QListView index to sort_name string'''
        return str(index.data().toPyObject())

    def selectReviewerByIndex(self, curr, prev):
        '''
        select Reviewer for editing as referenced by QListView index
        
        :param index curr: sort_name string of current selected reviewer
        :param index prev: QListView index of previously selected reviewer
        '''
        sort_name = self.index_to_ID(curr)
        self.selectReviewer(sort_name, prev)
        
    def setModel(self, model):
        self.reviewers = model
        self.reviewers_model = general_mvc_model.AGUP_MVC_Model(self.reviewers, parent=self)
        self.listView.setModel(self.reviewers_model)

        # select the first item in the list
        idx = self.listView.indexAt(QtCore.QPoint(0,0))
        self.listView.setCurrentIndex(idx)
        self.prior_selection_index = idx
        self.selectReviewerByIndex(idx, None)
    
    def isReviewerListModified(self):
        # TODO: support reviewer editing
        return self.details_panel.modified


class ArrowKeysEventFilter(QtCore.QObject):
    '''
    custom event filter
    '''

    def eventFilter(self, listView, event):
        '''
        watches for ArrowUp and ArrowDown (navigator keys) to change selection
        '''
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in NAVIGATOR_KEYS:
                prev = listView.currentIndex()
                listView.keyPressEvent(event)
                curr = listView.currentIndex()
                parent = listView.parent().parent()     # FIXME: fragile!
                parent.selectReviewerByIndex(curr, prev)
                return True
        return False


def main():
    '''simple starter program to develop this code'''
    import sys
    import os
    import revu_mvc_data
    TEST_FILE = os.path.join('project', '2015-2', 'panel.xml')
    reviewers = revu_mvc_data.AGUP_Reviewers_List()
    reviewers.importXml(TEST_FILE)

    app = QtGui.QApplication(sys.argv)
    mw = AGUP_Reviewers_View(reviewers=reviewers)
    mw.show()
    _r = app.exec_()
    sys.exit(_r)


if __name__ == '__main__':
    main()
