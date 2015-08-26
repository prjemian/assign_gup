
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
import email_template
import prop_mvc_data
import resources
import revu_mvc_data
import settings
import topics
import xml_utility

UI_FILE = 'main_window.ui'
AGUP_MASTER_ROOT_TAG = 'AGUP_Review_Session'
AGUP_XML_SCHEMA_FILE = resources.resource_file('agup_review_session.xsd')
AGUP_MASTER_VERSION = '1.0'


class AGUP_Data(QtCore.QObject):
    '''
    Complete data for a PRP review session
    '''

    def __init__(self, config = None):
        QtCore.QObject.__init__(self)

        self.settings = config or settings.ApplicationQSettings()
        self.clearAllData()
        self.modified = False
    
    def clearAllData(self):
        '''
        clear all data (except for self.settings)
        '''
        self.analyses = None            # TODO: remove this
        self.proposals = prop_mvc_data.AGUP_Proposals_List()
        self.reviewers = revu_mvc_data.AGUP_Reviewers_List()
        self.topics = topics.Topics()
        self.email = email_template.EmailTemplate()
    
    def openPrpFile(self, filename):
        '''
        '''
        if not os.path.exists(filename):
            history.addLog('PRP File not found: ' + filename)
            return False
        self.clearAllData()
        filename = str(filename)
        # self.importTopics()
        self.importReviewers(filename)
        self.importProposals(filename)
        self.importAnalyses(filename)
        self.importEmailTemplate(filename)
        self.modified = False

        return True
    
    def write(self, filename):
        '''
        write this data to an XML file
        '''
        if self.proposals is None: return
        if self.reviewers is None: return

        doc = etree.parse( StringIO.StringIO('<' + AGUP_MASTER_ROOT_TAG + '/>') )

        root = doc.getroot()
        root.attrib['cycle'] = self.proposals.cycle
        root.attrib['version'] = AGUP_MASTER_VERSION
        root.attrib['time'] = str(datetime.datetime.now())
        
        node = etree.SubElement(root, 'Topics')
        if self.topics is not None:
            for topic in self.topics:
                subnode = etree.SubElement(node, 'Topic')
                subnode.attrib['name'] = topic

        node = etree.SubElement(root, 'Review_panel')
        self.reviewers.writeXmlNode(node)
        node = etree.SubElement(root, 'Proposal_list')
        self.proposals.writeXmlNode(node)

        # provide this data in a second place, in case imported proposals destroy the original
        node = etree.SubElement(root, 'Assignments')
        self.analyses.writeXmlNode(node)
        
        self.email.writeXmlNode(root)

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
            define_new_topics = len(proposal.topics.getTopicList()) == 0
            break

        # merge findings with self.proposals and self.reviewers
        for prop_id, analysis in findings.analyses.items():
            proposal = self.proposals.getProposal(prop_id)      # raises exception if not found
            for topic in analysis.topics:
                value = analysis.getTopic(topic)
                if define_new_topics:
                    proposal.topics.add(topic, value)     # topic must NOT exist
                else:
                    proposal.topics.set(topic, value)     # topic must exist
                if not self.topics.exists(topic):
                    self.topics.add(topic)
            
            # TODO: check that assigned reviewers in proposal object match with proposal analysis finding

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

        cycle = self.settings.getReviewCycle()
        if cycle in (None, '', props.cycle):
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
    
    def importEmailTemplate(self, xmlFile):
        '''
        import the email template support
        '''
        try:
            self.email.importXml(xmlFile)
        except Exception:
            history.addLog(traceback.format_exc())
            return
    
    def getCycle(self):
        '''the review cycle, as defined by the proposals'''
        if self.proposals is None:
            return ''
        return self.proposals.cycle


def dev_test2():
    agup = AGUP_Data()
    agup.openPrpFile('project/agup_project.xml')
    print agup


if __name__ == '__main__':
#     developer_testing_of_this_module()
    dev_test2()
