
'''
Proposals: underlying data class for the MVC model 
'''

from lxml import etree
import os
import proposal
import xml_utility


class AGUP_Proposals_List(object):
    '''
    the list of all proposals (is this needed?)
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
        doc = etree.parse(filename)
        root = doc.getroot()
        self.cycle = root.attrib['period']
        db = {}
        self.prop_id_list = []
        for node in doc.findall('Proposal'):
            prop_id = xml_utility.getXmlText(node, 'proposal_id')
            prop = proposal.AGUP_Proposal_Data()
            prop.importXml(node)
            db[prop_id] = prop
            # db[prop_id] = node
            self.prop_id_list.append(prop_id)
        self.proposals = db

    def inOrder(self):
        return sorted(self.proposals.values())
