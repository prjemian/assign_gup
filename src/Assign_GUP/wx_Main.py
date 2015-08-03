#!/usr/bin/env python

'''
:mod:`Main` code runs the GUI.
'''

import os, sys
from PyQt4 import QtCore, QtGui
import qt_form_support
import history
import settings
import Proposals_ListView

UI_FILE = 'main_window.ui'
ABOUT_UI_FILE = 'about.ui'
DOCS_URL = 'http://Assign_GUP.readthedocs.org'
LICENSE_FILE = 'LICENSE'
RC_FILE = '.assign_gup.rc'
RC_SECTION = 'Assign_GUP'
addMessageToHistory = None


def addLog(message):
    global addMessageToHistory
    if addMessageToHistory is not None:
        addMessageToHistory(message)
    else:
        print message


def main():
    '''simple starter program to develop this code'''
    import sys
    app = QtGui.QApplication(sys.argv)
    main_window = AGUP_MainWindow()
    main_window.ui.show()
    _r = app.exec_()
    sys.exit(_r)


class AGUP_MainWindow(object):
    '''
    Creates a Qt GUI for the main window
    '''

    def __init__(self):
        global addMessageToHistory

        self.settings = settings.ApplicationSettings(RC_FILE, RC_SECTION)
        # TODO: support self.settings.modified flag

        self.ui = qt_form_support.load_form(UI_FILE)
        self.history_logger = history.Logger(log_file=None, 
                                             level=history.NO_LOGGING, 
                                             statusbar=self.ui.statusbar, 
                                             history_widget=self.ui.history)
        addMessageToHistory = self.history_logger.add

        # TODO: need handlers for widgets and config settings

        addLog('loaded "' + UI_FILE + '"')

        # assign values to each of the display widgets in the main window

        self.ui.settings_box.setTitle('settings from ' + self.settings.source)
        self.setPrpPathText(self.settings.getByKey('prp_path'))
        self.setRcFileText(self.settings.getByKey('rcfile'))
        self.setReviewCycleText(self.settings.getByKey('review_cycle'))
        self.setReviewersFileText(self.settings.getByKey('reviewers_file'))
        self.setProposalsFileText(self.settings.getByKey('proposals_file'))
        self.setAnalysesFileText(self.settings.getByKey('analyses_file'))

        for key in sorted(self.settings.getKeys()):
            addLog('Configuration option: %s = %s' % (key, self.settings.getByKey(key)))

        self.ui.actionNew_PRP_Folder.triggered.connect(self.doNewPrpFolder)
        self.ui.actionOpen_Folder.triggered.connect(self.doOpenPrpFolder)
        self.ui.actionImport_proposals.triggered.connect(self.doImportProposals)
        self.ui.actionSave_settings.triggered.connect(self.doSaveSettings)
        self.ui.actionReset_Defaults.triggered.connect(self.doResetDefaults)
        self.ui.actionExit.triggered.connect(self.doClose)
        self.ui.actionAbout.triggered.connect(self.doAbout)

    def doAbout(self, *args, **kw):
        addLog('About... box requested')
        ui = qt_form_support.load_form(ABOUT_UI_FILE)
        
        ui.docs_pb.clicked.connect(self.doUrl)
        ui.license_pb.clicked.connect(self.doLicense)

        ui.show()
        ui.exec_()
    
    def doUrl(self):
        addLog('opening documentation URL in default browser')
        url = QtCore.QUrl(DOCS_URL)
        service = QtGui.QDesktopServices()
        service.openUrl(url)
    
    def doLicense(self):
        addLog('opening License in new window')
        license_ui = qt_form_support.load_form('plainTextEdit.ui')

        path = os.path.abspath(os.path.join(qt_form_support.get_forms_path(), '..'))
        license_text = open(os.path.join(path, LICENSE_FILE), 'r').read()

        ui = putTextInWindow('LICENSE', license_text)
        ui.show()

    def doClose(self, *args, **kw):
        addLog('application exit requested')
        # TODO: refactor this to Qt
        #if self.settings.modified:
        #    # confirm this step
        #    result = self.RequestConfirmation('Exit (Quit)',
        #          'There are unsaved changes.  Exit (Quit) anyway?')
        #    if result != wx.ID_YES:
        #        return
        self.ui.close()
    
    def doOpenPrpFolder(self):
        addLog('Open PRP Folder requested')

        flags = QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks
        title = 'Choose PRP folder'

        prp_path = self.settings.getByKey('prp_path')
        path = QtGui.QFileDialog.getExistingDirectory(None, title, prp_path, options=flags)
        if os.path.exists(path):
            self.settings.setPrpPath(path)
            self.setPrpPathText(path)
            addLog('selected PRP Folder: ' + path)
    
    def doImportProposals(self):
        addLog('Import Proposals requested')

        title = 'Choose XML file with proposals'
        prp_path = self.settings.getByKey('prp_path')
        path = QtGui.QFileDialog.getOpenFileName(None, title, prp_path, "Images (*.xml)")
        path = str(path)
        if os.path.exists(path):
            # TODO: where's the beef?
            widget = Proposals_ListView.ProposalsView(path)
            widget.show()
            # widget.exec_()
            addLog('imported proposals file: ' + path)

    def doSaveSettings(self):
        addLog('Save Settings requested')
        self.settings.write()
        addLog('Settings written to: ' + self.settings.getByKey('rcfile'))
    
    def doResetDefaults(self):
        addLog('requested to reset default settings')
        self.settings.resetDefaults()
        addLog('default settings reset')
        # TODO: what about Save?

    def doNewPrpFolder(self):
        addLog('New PRP Folder requested')

    def setPrpPathText(self, text):
        self.ui.prp_path.setText(text)

    def setRcFileText(self, text):
        self.ui.rcfile.setText(text)
    
    def setReviewCycleText(self, text):
        self.ui.review_cycle.setText(text)

    def setReviewersFileText(self, text):
        self.ui.reviewers_file.setText(text)

    def setProposalsFileText(self, text):
        self.ui.proposals_file.setText(text)

    def setAnalysesFileText(self, text):
        self.ui.analyses_file.setText(text)


