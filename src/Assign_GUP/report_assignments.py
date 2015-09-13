#!/usr/bin/env python

'''
show a read-only text page with assignments for each proposal

======   ==========   ============   ====================   ==============================
GUP#     reviewer 1   reviewer 2     excluded reviewer(s)   title
======   ==========   ============   ====================   ==============================
11111    A Reviewer   Ima Reviewer                          Study of stuff
======   ==========   ============   ====================   ==============================
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


from PyQt4 import QtGui
import plainTextEdit
import pyRestTable


class Report(plainTextEdit.TextWindow):
    
    def __init__(self, parent, agup, settings):
        self.settings = settings
        self.agup = agup
        self.title = 'Reviewer Assignments'
        text = self.makeText()

        plainTextEdit.TextWindow.__init__(self, parent, self.title, text, self.settings)
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.show()
    
    def makeText(self):
        '''
        generate the text of the panel
        '''
        tbl = pyRestTable.Table()
        tbl.labels = ['GUP#', 'reviewer 1', 'reviewer 2', 'excluded reviewer(s)', 'title']
        for prop in self.agup.proposals:
            prop_id = prop.getKey('proposal_id')
            prop_title = prop.getKey('proposal_title')
            r1, r2 = prop.getAssignedReviewers()
            excluded = prop.getExcludedReviewers(self.agup.reviewers)
            tbl.rows.append([prop_id, r1, r2, ', '.join(excluded), prop_title])
        return tbl.reST()
    
    def update(self):
        text = self.makeText()
        self.setText(text)