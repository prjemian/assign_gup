
'''
MVC for proposals - test version

:see: http://www.saltycrane.com/blog/2008/01/pyqt-43-simple-qabstractlistmodel/
:see: http://www.saltycrane.com/blog/2007/12/pyqt-43-qtableview-qabstracttablemodel/
'''

from lxml import etree
import os, sys
from PyQt4 import QtGui, QtCore
import history
import ProposalDetails
import resources

UI_FILE = 'proposals_listview.ui'
PROPOSALS_TEST_FILE = os.path.join('project', '2015-2', 'proposals.xml')

# TODO: split each class into its own file

class AGUP_Proposals_View(QtGui.QWidget):
    '''
    Manage the list of proposals, including assignments of topic weights and reviewers
    '''
    
    def __init__(self, parent=None, proposals=None):
        self.parent = parent
        QtGui.QWidget.__init__(self)
        resources.loadUi(UI_FILE, self)

        self.details_panel = ProposalDetails.AGUP_ProposalDetails(self)
        layout = self.details_gb.layout()
        layout.addWidget(self.details_panel)

        if proposals is None:       # developer use
            proposals = AGUP_Proposals_List()
            proposals.importXml(PROPOSALS_TEST_FILE)
        self.proposals = proposals

        self.proposals_model = AGUP_Proposals_Model(self.proposals)
        self.listView.setModel(self.proposals_model)

        # select the first item in the list
        pt = QtCore.QPoint(0,0)
        idx = self.listView.indexAt(pt)
        self.listView.setCurrentIndex(idx)
        self.prior_selection = idx
        self.selectProposalByIndex(idx)
        self.listView.clicked.connect(self.on_item_clicked)
        self.listView.entered.connect(self.on_item_clicked)
        self.listView.installEventFilter(self)      # for keyboard events

    def eventFilter(self, listView, event):
        NAVIGATOR_KEYS = (QtCore.Qt.Key_Down, QtCore.Qt.Key_Up)
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in NAVIGATOR_KEYS:
                listView.keyPressEvent(event)
                index = listView.currentIndex()
                self.selectProposalByIndex(index)
                return True
        return False

    def on_item_clicked(self, index):
        '''
        called when changing the selected Proposal in the list
        '''
        if index == self.prior_selection:
            return False
        # TODO: check the "modified" flag here before proceeding
        self.prior_selection = index
        self.selectProposalByIndex(index)

    def selectProposal(self, prop_id):
        '''
        select Proposal for editing as referenced by ID number
        '''
        proposal = self.proposals.proposals[str(prop_id)]
        self.details_panel.setAll(
                                  proposal.db['proposal_id'], 
                                  proposal.db['proposal_title'], 
                                  proposal.db['review_period'], 
                                  proposal.db['spk_name'], 
                                  proposal.db['first_choice_bl'], 
                                  proposal.db['subjects'],
                                  )
        history.addLog('selected proposal: ' + str(prop_id))

    def selectProposalByIndex(self, index):
        '''
        select Proposal for editing as referenced by QListView index
        '''
        prop_id = str(index.data().toPyObject())
        self.selectProposal(prop_id)


class AGUP_Proposals_Model(QtCore.QAbstractListModel):
    '''
    MVC model for Proposals
    
    This is an adapter for the actual proposals data object: proposal_dict
    '''
    
    def __init__(self, proposals=[], headerdata=None, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.proposals = proposals

    def columnCount(self, parent):
        #return len(self.headerdata)     # table
        return 1        # list

    def rowCount(self, parent):
        return len(self.proposals)

    def data(self, index, role):
        if not index.isValid():
            return None
            # For the foreground role you will need to edit this to suit your data
        row = index.row()
        if role == QtCore.Qt.ForegroundRole:
            item = self.proposals.getByIndex(row)
        elif role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return self.proposals.getByIndex(row)

    # Use this only if you want the items in the table to be editable
    #   def setData(self, index, value, color):
    #       self.proposals.getByIndex(row) = value
    #       self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &, ''const QModelIndex &)'), index, index)
    #       return True

    #   def flags(self, index):
    #       return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable


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
        for proposal in self.proposals.values():
            yield proposal

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
            prop_id = getXmlText(node, 'proposal_id')
            prop = AGUP_Proposal_Data()
            prop.importXml(node)
            db[prop_id] = prop
            # db[prop_id] = node
            self.prop_id_list.append(prop_id)
        self.proposals = db

    def inOrder(self):
        return sorted(self.proposals.values())


class AGUP_Proposal_Data(object):
    '''
    A single General User Proposal
    '''
    tagList = (
       'proposal_id', 'proposal_type', 'proposal_title', 
       'review_period', 'spk_name', 'recent_req_period', 
       'first_choice_bl'
    )
    
    def __init__(self):
        self.db = dict(topics={}, eligible_reviewers={})

    def importXml(self, proposal):
        '''
        Fill the class variables with values from the XML node
        
        :param proposal: lxml node of the Proposal
        '''
        for key in self.tagList:
            self.db[key] = getXmlText(proposal, key)
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
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = AGUP_Proposals_View()
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
