
'''
Data for one Reviewer of General User Proposals
'''

from lxml import etree
import topics
import xml_utility


class AGUP_Reviewer_Data(topics.Topic_MixinClass):
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
            self.importXml( xmlParentNode )

    def __str__(self):
        '''
        Canonical string representation
        '''
        if self.getFullName() == None or self.db['email'] == None:
            return str(None)
        return "%s <%s>" % (self.db['full_name'], self.db['email'])

    def importXml(self, reviewer):
        '''
        Fill the class variables with values from the XML node
        
        :param reviewer: lxml node node of the Reviewer
        '''
        self.db['name'] = reviewer.attrib['name'].strip()
        for k in self.tagList:
            self.db[k] = xml_utility.getXmlText(reviewer, k)
        self.db['topics'] = {}
        node = reviewer.find('topics')
        if node is not None:
            for k, v in node.attrib.items():
                self.addTopic(k, v)
    
    def writeXmlNode(self, specified_node):
        '''
        write this Reviewer's data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        '''
        specified_node.attrib['name'] = self.getKey('name')
        for tag in self.tagList:
            etree.SubElement(specified_node, tag).text = self.getKey(tag)

        node = etree.SubElement(specified_node, 'Topics')
        for k, v in sorted(self.getTopics().items()):
            subnode = etree.SubElement(node, 'Topic')
            subnode.attrib['name'] = k
            subnode.attrib['value'] = str(v)
    
    def getFullName(self):
        return self.getKey('full_name')
    
    def getKey(self, key):
        return self.db[key]
