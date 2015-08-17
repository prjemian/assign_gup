
'''
Data model for a review session: proposals, reviewers, topics, and analyses
'''

import os, sys
import history
from PyQt4 import QtCore
import traceback
import analyses
import prop_mvc_data
import resources
import revu_mvc_data
import settings
import topics
import xml_utility

UI_FILE = 'main_window.ui'
RC_FILE = '.assign_gup.rc'
RC_SECTION = 'Assign_GUP'
DUMMY_TOPICS_LIST = '''bio chem geo eng mater med phys poly'''.split()


class AGUP_Data(QtCore.QObject):
    '''
    Complete data for a PRP review session
    '''

    def __init__(self):
        QtCore.QObject.__init__(self)

        self.settings = settings.ApplicationSettings(RC_FILE, RC_SECTION)
        self.analyses = None
        self.modified = False
        self.proposals = None
        self.reviewers = None
        self.topics = []
    
    def importAnalyses(self, xmlFile):
        '''
        '''
        if self.proposals is None:
            history.addLog('Must import proposals before analyses')
            return
        if self.reviewers is None:
            history.addLog('Must import reviewers before analyses')
            return

        findings = analyses.AGUP_Analyses()
        try:
            findings.importXml(xmlFile)
        except Exception, _exc:
            history.addLog(_exc)
            return

        # TODO: merge findings with self.proposals and self.reviewers
        # the reviewers and topics in the analyses must match the others

        self.analyses = findings
    
    def importProposals(self, xmlFile):
        '''
        '''
        props = prop_mvc_data.AGUP_Proposals_List()
        try:
            props.importXml(xmlFile)
        except Exception, _exc:
            history.addLog(_exc)
            return

        cycle = self.settings.getByKey('review_cycle')
        if len(cycle) == 0 or cycle == props.cycle:
            self.proposals = props
            self.settings.setReviewCycle(props.cycle)
        else:
            msg = 'Cannot import proposals for ' + props.cycle
            msg += ' into PRP session for cycle: ' + cycle
            history.addLog(msg)
    
    def importReviewers(self, xmlFile):
        '''
        import a complete set of reviewers (usually from a previous review cycle's file)
        
        Completely replace the set of reviewers currently in place.
        '''
        rvwrs = revu_mvc_data.AGUP_Reviewers_List()
        try:
            rvwrs.importXml(xmlFile)
        except Exception, _exc:
            history.addLog(traceback.format_exc())
            return

        self.reviewers = rvwrs


def main():
    '''simple starter program to develop this code'''
    import pprint
    agup = AGUP_Data()
    history.addLog( agup )
    history.addLog( agup.settings )
    history.addLog( agup.settings.config )

    # try to import the wrong reviewers files
    agup.importReviewers('Dilbert is a cartoon')
    history.addLog( 'reviewers: ' + str(agup.reviewers) )
    agup.importReviewers('Bullwinkle is a moose')
    history.addLog( 'proposals: ' + str(agup.proposals) )
    agup.importReviewers(os.path.abspath('project/2015-2/proposals.xml'))

    # set the current cycle wrong and try to import proposals
    agup.settings.setReviewCycle('1895-5')
    agup.importProposals(os.path.abspath('project/2015-2/proposals.xml'))
    history.addLog( 'proposals: ' + str(agup.proposals) )
    if agup.proposals is not None:
        history.addLog( '# proposals: ' + str(len(agup.proposals)) )

    # try to import the analyses before importing reviewers and proposals
    agup.importAnalyses(os.path.abspath('project/2015-2/analysis.xml'))

    history.addLog()
    history.addLog( '#'*40 )
    history.addLog()

    agup.settings.setPrpPath(os.path.abspath('project/prp'))
    agup.importReviewers(os.path.abspath('project/2015-2/panel.xml'))
    history.addLog( 'reviewers: ' + str(agup.reviewers) )
    if agup.reviewers is not None:
        history.addLog( '# reviewers: ' + str(len(agup.reviewers)) )

    # set the current cycle right and import proposals
    agup.settings.setReviewCycle('2015-2')
    agup.importProposals(os.path.abspath('project/2015-2/proposals.xml'))
    history.addLog( 'proposals: ' + str(agup.proposals) )
    if agup.proposals is not None:
        history.addLog( '# proposals: ' + str(len(agup.proposals)) )

    agup.importAnalyses(os.path.abspath('project/2015-2/analysis.xml'))
    history.addLog( 'analyses: ' + str(agup.analyses) )
    if agup.analyses is not None:
        history.addLog( '# analyses: ' + str(len(agup.analyses)))


if __name__ == '__main__':
    main()
