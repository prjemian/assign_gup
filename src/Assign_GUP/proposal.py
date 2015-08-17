
'''
Data for one General User Proposal
'''

from lxml import etree
import topics
import xml_utility


class AGUP_Proposal_Data(topics.Topic_MixinClass):
    '''
    A single General User Proposal
    '''
    tagList = ( # these are the XML tags to find in a proposal
       'proposal_id', 'proposal_type', 'proposal_title', 
       'review_period', 'spk_name', 'recent_req_period', 
       'first_choice_bl'
    )
    
    def __init__(self, xmlParentNode = None, xmlFile = None):
        self.db = dict(topics={}, eligible_reviewers={})
        self.xmlFile = xmlFile
        if xmlParentNode != None:
            self.importXml( xmlParentNode )

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
    
    def writeXmlNode(self, specified_node):
        '''
        write this Proposal's data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        
        example::

          <proposal_id>42345</proposal_id>
          <proposal_type>GUP</proposal_type>
          <proposal_title>Effect of Solvent on the Structure and Assembly of Kafirin</proposal_title>
          <review_period>2015-1</review_period>
          <notification_date>03/07/2015</notification_date>
          <project_type>regular</project_type>
          <spk_name>Qingrong Huang</spk_name>
          <recent_req_period>2015-1</recent_req_period>
          <first_choice_bl>18-ID-BIO</first_choice_bl>
          <subject>
            <name>Materials science</name>
            <name>Polymers</name>
          </subject>
          <reviewer>
            <name>Peter Jemian</name>
            <name assigned="reviewer2">John Flanagan</name>
            <name>Suresh Narayanan</name>
            <name>Fan Zhang</name>
            <name assigned="reviewer1">Sagar Kathuria</name>
            <name>Deborah Myers</name>
          </reviewer>
        </Proposal>

        '''
        for tag in self.tagList:
            etree.SubElement(specified_node, tag).text = self.getKey(tag)

        node = etree.SubElement(specified_node, 'subject')
        for v in [_.strip() for _ in self.db['subjects'].split(',')]:
            subnode = etree.SubElement(node, 'name')
            subnode.text = str(v)

        node = etree.SubElement(specified_node, 'reviewer')
        for k, v in sorted(self.db['eligible_reviewers'].items()):
            subnode = etree.SubElement(node, 'name')
            subnode.text = str(k)
            if v in (1, 2):
                subnode.attrib['assigned'] = 'reviewer' + str(v)

        node = etree.SubElement(specified_node, 'Topics')
        for k, v in sorted(self.getTopics().items()):
            subnode = etree.SubElement(node, 'Topic')
            subnode.attrib['name'] = k
            subnode.attrib['value'] = str(v)
    
    def getKey(self, key):
        return self.db[key]
