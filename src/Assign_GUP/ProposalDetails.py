
'''
QtGui widget to edit one Proposal instance
'''


from PyQt4 import QtGui, QtCore
import qt_form_support
import topic_slider
import main_window


UI_FILE = 'proposal_details.ui'


class AGUP_ProposalDetails(QtGui.QWidget):
    '''
    QtGui widget to edit one Proposal instance
    '''

    def __init__(self, owner=None, proposal=None, parent=None):
        '''
        :param owner: main window (QtGui object)
        :param proposal: instance of Proposal object
        '''
        self.owner = owner
        self.proposal = proposal
        QtGui.QWidget.__init__(self, parent)
        qt_form_support.loadUi(UI_FILE, self)

        self.save_pb.clicked.connect(self.onSaveButton)
        self.revert_pb.clicked.connect(self.onRevertButton)
    
    def onSaveButton(self, value):
        # TODO: handle self.save_pb
        main_window.addLog("save_pb not handled yet")
    
    def onRevertButton(self, value):
        # TODO: handle self.revert_pb
        main_window.addLog("revert_pb not handled yet")

    def setProposalId(self, value):
        self.proposal_id.setText(value)
    
    def setProposalTitle(self, value):
        self.proposal_title.setPlainText(value)

    def setReviewPeriod(self, value):
        self.review_period.setText(value)

    def setSpkName(self, value):
        self.spk_name.setText(value)

    def setFirstChoiceBl(self, value):
        self.first_choice_bl.setText(value)

    def setSubjects(self, value):
        self.subjects.setPlainText(value)


def AGUP_main():
    '''simple starter program to develop this code'''
    import sys
    app = QtGui.QApplication(sys.argv)
    mw = AGUP_ProposalDetails(None, None)
    main_window.addLog("created main window")
    
    mw.setProposalId('GUP-421654')
    mw.setProposalTitle('USAXS study of nothing in something')
    mw.setReviewPeriod('2025-5')
    mw.setSpkName('Joe User')
    mw.setFirstChoiceBl('45-ID-K')
    mw.setSubjects('medical, environmental, earth, solar, electrical, long-winded')
# 
    # setup some examples for testing
    topic_dict = dict(SAXS=0.5, XPCS=0.1, GISAXS=0.9)
    topics = sorted(topic_dict.keys())
    w = {}
    for row, key in enumerate(topics):
        w[key] = topic_slider.AGUP_TopicSlider(mw.topic_layout, row, key, topic_dict[key])
    mw.topic_layout.setColumnStretch(1,3)
    main_window.addLog("defined some default data")

    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    AGUP_main()
