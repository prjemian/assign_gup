
'''
Data for one Reviewer of General User Proposals
'''

from lxml import etree
import os
import xml_utility


TEST_FILE = os.path.join('project', '2015-2', 'panel.xml')


class AGUP_Reviewer_Data(object):
    '''
    A Reviewer of General User Proposals
    '''
    
    # these are the XML tags to find in a Reviewer node
    tagList = ('full_name', 'phone', 'email', 'notes', 'joined', 'URL')
    
    def __init__(self, xmlParentNode = None, xmlFile = None):
        '''
        :param xmlParentNode: lxml node of the Reviewer
        :param xmlFile: name of the XML file
        :param xmlFile: str
        '''
        self.db = { 'topics': {} }
        self.db['name'] = None
        self.xmlFile = xmlFile

        for item in self.tagList:
            self.db[item] = None
        if xmlParentNode != None:
            self.readReviewerNode( xmlParentNode )

    def __str__(self):
        '''
        Canonical string representation
        '''
        if self.db['full_name'] == None or self.db['email'] == None:
            return str(None)
        return "%s <%s>" % (self.db['full_name'], self.db['email'])

    def readReviewerNode(self, reviewer = None):
        '''
        Fill the class variables with values from the XML node
        
        :param reviewer: lxml node node of the Reviewer
        '''
        self.db['name'] = reviewer.attrib['name'].strip()
        for k in self.tagList:
            self.db[k] = xml_utility.getXmlText(reviewer, k)
        self.db['topics'] = {}
        node = reviewer.find('topics')
        for k, v in node.attrib.items():
            self.addTopic(k, v)

    def importXml(self, proposal):
        '''
        Fill the class variables with values from the XML node
        
        :param proposal: lxml node of the Reviewer
        '''
        pass

    def addTopic(self, key, initial_value=0.0):
        '''
        add a new topic key and initial value
        '''
        initial_value = float(initial_value)
        if initial_value < 0 or initial_value > 1.0:
            raise ValueError, 'initial value must be between 0 and 1: given=' + str(initial_value)
        if key not in self.db['topics']:
            self.db['topics'][key] = initial_value

    def removeTopic(self, key):
        '''
        remove an existing topic key
        '''
        if key in self.db['topics']:
            del self.db['topics'][key]

    def getTopics(self):
        '''
        return a dictionary of topics: values
        '''
        return self.db['topics']

    def setTopics(self, topic_dict):
        '''
        set topic values from a dictionary, each topic name must already exist
        '''
        for topic, value in topic_dict.items():
            self.setTopic(topic, value)

    def setTopic(self, topic, value):
        '''
        set the value of an existing topic
        '''
        if value < 0 or value > 1.0:
            raise ValueError, 'value must be between 0 and 1: given=' + str(value)
        if topic not in self.db['topics']:
            raise KeyError, 'Topic not found: ' + str(topic)
        self.db['topics'][topic] = value


if __name__ == '__main__':
    xmlFile = TEST_FILE
    doc = etree.parse(xmlFile)
    reviewerNode = doc.find('Reviewer')
    print str(reviewerNode)
    reviewer = AGUP_Reviewer_Data(reviewerNode, xmlFile)
    print str(reviewer)
