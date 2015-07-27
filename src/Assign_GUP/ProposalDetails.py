
'''
QtGui widget to edit one Proposal instance
'''


from PyQt4 import QtGui, QtCore
import qt_form_support
import topic_slider


UI_FILE = 'proposal_details.ui'


class AGUP_ProposalDetails(object):
    '''
    QtGui widget to edit one Proposal instance
    '''

    def __init__(self, parent, proposal):
        '''
        :param parent: owner (QtGui object)
        :param proposal: instance of Proposal object
        '''
        self.parent = parent
        self.proposal = proposal
        self.ui = qt_form_support.load_form(UI_FILE)

        self.ui.save_pb.clicked.connect(self.onSaveButton)
        self.ui.revert_pb.clicked.connect(self.onRevertButton)
    
    def onSaveButton(self, value):
        # TODO: handle self.ui.save_pb
        print "ui.save_pb not handled yet"
    
    def onRevertButton(self, value):
        # TODO: handle self.ui.revert_pb
        print "ui.revert_pb not handled yet"

    def setProposalId(self, value):
        self.ui.proposal_id.setText(value)
    
    def setProposalTitle(self, value):
        self.ui.proposal_title.setPlainText(value)

    def setReviewPeriod(self, value):
        self.ui.review_period.setText(value)

    def setSpkName(self, value):
        self.ui.spk_name.setText(value)

    def setFirstChoiceBl(self, value):
        self.ui.first_choice_bl.setText(value)

    def setSubjects(self, value):
        self.ui.subjects.setPlainText(value)
    

# def report(mw):
#     print 'getFullName', mw.getFullName()
#     print 'getSortName', mw.getSortName()
#     print 'getPhone', mw.getPhone()
#     print 'getEmail', mw.getEmail()
#     print 'getJoined', mw.getJoined()
#     print 'getUrl', mw.getUrl()
#     print 'getNotes', mw.getNotes()


def AGUP_main():
    '''simple starter program to develop this code'''
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = AGUP_ProposalDetails(None, None)
    
    main_window.setProposalId('GUP-421654')
    main_window.setProposalTitle('USAXS study of nothing in something')
    main_window.setReviewPeriod('2025-5')
    main_window.setSpkName('Joe User')
    main_window.setFirstChoiceBl('45-ID-K')
    main_window.setSubjects('medical,environmental,earth')
# 
    # setup some examples for testing
    topic_dict = dict(SAXS=0.5, XPCS=0.1, GISAXS=0.9)
    topics = sorted(topic_dict.keys())
    w = {}
    for row, key in enumerate(topics):
        w[key] = topic_slider.AGUP_TopicSlider(main_window.ui.topic_layout, row, key, topic_dict[key])
    main_window.ui.topic_layout.setColumnStretch(1,3)

    main_window.ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    AGUP_main()
