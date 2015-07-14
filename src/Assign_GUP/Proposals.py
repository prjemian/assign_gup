#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

'''
Maintain the list of beam time proposals.
'''

from lxml import etree
import os
import Proposal
import ui
import sys
import config
from pyRestTable import rest_table
import Reviewers

class Proposals:
    '''
    Maintain the list of beam time proposals.
    Treat the input file here as read-only.
    Do not store any assignments or analysis to this file.
    That way, it can be updated from the APS server without
    removing additions.
    '''

    def __init__(self, proposalsFile = None, analysisFile = None):
        '''
        :param str proposalsFile: name of XML file with proposals
        '''
        self.db = {}
        self.keyField = 'proposal_id'
        self.xmlFile = 'proposals.xml'
        self.analysisFile = 'analysis.xml'
        self.topics = {}
        self.sorted_proposals_list = None
        if proposalsFile != None:
            if os.path.exists(proposalsFile):
                self.xmlFile = proposalsFile
        if analysisFile != None:
            if os.path.exists(analysisFile):
                self.analysisFile = analysisFile

    def __str__(self):
        '''
        Canonical string representation
        '''
        who = Reviewers.Reviewers(config.build_filename('panel', 'xml'))
        who.readXml()
        panel = who.reviewers(sort=False)
        table = rest_table.Table()
        table.labels = ('GUP#', 'reviewer 1', 'reviewer 2', 'excluded reviewer(s)', 'title')
        for gup_number in self.proposals():
            if gup_number in self.db:
                gup = self.db[gup_number]
                r1, r2 = gup.getReviewers()
                excluded = gup.getExcludedReviewers(panel)
                prop_id = gup.getIdAsStr()
                title = gup.getTitle()
                table.rows.append( [prop_id, str(r1), str(r2), ', '.join(excluded), title] )
        return table.reST(fmt='simple')

    def readXml(self):
        '''
        read the XML file with the beam time proposals
        '''
        doc = etree.parse(self.xmlFile)
        root = doc.getroot()
        self.cycle = root.attrib['period']
        for prop_node in doc.findall('Proposal'):
            try:
                proposal = Proposal.Proposal(prop_node)
            except:
                import traceback
                print "Problem with ", prop_node
                print traceback.format_exc()
                #print sys.exc_info()
            proposal.SetTopics(self.topics)
            proposal.SetAnalysisFile(self.analysisFile)
            prop_id = proposal.db['proposal_id']
            self.db[prop_id] = proposal

        if not os.path.exists(self.analysisFile):
            ui.log("created analysis file: %s" % self.analysisFile)
            for prop_id in sorted(self.db):
                self.db[prop_id].UpdateXmlFile()
                ui.log("added proposal ID=%s to analysis file" % str(prop_id))
        doc = etree.parse(self.analysisFile)
        for prop_node in doc.xpath('/analysis/Proposals/Proposal'):
            prop_id = prop_node.attrib['id']
            prop = self.db[prop_id]
            topics_node = prop_node.find('Topics')
            if topics_node is not None:
                for k, v in topics_node.attrib.items():
                    prop.db['topics'][k] = v
            rev_node = prop_node.find('Reviewers')
            if rev_node is not None:
                for i in (1, 2):
                    key = 'reviewer%d' % i
                    if key in rev_node.attrib:
                        v = rev_node.attrib[key]
                        if len(v.strip()) > 0:
                            if v in prop.db['eligible_reviewers']:
                                prop.db['eligible_reviewers'][v] = str(i)
                            else:
                                msg = "problem with GUP-%s, ./Reviewers/@%s" % (prop_id, key)
                                raise Exception, msg
                        

    def proposals(self, sort = True):
        '''
        :return: list with proposal IDs
        '''
        if sort:
            if self.sorted_proposals_list != None:
                # pull it from the cache
                liszt = self.sorted_proposals_list
            else:
                liszt = sorted(self.db.keys())
                self.sorted_proposals_list = liszt
        else:
            liszt = self.db.keys()
        return liszt

    def SetTopics(self, topics = []):
        '''
        The topics are a list of categories used to assign 
        reviewers to proposal topics with which they are most 
        experienced.  Each topic will be assigned a value
        from 0.0 to 1.0 (empty or None is 0.0) indicating the
        amount that topic is represented in the proposal.
        This will be matched (dot product) with topics values 
        for each reviewer to identify the most experienced reviewers.
        
        :param topics: list of topics
        '''
        # convert the input list to a dictionary
        self.topics = {}
        for key in topics:
            self.topics[key] = None

    def SetAnalysisFile(self, xmlFile = 'analysis.xml'):
        '''
        The information from assignments or analyses is stored in 
        a separate file from the proposals.
        This allows the proposals file to be reloaded from
        the APS server without losing the additional information
        from assignments or analyses.
        This is passed to each Proposal object to allow
        for updating.
        
        :param xmlFile: analysis file
        '''
        self.analysisFile = xmlFile


if __name__ == '__main__':
    proposals_file = config.build_filename('proposals', 'xml')
    analysis_file = config.build_filename('analysis', 'xml')
    proposals = Proposals(proposals_file)
    proposals.SetAnalysisFile(analysis_file)
    proposals.readXml()
    #import pprint
    #pprint.pprint(proposals.db)
    print proposals
    print proposals.proposals()
    print proposals.cycle
