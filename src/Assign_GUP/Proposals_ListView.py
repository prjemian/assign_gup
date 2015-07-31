
'''
MVC for proposals - test version
'''

import os, sys
from PyQt4 import QtGui, QtCore
import qt_form_support
from lxml import etree
import ProposalDetails

PROPOSALS_UI_FILE = 'proposals_listview.ui'
PROPOSAL_DETAILS_UI_FILE = 'proposal_details.ui'
PROPOSALS_TEST_FILE = 'project/2015-2/proposals.xml'

def xmlToString(obj):
    s = etree.tostring(obj, 
                       pretty_print=True, 
                       xml_declaration=True, 
                       encoding="UTF-8")
    return s


class ProposalsView(object):
    '''
    QtGui widget to view and assign all proposals
    '''

    def __init__(self, xml_proposal_file):
        '''
        '''
        self.ui = qt_form_support.load_form(PROPOSALS_UI_FILE)
        self.details_panel = qt_form_support.load_form(PROPOSAL_DETAILS_UI_FILE)
        layout = self.ui.details_gb.layout()
        layout.addWidget(self.details_panel)
        self.model = None

        self.proposals = Proposals__Container(xml_proposal_file)
        self.proposals.load()
        self.populateList()
        
        self.ui.listWidget.currentItemChanged.connect(self.on_item_changed)
            
    def listItemChanged(self, *args, **kws):
        print args, kws

    def on_item_changed(self, curr, prev):
        text = curr.text()
        proposal = self.proposals.proposal(str(text))
        # TODO: let AGUP_ProposalDetails do this work
        # self.details = ProposalDetails.AGUP_ProposalDetails(self, )
        self.details_panel.proposal_id.setText(text)
        self.details_panel.proposal_title.setPlainText(getXmlText(proposal, 'proposal_title'))
        self.details_panel.review_period.setText(getXmlText(proposal, 'review_period'))
        self.details_panel.spk_name.setText(getXmlText(proposal, 'spk_name'))
        self.details_panel.first_choice_bl.setText(getXmlText(proposal, 'first_choice_bl'))
        # TODO: subjects has element content
        # self.details_panel.subjects.setText(getXmlText(proposal, 'subjects'))
    
    def populateList(self, selectedProposal=None):
        selected = None
        self.ui.listWidget.clear()
        for proposal in self.proposals.inOrder():
            key = getXmlText(proposal, 'proposal_id')
            item = QtGui.QListWidgetItem(key)
            self.ui.listWidget.addItem(item)
            if selectedProposal is not None and selectedProposal == id(proposal):
                selected = item
        if selected is not None:
            selected.setSelected(True)
            self.ui.listWidget.setCurrentItem(selected)
    
    def show(self):
        self.ui.show()


class Proposals__Container(object):
    
    def __init__(self, xml_proposal_filename):
        self.filename = xml_proposal_filename
        self.dirty = False
        self.proposals = {}

    def proposal(self, gup_number):
        return self.proposals.get(gup_number)

    # def addProposal(self, proposal):
    #     self.proposals[id(proposal)] = proposal
    #     self.dirty = True

    # def removeProposal(self, proposal):
    #     del self.proposals[id(proposal)]
    #     del proposal
    #     self.dirty = True

    def __len__(self):
        return len(self.proposals)

    def __iter__(self):
        for proposal in self.proposals.values():
            yield proposal

    def inOrder(self):
        return sorted(self.proposals.values())

    def load(self):
        doc = etree.parse(self.filename)
        root = doc.getroot()
        self.cycle = root.attrib['period']
        db = {}
        for node in doc.findall('Proposal'):
            prop_id = getXmlText(node, 'proposal_id')
            db[prop_id] = Proposal__Data(node)
            # db[prop_id] = node
        self.proposals = db


class Proposal__Data(object):
    
    def __init__(self, xmlNode):
        self.xmlNode = xmlNode
        self.proposal_id = getXmlText(xmlNode, 'proposal_id')
        # TODO: make this compatible with ProposalDetails
    
    def __cmp__(self, other):
        return QtCore.QString.localeAwareCompare(self.proposal_id.lower(), 
                                                 other.proposal_id.lower())
    
    def find(self, tag):
        return self.xmlNode.find(tag)
    
    def toString(self):
        return xmlToString(self.xmlNode)


def getXmlText(parent, tag):
    '''
    Read the text content of an XML node
    
    :param reviewer: lxml node node of the Reviewer
    :return: node text or None
    '''
    node = parent.find(tag)
    if node is None:
        return None
    if node.text is None:
        return None
    text = node.text.strip()
    return text


def main():
    '''simple starter program to develop this code'''
    app = QtGui.QApplication(sys.argv)
    main_window = ProposalsView()
    main_window.ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
