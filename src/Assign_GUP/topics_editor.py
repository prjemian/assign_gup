
'''
GUI to edit the list of topics
'''


from PyQt4 import QtGui, QtCore
import history
import qt_utils
import resources
import topics


UI_FILE = 'topics_editor.ui'


class AGUP_TopicsEditor(QtGui.QWidget):
    '''add topic, slider, value_entry to a QGridLayout'''
    
    def __init__(self, parent=None, topics_list=None):
        self.parent = parent
        self.topics_list = topics.Topics()
        self.topics_list.addItems(topics_list or 'one two three'.split())

        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)
        self.setWindowTitle('AGUP List of Topics')
        self.listWidget.addItems(self.topics_list.getList())
        
        # select the first item in the list
        idx = self.listWidget.indexAt(QtCore.QPoint(0,0))
        self.listWidget.setCurrentIndex(idx)

        # self.listWidget.currentItemChanged.connect(self.on_item_changed)
        self.add_pb.clicked.connect(self.onAdd)
        self.newTopic.returnPressed.connect(self.onAdd)
        self.delete_pb.clicked.connect(self.onDelete)
    
    def getList(self):
        '''
        when all editing is complete, call this method to get the final list
        '''
        return self.topics_list.getList()

    def onAdd(self, *args, **kw):
        txt = str(self.newTopic.text())
        if self.topics_list.exists(txt):
            # raise KeyError, 'This topic is already defined: ' + txt
            return
        if len(txt.strip()) == 0:
            # raise KeyError, 'Must give a value for the topic'
            return
        if len(txt.strip().split()) != 1:
            # raise KeyError, 'topic cannot have embedded white space: ' + txt
            return
        txt = txt.strip()
        self.listWidget.addItem(txt)
        self.topics_list.add(txt)
        self.listWidget.sortItems()
        self.newTopic.setText('')

    def onDelete(self, *args):
        curr = self.listWidget.currentItem()
        if curr is not None:
            row = self.listWidget.row(curr)
            self.listWidget.takeItem(row)
            self.topics_list.remove(curr.text())
