
'''
Data for one General User Proposal
'''

from lxml import etree
import xml_utility


class AGUP_Proposal_Data(object):
    '''
    A single General User Proposal
    '''
    tagList = ( # these are the XML tags to find in a proposal
       'proposal_id', 'proposal_type', 'proposal_title', 
       'review_period', 'spk_name', 'recent_req_period', 
       'first_choice_bl'
    )
    
    def __init__(self):
        self.db = dict(topics={}, eligible_reviewers={})

    def importXml(self, proposal):
        '''
        Fill the class variables with values from the XML node
        
        :param proposal: lxml node of the Proposal
        '''
        for key in self.tagList:
            self.db[key] = xml_utility.getXmlText(proposal, key)
        subject_node = proposal.find('subject')
        if subject_node is not None:
            subjects = [node.text.strip() for node in subject_node.findall('name')]
        else:
            subjects = ''
        self.db['subjects'] = ", ".join(subjects)
        eligible_reviewers = self.db['eligible_reviewers']
        node = proposal.find('reviewer')
        for name in node.findall('name'):
            who = name.text.strip()
            assignment = name.get('assigned', None)
            if assignment is not None:
                assignment = int(assignment[-1])
            excluded = name.get('excluded', 'false') == 'true'
            if who not in eligible_reviewers and not excluded:
                eligible_reviewers[who] = assignment

        if False:   # the old way
            for reviewer_number in (1, 2):
                position = 'reviewer%d' % reviewer_number
                node = proposal.find(position)
                assigned = node.attrib['assigned']
                for name in node.findall('name'):
                    who = name.text.strip()
                    if who == assigned:
                        # note this reviewer is assigned primary (1) or secondary (2) role
                        self.db['eligible_reviewers'][who] = reviewer_number
                    else:
                        # not assigned
                        if who not in self.db['eligible_reviewers']:
                            # add to list of reviewers eligible for this proposal
                            self.db['eligible_reviewers'][who] = None
