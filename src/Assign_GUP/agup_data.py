
# Copyright (c) 2009 - 2016, UChicago Argonne, LLC.
# See LICENSE file for details.

'''
Data model for a review session: proposals, reviewers, topics, and analyses
'''

import datetime
from lxml import etree
import history
import os, sys
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    from mock_PyQt4 import QtCore
else:
    from PyQt4 import QtCore
import StringIO
import traceback

import prop_mvc_data
import resources
import reviewer
import revu_mvc_data
import tools
import topics

UI_FILE = 'main_window.ui'
AGUP_MASTER_ROOT_TAG = 'AGUP_Review_Session'
AGUP_XML_SCHEMA_FILE = resources.resource_file('agup_review_session.xsd')
AGUP_MASTER_VERSION = '1.0'
SUBJECT_STRENGTH_FULL = 1.0


class AGUP_Data(QtCore.QObject):
    '''
    Complete data for a PRP review session
    '''

    def __init__(self, config = None):
        import settings
        QtCore.QObject.__init__(self)

        self.settings = config or settings.ApplicationQSettings()
        self.clearAllData()
        self.modified = False
    
    def clearAllData(self):
        '''
        clear all data (except for self.settings)
        '''
        import email_template
        self.proposals = prop_mvc_data.AGUP_Proposals_List(self)
        self.reviewers = revu_mvc_data.AGUP_Reviewers_List(self)
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
        self.importTopics(filename)
        self.importReviewers(filename)
        self.importProposals(filename)
        self.importEmailTemplate(filename)
        self.modified = False

        return True
    
    def write(self, filename):
        '''
        write this data to an XML file
        '''
        if self.topics is None: return
        if self.proposals is None: return
        if self.reviewers is None: return

        doc = etree.parse( StringIO.StringIO('<' + AGUP_MASTER_ROOT_TAG + '/>') )

        root = doc.getroot()
        root.attrib['cycle'] = self.proposals.cycle
        root.attrib['version'] = AGUP_MASTER_VERSION
        root.attrib['time'] = str(datetime.datetime.now())
        
        self.topics.writeXml(root, False)
        self.reviewers.writeXmlNode(root)
        self.proposals.writeXmlNode(root)
        
        self.email.writeXmlNode(root)

        s = etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding=tools.XML_CODEPOINT)
        open(filename, 'w').write(s)
    
    def importProposals(self, xmlFile):
        '''
        import a Proposals XML file as generated by the APS or proposals from a PRP Project file
        '''
        props = prop_mvc_data.AGUP_Proposals_List(self)
        props.importXml(xmlFile)
        
        if len(self.reviewers) == 0:
            self._auto_assess(props)
        self._restore_assignments(props)

        _review_cycle_settings = self.settings.getReviewCycle()
        _review_cycle_proposals = props.cycle or _review_cycle_settings
        if _review_cycle_settings in (None, '', _review_cycle_proposals):
            self.proposals = props
            self.settings.setReviewCycle(_review_cycle_proposals or '')
        else:
            msg = 'Cannot import proposals from cycle "' + _review_cycle_proposals
            msg += '" into PRP session for cycle "' + _review_cycle_settings + '"'
            raise KeyError, msg
    
    def _auto_assess(self, props):
        '''
        get the list of reviewers and topics from the proposals, assess topic values for each proposal
        '''
        # get list of subjects from all proposals
        names = []
        subjects = []
        for prop in props:
            for full_name in prop.eligible_reviewers.keys():
                if full_name not in names:
                    names.append(full_name)
            for subject in prop.getSubjects():
                if subject not in subjects:
                    subjects.append(subject)
        self.topics.addTopics(subjects)
        
        # build up a list of reviewers from the proposals
        for item, full_name in enumerate(names):
            sort_name = full_name.split()[-1] + '_' + str(item)
            rvwr_obj = reviewer.AGUP_Reviewer_Data()
            for key in rvwr_obj.tagList:
                rvwr_obj.setKey(key, 'unknown')
            rvwr_obj.setKey('full_name', full_name)
            rvwr_obj.setKey('name', sort_name)
            rvwr_obj.addTopics(subjects)
            rr = self.reviewers.reviewers
            rr[sort_name] = rvwr_obj
            self.reviewers.reviewer_sort_list.append(sort_name)
        self.reviewers.reviewer_sort_list = sorted(rr.keys())

        # auto-assign topic values to proposal
        for prop in props:
            prop.addTopics(subjects)        # proposal gets all the known topics
            for subject in prop.getSubjects():
                prop.setTopic(subject, SUBJECT_STRENGTH_FULL)     # this subject was selected by proposer
    
    def _restore_assignments(self, props):
        '''restore any assessments or assignments'''
        for new_proposal in props:
            prop_id = new_proposal.getKey('proposal_id')
            if self.proposals.exists(prop_id):
                existing_prop = self.proposals.getProposal(prop_id)
                new_proposal.topics = existing_prop.topics
            
                for full_name, role in existing_prop.eligible_reviewers.items():
                    if full_name in ('', None):
                        continue
    
                    # check that assigned reviewer is listed as an eligible reviewer
                    if full_name not in new_proposal.eligible_reviewers:
                        msg = 'Reviewer "' + str(full_name)
                        msg += '" assigned to proposal "' + prop_id
                        msg += '" is not on the list of reviewers for that proposal'
                        raise ValueError, msg
    
                    # assign the reviewer's role
                    rvwr = self.reviewers.getByFullName(full_name)
                    new_proposal.setAssignedReviewer(rvwr, role)

            if len(new_proposal.getTopicList()) == 0:
                subject_list = new_proposal.getSubjects()
                new_proposal.addTopics(self.topics.getTopicList())
                for subject in subject_list:
                    if self.topics.exists(subject):
                        new_proposal.setTopic(subject, SUBJECT_STRENGTH_FULL)
    
    def importReviewers(self, xmlFile):
        '''
        import a complete set of reviewers (usually from a previous review cycle's file)
        
        Completely replace the set of reviewers currently in place.
        '''
        rvwrs = revu_mvc_data.AGUP_Reviewers_List(self)
        rvwrs.importXml(xmlFile)        # pass exceptions straight to the caller 

        if len(rvwrs) > 0:              # synchronize lists of topics
            sort_name = rvwrs.getByIndex(0)
            reviewer = rvwrs.getReviewer(sort_name)
            for topic in reviewer.topics:
                if not self.topics.exists(topic):
                    self.topics.add(topic)
                    self.proposals.addTopic(topic)
            for topic in self.topics:
                if not reviewer.topics.exists(topic):
                    rvwrs.addTopic(topic)

        self.reviewers = rvwrs
    
    def importTopics(self, xmlFile):
        '''
        import a complete set of Topics (usually from a previous PRP Project file)
         
        Completely replace the set of Topics currently in place.
        '''
        topics_obj = topics.Topics()
        topics_obj.importXml(xmlFile, False)     
        
       # merge with other lists
        for topic in topics_obj.topics:
            if not self.topics.exists(topic):
                self.topics.add(topic)
                self.proposals.addTopic(topic)
                self.reviewers.addTopic(topic)
    
    def importEmailTemplate(self, xmlFile):
        '''
        import the email template support
        '''
        self.email.importXml(xmlFile)        # pass exceptions straight to the caller
    
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
