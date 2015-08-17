#!/usr/bin/env python

'''
:mod:`Main` code runs the GUI.
'''

import os, sys
from PyQt4 import QtCore, QtGui, uic
import traceback

import about
import history
import prop_mvc_data
import prop_mvc_view
import resources
import revu_mvc_view
import settings
import topics
import topics_editor
import xml_utility

UI_FILE = 'main_window.ui'
RC_FILE = '.assign_gup.rc'
RC_SECTION = 'Assign_GUP'
DUMMY_TOPICS_LIST = '''bio chem geo eng mater med phys poly'''.split()


class AGUP_MainWindow(QtGui.QMainWindow):
    '''
    Creates a Qt GUI for the main window
    '''

    def __init__(self):
        self.settings = settings.ApplicationSettings(RC_FILE, RC_SECTION)

        QtGui.QMainWindow.__init__(self)
        resources.loadUi(UI_FILE, baseinstance=self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_window_title = self.windowTitle()

        self.modified = False
        self.forced_exit = False

        self.proposals = None
        self.proposal_view = None
        self.reviewers = None
        self.reviewer_view = None
        self.topics = topics.Topics()
        
        # dummy topics for now
        topics_list = DUMMY_TOPICS_LIST
        for key in topics_list:
            self.topics.add(key)

        self._init_history_()

        # TODO: need handlers for widgets and config settings

        history.addLog('loaded "' + UI_FILE + '"')

        # assign values to each of the display widgets in the main window
        self._init_mainwindow_widget_values_()

        self._init_connections_()

        self.openPrpFolder(self.settings.getByKey('prp_path'))
        self.settings.modified = False
        self.modified = False
        self.adjustMainWindowTitle()

    def _init_history_(self):
        self.history_logger = history.Logger(log_file=None, 
                                             level=history.NO_LOGGING, 
                                             statusbar=self.statusbar, 
                                             history_widget=self.history)
        history.addMessageToHistory = self.history_logger.add

    def _init_mainwindow_widget_values_(self):
        self.settings_box.setTitle('settings from ' + self.settings.source)
        self.setPrpPathText(self.settings.getByKey('prp_path'))
        self.setRcFileText(self.settings.getByKey('rcfile'))
        self.setReviewCycleText(self.settings.getByKey('review_cycle'))
        self.setReviewersFileText(self.settings.getByKey('reviewers_file'))
        self.setProposalsFileText(self.settings.getByKey('proposals_file'))
        self.setAnalysesFileText(self.settings.getByKey('analyses_file'))
 
        for key in sorted(self.settings.getKeys()):
            value = self.settings.getByKey(key)
            history.addLog('Configuration option: %s = %s' % (key, value))

    def _init_connections_(self):
        self.actionNew_PRP_Folder.triggered.connect(self.doNewPrpFolder)
        self.actionOpen_Folder.triggered.connect(self.doOpenPrpFolder)
        self.actionImport_proposals.triggered.connect(self.doImportProposals)
        self.actionEdit_proposals.triggered.connect(self.doEditProposals)
        self.actionEdit_Reviewers.triggered.connect(self.doEditReviewers)
        self.actionEdit_Topics.triggered.connect(self.doEditTopics)
        self.actionSave.triggered.connect(self.doSave)
        self.actionSaveAs.triggered.connect(self.doSaveAs)
        self.actionSave_settings.triggered.connect(self.doSaveSettings)
        self.actionReset_Defaults.triggered.connect(self.doResetDefaults)
        self.actionExit.triggered.connect(self.doClose)
        self.actionAbout.triggered.connect(self.doAbout)

    def doAbout(self, *args, **kw):
        '''
        describe this application and where to get more info
        '''
        history.addLog('About... box requested')
        ui = about.AboutBox(self)
        ui.show()
    
    def adjustMainWindowTitle(self):
        '''
        indicate in main window title when there are unsaved modifications (when self.cannotExit() is True)
        '''
        title = self.main_window_title
        if self.cannotExit():
            title += ' (*)'
        self.setWindowTitle(title)

    def cannotExit(self):
        '''
        advise if the application has unsaved changes
        '''
        if self.forced_exit:
            return False
        decision = self.modified
        decision |= self.settings.modified
        if self.proposal_view is not None:
            decision |= self.proposal_view.isProposalListModified()
        if self.reviewer_view is not None:
            decision |= self.reviewer_view.isReviewerListModified()
        return decision

    def closeEvent(self, event):
        '''
        'called when user clicks the big [X] to quit
        '''
        history.addLog('application forced quit requested')
        if self.cannotExit():
            if self.doNotQuitNow():
                event.ignore()
            else:
                event.accept()
        else:
            self.doClose()
            event.accept() # let the window close

    def doClose(self, *args, **kw):
        '''
        'called when user chooses exit (or quit), or from closeEvent()
        '''
        history.addLog('application exit requested')
        if self.cannotExit():
            if self.doNotQuitNow():
                return

        if self.proposal_view is not None:  # TODO: why is this needed?
            self.proposal_view.close()
        self.close()
    
    def doNotQuitNow(self):
        '''
        Ask user to save changes before exit.
        
        Return True if application should *NOT* exit.
        '''
        box = QtGui.QMessageBox()
        box.setText('The session data has changed.')
        box.setInformativeText('Save the changes?')
        box.setStandardButtons(QtGui.QMessageBox.Save 
                               | QtGui.QMessageBox.Discard
                               | QtGui.QMessageBox.Cancel)
        box.setDefaultButton(QtGui.QMessageBox.Save)
        ret = box.exec_()

        if ret == QtGui.QMessageBox.Save:
            history.addLog('Save before Exit was selected')
            self.doSave()       # TODO: or doSaveAs() ?
            self.doSaveSettings()
        elif ret == QtGui.QMessageBox.Cancel:
            history.addLog('Application Exit was canceled')
            return True     # application should NOT exit
        elif ret == QtGui.QMessageBox.Discard:
            self.forced_exit = True
            history.addLog('Discard Changes was chosen')
        else:
            msg = 'wrong button value from confirm close dialog: ' + str(ret)
            history.addLog('ValueError: ' + msg)
            raise ValueError, msg
        return False    # application should exit

    def doOpenPrpFolder(self):
        '''
        '''
        history.addLog('Open PRP Folder requested')

        flags = QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks
        title = 'Choose PRP folder'

        prp_path = self.settings.getByKey('prp_path')
        path = QtGui.QFileDialog.getExistingDirectory(None, title, prp_path, options=flags)
        if os.path.exists(path):
            self.settings.setPrpPath(path)
            self.openPrpFolder(path)
            history.addLog('selected PRP Folder: ' + path)
    
    def openPrpFolder(self, path):
        '''
        choose the directory that holds the files for this PRP review
        '''
        history.addLog('Opening PRP folder: ' + path)
        self.setPrpPathText(path)

        prop_filename = os.path.join(path, 'proposals.xml')
        reviewers_filename = os.path.join(path, 'panel.xml')
        analysis_filename = os.path.join(path, 'analysis.xml')

        if not os.path.exists(prop_filename):
            return
        history.addLog('Importing Proposals file: ' + prop_filename)
        self.importProposals(prop_filename)

        if not os.path.exists(reviewers_filename):
            return
        history.addLog('Importing Reviewers file: ' + reviewers_filename)
        self.importReviewers(reviewers_filename)

        if not os.path.exists(analysis_filename):
            return
        history.addLog('Importing Analyses file: ' + analysis_filename)
        self.importAnalyses(analysis_filename)

    def doImportProposals(self):
        '''
        '''
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
        self.proposals = prop_mvc_data.AGUP_Proposals_List()

        exception_list = (xml_utility.IncorrectXmlRootTag, 
                          xml_utility.InvalidWithXmlSchema)
        try:
           self.proposals.importXml(filename)
        except exception_list, exc:
            history.addLog(traceback.format_exc())
            return

        self.setProposalsFileText(filename)
        txt = self.getReviewCycleText()
        if self.getReviewCycleText() == '':
            self.setReviewCycleText(self.proposals.cycle)

    def doEditProposals(self):
        '''
        '''
        if self.proposal_view is None:
            self.proposal_view = prop_mvc_view.AGUP_Proposals_View(self, self.proposals, self.topics)
        self.proposal_view.show()

    def doEditReviewers(self):
        '''
        '''
        if self.reviewer_view is None:
            self.reviewer_view = revu_mvc_view.AGUP_Reviewers_View(self, self.reviewers, self.topics)
        self.reviewer_view.show()

    def importReviewers(self, filename):
        '''
        '''
        history.addLog('Importing Reviewers file: NOT IMPLEMENTED NOW')
        self.setReviewersFileText(filename)

    def importAnalyses(self, filename):
        '''
        '''
        history.addLog('Importing Analyses file: NOT IMPLEMENTED NOW')
        self.setAnalysesFileText(filename)

    def doEditTopics(self):
        '''
        Create Window to edit list of Topics
        '''
        # post the editor GUI
        history.addLog('Edit Topics ... requested')
        if self.proposal_view is not None:
            self.proposal_view.close()
            self.proposal_view = None
        
        known_topics = self.topics.getList()
        edit_topics_ui = topics_editor.AGUP_TopicsEditor(self, known_topics)
        edit_topics_ui.exec_()   # Modal Dialog
        
        # learn what changed
        topics_list = edit_topics_ui.getList()
        added = [_ for _ in topics_list if _ not in known_topics]
        removed = [_ for _ in known_topics if _ not in topics_list]
        if len(added) + len(removed) == 0:
            history.addLog('list of topics unchanged')
            self.adjustMainWindowTitle()
            return
        
        # confirm before proceeding
        box = QtGui.QMessageBox()
        box.setText('The list of topics has changed.')
        box.setInformativeText('Save the changes?')
        box.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard)
        box.setDefaultButton(QtGui.QMessageBox.Save)
        ret = box.exec_()
        if ret == QtGui.QMessageBox.Discard:
            history.addLog('revised list of topics not accepted')
            self.adjustMainWindowTitle()
            return
        
        #---
        # TODO: merge final list form editor with
        # x self.topics
        # x proposals    TODO: need to re-check this one
        # - reviewers
        for key in added:
            self.topics.add(key)
            self.proposals.addTopic(key)
        for key in removed:
            self.topics.remove(key)
            self.proposals.removeTopic(key)
        history.addLog('added topics: ' + ' '.join(added))
        history.addLog('deleted topics: ' + ' '.join(removed))
        self.modified = True
        self.adjustMainWindowTitle()

    def doSave(self):
        '''
        '''
        # TODO: consider saving window geometries
        history.addLog('Save requested')
        self.modified = False
        self.adjustMainWindowTitle()
        history.addLog('NOTE: Save NOT IMPLEMENTED YET')

    def doSaveAs(self):
        '''
        '''
        history.addLog('Save As requested')
        self.modified = False
        self.adjustMainWindowTitle()
        history.addLog('NOTE: Save As NOT IMPLEMENTED YET')

    def doSaveSettings(self):
        '''
        '''
        history.addLog('Save Settings requested')
        self.settings.write()
        history.addLog('Settings written to: ' + self.settings.getByKey('rcfile'))
        self.adjustMainWindowTitle()
    
    def doResetDefaults(self):
        '''
        '''
        history.addLog('requested to reset default settings')
        self.settings.resetDefaults()
        history.addLog('default settings reset')
        history.addLog('NOTE: default settings reset NOT IMPLEMENTED YET')
        # TODO: what about Save?
        self.adjustMainWindowTitle()

    def doNewPrpFolder(self):
        '''
        '''
        history.addLog('New PRP Folder requested')
        self.adjustMainWindowTitle()

    # widget getters and setters

    def setPrpPathText(self, text):
        self.prp_path.setText(text)
        self.settings.setPrpPath(text)
        self.adjustMainWindowTitle()

    def setRcFileText(self, text):
        self.rcfile.setText(text)
        self.settings.setRcFile(text)
        self.adjustMainWindowTitle()

    def getReviewCycleText(self):
        return str(self.review_cycle.text())
    
    def setReviewCycleText(self, text):
        self.review_cycle.setText(text)
        self.settings.setReviewCycle(text)
        self.adjustMainWindowTitle()

    def setReviewersFileText(self, text):
        self.reviewers_file.setText(text)
        self.adjustMainWindowTitle()

    def setProposalsFileText(self, text):
        self.proposals_file.setText(text)
        self.adjustMainWindowTitle()

    def setAnalysesFileText(self, text):
        self.analyses_file.setText(text)
        self.adjustMainWindowTitle()


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