def putTextInWindow(title, text, width=300, height=300):
    '''puts *text* in a QPlainTextEdit window and returns the object'''
    ui = qt_form_support.load_form('plainTextEdit.ui')
    ui.setWindowTitle(title)
    ui.plainTextEdit.setPlainText(text)
    # TODO: why doesn't this work?
    # geom = ui.geometry()
    # geom.setWidth(width)
    # geom.setHeight(height)
    # ui.setGeometry(geom)
    return ui


if __name__ == '__main__':
    main()

# legacy wx Boa Constructore GUI code - leave for reference during development

# import ListPanel
# import ProposalPanel
# import Proposals
# import ReviewerPanel
# import Reviewers
# import ui
# import wx
# import wx.grid
# #import sys
# import config
# import Analysis
# 
# 
# # TODO: need an assessment of panel strength in each subject area
# # TODO: need an assessment of panel strength across all current proposals
# 
# 
# # for the About... box
# __version__ = "2015.0715.0"
# __progname__ = "assign_gup"
# __copyright__ = "(c) 2011-2015"
# __license__ = "ANL Open Source License"
# __long_description__ = '''Help assigning APS SAXS General User Proposals'''
# __URL__ = "http://Assign_GUP.ReadTheDocs.org"
# __website__ = __URL__
# __developers__ = [ "Pete Jemian", "jemian@anl.gov" ]
# 
#     # ===============================================================
# 
# 
# [wxID_MAIN, wxID_MAINSTATUSBAR1, wxID_MAINTREEBOOK1, 
# ] = [wx.NewId() for _init_ctrls in range(3)]
# 
# 
# [wxID_MAINMENUFILEEXIT] = [wx.NewId() for _init_coll_menuFile_Items in range(1)]
# 
# [wxID_MAINMENUHELPABOUT] = [wx.NewId() for _init_coll_menuHelp_Items in range(1)]
# 
# class Main(wx.Frame):
#     '''main GUI'''
#     def _init_coll_menuBar1_Menus(self, parent):
#         # generated method, don't edit
# 
#         parent.Append(menu=self.menuFile, title='File')
#         parent.Append(menu=self.menuHelp, title='Help')
# 
#     def _init_coll_menuHelp_Items(self, parent):
#         # generated method, don't edit
# 
#         parent.Append(help='Display general information about Assign GUP',
#               id=wxID_MAINMENUHELPABOUT, kind=wx.ITEM_NORMAL, text='About ...')
#         self.Bind(wx.EVT_MENU, self.OnMenuHelpAboutMenu,
#               id=wxID_MAINMENUHELPABOUT)
# 
#     def _init_coll_menuFile_Items(self, parent):
#         # generated method, don't edit
# 
#         parent.Append(help='Quit the application', id=wxID_MAINMENUFILEEXIT,
#               kind=wx.ITEM_NORMAL, text='Exit')
#         self.Bind(wx.EVT_MENU, self.OnMenuFileExitMenu,
#               id=wxID_MAINMENUFILEEXIT)
# 
#     def _init_coll_statusBar1_Fields(self, parent):
#         # generated method, don't edit
#         parent.SetFieldsCount(1)
# 
#         parent.SetStatusText(number=0, text='status')
# 
#         parent.SetStatusWidths([-1])
# 
#     def _init_utils(self):
#         # generated method, don't edit
#         self.menuFile = wx.Menu(title='File')
# 
#         self.menuHelp = wx.Menu(title='Help')
# 
#         self.menuBar1 = wx.MenuBar()
# 
#         self._init_coll_menuFile_Items(self.menuFile)
#         self._init_coll_menuHelp_Items(self.menuHelp)
#         self._init_coll_menuBar1_Menus(self.menuBar1)
# 
#     def _init_ctrls(self, prnt):
#         # generated method, don't edit
#         wx.Frame.__init__(self, id=wxID_MAIN, name='Main', parent=prnt,
#               pos=wx.Point(84, 66), size=wx.Size(887, 550),
#               style=wx.DEFAULT_FRAME_STYLE, title='Assign GUP')
#         self._init_utils()
#         self.SetClientSize(wx.Size(871, 512))
#         self.SetMenuBar(self.menuBar1)
# 
#         self.statusBar1 = wx.StatusBar(id=wxID_MAINSTATUSBAR1,
#               name='statusBar1', parent=self, style=0)
#         self._init_coll_statusBar1_Fields(self.statusBar1)
#         self.SetStatusBar(self.statusBar1)
# 
#         self.treebook1 = wx.Treebook(id=wxID_MAINTREEBOOK1, name='treebook1',
#               parent=self, pos=wx.Point(0, 0), size=wx.Size(871, 469), style=0)
#         self.treebook1.Bind(wx.EVT_TREEBOOK_PAGE_CHANGED,
#               self.OnTreebook1TreebookPageChanged, id=wxID_MAINTREEBOOK1)
# 
#     def __init__(self, parent):
#         self._init_ctrls(parent)
#         ui.log('basic UI initialized', self)
#         self.widget = {}
#         self.init_data()
#         self.init_TreeBook(self.treebook1)
#         
#     # ===============================================================
# 
#     def OnMenuHelpAboutMenu(self, event):
#         '''
#         describe this application
# 
#         :param event: wxPython event object
#         '''
#         # derived from http://wiki.wxpython.org/Using%20wxPython%20Demo%20Code
#         # First we create and fill the info object
#         ui.log("Requested About... box")
#         info = wx.AboutDialogInfo()
#         info.Name = __progname__
#         info.Version = __version__
#         info.Copyright = __copyright__
#         info.Description = __long_description__
#         info.URL = __URL__
#         info.WebSite = __website__
#         info.Developers = __developers__
#         info.License = __license__
#         # Then we call wx.AboutBox giving it the info object
#         wx.AboutBox(info)
# 
#     def OnMenuFileExitMenu(self, event):
#         '''
#         User requested to quit the application
# 
#         :param event: wxPython event object
#         '''
#         #if self.dirty:
#         #    # confirm this step
#         #    result = self.RequestConfirmation('Exit (Quit)',
#         #          'There are unsaved changes.  Exit (Quit) anyway?')
#         #    if result != wx.ID_YES:
#         #        return
#         self.Close()
# 
#     def OnTreebook1TreebookPageChanged(self, event):
#         index = event.GetSelection()
#         name = self.treebook1.GetPageText(index)
#         ui.log("changed treebook to %s" % name)
#         if name == 'status log':
#             self.status_log_ListPanel.block.SetValue( str(ui.ShowLogs()) )
#         elif name == 'Proposals':
#             msg = str(self.proposals)
#             textctrl = self.widget[name].block
#             textctrl.Clear()
#             textctrl.WriteText( msg )
#         elif name == 'Reports':
#             msg = self.MakeReport()
#             self.widget[name].block.SetValue( msg )
#         elif name == 'Strengths':
#             msg = Analysis.DescriptionPanel(self)
#             self.widget[name].block.SetValue( msg )
#         elif name.startswith('email '):
#             member = name[len('email '):]
#             msg = self.MakeEmail(self.team.db[member])
#             self.widget[name].block.SetValue( msg )
#         else:
#             #print "page:", index, name
#             print "treebook: <%s>" % name
#             ui.log("unhandled treebook page %d (%s)" % (index, name) )
#         
#     # ===============================================================
# 
#     def init_data(self):
#         '''
#         Read in the lists of proposals and reviewers
#         '''
#         self.team = Reviewers.Reviewers(config.PANEL_FILE)
#         self.team.readXml()
#         ui.log('panel data from: %s' % config.PANEL_FILE)
#         self.proposals = Proposals.Proposals(config.PROPOSALS_FILE)
#         # note that self.team.topics is a list
#         self.proposals.SetTopics(self.team.topics)
#         self.proposals.SetAnalysisFile(config.ANALYSIS_FILE)
#         self.proposals.readXml()
#         ui.log('proposals data from: %s' % config.PANEL_FILE)
# 
#     def init_TreeBook(self, treebook):
#         '''
#         Populate the wx.treebook instance
#         
# 		:param treebook: parent object
#         '''
#         item = ListPanel.ListPanel(treebook, str(self.team))
#         treebook.AddPage(item, 'Reviewers')
#         for member in self.team.reviewers():
#             ref = self.team.db[member]
#             item = ReviewerPanel.ReviewerPanel(treebook, ref)
#             treebook.AddSubPage(item, member)
#         treebook.ExpandNode(0, True)
# 
#         item = ListPanel.ListPanel(treebook, str(self.proposals))
#         # TODO: consider using a GridStringTable() instead
#         self.widget['Proposals'] = item
#         treebook.AddPage(item, 'Proposals')
#         for prop_id in self.proposals.proposals():
#             item = ProposalPanel.ProposalPanel(treebook, 
#                                                self,
#                                                self.proposals.db[prop_id], 
#                                                self.team)
#             treebook.AddSubPage(item, str(prop_id))
# 
#         # Reports is empty for now, will make when page is selected
#         item = ListPanel.ListPanel(treebook, "") 
#         self.widget['Reports'] = item
#         treebook.AddPage(item, 'Reports')
#         for member in self.team.reviewers():
#             #msg = self.MakeEmail(self.team.db[member])
#             msg = "" # empty for now, will make when page is selected
#             item = ListPanel.ListPanel(treebook, msg)
#             key = "email %s" % member
#             treebook.AddSubPage(item, key)
#             self.widget[key] = item
# 
#         # Strengths
#         item = ListPanel.ListPanel(treebook, "") 
#         self.widget['Strengths'] = item
#         treebook.AddPage(item, 'Strengths')
# 
#         self.analysis_grid = Analysis.AnalysisGrid(treebook, self)
#         treebook.AddSubPage(self.analysis_grid, 'Analysis Grid')
#         
#         # TODO: could add "Export Analysis Grid..."
#         # TODO: could add "Print Analysis Grid..."
#         
#         w = Analysis.AssignProposalTopicValues(treebook, self)
#         treebook.AddSubPage(w, 'Assign Proposal Topic Values')
# 
#         item = ListPanel.ListPanel(treebook, str(ui.ShowLogs()))
#         treebook.AddPage(item, 'status log')
#         self.status_log_ListPanel = item
# 
#         ui.log('treebook initialized')
# 
#     def RequestConfirmation(self, command, text):
#         '''
#         Present a dialog asking user to confirm step
# 
#         :param command: action to be confirmed
#         :type command: string
#         :param text: message to user
#         :type text: string
#         '''
#         # confirm this step
#         ui.log('Request Confirmation: (%s) (%s)' % (command, text) )
#         confirmation = 'Confirm %s' % command
#         dlg = wx.MessageDialog(self, text, confirmation, wx.YES|wx.NO)
#         result = dlg.ShowModal()
#         dlg.Destroy()           # destroy first
#         if result == wx.ID_YES:
#             ui.log('accepted request: %s' % command)
#         else:
#             ui.log('canceled request: %s' % command)
#         return result
# 
#     def MakeEmail(self, reviewer):
#         '''
#         Create the email message for a reviewer
# 
#         :param reviewer: instance of a Reviewer object
#         :type reviewer: object
#         :return: (multiline) email message
#         :rtype: string
#         '''
#         cycle = self.proposals.cycle
#         name = reviewer.db['full_name']
#         email = reviewer.db['email']
#         assignments = self.GetAssignments(name)
# 	venue = config.REVIEW_VENUE
#         return ui.EmailMsg(name, email, cycle, 
# 	                   assignments[0], assignments[1], venue)
# 
#     def GetAssignments(self, this_reviewer):
#         '''
#         Find the proposals assigned to a named reviewer
# 
#         :param this_reviewer: name of the reviewer
#         :param type: string
#         :return: tuple of primary, secondary = ([], [])
#         '''
#         assignments = ([], [])
#         for prop_id in self.proposals.proposals():
#             prop = self.proposals.db[prop_id]
#             reviewers = prop.db['eligible_reviewers']
#             if this_reviewer in reviewers:
#                 assignment = reviewers[this_reviewer]
#             else:
#                 # this reviewer is not eligible
#                 assignment = None
#             if assignment in ('1', '2'):
#                 assignments[int(assignment)-1].append( prop_id )
#         return assignments
# 
#     def MakeReport(self):
#         '''
#         Create the content of the Reports page
# 
#         :return: multiline text
#         :rtype: string
#         '''
#         msg = []
#         msg.append( 'total number of proposals: %d' % len(self.proposals.proposals()) )
#         v = float( len(self.proposals.proposals()) ) / len( self.team.reviewers() )
#         msg.append( 'primary proposals/reviewer: %.1f' % v )
# 
#         msg.append('')
#         msg.append('Overall topic weight: TBA')  # TODO: calculate the overall weight
# 
#         assignments = {}
#         for name in self.team.reviewers():
#             assignments[name] = self.GetAssignments(name)
#         msg.append('')
#         msg.append('Reviewer Primary assignments:')
#         for name in self.team.reviewers():
#             primaries = "\t".join(assignments[name][0])
#             msg.append( '%-25s\t%d:\t%s' % (name, len(assignments[name][0]), primaries) )
#         msg.append('')
#         msg.append('Reviewer Secondary assignments:')
#         for name in self.team.reviewers():
#             secondaries = "\t".join(assignments[name][1])
#             msg.append( '%-25s\t%d:\t%s' % (name, len(assignments[name][1]), secondaries) )
# 
#         liszt = []
#         for prop_id in self.proposals.proposals():
#             rr = self.proposals.db[prop_id].getReviewers()
#             if rr[0] == None or rr[1] == None:
#                 liszt.append( prop_id )
#         msg.append('')
#         if len(liszt) > 0:
#             msg.append('Unassigned proposals:\t' + "\t".join(liszt))
#         else:
#             msg.append('No unassigned proposals')
# 
#         return "\n".join(msg)
# 
# 
#     # ===============================================================
