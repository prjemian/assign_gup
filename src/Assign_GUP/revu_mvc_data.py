
'''
Reviewers: underlying data class for the MVC model 
'''

from PyQt4 import QtCore
from lxml import etree
import os
import traceback
import reviewer
import resources
import xml_utility


XML_SCHEMA_FILE = resources.resource_file('reviewers.xsd')
ROOT_TAG = 'Review_panel'

class AGUP_Reviewers_List(QtCore.QObject):
    '''
    the list of all reviewers
    '''
    
    def __init__(self):
        QtCore.QObject.__init__(self)

        self.reviewers = {}     # .clear()
        self.reviewer_sort_list = []
    
    def __len__(self):
        return len(self.reviewers)

    def __iter__(self):
        for item in self.reviewers.values():
            yield item

    def getByIndex(self, index):
        if index < 0 or index >= len(self.reviewer_sort_list):
            raise IndexError, 'Index not found: ' + str(index)
        return self.reviewer_sort_list[index]

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with reviewers
        '''
        if not os.path.exists(filename):
            raise IOError, 'file not found: ' + filename

        try:
            doc = etree.parse(filename)
        except etree.XMLSyntaxError, exc:
            raise xml_utility.XmlSyntaxError, str(exc)

        try:
            self.validateXml(doc)
        except Exception, exc:
            msg = 'In ' + filename + ': ' + traceback.format_exc()
            raise Exception, msg

        db = {}
        self.reviewer_sort_list = []
        root = doc.getroot()
        self.cycle = root.attrib['period']
        for node in doc.findall('Reviewer'):
            sort_name = node.attrib['name'].strip()
            panelist = reviewer.AGUP_Reviewer_Data(node, filename)
            db[sort_name] = panelist
            self.reviewer_sort_list.append(sort_name)
        self.reviewers = db

    def inOrder(self):
        return sorted(self.reviewers.values())
    
    def validateXml(self, xmlDoc):
        '''validateXml XML document for correct root tag & XML Schema'''
        # TODO: plan to import from master XML file (different schema)
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
        add a new topic key and initial value to all reviewers
        '''
        if initial_value < 0 or initial_value >= 1.0:
            raise ValueError, 'initial value must be between 0 and 1: given=' + str(initial_value)
        for item in self.inOrder():
            item.addTopic(key, initial_value)

    def removeTopic(self, key):
        '''
        remove an existing topic key from all reviewers
        '''
        for item in self.inOrder():
            item.removeTopic(key)

    def setTopicValue(self, sort_name, topic, value):
        '''
        set the topic value on a reviewer identified by sort_name
        '''
        if value < 0 or value > 1.0:
            raise ValueError, 'value must be between 0 and 1: given=' + str(value)
        if sort_name not in self.reviewers:
            raise KeyError, 'Reviewer name not found: ' + str(sort_name)
        self.reviewers[sort_name].setTopic(topic, value)
