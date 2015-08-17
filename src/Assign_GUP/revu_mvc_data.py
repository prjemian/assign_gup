
'''
Reviewers: underlying data class for the MVC model 
'''

from PyQt4 import QtCore
from lxml import etree
import os
import traceback
import history
import reviewer
import resources
import xml_utility


XML_SCHEMA_FILE = resources.resource_file('reviewers.xsd')
ROOT_TAG = 'Review_panel'
AGUP_XML_SCHEMA_FILE = resources.resource_file('agup_review_session.xsd')
AGUP_ROOT_TAG = 'AGUP_Review_Session'

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

    def exists(self, sort_name):
        '''given sort_name string, does reviewer exist?'''
        return sort_name in self.reviewer_sort_list
    
    def getProposal(self, sort_name):
        '''return reviewer selected by sort_name string'''
        if not self.exists(sort_name):
            raise IndexError, 'Reviewer not found: ' + sort_name
        return self.reviewers[sort_name]
    
    def getByFullName(self, full_name):
        '''return reviewer selected by full_name string'''
        sort_name = None
        for rvwr in self.inOrder():
            if rvwr.getFullName() == full_name:
                sort_name = rvwr.getKey('name')
                break
        if sort_name is None:
            raise IndexError, 'Reviewer not found: ' + full_name
        return self.reviewers[sort_name]

    def getByIndex(self, index):
        if index < 0 or index >= len(self.reviewer_sort_list):
            raise IndexError, 'Index not found: ' + str(index)
        return self.reviewer_sort_list[index]

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with reviewers
        '''
        doc = xml_utility.readValidXmlDoc(filename, 
                                          AGUP_ROOT_TAG, AGUP_XML_SCHEMA_FILE,
                                          alt_root_tag=ROOT_TAG, 
                                          alt_schema=XML_SCHEMA_FILE,
                                          )
        root = doc.getroot()
        if root.tag == AGUP_ROOT_TAG:
            reviewers_node = root.find(ROOT_TAG)    # pre-agup reviewers file
        else:
            reviewers_node = root

        db = {}
        self.reviewer_sort_list = []
        self.cycle = reviewers_node.get('period', None)
        for node in reviewers_node.findall('Reviewer'):
            sort_name = node.attrib['name'].strip()
            panelist = reviewer.AGUP_Reviewer_Data(node, filename)
            db[sort_name] = panelist
            self.reviewer_sort_list.append(sort_name)
        self.reviewers = db
    
    def writeXmlNode(self, specified_node):
        '''
        write Reviewers' data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        '''
        for rvwr in self.inOrder():
            rvwr.writeXmlNode(etree.SubElement(specified_node, 'Reviewer'))

    def inOrder(self):
        return sorted(self.reviewers.values())

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
