
'''
QtGui widget to edit one Reviewer instance
'''


from PyQt4 import QtGui, QtCore
import qt_form_support
import topic_slider


UI_FILE = 'reviewer_details.ui'


class AGUP_ReviewerDetails(QtGui.QWidget):
    '''
    QtGui widget to edit one Reviewer instance
    '''

    def __init__(self, parent=None, reviewer=None):
        '''
        :param parent: owner (QtGui object)
        :param reviewer: instance of Reviewer object
        '''
        self.parent = parent
        self.reviewer = reviewer
        QtGui.QWidget.__init__(self, parent)
        qt_form_support.loadUi(UI_FILE, self)

        self.save_pb.clicked.connect(self.onSaveButton)
        self.revert_pb.clicked.connect(self.onRevertButton)
    
    def onSaveButton(self, value):
        # TODO: handle self.save_pb
        print "save_pb not handled yet"
    
    def onRevertButton(self, value):
        # TODO: handle self.revert_pb
        print "revert_pb not handled yet"
    
    def getFullName(self):
        return str(self.full_name.text())
    
    def getSortName(self):
        return str(self.sort_name.text())
    
    def getPhone(self):
        return str(self.phone.text())
    
    def getEmail(self):
        return str(self.email.text())
    
    def getJoined(self):
        return str(self.joined.text())
    
    def getUrl(self):
        return str(self.url.text())
    
    def getNotes(self):
        return str(self.notes.toPlainText())
    
    def setFullName(self, value):
        self.full_name.setText(value)
    
    def setSortName(self, value):
        self.sort_name.setText(value)
    
    def setPhone(self, value):
        self.phone.setText(value)
    
    def setEmail(self, value):
        self.email.setText(value)
    
    def setJoined(self, value):
        self.joined.setText(value)
    
    def setUrl(self, value):
        self.url.setText(value)
    
    def setNotes(self, value):
        self.notes.setPlainText(value)


def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    mw = AGUP_ReviewerDetails()
    
    mw.setFullName('Joe Reviewer')
    mw.setSortName('Reviewer')
    mw.setPhone('555-555-5555')
    mw.setEmail('joe@user.com')
    mw.setJoined('2010-2')
    mw.setUrl('http://user.com')
    mw.setNotes('''That URL is fake.\nDo not trust it!''')

    # setup some examples for testing
    topic_dict = dict(SAXS=0.5, XPCS=0.1, GISAXS=0.9)
    topics = sorted(topic_dict.keys())
    w = {}
    for row, key in enumerate(topics):
        w[key] = topic_slider.AGUP_TopicSlider(mw.topic_layout, row, key, topic_dict[key])
    mw.topic_layout.setColumnStretch(1,3)

    print mw.getFullName()
    print mw.getSortName()
    print mw.getPhone()
    print mw.getEmail()
    print mw.getJoined()
    print mw.getUrl()
    print mw.getNotes()

    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
