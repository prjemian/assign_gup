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
LOG_MINOR_DETAILS = False
LOG_MINOR_DETAILS = True        # TODO: remove for production release


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
            self.openPrpFile(filename)

        self.modified = False
        self.adjustMainWindowTitle()

    def _init_history_(self):
        self.history_logger = history.Logger(log_file=None, 
                                             level=history.NO_LOGGING, 
                                             statusbar=self.statusbar, 
                                             history_widget=self.history,
                                             minor_details=LOG_MINOR_DETAILS)
        history.addMessageToHistory = self.history_logger.add

    def _init_mainwindow_widget_values_(self):
        self.setPrpFileText(self.settings.getPrpFile())
        self.setRcFileText(self.settings.fileName())
        self.setReviewCycleText(self.settings.getReviewCycle())
 
        for key in sorted(self.settings.allKeys()):
            value = self.settings.getKey(key)
            history.addLog('Configuration option: %s = %s' % (key, str(value)), False)

    def _init_connections_(self):
        self.actionNew_PRP_Project.triggered.connect(self.doNewPrpFile)
        self.actionOpen.triggered.connect(self.doOpenPrpFile)
        # self.actionUndo.triggered.connect()
        # self.actionCut.triggered.connect()
        # self.actionCopy.triggered.connect()
        # self.actionPaste.triggered.connect()
        # self.actionSelect_All.triggered.connect()
        self.actionImport_Topics.triggered.connect(self.doImportTopics)
        self.actionImport_Reviewers.triggered.connect(self.doImportReviewers)
        self.actionImport_Proposals.triggered.connect(self.doImportProposals)
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
        history.addLog('Info... box requested', False)
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
        history.addLog('application forced quit requested', False)
        if self.cannotExit():
            if self.doNotQuitNow():
                event.ignore()
            else:
                event.accept()
        else:
            self.doClose()
            event.accept() # let the window close

    def closeSubwindows(self):
        '''
        close all other windows created by this code
        '''
        if self.reviewer_view is not None:
            self.reviewer_view.close()
            self.reviewer_view.destroy()
            self.reviewer_view = None
        if self.proposal_view is not None:
            self.proposal_view.close()
            self.proposal_view.destroy()
            self.proposal_view = None

    def doClose(self, *args, **kw):
        '''
        called when user chooses exit (or quit), or from closeEvent()
        '''
        history.addLog('application exit requested', False)
        if self.cannotExit():
            if self.doNotQuitNow():
                return

        self.saveWindowGeometry()
        self.closeSubwindows()
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

    def doResetDefaultSettings(self):
        '''
        user requested to reset the settings to their default values
        
        Note: does not write to the rcfile
        '''
        history.addLog('Reset to Default Settings requested', False)
        self.settings.resetDefaults()
        self.adjustMainWindowTitle()

    def doNewPrpFile(self):
        '''
        clear the data in self.agup
        '''
        history.addLog('New PRP File requested', False)

        if self.cannotExit():
            box = QtGui.QMessageBox()
            box.setText('There are unsaved changes.')
            box.setInformativeText('Forget about them?')
            box.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
            box.setDefaultButton(QtGui.QMessageBox.Cancel)
            ret = box.exec_()
            if ret == QtGui.QMessageBox.Cancel:
                return

        self.closeSubwindows()
        self.agup.clearAllData()
        self.setPrpFileText('')
        self.setIndicators()
        history.addLog('New PRP File')
        self.adjustMainWindowTitle()

    def doOpenPrpFile(self):
        '''
        open an existing PRP file
        '''
        history.addLog('Open PRP File requested', False)

        flags = QtGui.QFileDialog.DontResolveSymlinks
        title = 'Open PRP file'

        prp_file = self.settings.getPrpFile()
        if len(prp_file) == 0:
            prp_path = ''
        else:
            prp_path = os.path.dirname(prp_file)

        filters = ('PRP project (*.agup *.prp *.xml)', 'any file (*.*)')
        filename = QtGui.QFileDialog.getOpenFileName(None, title, prp_path, ';;'.join(filters))

        if os.path.exists(filename):
            self.openPrpFile(filename)
            history.addLog('selected PRP file: ' + filename)
    
    def openPrpFile(self, filename):
        '''
        choose the XML file with data for this PRP review
        '''
        history.addLog('Opening PRP file: ' + filename)
        self.closeSubwindows()
        
        try:
            self.agup.openPrpFile(filename)
        except Exception:
            history.addLog(traceback.format_exc())
            # TODO: put up a "failed" dialog to acknowledge 'that was not a PRP Project file'
            return

        self.setPrpFileText(filename)
        self.setIndicators()
        history.addLog('Open PRP file: ' + filename)

    def doEditProposals(self):
        '''
        edit the list of Proposals
        '''
        if self.proposal_view is None:
            self.proposal_view = prop_mvc_view.AGUP_Proposals_View(self, self.agup, self.settings)
        self.proposal_view.show()

    def doEditReviewers(self):
        '''
        edit the list of Reviewers
        '''
        if self.reviewer_view is None:
            self.reviewer_view = revu_mvc_view.AGUP_Reviewers_View(self, self.agup, self.settings)
            self.reviewer_view.custom_signals.recalc.connect(self.doRecalc)
        self.reviewer_view.show()

    def doEditTopics(self):
        '''
        Create Window to edit list of Topics
        '''
        # post the editor GUI
        history.addLog('Edit Topics ... requested', False)
        self.closeSubwindows()
        
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

    def doImportProposals(self):
        '''
        import the proposal file as downloaded from the APS web site
        '''
        history.addLog('Import Proposals requested', False)
        title = 'Choose XML file with proposals'
        prp_path = os.path.dirname(self.settings.getPrpFile())

        path = filename = QtGui.QFileDialog.getOpenFileName(None, title, prp_path, "Proposals (*.xml)")
        path = str(path)
        if os.path.exists(path):
            history.addLog('selected file: ' + path)
            self.importProposals(path)
            history.addLog('imported proposals file: ' + path)

    def importProposals(self, filename):
        '''read a proposals XML file and set the model accordingly'''
        try:
            self.agup.importProposals(filename)
        except:
            history.addLog(traceback.format_exc())
            # TODO: put up a "failed" dialog to acknowledge 'that was not an APS Proposals file'
            return

        # ensure each imported proposal has the correct Topics
        for prop in self.agup.proposals:
            added, removed = self.agup.topics.diff(prop.topics)
            prop.addTopics(added)
            prop.removeTopics(removed)
        
        self.setIndicators()
        history.addLog('imported Proposals from: ' + filename)

        if self.getReviewCycleText() == '':
            self.setReviewCycleText(self.agup.proposals.cycle)

    def doImportReviewers(self):
        '''
        copy the list of Reviewers into this project from another PRP Project file
        '''
        history.addLog('Import Reviewers requested', False)
        title = 'Choose a PRP Project file (XML) to copy its Reviewers'
        prp_path = os.path.dirname(self.settings.getPrpFile())

        path = QtGui.QFileDialog.getOpenFileName(None, title, prp_path, "PRP Project (*.xml)")
        path = str(path)
        if os.path.exists(path):
            self.importReviewers(path)
    
    def importReviewers(self, filename):
        '''read Reviewers from a PRP Project file and set the model accordingly'''
        self.agup.importReviewers(filename)
        self.setNumTopicsWidget(len(self.agup.topics))
        self.setNumReviewersWidget(len(self.agup.reviewers))
        history.addLog('imported Reviewers from: ' + filename)

    def doImportTopics(self):
        '''
        copy the list of Topics from another PRP file into this project
        '''
        history.addLog('Import Topics requested', False)
        title = 'Choose a PRP Project file (XML) to copy its Topics'
        prp_path = os.path.dirname(self.settings.getPrpFile())

        filename = QtGui.QFileDialog.getOpenFileName(None, title, prp_path, "PRP Project (*.xml)")
        filename = str(filename)
        if os.path.exists(filename):
            self.importTopics(filename)
            history.addLog('imported Topics from: ' + filename)
    
    def importTopics(self, filename):
        '''read Topics from a PRP Project file and set the model accordingly'''
        self.agup.importTopics(filename)
        self.setNumTopicsWidget(len(self.agup.topics))
        history.addLog('imported topics from: ' + filename)

    def doRecalc(self):
        if self.proposal_view is not None:
            self.proposal_view.recalc()

    def doSave(self):
        '''
        save the self.agup data to the known project file name
        '''
        history.addLog('Save requested', False)
        filename = self.settings.getPrpFile()
        if len(filename) == 0:
            self.doSaveAs()
        else:
            self.agup.write(filename)
            self.modified = False
            self.adjustMainWindowTitle()
            history.addLog('saved: ' + filename)

    def doSaveAs(self):
        '''
        save the self.agup data to the data file name selected from a dialog box
        
        You may choose any file name and extension that you prefer.
        It is strongly suggested you choose the default file extension,
        to identify AGUP PRP Project files more easily on disk.
        Multiple projects files, perhaps for different review cycles,
        can be saved in the same directory.  Or you can save each project file
        in a different directory as you choose.

        By default, the file extension will be **.agup**, indicating
        that this is an AGUP PRP Project file.  The extensions *.prp* or *.xml*
        may be used as alternatives.  Each of these describes a file with *exactly 
        the same file format*, an XML document.
        '''
        history.addLog('Save As requested', False)
        filename = self.settings.getPrpFile()
        filters = ('AGUP PRP Project (*.agup)', 'PRP Project (*.prp)', 'XML File (*.xml)')
        filename = QtGui.QFileDialog.getSaveFileName(parent=self, 
                                                     caption="Save the PRP project", 
                                                     directory=filename,
                                                     filter=';;'.join(filters))
        filename = str(os.path.abspath(filename))
        if len(filename) == 0:
            return
        if os.path.isdir(filename):
            history.addLog('cannot save, selected a directory: ' + filename)
            return
        if os.path.islink(filename):     # might need deeper analysis
            history.addLog('cannot save, selected a link: ' + filename)
            return
        if os.path.ismount(filename):
            history.addLog('cannot save, selected a mount point: ' + filename)
            return
        self.agup.write(filename)
        self.setPrpFileText(filename)
        self.modified = False
        history.addLog('saved: ' + filename)
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
    
    def _num_to_text_(self, number):
        if number > 0:
            text = str(number)
        else:
            text = 'no'
        return text

    def setNumTopicsWidget(self, number):
        self.num_topics.setText(self._num_to_text_(number))

    def setNumReviewersWidget(self, number):
        self.num_reviewers.setText(self._num_to_text_(number))

    def setNumProposalsWidget(self, number):
        self.num_proposals.setText(self._num_to_text_(number))
    
    def setIndicators(self):
        self.setNumTopicsWidget(len(self.agup.topics))
        self.setNumReviewersWidget(len(self.agup.reviewers))
        self.setNumProposalsWidget(len(self.agup.proposals))
        self.setReviewCycleText(self.agup.getCycle())


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
