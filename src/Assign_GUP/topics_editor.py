
'''
GUI to edit the list of topics
'''


from PyQt4 import QtGui, QtCore
import history
import qt_utils
import resources
import topics


UI_FILE = 'topics_editor.ui'


class CustomSignals(QtCore.QObject):
    '''custom signals'''
    
    closed = QtCore.pyqtSignal()

class AGUP_TopicsEditor(QtGui.QDialog):
    '''add topic, slider, value_entry to a QGridLayout'''
    
    def __init__(self, parent=None, topics_list=None, settings=None):
        self.parent = parent
        self.topics = topics.Topics()
        self.topics.addTopics(topics_list)
        self.settings = settings

        QtGui.QDialog.__init__(self)
        resources.loadUi(UI_FILE, self)
        self.restoreWindowGeometry()

        self.setWindowTitle('AGUP List of Topics')
        self.listWidget.addItems(self.topics.getTopicList())

        self.listWidget.currentItemChanged.connect(self.on_item_changed)
        self.add_pb.clicked.connect(self.onAdd)
        self.newTopic.returnPressed.connect(self.onAdd)
        self.delete_pb.clicked.connect(self.onDelete)
        self.close_pb.clicked.connect(self.onCloseButton)
        
        # select the first item in the list
        idx = self.listWidget.indexAt(QtCore.QPoint(0,0))
        self.listWidget.setCurrentIndex(idx)

        self.custom_signals = CustomSignals()
    
    def getTopicList(self):
        '''
        when all editing is complete, call this method to get the final list
        '''
        return self.topics.getTopicList()

    def onAdd(self, *args, **kw):
        '''
        add the text in the entry box to the list of topics
        '''
        txt = str(self.newTopic.text())
        if self.topics.exists(txt):
            # raise KeyError, 'This topic is already defined: ' + txt
            return
        if len(txt.strip()) == 0:
            # raise KeyError, 'Must give a value for the topic'
            return
        if len(txt.strip().split()) != 1:
            # raise KeyError, 'topic cannot have embedded white space: ' + txt
            return
        txt = txt.strip()
        #
        # FIXME: problem when adding new topic into existing list, seems to replace a topic
        #
        self.listWidget.addItem(txt)
        self.topics.add(txt)
        self.listWidget.sortItems()
        self.newTopic.setText('')

    def onDelete(self, *args):
        '''
        remove the selected item from the list of topics
        '''
        curr = self.listWidget.currentItem()
        if curr is not None:
            row = self.listWidget.row(curr)
            self.listWidget.takeItem(row)
            self.topics.remove(str(curr.text()))

    def on_item_changed(self, curr, prev):
        '''
        when selecting an item in the list, put it's text in the entry box
        '''
        if curr is not None:
            self.newTopic.setText(curr.text())
    
    def onCloseButton(self, event):
        self.close()
    
    def closeEvent(self, event):
        self.custom_signals.closed.emit()   # this window is closing - needed?
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
