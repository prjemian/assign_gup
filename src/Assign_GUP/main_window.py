#!/usr/bin/env python

'''
:mod:`Main` code runs the GUI.
'''

import os, sys
from PyQt4 import QtCore, QtGui, uic
import traceback

import about
import agup_data
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


class AGUP_MainWindow(QtGui.QMainWindow):
    '''
    Creates a Qt GUI for the main window
    '''

    def __init__(self):
        self.settings = settings.ApplicationQSettings()
        self.agup = agup_data.AGUP_Data(self.settings)

        QtGui.QMainWindow.__init__(self)
        resources.loadUi(UI_FILE, baseinstance=self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_window_title = self.windowTitle()
        self.restoreWindowGeometry()

        self.modified = False
        self.forced_exit = False

        self.proposal_view = None
        self.reviewer_view = None

        self._init_history_()

        # TODO: need handlers for widgets and config settings

        history.addLog('loaded "' + UI_FILE + '"')

        self._init_mainwindow_widget_values_()
        self._init_connections_()
        
        filename = self.settings.getPrpFile()
        if os.path.exists(filename):
            self.agup.openPrpFile(filename)

        self.modified = False
        self.adjustMainWindowTitle()

    def _init_history_(self):
        self.history_logger = history.Logger(log_file=None, 
                                             level=history.NO_LOGGING, 
                                             statusbar=self.statusbar, 
                                             history_widget=self.history)
        history.addMessageToHistory = self.history_logger.add

    def _init_mainwindow_widget_values_(self):
        self.setPrpFileText(self.settings.getPrpFile())
        self.setRcFileText(self.settings.fileName())
        self.setReviewCycleText(self.settings.getReviewCycle())
 
        for key in sorted(self.settings.allKeys()):
            value = self.settings.getKey(key)
            history.addLog('Configuration option: %s = %s' % (key, str(value)))

    def _init_connections_(self):
        self.actionNew_PRP_Project.triggered.connect(self.doNewPrpFile)
        self.actionOpen.triggered.connect(self.doOpenPrpFile)
        self.actionImport_Proposals.triggered.connect(self.doImportProposals)
        self.actionImport_Reviewers.triggered.connect(self.doImportReviewers)
        self.actionEdit_proposals.triggered.connect(self.doEditProposals)
        self.actionEdit_Reviewers.triggered.connect(self.doEditReviewers)
        self.actionEdit_Topics.triggered.connect(self.doEditTopics)
        self.actionSave.triggered.connect(self.doSave)
        self.actionSaveAs.triggered.connect(self.doSaveAs)
        self.actionReset_settings.triggered.connect(self.doResetDefaultSettings)
        self.actionExit.triggered.connect(self.doClose)
        self.actionAgupInfo.triggered.connect(self.doAgupInfo)

    def doAgupInfo(self, *args, **kw):
        '''
        describe this application and where to get more info
        '''
        history.addLog('Info... box requested')
        ui = about.InfoBox(self)    # bless the Mac that it handles "about" differently
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
        if self.proposal_view is not None:
            decision |= self.proposal_view.isProposalListModified()
        if self.reviewer_view is not None:
            decision |= self.reviewer_view.isReviewerListModified()
        return decision

    def closeEvent(self, event):
        '''
        called when user clicks the big [X] to quit
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
        called when user chooses exit (or quit), or from closeEvent()
        '''
        history.addLog('application exit requested')
        if self.cannotExit():
            if self.doNotQuitNow():
                return

        self.saveWindowGeometry()
        if self.reviewer_view is not None:
            self.reviewer_view.close()
            self.reviewer_view.destroy()
            self.reviewer_view = None
        if self.proposal_view is not None:
            self.proposal_view.close()
            self.proposal_view.destroy()
            self.proposal_view = None
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

    def doOpenPrpFile(self):
        '''
        '''
        history.addLog('Open PRP File requested')

        flags = QtGui.QFileDialog.DontResolveSymlinks
        title = 'Open PRP file'

        prp_file = str(self.settings.getPrpFile()).strip()
        if len(prp_file) == 0:
            prp_path = ''
        else:
            prp_path = os.path.dirname(prp_file)

        filename = QtGui.QFileDialog.getOpenFileName(None, title, prp_path, "Images (*.xml)")

        if os.path.exists(filename):
            self.openPrpFile(filename)
            history.addLog('selected PRP file: ' + filename)
    
    def openPrpFile(self, filename):
        '''
        choose the XML file with data for this PRP review
        '''
        history.addLog('Opening PRP file: ' + filename)
        if self.proposal_view is not None:
            self.proposal_view.close()
            self.proposal_view.destroy()
            self.proposal_view = None
        if self.reviewer_view is not None:
            self.reviewer_view.close()
            self.reviewer_view.destroy()
            self.reviewer_view = None
        if self.agup.openPrpFile(filename):
            self.setPrpFileText(filename)
            self.settings.setPrpFile(filename)
            self.setReviewCycleText(self.agup.getCycle())
            history.addLog('Open PRP file: ' + filename)

    def doImportProposals(self):
        '''
        '''
        history.addLog('Import Proposals requested')
        title = 'Choose XML file with proposals'
        prp_file = self.settings.getPrpFile()

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

        txt = self.getReviewCycleText()
        if self.getReviewCycleText() == '':
            self.setReviewCycleText(self.proposals.cycle)

    def doEditProposals(self):
        '''
        '''
        if self.proposal_view is None:
            self.proposal_view = prop_mvc_view.AGUP_Proposals_View(self, self.agup, self.settings)
        self.proposal_view.show()

    def doEditReviewers(self):
        '''
        '''
        if self.reviewer_view is None:
            self.reviewer_view = revu_mvc_view.AGUP_Reviewers_View(self, self.agup, self.settings)
            self.reviewer_view.custom_signals.recalc.connect(self.doRecalc)
        self.reviewer_view.show()

    def doImportReviewers(self):
        '''
        '''
        history.addLog('Import Reviewers selected: NOT IMPLEMENTED NOW')

    def importReviewers(self, filename):
        '''
        '''
        history.addLog('Importing Reviewers file: NOT IMPLEMENTED NOW')

    def importAnalyses(self, filename):
        '''
        '''
        history.addLog('Importing Analyses file: NOT IMPLEMENTED NOW')

    def importTopics(self, filename):
        '''
        '''
        history.addLog('Importing Topics file: NOT IMPLEMENTED NOW')

    def doEditTopics(self):
        '''
        Create Window to edit list of Topics
        '''
        # post the editor GUI
        history.addLog('Edit Topics ... requested')
        if self.proposal_view is not None:
            self.proposal_view.close()
            self.proposal_view = None
        if self.reviewer_view is not None:
            self.reviewer_view.close()
            self.reviewer_view = None
        
        known_topics = self.agup.topics.getTopicList()
        edit_topics_ui = topics_editor.AGUP_TopicsEditor(self, known_topics, self.settings)
        edit_topics_ui.exec_()   # Modal Dialog
        
        # learn what changed
        topics_list = edit_topics_ui.getTopicList()
        added, removed = topics.diffLists(topics_list, known_topics)
        if len(added) + len(removed) == 0:
            history.addLog('list of topics unchanged')
            self.adjustMainWindowTitle()
            return

        if not self.confirmEditTopics():
            history.addLog('revised list of topics not accepted')
            self.adjustMainWindowTitle()
            return False

        self.agup.topics.addTopics(added)
        self.agup.proposals.addTopics(added)
        self.agup.reviewers.addTopics(added)
        history.addLog('added topics: ' + ' '.join(added))

        self.agup.topics.removeTopics(removed)
        self.agup.proposals.removeTopics(removed)
        self.agup.reviewers.removeTopics(removed)
        history.addLog('deleted topics: ' + ' '.join(removed))
        history.addLog('Note: Be sure to review Topics for all Proposals and Reviewers.')

        self.modified = True
        self.adjustMainWindowTitle()
    
    def confirmEditTopics(self):
        '''
        confirm before proceeding
        '''
        box = QtGui.QMessageBox()
        box.setText('The list of topics has changed.')
        box.setInformativeText('Save the changes?')
        box.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard)
        box.setDefaultButton(QtGui.QMessageBox.Save)
        ret = box.exec_()
        return ret == QtGui.QMessageBox.Save

    def doSave(self):
        '''
        save the self.agup data to the known data file name
        '''
        history.addLog('Save requested')
        filename = str(self.settings.getPrpFile())
        self.agup.write(filename)
        self.modified = False
        self.adjustMainWindowTitle()
        history.addLog('saved: ' + filename)

    def doSaveAs(self):
        '''
        save the self.agup data to the data file name selected from a dialog box
        '''
        history.addLog('Save As requested')
        filename = self.settings.getPrpFile()
        filename = QtGui.QFileDialog.getSaveFileName(parent=self, 
                                                     caption="Save the PRP project", 
                                                     directory=filename,
                                                     filter='XML File (*.xml)')
        filename = str(os.path.abspath(filename))
        if len(filename) > 0:
            self.agup.write(filename)
            self.settings.setPrpFile(filename)
            self.setPrpFileText(filename)
            self.modified = False
        history.addLog('saved: ' + filename)
        self.adjustMainWindowTitle()

    def doResetDefaultSettings(self):
        '''
        user requested to reset the settings to their default values
        
        Note: does not write to the rcfile
        '''
        history.addLog('Reset to Default Settings requested')
        self.settings.resetDefaults()
        self.adjustMainWindowTitle()

    def doNewPrpFile(self):
        '''
        clear the data in self.agup
        '''
        history.addLog('New PRP File requested')
        if False:
            self.agup.clearAllData()
            self.setPrpFileText('')
        history.addLog('New PRP File: NOT IMPLEMENTED YET')
        self.adjustMainWindowTitle()
    
    def saveWindowGeometry(self):
        '''
        remember where the window was
        '''
        if self.settings is not None:
            self.settings.saveWindowGeometry(self)

    def restoreWindowGeometry(self):
        '''
        put the window back where it was
        '''
        if self.settings is not None:
            self.settings.restoreWindowGeometry(self)

    def doRecalc(self):
        if self.proposal_view is not None:
            self.proposal_view.recalc()

    # widget getters and setters

    def setPrpFileText(self, text):
        self.prp_file.setText(text)
        self.settings.setPrpFile(text)
        self.adjustMainWindowTitle()

    def setRcFileText(self, text):
        self.rcfile.setText(text)
        self.adjustMainWindowTitle()

    def getReviewCycleText(self):
        return str(self.review_cycle.text())
    
    def setReviewCycleText(self, text):
        self.review_cycle.setText(text or '')
        self.settings.setReviewCycle(text)
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
