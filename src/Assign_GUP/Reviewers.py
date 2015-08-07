#!/usr/bin/env python

'''
Set of review panel members
'''

from lxml import etree
import os
import Reviewer


class Reviewers(object):
    '''
    The set of review panel members
    '''

    def __init__(self, filename = 'panel.xml'):
        '''
        Constructor
        '''
        self.db = {}
        self.topics = []
        self.keyField = 'full_name'
        self.sorted_reviewers_list = None
        self.xmlFile = filename
        #if filename != None:
        #    if not os.path.exists(filename):
        #        self.xmlfilename = filename

    def __str__(self):
        '''
        Canonical string representation
        '''
        liszt = []
        for key in self.reviewers():
            liszt.append( str(self.db[key]) )
        return "\n".join( liszt )

    def readXml(self):
        '''
        read the XML file
        '''
        self.topics = []
        doc = etree.parse(self.xmlFile)
        self.sort_dict = {}
        for reviewer in doc.findall('Reviewer'):
            member = Reviewer.Reviewer(reviewer, self.xmlFile)
            key = member.db[self.keyField]
            self.sort_dict[member.db['name']] = key
            self.db[key] = member
            # collect a list of all the topics
            for topic in member.db['topics'].keys():
                if topic not in self.topics:
                    self.topics.append( topic )
        # make sure each reviewer has a value assigned for each topic
        for key, member in self.db.items():
            for topic in self.topics:
                if topic not in member.db['topics']:
                    member.db['topics'][topic] = "0"

    def reviewers(self, sort = True):
        '''
        :return: list with names of review panel members
        '''
        if sort:
            if self.sorted_reviewers_list != None:
                # pull it from the cache
                liszt = self.sorted_reviewers_list
            else:
                liszt = []
                for key in sorted(self.sort_dict.keys()):
                    liszt.append( self.sort_dict[key] )
                self.sorted_reviewers_list = liszt
        else:
            liszt = self.db.keys()
        return liszt

def demo(xml_file_name = '2012-2-panel.xml'):
    '''
    print various items from a panel.xml file
    
    Example XML data::

        <Reviewer name="Pete">
            <full_name>Pete Jemian</full_name>
            <phone>630-252-3189</phone>
            <email>jemian@anl.gov</email>
            <notes>ANL, USAXS, ASAXS</notes>
            <joined>2005-2</joined>
            <topics  bio="0.1" chem="0.3" phys="0.7" mater="1.0" poly="0.9" GI="0.7" XPCS="0.8" USAXS="1.0" />
        </Reviewer>

    '''
    panel = Reviewers('')
    panel.readXml()
    # import pprint
    #pprint.pprint(panel.db)
    print panel.topics
    print panel.reviewers()
    print panel


if __name__ == '__main__':
    demo()
