
'''
QtGui widget to edit one Reviewer instance
'''


from PyQt4 import QtGui, QtCore
import qt_form_support
import topic_slider


UI_FILE = 'reviewerDetails.ui'


class AGUP_ReviewerDetails(object):
    '''
    QtGui widget to edit one Reviewer instance
    '''

    def __init__(self, parent, reviewer):
        '''
        :param parent: owner (treebook object)
        :param reviewer: instance of Reviewer object
        '''
        self.treebook = parent
        self.reviewer = reviewer
        self.ui = qt_form_support.load_form(UI_FILE)
        # self._init_tables_(self.ui.tables)

        self.ui.save_pb.clicked.connect(self.onSaveButton)
        self.ui.revert_pb.clicked.connect(self.onRevertButton)
    
    def onSaveButton(self, value):
        # TODO: handle self.ui.save_pb
        print "ui.save_pb not handled yet"
        self.treebook(self)
    
    def onRevertButton(self, value):
        # TODO: handle self.ui.revert_pb
        print "ui.revert_pb not handled yet"
    
    def getFullName(self):
        return str(self.ui.full_name.text())
    
    def getSortName(self):
        return str(self.ui.sort_name.text())
    
    def getPhone(self):
        return str(self.ui.phone.text())
    
    def getEmail(self):
        return str(self.ui.email.text())
    
    def getJoined(self):
        return str(self.ui.joined.text())
    
    def getUrl(self):
        return str(self.ui.url.text())
    
    def getNotes(self):
        return str(self.ui.notes.toPlainText())
    
    def setFullName(self, value):
        self.ui.full_name.setText(value)
    
    def setSortName(self, value):
        self.ui.sort_name.setText(value)
    
    def setPhone(self, value):
        self.ui.phone.setText(value)
    
    def setEmail(self, value):
        self.ui.email.setText(value)
    
    def setJoined(self, value):
        self.ui.joined.setText(value)
    
    def setUrl(self, value):
        self.ui.url.setText(value)
    
    def setNotes(self, value):
        self.ui.notes.setPlainText(value)


def report(mw):
    print 'getFullName', mw.getFullName()
    print 'getSortName', mw.getSortName()
    print 'getPhone', mw.getPhone()
    print 'getEmail', mw.getEmail()
    print 'getJoined', mw.getJoined()
    print 'getUrl', mw.getUrl()
    print 'getNotes', mw.getNotes()


def AGUP_main():
    '''simple starter program to develop this code'''
    import sys
    app = QtGui.QApplication(sys.argv)
    # NOTE: for development, "showIt" used here to 
    # pass the print routine to the class
    # This is wired to the "Save" button for demo only.
    main_window = AGUP_ReviewerDetails(report, None)
    
    main_window.setFullName('Joe Reviewer')
    main_window.setSortName('Reviewer')
    main_window.setPhone('555-555-5555')
    main_window.setEmail('joe@user.com')
    main_window.setJoined('2010-2')
    main_window.setUrl('http://user.com')
    main_window.setNotes('''That URL is fake.\nDo not trust it!''')

    # setup some examples for testing
    topic_dict = dict(SAXS=0.5, GISAXS=0.9, XPCS=0.1)
    topics = sorted(topic_dict.keys())
    w = {}
    for row, key in enumerate(topics):
        w[key] = topic_slider.AGUP_TopicSlider(main_window.ui.topic_layout, row, key, topic_dict[key])
        #print row, key, w[key].getSliderValue(), w[key].getValue()
    main_window.ui.topic_layout.setColumnStretch(1,3)

    report(main_window)

    main_window.ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    AGUP_main()
