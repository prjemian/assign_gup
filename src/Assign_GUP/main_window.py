#!/usr/bin/env python

'''
:mod:`Main` code runs the GUI.
'''

import os, sys
from PyQt4 import QtCore, QtGui, uic
import about
import history
import prop_mvc_data
import prop_mvc_view
import resources
import settings
import topics

UI_FILE = 'main_window.ui'
RC_FILE = '.assign_gup.rc'
RC_SECTION = 'Assign_GUP'


class AGUP_MainWindow(QtGui.QMainWindow):
    '''
    Creates a Qt GUI for the main window
    '''

    def __init__(self):
        self.settings = settings.ApplicationSettings(RC_FILE, RC_SECTION)
        # TODO: support self.settings.modified flag

        QtGui.QMainWindow.__init__(self)
        resources.loadUi(UI_FILE, baseinstance=self)
        self.proposal_view = None
        self.reviewer_view = None
        self.modified = False
        self.topics = topics.Topics()

        self.history_logger = history.Logger(log_file=None, 
                                             level=history.NO_LOGGING, 
                                             statusbar=self.statusbar, 
                                             history_widget=self.history)
        history.addMessageToHistory = self.history_logger.add

        # TODO: need handlers for widgets and config settings

        history.addLog('loaded "' + UI_FILE + '"')

        # assign values to each of the display widgets in the main window

        self.settings_box.setTitle('settings from ' + self.settings.source)
        self.setPrpPathText(self.settings.getByKey('prp_path'))
        self.setRcFileText(self.settings.getByKey('rcfile'))
        self.setReviewCycleText(self.settings.getByKey('review_cycle'))
        self.setReviewersFileText(self.settings.getByKey('reviewers_file'))
        self.setProposalsFileText(self.settings.getByKey('proposals_file'))
        self.setAnalysesFileText(self.settings.getByKey('analyses_file'))
 
        for key in sorted(self.settings.getKeys()):
            history.addLog('Configuration option: %s = %s' % (key, self.settings.getByKey(key)))
 
        self.actionNew_PRP_Folder.triggered.connect(self.doNewPrpFolder)
        self.actionOpen_Folder.triggered.connect(self.doOpenPrpFolder)
        self.actionImport_proposals.triggered.connect(self.doImportProposals)
        self.actionSave.triggered.connect(self.doSave)
        self.actionSaveAs.triggered.connect(self.doSaveAs)
        self.actionSave_settings.triggered.connect(self.doSaveSettings)
        self.actionReset_Defaults.triggered.connect(self.doResetDefaults)
        self.actionExit.triggered.connect(self.doClose)
        self.actionAbout.triggered.connect(self.doAbout)

    def doAbout(self, *args, **kw):
        history.addLog('About... box requested')
        ui = about.AboutBox(self)
        ui.show()

    def doClose(self, *args, **kw):
        history.addLog('application exit requested')
        # TODO: refactor this to Qt
        #if self.modified or self.settings.modified:
        #    # confirm this step
        #    result = self.RequestConfirmation('Exit (Quit)',
        #          'There are unsaved changes.  Exit (Quit) anyway?')
        #    if result != wx.ID_YES:
        #        return
        self.close()
    
    def doOpenPrpFolder(self):
        history.addLog('Open PRP Folder requested')

        flags = QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks
        title = 'Choose PRP folder'

        prp_path = self.settings.getByKey('prp_path')
        path = QtGui.QFileDialog.getExistingDirectory(None, title, prp_path, options=flags)
        if os.path.exists(path):
            self.settings.setPrpPath(path)
            self.setPrpPathText(path)
            history.addLog('selected PRP Folder: ' + path)
    
    def doImportProposals(self):
        history.addLog('Import Proposals requested')

        title = 'Choose XML file with proposals'
        prp_path = self.settings.getByKey('prp_path')
        path = QtGui.QFileDialog.getOpenFileName(None, title, prp_path, "Images (*.xml)")
        path = str(path)
        if os.path.exists(path):
            history.addLog('selected file: ' + path)
            self.importProposals(path)
            history.addLog('imported proposals file: ' + path)
    
    def importProposals(self, filename):
        '''read a proposals XML file and set the model accordingly'''
        exception_list = (prop_mvc_data.IncorrectXmlRootTag, prop_mvc_data.InvalidWithXmlSchema)
        proposals = prop_mvc_data.AGUP_Proposals_List()
        try:
            proposals.importXml(filename)
        except exception_list, exc:
            history.addLog(str(exc))
            return
        # TODO: revise self.topics based on proposal list
        self.proposal_view = prop_mvc_view.AGUP_Proposals_View(self, proposals)
        self.proposal_view.show()

    def doSave(self):
        history.addLog('Save requested')
        history.addLog('NOTE: Save NOT IMPLEMENTED YET')

    def doSaveAs(self):
        history.addLog('Save As requested')
        history.addLog('NOTE: Save As NOT IMPLEMENTED YET')

    def doSaveSettings(self):
        history.addLog('Save Settings requested')
        self.settings.write()
        history.addLog('Settings written to: ' + self.settings.getByKey('rcfile'))
    
    def doResetDefaults(self):
        history.addLog('requested to reset default settings')
        self.settings.resetDefaults()
        history.addLog('default settings reset')
        history.addLog('NOTE: default settings reset NOT IMPLEMENTED YET')
        # TODO: what about Save?

    def doNewPrpFolder(self):
        history.addLog('New PRP Folder requested')

    def setPrpPathText(self, text):
        self.prp_path.setText(text)

    def setRcFileText(self, text):
        self.rcfile.setText(text)
    
    def setReviewCycleText(self, text):
        self.review_cycle.setText(text)

    def setReviewersFileText(self, text):
        self.reviewers_file.setText(text)

    def setProposalsFileText(self, text):
        self.proposals_file.setText(text)

    def setAnalysesFileText(self, text):
        self.analyses_file.setText(text)


def main():
    '''simple starter program to develop this code'''
    import sys
    app = QtGui.QApplication(sys.argv)
    mw = AGUP_MainWindow()
    mw.show()
    _r = app.exec_()
    sys.exit(_r)


if __name__ == '__main__':
    main()
