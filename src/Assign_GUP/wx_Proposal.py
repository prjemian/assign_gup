#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

'''
A single General User Proposal
'''

from lxml import etree
import os
import pprint
import StringIO
import ui
import datetime


class Proposal:
    '''
    A single General User Proposal
    '''
    tagList = (
       'proposal_id', 'proposal_type', 'proposal_title', 
       'review_period', 'spk_name', 'recent_req_period', 
       'first_choice_bl'
    )

    def __init__(self, xmlParentNode = None, xmlFile = None):
        '''
        In eligible_reviewers, 
        key is reviewer full_name, 
        value is review assignment: None, 1, or 2
        
        :param obj xmlParentNode: object in lxml structure
        :param str xmlFile: name of XML file with proposals
        '''
        self.db = { 'topics': {}, 'eligible_reviewers': {} }
        self.xmlFile = xmlFile
        self.analysisFile = 'analysis.xml'
        for key in self.tagList:
            self.db[key] = None
        if xmlParentNode != None:
            self.readProposalNode( xmlParentNode )

    def __str__(self):
        '''
        Canonical string representation
        '''
        if self.getId() is None:
            return str(None)
        r1, r2 = self.getReviewers()
        prop_id = self.getIdAsStr()
        title = self.getTitle()
        return "%s: (%s, %s): %s" % (prop_id, str(r1), str(r2), title)

    def getId(self):
        '''returns the proposal number (or None)'''
        return self.getIdAsStr()

    def getIdAsStr(self):
        '''returns the proposal number (or None) as a string'''
        return str(self.db['proposal_id'])

    def getTitle(self):
        '''returns the proposal title'''
        v = self.db['proposal_title']
        return str(v)

    def getReviewers(self):
        '''
        Identify the reviewers assigned to this proposal
        
        :return: tuple of reviewers (primary, secondary), None if unassigned
        '''
        primary, secondary = (None, None)
        for k, v in self.db['eligible_reviewers'].items():
            if v == "1": primary = k
            if v == "2": secondary = k
        return primary, secondary

    def getExcludedReviewers(self, panelists):
        '''
        Identify the reviewers excluded from reviewing this proposal
        
        :return: list of reviewers
        '''
        excluded = []
        possibles = self.db['eligible_reviewers'].keys()
        for reviewer in panelists:
            if reviewer not in possibles:
                excluded.append( reviewer )
        return excluded

    def getXmlText(self, parent, tag):
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

    def readProposalNode(self, proposal = None):
        '''
        Fill the class variables with values from the XML node
        
        :param proposal: lxml node of the Proposal
        '''
        for key in self.tagList:
            self.db[key] = self.getXmlText(proposal, key)
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

    def SetTopics(self, topics = {}):
        '''
        Fill the class variables with values from the XML node
        
        :param proposal: lxml node of the Proposal
        '''
        self.db['topics'].update(topics)

    def SetAnalysisFile(self, xmlFile = 'analysis.xml'):
        '''
        :param xmlFile: analysis file
        '''
        self.analysisFile = xmlFile

    def TellUI(self):
        '''
        Tell an editor about our internal data so that a UI may be 
        constructed for editing an instance of this object.
        Make a list of the items to show.
        Each item in the list will be a dictionary with at least a
        'type' key that describes what kind of item is to be presented.
        A 'set' key is used to identify values for the list of "topics".
        The items will display in the GUI in the order of definition below.
        
        :return: list for use in GUI setup routine
        '''
        liszt = []
        for key in self.tagList:
            if key in ('proposal_type', 'recent_req_period'):
                continue
            dct = { }
            if key in ('proposal_title'):
                dct['type'] = ui.LABEL_ENTRY_MULTILINE
            else:
                dct['type'] = ui.LABEL_ENTRY
            dct['set'] = 'main'
            dct['key'] = key
            dct['label'] = key
            dct['editable'] = False
            dct['entry'] = self.db[key]
            liszt.append( dct )
        for key in sorted(self.db['eligible_reviewers'].keys()):
            if len(key.strip()) == 0:
                pprint.pprint (self.db['eligible_reviewers'])
                raise Exception, "key should not be blank: GUP-%s" % self.getId()
            # expect the entry of each reviewer is in [None, 1, 2]
            dct = { }
            # TODO this would be better with radio buttons
            dct['type'] = ui.LABEL_ENTRY
            dct['set'] = 'eligible'
            dct['key'] = key
            dct['label'] = key
            dct['editable'] = True
            dct['entry'] = self.db['eligible_reviewers'][key]
            liszt.append( dct )
        for key in sorted(self.db['topics'].keys()):
            dct = { }
            dct['type'] = ui.LABEL_ENTRY
            dct['set'] = 'topic'
            dct['key'] = key
            dct['label'] = key
            dct['editable'] = True
            dct['entry'] = self.db['topics'][key]
            liszt.append( dct )
        dct = { }
        dct['type'] = ui.LABEL_ENTRY
        dct['set'] = 'main'
        dct['key'] = 'subjects'
        dct['label'] = 'subjects'
        dct['editable'] = False
        dct['entry'] = self.db['subjects']
        liszt.append( dct )
        return liszt

    def SaveUI(self, revisions):
        '''
        A UI has told us to save a revised version of our data.
        
        :param revisions: list with revised values, using list from TellUI() method
        '''
        xref = {
            'main': self.db, 
            'eligible': self.db['eligible_reviewers'], 
            'topic': self.db['topics']
        }
        for dct in revisions:
            if 'editable' in dct and dct['editable']:
                key = dct['key']
                entry = dct['entry']
                base = xref[ dct['set'] ]
                base[key] = str(entry)
        self.UpdateXmlFile()

    def UpdateXmlFile(self):
        '''
        Write the in-memory data back to the XML file.
        Use XPATH and lxml to edit the XML file in place.
        '''
        if not os.path.exists(self.analysisFile):
            # make the file
            doc = etree.parse( StringIO.StringIO("<analysis />") )
        else:
            doc = etree.parse(self.analysisFile)
        root = doc.getroot()
        root.attrib['time'] = str(datetime.datetime.now())

        node1 = self.OpenChildnode(root, "Proposals")
        xpathStr = "Proposal[@id='%s']" % self.getId()
        nodeList = node1.xpath(xpathStr)
        if len(nodeList) == 1:
            prop_node = nodeList[0]
        elif len(nodeList) > 1:
            msg = "Found multiple node %s in file %s" % (xpathStr, self.analysisFile)
            raise Exception, msg
        else:
            prop_node = etree.SubElement(node1, "Proposal")
            prop_node.attrib['id'] = self.getId()

        topics_node = self.OpenChildnode(prop_node, "Topics")
        for k, v in self.db['topics'].items():
            if v is None or v.strip() == "": v = "0.0"
            topics_node.attrib[k] = str(v)

        revList = self.getReviewers()
        rev_node = self.OpenChildnode(prop_node, "Reviewers")
        for i, v in enumerate(revList):
            label = "reviewer%d" % (i+1)
            rev_node.attrib[label] = v or ''

        #doc.write(self.analysisFile, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        # pretty-print is not working, let's line-break for each element node        
        s = etree.tostring(doc, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        s = s.replace('><', '>\n<')
        with open(self.analysisFile, 'w') as fp:
            fp.write(s)

        ui.log("updated (%s) in file: %s" % (str(self), self.xmlFile) )

    def OpenChildnode(self, parent, tag):
        '''
        Open a child node in an XML document.  
        Create it if it does not exist.
        
        :param parent: parent of the node to be found
        :param tag: tag name of the node
        '''
        node = parent.find(tag)
        if node is None:
            node = etree.SubElement(parent, tag)
        return node


if __name__ == '__main__':
    # these two must be coordinated
    test_file = '2011-3-proposals.xml'
    test_gup_id = '25555'
    
    xmlFile = test_file
    doc = etree.parse(xmlFile)
    node = doc.find('Proposal')
    node = doc.xpath('Proposal[proposal_id="%s"]' % test_gup_id)
    node = node[0]
    print str(node)
    proposal = Proposal(node, xmlFile)
    print str(proposal)
    tel = proposal.TellUI()
    pprint.pprint(tel)
    proposal.SaveUI(tel)
    #proposal.UpdateXmlFile()
