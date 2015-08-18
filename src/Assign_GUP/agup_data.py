
'''
Data model for a review session: proposals, reviewers, topics, and analyses
'''

import datetime
from lxml import etree
import os, sys
import history
from PyQt4 import QtCore
import StringIO
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
TEST_OUTPUT_FILE = os.path.join('project', 'agup_project.xml')
AGUP_MASTER_ROOT_TAG = 'AGUP_Review_Session'
AGUP_XML_SCHEMA_FILE = resources.resource_file('agup_review_session.xsd')
AGUP_MASTER_VERSION = '1.0'


class AGUP_Data(QtCore.QObject):
    '''
    Complete data for a PRP review session
    '''

    def __init__(self, config = None):
        QtCore.QObject.__init__(self)

        self.settings = config or settings.ApplicationSettings(RC_FILE, RC_SECTION)
        self.analyses = None
        self.modified = False
        self.proposals = None
        self.reviewers = None
        self.topics = None
    
    def openPrpFile(self, filename):
        '''
        '''
        if not os.path.exists(filename):
            history.addLog('PRP File not found: ' + filename)
            return False
        filename = str(filename)
        self.importReviewers(filename)
        self.importProposals(filename)
        self.importAnalyses(filename)

        return True
    
    def write(self, filename):
        '''
        write this data to an XML file
        '''
        if self.proposals is None: return
        if self.reviewers is None: return

#         if not os.path.exists(filename):
#             # make the file
#             doc = etree.parse( StringIO.StringIO('<' + AGUP_MASTER_ROOT_TAG + '/>') )
#         else:
#             doc = etree.parse(filename)
        doc = etree.parse( StringIO.StringIO('<' + AGUP_MASTER_ROOT_TAG + '/>') )

        root = doc.getroot()
        root.attrib['cycle'] = self.proposals.cycle
        root.attrib['version'] = AGUP_MASTER_VERSION
        root.attrib['time'] = str(datetime.datetime.now())
        
        node = etree.SubElement(root, 'Topics')
        if self.topics is not None:
            for topic in sorted(self.topics):
                subnode = etree.SubElement(node, 'Topic')
                subnode.attrib['name'] = topic

        node = etree.SubElement(root, 'Review_panel')
        self.reviewers.writeXmlNode(node)
        node = etree.SubElement(root, 'Proposal_list')
        self.proposals.writeXmlNode(node)

        # provide this data in a second place, in case imported proposals destroy the original
        node = etree.SubElement(root, 'Assignments')
        self.analyses.writeXmlNode(node)

        s = etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding='UTF-8')
        open(filename, 'w').write(s)

    def importAnalyses(self, xmlFile):
        '''
        read analyses, assignments, & assessments from XML file

        apply decision tree:
          if no topics are known
             define new topics names and set values
          else 
             match all topics lists
             only if successful matches all around, set values
        
        simple test if topics are defined for first proposal since others MUST match
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
        except Exception:
            history.addLog(traceback.format_exc())
            return

        self.topics = topics.Topics()
        define_new_topics = False
        for prop_id in findings.analyses.keys():
            proposal = self.proposals.getProposal(prop_id)      # raises exception if not found
            define_new_topics = len(proposal.getTopics().keys()) == 0
            break

        # merge findings with self.proposals and self.reviewers
        for prop_id, analysis in findings.analyses.items():
            proposal = self.proposals.getProposal(prop_id)      # raises exception if not found
            for topic, value in analysis['Topics'].items():
                if define_new_topics:
                    proposal.addTopic(topic, value)     # topic must NOT exist
                else:
                    proposal.setTopic(topic, value)     # topic must exist
                if not self.topics.exists(topic):
                    self.topics.add(topic)
            for reviewer_name in analysis['Reviewers'].values():
                if len(reviewer_name) > 0:
                    reviewer = self.reviewers.getByFullName(reviewer_name)
                    for topic, value in analysis['Topics'].items():
                        if define_new_topics:
                            reviewer.addTopic(topic, value)     # topic must NOT exist
                        else:
                            reviewer.setTopic(topic, value)     # topic must exist

        self.analyses = findings
    
    def importProposals(self, xmlFile):
        '''
        import a Proposals XML file as generated by the APS
        '''
        props = prop_mvc_data.AGUP_Proposals_List()
        try:
            props.importXml(xmlFile)
        except Exception:
            history.addLog(traceback.format_exc())
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
        except Exception:
            history.addLog(traceback.format_exc())
            return

        self.reviewers = rvwrs
    
    def getCycle(self):
        '''the review cycle, as defined by the proposals'''
        if self.proposals is None:
            return ''
        return self.proposals.cycle


def developer_testing_of_this_module():
    '''simple starter program to develop this code'''
    agup = AGUP_Data()
    history.addLog( agup )
    history.addLog( agup.settings )
    history.addLog( agup.settings.config )

    # mistake: try to import the wrong reviewers files
    agup.importReviewers('Dilbert is a cartoon')
    history.addLog( 'reviewers: ' + str(agup.reviewers) )
    agup.importReviewers('Bullwinkle is a moose')
    history.addLog( 'proposals: ' + str(agup.proposals) )
    agup.importReviewers(os.path.abspath('project/2015-2/proposals.xml'))

    # mistake: set the current cycle wrong and try to import proposals
    agup.settings.setReviewCycle('1895-5')
    agup.importProposals(os.path.abspath('project/2015-2/proposals.xml'))
    history.addLog( 'proposals: ' + str(agup.proposals) )
    if agup.proposals is not None:
        history.addLog( '# proposals: ' + str(len(agup.proposals)) )

    # mistake: try to import the analyses before importing reviewers and proposals
    agup.importAnalyses(os.path.abspath('project/2015-2/analysis.xml'))

    history.addLog()
    history.addLog( '#'*40 + '  now, do things right, in order')
    history.addLog()

    # import review panelists, cycle does not have to match
    #agup.settings.setPrpPath(os.path.abspath('project/prp'))
    agup.importReviewers(os.path.abspath('project/2015-2/panel.xml'))
    history.addLog( 'reviewers: ' + str(agup.reviewers) )
    if agup.reviewers is not None:
        history.addLog( '# reviewers: ' + str(len(agup.reviewers)) )

    # set the current cycle right
    agup.settings.setReviewCycle('2015-2')

    # import proposals
    agup.importProposals(os.path.abspath('project/2015-2/proposals.xml'))
    history.addLog( 'proposals: ' + str(agup.proposals) )
    if agup.proposals is not None:
        history.addLog( '# proposals: ' + str(len(agup.proposals)) )

    # import analyses
    agup.importAnalyses(os.path.abspath('project/2015-2/analysis.xml'))
    history.addLog( 'analyses: ' + str(agup.analyses) )
    if agup.analyses is not None:
        history.addLog( '# analyses: ' + str(len(agup.analyses)))

    agup.write(TEST_OUTPUT_FILE)
    

def dev_test2():
    agup = AGUP_Data()
    agup.openPrpFile('project/agup_project.xml')
    print agup


if __name__ == '__main__':
#     developer_testing_of_this_module()
    dev_test2()
