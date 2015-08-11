
'''
QtGui widget to edit one Proposal instance
'''


from PyQt4 import QtGui, QtCore
import history
import resources
import topic_slider


UI_FILE = 'proposal_details.ui'


class AGUP_ProposalDetails(QtGui.QWidget):
    '''
    QtGui widget to edit one Proposal instance
    '''

    def __init__(self, parent=None):
        '''
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
        prop_id = str(self.getProposalId())
        self.custom_signals.topicValueChanged.emit(prop_id, str(topic), value)
    
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
    
    def clear(self):
        self.setProposalId('')
        self.setProposalTitle('')
        self.setReviewPeriod('')
        self.setSpkName('')
        self.setFirstChoiceBl('')
        self.setSubjects('')
    
    def setAll(self, prop_id, title, period, speaker, choice, subjects):
        self.setProposalId(prop_id)
        self.setProposalTitle(title)
        self.setReviewPeriod(period)
        self.setSpkName(speaker)
        self.setFirstChoiceBl(choice)
        self.setSubjects(subjects)

    def getProposalId(self):
        return self.proposal_id.text()

    def setProposalId(self, value):
        self.proposal_id.setText(value)
        self.modified = True
    
    def setProposalTitle(self, value):
        self.proposal_title.setPlainText(value)
        self.modified = True

    def setReviewPeriod(self, value):
        self.review_period.setText(value)
        self.modified = True

    def setSpkName(self, value):
        self.spk_name.setText(value)
        self.modified = True

    def setFirstChoiceBl(self, value):
        self.first_choice_bl.setText(value)
        self.modified = True

    def setSubjects(self, value):
        self.subjects.setPlainText(value)
        self.modified = True


class CustomSignals(QtCore.QObject):
    '''custom signals'''
    
    topicValueChanged = QtCore.pyqtSignal(str, str, float)


# def AGUP_main():
#     '''simple starter program to develop this code'''
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     mw = AGUP_ProposalDetails()
#     history.addLog("created main window")
#      
#     mw.setProposalId('GUP-421654')
#     mw.setProposalTitle('USAXS study of nothing in something')
#     mw.setReviewPeriod('2025-5')
#     mw.setSpkName('Joe User')
#     mw.setFirstChoiceBl('45-ID-K')
#     mw.setSubjects('medical, environmental, earth, solar, electrical, long-winded')
#  
#     # setup some examples for testing
#     topic_dict = dict(SAXS=0.5, XPCS=0.1, GISAXS=0.9)
#     for key in sorted(topic_dict.keys()):
#         mw.addTopic(key, topic_dict[key])
#     mw.topic_layout.setColumnStretch(1,3)
#     history.addLog("defined some default data")
#      
#     mw.setTopic('SAXS', 0.05)
#     #mw.setTopic('gonzo', 0.05)
#  
#     mw.show()
#     sys.exit(app.exec_())
#  
#  
# if __name__ == '__main__':
#     AGUP_main()
