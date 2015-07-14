#!/usr/bin/env python

'''
Reviewer is a member of the General User Proposal review panel
'''

from lxml import etree
import ui


class Reviewer:
    '''
    A Reviewer is a member of the General User Proposal review panel for at least one cycle.
    '''
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

    def getXmlText(self, parent, tag):
        '''
        Read the text content of an XML node
        
        :param reviewer: lxml node node of the Reviewer
        :return: node text or None
        '''
        node = parent.find(tag)
        if node == None:
            return None
        return etree.tostring(node, method="text").strip()

    def readReviewerNode(self, reviewer = None):
        '''
        Fill the class variables with values from the XML node
        
        :param reviewer: lxml node node of the Reviewer
        '''
        self.db['name'] = reviewer.attrib['name'].strip()
        for k in self.tagList:
            self.db[k] = self.getXmlText(reviewer, k)
        self.db['topics'] = {}
        node = reviewer.find('topics')
        for k, v in node.attrib.items():
            self.db['topics'][k] = v

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
        # note: full_name is used as an index key by Panel, it should not be editable
        liszt.append( {'type': ui.LABEL_ENTRY, 'set': 'main', 'key': 'full_name', 'editable': False, 'label': 'full name', 'entry': self.db['full_name']} )
        liszt.append( {'type': ui.LABEL_ENTRY, 'set': 'main', 'key': 'name', 'label': 'sort name', 'entry': self.db['name']} )
        liszt.append( {'type': ui.LABEL_ENTRY, 'set': 'main', 'key': 'phone', 'label': 'phone', 'entry': self.db['phone']} )
        liszt.append( {'type': ui.LABEL_ENTRY, 'set': 'main', 'key': 'email', 'label': 'email', 'entry': self.db['email']} )
        liszt.append( {'type': ui.LABEL_ENTRY, 'set': 'main', 'key': 'joined', 'label': 'joined', 'entry': self.db['joined']} )
        liszt.append( {'type': ui.LABEL_ENTRY, 'set': 'main', 'key': 'URL', 'label': 'URL', 'entry': self.db['URL']} )
        # note: the 'notes' field is multiline
        liszt.append( {'type': ui.LABEL_ENTRY_MULTILINE, 'set': 'main', 'key': 'notes', 'label': 'notes', 'entry': self.db['notes']} )
        for key in sorted(self.db['topics'].keys()):
            value = self.db['topics'][key]
            if value == None:  value = ""
            liszt.append( {'type': ui.LABEL_ENTRY, 'set': 'topics', 'key': key, 'label': key, 'entry': str(value)} )
        return liszt

    def SaveUI(self, revisions):
        '''
        A UI has told us to save a revised version of our data.
        
        :param revisions: list with revised values, using list from TellUI() method
        '''
        # revise the in-memory data
        self.db = { 'topics': {} }
        for dct in revisions:
            if dct['set'] == 'main':
                self.db[dct['key']] = dct['entry']
            elif dct['set'] == 'topics':
                self.db['topics'][dct['key']] = dct['entry']
        self.UpdateXmlFile()

    def UpdateXmlFile(self):
        '''
        Write the in-memory data back to the XML file.
        Use XPATH and lxml to edit the XML file in place.
        '''
        doc = etree.parse(self.xmlFile)
        xpathStr = "/Review_panel/Reviewer[@name='%s']" % self.db['name']
        nodeList = doc.xpath(xpathStr)
        if len(nodeList) != 1:
            msg = "Found %d nodes matching XPATH %s in file %s" % (len(nodeList), xpathStr, self.xmlFile)
            raise Exception, msg
        reviewer_node = nodeList[0]
        for key in ('phone', 'email', 'notes', 'joined', 'URL'):
            nodeList = reviewer_node.xpath(key)
            if len(nodeList) == 1:
                node = nodeList[0]
            elif len(nodeList) > 1:
                msg = "Found %d nodes matching XPATH %s in file %s" % (len(nodeList), key, self.xmlFile)
                raise Exception, msg
            else:
                node = etree.SubElement(reviewer_node, key)
            node.text = self.db[key]
        node = reviewer_node.xpath('topics')[0]
        for k, v in self.db['topics'].items():
            if v == None: v = "0.0"
            node.attrib[k] = str(v)
        doc.write(self.xmlFile, pretty_print=True, xml_declaration=True, encoding="UTF-8")
        ui.log("updated (%s) in file: %s" % (str(self), self.xmlFile) )


if __name__ == '__main__':
    xmlFile = '2012-2-panel.xml'
    doc = etree.parse(xmlFile)
    reviewerNode = doc.find('Reviewer')
    print str(reviewerNode)
    reviewer = Reviewer(reviewerNode, xmlFile)
    print str(reviewer)
    #import pprint
    #pprint.pprint(reviewer.TellUI())
    tel = reviewer.TellUI()
    tel[2]['entry'] = '(847)204-2690'
    tel[2]['entry'] = '(630)252-3189'
    tel[2]['entry'] = '630-252-3189'
    reviewer.SaveUI(tel)
