
'''
Proposals: underlying data class for the MVC model 
'''

from PyQt4 import QtCore
from lxml import etree
import os
import proposal
import resources
import xml_utility


XML_SCHEMA_FILE = resources.resource_file('proposals.xsd')
ROOT_TAG = 'Review_list'

class AGUP_Proposals_List(QtCore.QObject):
    '''
    the list of all proposals
    '''
    
    def __init__(self):
        self.proposals = {}
        self.prop_id_list = []
    
    def __len__(self):
        return len(self.proposals)

    def __iter__(self):
        for prop in self.proposals.values():
            yield prop

    def getByIndex(self, index):
        if index < 0 or index >= len(self.prop_id_list):
            raise IndexError, 'Index not found: ' + str(index)
        return self.prop_id_list[index]

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with proposals
        '''
        if not os.path.exists(filename):
            raise IOError, 'file not found: ' + filename

        try:
            doc = etree.parse(filename)
        except etree.XMLSyntaxError, exc:
            raise xml_utility.XmlSyntaxError, str(exc)

        self.validateXml(doc)

        db = {}
        self.prop_id_list = []
        root = doc.getroot()
        self.cycle = root.attrib['period']
        for node in doc.findall('Proposal'):
            prop_id = xml_utility.getXmlText(node, 'proposal_id')
            prop = proposal.AGUP_Proposal_Data(node, filename)
            db[prop_id] = prop
            self.prop_id_list.append(prop_id)
        self.proposals = db

    def inOrder(self):
        return sorted(self.proposals.values())
    
    def validateXml(self, xmlDoc):
        '''validateXml XML document for correct root tag & XML Schema'''
        root = xmlDoc.getroot()
        if root.tag != ROOT_TAG:
            msg = 'expected=' + ROOT_TAG
            msg += ', received=' + root.tag
            raise xml_utility.IncorrectXmlRootTag, msg
        try:
            xml_utility.validate(xmlDoc, XML_SCHEMA_FILE)
        except etree.DocumentInvalid, exc:
            raise xml_utility.InvalidWithXmlSchema, str(exc)
        return True

    def addTopic(self, key, initial_value=0.0):
        '''
        add a new topic key and initial value to all proposals
        '''
        if initial_value < 0 or initial_value >= 1.0:
            raise ValueError, 'initial value must be between 0 and 1: given=' + str(initial_value)
        for prop in self.inOrder():
            prop.addTopic(key, initial_value)

    def removeTopic(self, key):
        '''
        remove an existing topic key from all proposals
        '''
        for prop in self.inOrder():
            prop.removeTopic(key)

    def setTopicValue(self, prop_id, topic, value):
        '''
        set the topic value on a proposal identified by GUP ID
        '''
        if value < 0 or value > 1.0:
            raise ValueError, 'value must be between 0 and 1: given=' + str(value)
        if prop_id not in self.proposals:
            raise KeyError, 'Proposal ID not found: ' + str(prop_id)
        self.proposals[prop_id].setTopic(topic, value)
