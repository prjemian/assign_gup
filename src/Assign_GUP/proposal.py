
'''
Data for one General User Proposal
'''

from lxml import etree
import topics
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
    
    def __init__(self, xmlParentNode = None, xmlFile = None):
        self.db = {}
        self.eligible_reviewers = {}
        self.topics = topics.Topics()
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
        eligibles = self.eligible_reviewers
        node = proposal.find('reviewer')
        for name in node.findall('name'):
            who = name.text.strip()
            assignment = name.get('assigned', None)
            if assignment is not None:
                assignment = int(assignment[-1])
            excluded = name.get('excluded', 'false') == 'true'
            if who not in eligibles and not excluded:
                eligibles[who] = assignment
    
    def writeXmlNode(self, specified_node):
        '''
        write this Proposal's data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        '''
        for tag in self.tagList:
            etree.SubElement(specified_node, tag).text = self.getKey(tag)

        node = etree.SubElement(specified_node, 'subject')
        for v in [_.strip() for _ in self.db['subjects'].split(',')]:
            subnode = etree.SubElement(node, 'name')
            subnode.text = str(v)

        node = etree.SubElement(specified_node, 'reviewer')
        for k, v in sorted(self.eligible_reviewers.items()):
            subnode = etree.SubElement(node, 'name')
            subnode.text = str(k)
            if v in (1, 2):
                subnode.attrib['assigned'] = 'reviewer' + str(v)

        node = etree.SubElement(specified_node, 'Topics')
        for k in self.topics:
            subnode = etree.SubElement(node, 'Topic')
            subnode.attrib['name'] = k
            subnode.attrib['value'] = str(self.topics.get(v))
    
    def getKey(self, key):
        return self.db[key]
    
    def getTopic(self, topic):
        '''
        return the value of the named topic
        '''
        return self.topics.get(topic)
    
    def getTopicList(self):
        '''
        return a list of all topics
        '''
        return self.topics.getTopicList()
    
    def addTopic(self, topic, value=topics.DEFAULT_TOPIC_VALUE):
        '''
        declare a new topic and give it an initial value
        
        topic must not exist or KeyError exception will be raised
        '''
        self.topics.add(topic, value)
    
    def addTopics(self, topics_list):
        '''
        declare several new topics and give them all default values
        
        each topic must not exist or KeyError exception will be raised
        '''
        self.topics.addTopics(topics_list)
    
    def setTopic(self, topic, value=topics.DEFAULT_TOPIC_VALUE):
        '''
        set value of an existing topic
        
        topic must exist or KeyError exception will be raised
        '''
        self.topics.set(topic, value)

    def removeTopic(self, key):
        '''
        remove the named topic
        '''
        self.topics.remove(key)

    def removeTopics(self, key_list):
        '''
        remove several topics at once
        '''
        self.topics.removeTopics(key)
