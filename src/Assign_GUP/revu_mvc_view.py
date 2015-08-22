
'''
MVC View for reviewers

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
:see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/
'''

import os, sys
from PyQt4 import QtGui, QtCore
import event_filters
import history
import general_mvc_model
import reviewer_details
import qt_utils
import resources
import topics

UI_FILE = 'listview.ui'
REVIEWERS_TEST_FILE = os.path.join('project', 'agup_project.xml')


class AGUP_Reviewers_View(QtGui.QWidget):
    '''
    Manage the list of Reviewers, including assignments of topic weights
    '''
    
    def __init__(self, parent=None, reviewers=None, topics_object=None, settings=None):
        self.parent = parent
        self.topics = topics_object or topics.Topics()
        self.settings = settings

        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)
        self.restoreWindowGeometry()
        
        self.setWindowTitle('Assign_GUP - Reviewers')
        self.listview_gb.setTitle('Reviewers')
        self.details_gb.setTitle('Reviewer Details')

        self.details_panel = reviewer_details.AGUP_ReviewerDetails(self)
        layout = self.details_gb.layout()
        layout.addWidget(self.details_panel)

        for topic in self.topics:
            self.details_panel.addTopic(topic, topics.DEFAULT_TOPIC_VALUE)

        if reviewers is not None:
            self.setModel(reviewers)
            if len(reviewers) > 0:
                sort_name = reviewers.keyOrder()[0]
                self.editReviewer(sort_name, None)
                self.selectFirstListItem()

        self.listView.clicked.connect(self.on_item_clicked)
        self.listView.entered.connect(self.on_item_clicked)
        self.details_panel.custom_signals.topicValueChanged.connect(self.onTopicValueChanged)
        self.details_panel.full_name.textEdited.connect(self.onTextChanged)
        self.details_panel.sort_name.textEdited.connect(self.onTextChanged)
        self.details_panel.phone.textEdited.connect(self.onTextChanged)
        self.details_panel.email.textEdited.connect(self.onTextChanged)
        self.details_panel.joined.textEdited.connect(self.onTextChanged)
        self.details_panel.url.textEdited.connect(self.onTextChanged)
        self.details_panel.notes.textChanged.connect(self.onTextChanged)

        self.arrowKeysEventFilter = event_filters.ArrowKeysEventFilter()
        self.listView.installEventFilter(self.arrowKeysEventFilter)

    def on_item_clicked(self, index):
        '''
        called when changing the selected Reviewer in the list
        '''
        if index == self.prior_selection_index:   # clicked on the current item
            return False
        self.selectModelByIndex(index, self.prior_selection_index)

    def onTopicValueChanged(self, sort_name, topic, value):
        '''
        called when user changed a topic value in the details panel
        '''
        self.reviewers.setTopicValue(str(sort_name), str(topic), value)
        self.details_panel.modified = True
    
    def onTextChanged(self, qtext):
        self.details_panel.modified = True
    
    def details_modified(self):
        '''OK to select a different reviewer now?'''
        return self.details_panel.modified

    def editReviewer(self, sort_name, prev_index):
        '''
        select Reviewer for editing as referenced by sort_name
        '''
#         if self.details_modified():
#             # TODO: get values from details panel and store in main
#             history.addLog('need to save modified reviewer details')
#             pass
            
        if sort_name is None:
            return
        panelist = self.reviewers.getReviewer(str(sort_name))

        self.details_panel.setFullName(panelist.db['full_name'])
        self.details_panel.setSortName(panelist.db['name'])
        self.details_panel.setPhone(panelist.db['phone'])
        self.details_panel.setEmail(panelist.db['email'])
        self.details_panel.setNotes(panelist.db['notes'])
        self.details_panel.setJoined(panelist.db['joined'])
        self.details_panel.setUrl(panelist.db['URL'])

        topics_list = panelist.getTopicList()
        for topic in topics_list:
            value = panelist.getTopic(topic)
            self.details_panel.setTopic(topic, value)
        # set reviewers
        self.prior_selection_index = self.listView.currentIndex()
        self.details_panel.modified = False
        history.addLog('selected reviewer: ' + str(sort_name))

    def selectModelByIndex(self, curr, prev):
        '''
        select Reviewer for editing as referenced by QListView index
        
        :param index curr: sort_name string of current selected reviewer
        :param index prev: QListView index of previously selected reviewer
        '''
        sort_name = self.index_to_ID(curr)
        if sort_name is None:
            return
        self.editReviewer(sort_name, prev)
    
    def selectFirstListItem(self):
        idx = self.listView.indexAt(QtCore.QPoint(0,0))
        self.listView.setCurrentIndex(idx)
        return idx
    
    def index_to_ID(self, index):
        '''convert QListView index to sort_name string'''
        obj = index.data().toPyObject()
        if obj is None:
            return obj
        return str(obj)
        
    def setModel(self, model):
        self.reviewers = model
        self.reviewers_model = general_mvc_model.AGUP_MVC_Model(self.reviewers, parent=self)
        self.listView.setModel(self.reviewers_model)
    
    def isReviewerListModified(self):
        # TODO: support reviewer editing
        return self.details_panel.modified

    def closeEvent(self, event):
        self.saveWindowGeometry()
        event.accept()
    
    def saveWindowGeometry(self):
        '''
        remember where the window was
        '''
        if self.settings is not None:
            self.settings.saveWindowGeometry(self)

    def restoreWindowGeometry(self):
        '''
        put the window back where it was
        '''
        if self.settings is not None:
            self.settings.restoreWindowGeometry(self)


def main():
    '''simple starter program to develop this code'''
    import sys
    import os
    import revu_mvc_data
    reviewers = revu_mvc_data.AGUP_Reviewers_List()
    reviewers.importXml(REVIEWERS_TEST_FILE)
    sort_name = reviewers.keyOrder()[0]
    reviewer = reviewers.getReviewer(sort_name)

    app = QtGui.QApplication(sys.argv)
    mw = AGUP_Reviewers_View(None, reviewers, reviewer.topics)
    mw.show()
    _r = app.exec_()
    sys.exit(_r)


if __name__ == '__main__':
    main()
