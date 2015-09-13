#!/usr/bin/env python

'''
edit the template to send emails, include editor for keyword substitutions
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


from PyQt4 import QtGui
import email_template
import history
import resources
import signals


UI_FILE = 'editor_email_template.ui'
DISABLED_STYLE = 'background: #eee'
# TODO: add controls to add or remove keywords in self.agup.email.keyword_dict


class Editor(QtGui.QWidget):
    
    def __init__(self, parent, agup, settings=None):
        self.parent = parent
        self.agup = agup
        self.settings = settings
        self.keyword_dict = self.agup.email.keyword_dict
        self.current_key = None
        self.signals = signals.CustomSignals()

        QtGui.QWidget.__init__(self, parent)
        resources.loadUi(UI_FILE, self)
        self.restoreWindowGeometry()
        self.restoreSplitterDetails()

        self.listWidget.addItems(sorted(self.keyword_dict.keys()))
        self.listWidget.addItems(sorted(email_template.REVIEWER_FIELDS.keys()))
        self.template.setPlainText(self.agup.email.email_template)

        self.listWidget.currentItemChanged.connect(self.doCurrentItemChanged)
        self.template.textChanged.connect(self.doTemplateTextChanged)
        self.plainTextEdit.textChanged.connect(self.doKeywordTextChanged)
        self.plainTextEdit.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.disabled_style = DISABLED_STYLE
        self.enabled_style = self.plainTextEdit.styleSheet()
        
        self.doMerge()
        self.show()

    def doCurrentItemChanged(self, widget_item):
        self.current_key = key = str(widget_item.text())
        if key in self.keyword_dict.keys():
            value = self.keyword_dict[key]
        else:
            value = email_template.REVIEWER_FIELDS[key]
        self.plainTextEdit.setPlainText(value)
        # check if keyword is to be filled in from reviewer (or proposal) data
        if key in email_template.REVIEWER_FIELDS.keys():
            self.plainTextEdit.setReadOnly(True)
            self.plainTextEdit.setStyleSheet(self.disabled_style)
            self.plainTextEdit.setToolTip('this value is set for each reviewer')
        else:
            self.plainTextEdit.setReadOnly(False)
            self.plainTextEdit.setStyleSheet(self.enabled_style)
            self.plainTextEdit.setToolTip('you may edit this value')
    
    def doKeywordTextChanged(self, *args, **kw):
        if self.current_key is not None and self.current_key in self.keyword_dict.keys():
            s = str(self.plainTextEdit.toPlainText())
            if s != self.keyword_dict[self.current_key]:
                self.keyword_dict[self.current_key] = s
                self.signals.changed.emit()
                self.doMerge()
    
    def doTemplateTextChanged(self, *args, **kw):
        s = str(self.template.toPlainText())
        if s != self.agup.email.email_template:
            self.agup.email.email_template = s
            self.signals.changed.emit()
            self.doMerge()
    
    def doMerge(self):
        text = self.agup.email.mail_merge(**email_template.REVIEWER_FIELDS)
        self.mail_merge.setPlainText(text)

    def saveWindowGeometry(self):
        '''
        remember where the window was
        '''
        if self.settings is not None:
            self.settings.saveWindowGeometry(self, 'TemplateEditor_geometry')

    def restoreWindowGeometry(self):
        '''
        put the window back where it was
        '''
        if self.settings is not None:
            self.settings.restoreWindowGeometry(self, 'TemplateEditor_geometry')

    def saveSplitterDetails(self):
        '''
        ember where the splitters were
        '''
        def handler(group, splitter):
            sizes = map(int, splitter.sizes())
            self.settings.setKey(group + '/widths', ' '.join(map(str, sizes)))

        if self.settings is not None:
            handler('TemplateEditor_v_splitter', self.v_splitter)
            handler('TemplateEditor_h_splitter', self.h_splitter)
            handler('TemplateEditor_splitter3', self.splitter3)

    def restoreSplitterDetails(self):
        '''
        put the splitters back where they were
        '''
        def handler(group, splitter):
            sizes = self.settings.getKey(group + '/widths')
            if sizes is not None:
                splitter.setSizes(map(int, str(sizes).split()))

        if self.settings is not None:
            handler('TemplateEditor_v_splitter', self.v_splitter)
            handler('TemplateEditor_h_splitter', self.h_splitter)
            handler('TemplateEditor_splitter3', self.splitter3)

    def closeEvent(self, event):
        self.saveWindowGeometry()
        self.saveSplitterDetails()
        event.accept()
        self.close()
    

if __name__ == '__main__':
    import os
    import sys
    import pprint
    import agup_data

    agup = agup_data.AGUP_Data()
    agup.openPrpFile('project/agup_project.xml')

    app = QtGui.QApplication(sys.argv)
    mw = Editor(None, agup)
    _r = app.exec_()
    pprint.pprint(agup.email.keyword_dict)
    pprint.pprint(agup.email.email_template)
    sys.exit(_r)