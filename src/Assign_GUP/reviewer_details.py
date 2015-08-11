
'''
QtGui widget to edit one Reviewer instance
'''


from PyQt4 import QtGui, QtCore
import history
import resources
import topic_slider


UI_FILE = 'reviewer_details.ui'


class AGUP_ReviewerDetails(QtGui.QWidget):
    '''
    QtGui widget to edit one Reviewer instance
    '''

    def __init__(self, parent=None):
        '''
        :param parent: owner (QtGui object)
        '''
        self.parent = parent

        QtGui.QWidget.__init__(self, parent)
        resources.loadUi(UI_FILE, self)

        self.modified = False
        self.topic_list = []
        self.topic_widgets = {}

        self.custom_signals = CustomSignals()
    
    def onTopicValueChanged(self, topic):
        value = self.topic_widgets[topic].getValue()
        history.addLog("topic (" + topic + ") value changed: " + str(value))
        self.modified = True
        sort_name = str(self.getSortName())
        self.custom_signals.topicValueChanged.emit(sort_name, str(topic), value)
    
    def addTopic(self, topic, value):
        if topic not in self.topic_list:
            self.topic_list.append(topic)
        row = self.topic_list.index(topic)
        topicslider = topic_slider.AGUP_TopicSlider(self.topic_layout, row, topic, value)
        self.topic_widgets[topic] = topicslider
        topicslider.slider.valueChanged.connect(lambda: self.onTopicValueChanged(topic))

    def setTopic(self, key, value):
        if key not in self.topic_list:
            raise KeyError, 'unknown Topic: ' + key
        if value < 0 or value > 1:
            raise ValueError, 'Topic value must be between 0 and 1, given' + str(value)
        self.topic_widgets[key].setValue(value)
        self.topic_widgets[key].onValueChange(value)    # sets the slider
        self.modified = True
    
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
        self.modified = True
    
    def setSortName(self, value):
        self.sort_name.setText(value)
        self.modified = True
    
    def setPhone(self, value):
        self.phone.setText(value)
        self.modified = True
    
    def setEmail(self, value):
        self.email.setText(value)
        self.modified = True
    
    def setJoined(self, value):
        self.joined.setText(value)
        self.modified = True
    
    def setUrl(self, value):
        self.url.setText(value or '')
        self.modified = True
    
    def setNotes(self, value):
        self.notes.setPlainText(value)
        self.modified = True


class CustomSignals(QtCore.QObject):
    '''custom signals'''
    
    topicValueChanged = QtCore.pyqtSignal(str, str, float)


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

    print 'getFullName', mw.getFullName()
    print 'getSortName', mw.getSortName()
    print 'getPhone', mw.getPhone()
    print 'getEmail', mw.getEmail()
    print 'getJoined', mw.getJoined()
    print 'getUrl', mw.getUrl()
    print 'getNotes', mw.getNotes()

    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
