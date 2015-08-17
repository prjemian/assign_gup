
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
AGUP_XML_SCHEMA_FILE = resources.resource_file('agup_review_session.xsd')
AGUP_ROOT_TAG = 'AGUP_Review_Session'

class AGUP_Proposals_List(QtCore.QObject):
    '''
    the list of all proposals
    '''
    
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.proposals = {}
        self.prop_id_list = []
    
    def __len__(self):
        return len(self.proposals)

    def __iter__(self):
        for prop in self.proposals.values():
            yield prop

    def exists(self, prop_id):
        '''given ID string, does proposal exist?'''
        return prop_id in self.prop_id_list
    
    def getProposal(self, prop_id):
        '''return proposal selected by ID string'''
        if not self.exists(prop_id):
            raise IndexError, 'Proposal not found: ' + prop_id
        return self.proposals[prop_id]

    def getByIndex(self, index):
        '''
        given index in sorted list of proposals, return indexed proposal
        
        note:  index is *not* the proposal ID number
        '''
        if index < 0 or index >= len(self.prop_id_list):
            raise IndexError, 'Index not found: ' + str(index)
        return self.prop_id_list[index]

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with proposals
        '''
        doc = xml_utility.readValidXmlDoc(filename, 
                                          AGUP_ROOT_TAG, AGUP_XML_SCHEMA_FILE,
                                          alt_root_tag=ROOT_TAG, 
                                          alt_schema=XML_SCHEMA_FILE,
                                          )
        root = doc.getroot()
        if root.tag == AGUP_ROOT_TAG:
            proposals_node = root.find(ROOT_TAG)    # pre-agup reviewers file
        else:
            proposals_node = root

        db = {}
        self.prop_id_list = []
        self.cycle = root.get('cycle', None) or root.get('period', None)
        for node in proposals_node.findall('Proposal'):
            prop_id = xml_utility.getXmlText(node, 'proposal_id')
            prop = proposal.AGUP_Proposal_Data(node, filename)
            db[prop_id] = prop
            self.prop_id_list.append(prop_id)
        self.proposals = db
    
    def writeXmlNode(self, specified_node):
        '''
        write Proposals' data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        '''
        for prop in self.inOrder():
            prop.writeXmlNode(etree.SubElement(specified_node, 'Proposal'))

    def inOrder(self):
        return sorted(self.proposals.values())

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
