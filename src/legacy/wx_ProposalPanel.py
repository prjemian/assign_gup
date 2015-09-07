
'''
GUI wx.Panel to provide edit controls for one Proposal instance
'''

import wx
import ui
import pprint
import ProposalReviewerRow
import time
import config
import Analysis


# TODO: need a way to mark proposals as correlated
# TODO: could add a "notes" field for me
# TODO: automatically trigger [Save] button press after entering changes in reviewer or topic (~5 sec delay), checkbox/menu controlled


DEFAULT_COLOR = (240, 240, 240, 255)


class ProposalPanel(wx.Panel):
    '''
    Creates a GUI wxPanel to provide edit controls for one Proposal instance
    '''

    def __init__(self, parent, main_obj, proposal, reviewers):
        '''
        :param obj parent: owner (treebook object)
        :param obj main_obj: instance of Main object
        :param obj proposal: instance of Proposal object
        :param obj reviewers: instance of Reviewers object
        '''
        self.treebook = parent
        self.main_obj = main_obj
        self.proposal = proposal
        self.reviewers = reviewers
        self.recomputeTriggered = False
        self.recomputeNeeded = False
        self.recompute_poll_interval_ms = config.RECOMPUTE_POLL_INTERVAL_MS
        self.recompute_delay_s = config.RECOMPUTE_DELAY_S       # TODO: make this a user choice
        self.auto_recompute = config.AUTO_RECOMPUTE             # TODO: make this a user choice
        self.recompute_target_time = time.time()
        wx.Panel.__init__(self, parent=self.treebook, id=wx.ID_ANY)
        self._init_two_panels_()
        self.recomputePoll()            # start polling in case a recomputation is needed
        self.panel_is_dirty = False
        self.ClearDirty()
        self.save_button.Disable()
        self.save_button.SetBackgroundColour(DEFAULT_COLOR)
        self.revert_button.Disable()

    def _init_two_panels_(self):
        '''
        Make two (sub)panels.
        Use subroutines to set up the subpanels.
        This avoids confusion with the sizers.
        '''
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.widgets = {}
        
        main = wx.Panel(self)
        sizer.Add(main, 1, wx.ALL | wx.GROW | wx.EXPAND, 5)
        self._init_main_panel_(main)
        
        side = wx.Panel(self)
        sizer.Add(side, 0, wx.ALL | wx.GROW | wx.EXPAND, 5)
        self._init_side_panel_(side)
        
        # TODO need to show somewhere reviewers in order of highest Topics score to lowest
        
        self.SetSizer(sizer)

    def _init_main_panel_(self, panel):
        '''
        set up most text entry fields
        
        :param panel: container
        '''
        sizer = wx.FlexGridSizer(cols=2)

        sizer.AddGrowableCol(1, 1) 
        # TODO Can we use a Validator() method to populate the entry widgets?
        row = -1
        for dct in self.proposal.TellUI():
            if dct['set'] == 'main':
                row += 1
                dct['row'] = row
                self.widgets[dct['key']] = ui.make(panel, sizer, dct)
            
        # add another row with some buttons
        sizer.Add(wx.StaticText(panel, wx.ID_ANY, label="", style=0), 0, wx.ALL, 5)
        buttonPanel = wx.Panel(panel)
        sizer.Add(buttonPanel, 1, wx.ALL | wx.GROW | wx.EXPAND, 5)
        
        boxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.save_button = wx.Button(buttonPanel, label="Save")
        self.revert_button = wx.Button(buttonPanel, label="Revert")
        boxSizer.Add(self.save_button, 0, wx.ALL, 5)
        boxSizer.Add(self.revert_button, 0, wx.ALL, 5)
        self.save_button.Bind(wx.EVT_BUTTON, self.OnSaveButtonPush)
        self.revert_button.Bind(wx.EVT_BUTTON, self.OnRevertButtonPush)
        buttonPanel.SetSizer(boxSizer)

        # TODO: could put composite score here in 1st column
        # recompute composite when topics are re-scored or reviewers assigned
        sizer.Add(wx.StaticText(panel, wx.ID_ANY, label="", style=0), 0, wx.ALL, 5) # skip 1st column
        sizer.Add(self._init_reviewer_panel_(panel), 1, wx.ALL | wx.GROW | wx.EXPAND, 5)

        panel.SetSizer(sizer)

    def _init_reviewer_panel_(self, parent):
        '''
        Build the GUI panel with the table of the reviewers for this proposal

        =======   =========   =======   =========================
        primary   secondary   comfort   Reviewer Name
        =======   =========   =======   =========================
        [ ]       [ ]         1%        Panel Member
        [x]       [ ]         100%      Joe User
        [ ]       [x]         80%       Second Reviewer
        =======   =========   =======   =========================
        
        For compatibility with our ui module and the Save/Revert button actions,
        ProposalReviewerRow is a class for each row in the table above with the correct signature
        as well as a SetComfortText(value) method.  SetValue() should set/clear the
        checkboxes for that reviewer based on value of 0, 1, or 2, respectively above.
        
        :param parent: panel that contains this table
        '''
        panel = wx.Panel(parent)
        sizer = wx.FlexGridSizer(cols=4)
        panel.SetSizer(sizer)
        sizer.AddGrowableCol(3, 1) 

        for text in ('R1', 'R2', '%', 'Reviewer Name'):
            label = wx.StaticText(panel, wx.ID_ANY, label=text, style=0)
            sizer.Add(label, 0, wx.ALL, 5)

        self.propRevRows = []
        for dct in self.proposal.TellUI():
            if dct['set'] in ('eligible',):
                key = dct['key']
                rev = self.reviewers.db[key]
                eligibles = self.proposal.db['eligible_reviewers']
                assignmentCode = 0
                if key in eligibles:
                    assignmentCode = eligibles[key]
                    if assignmentCode == None:
                        assignmentCode = 0
                comfort = int(100*ui.DotProduct(self.proposal, rev))
                w = ProposalReviewerRow.ProposalReviewerRow(panel, 
                                        sizer, self.CrossCheck, key, self)
                w.SetValue(int(assignmentCode))
                w.SetComfortText(comfort)
                self.propRevRows.append( w )
                self.widgets[dct['key']] = w

        return panel

    def _init_side_panel_(self, panel):
        '''
        set topic fields
        
        :param panel: container
        '''
        sizer = wx.FlexGridSizer(cols=3)
        row = -1
        self.topicWidgets = {}
        for dct in self.proposal.TellUI():
            if dct['set'] in ('topic',):
                row += 1
                dct['row'] = row
                w = ui.make(panel, sizer, dct)
                self.widgets[dct['key']] = w
                label = wx.StaticText(panel, wx.ID_ANY, style=0)
                sizer.Add(label, 0, wx.ALL, 5)
                self.topicWidgets[ dct['key'] ] = w
                w.Bind(wx.EVT_CHAR, self.OnTopicEdit)
                # TODO: should re-compute comfort when topic values are changed
        panel.SetSizer(sizer)

    def CrossCheck(self, caller):
        '''
        Ensure that no two reviewers have 
        primary or secondary as their assignment.
        Responds to a checkbox click in any ProposalReviewerRow object
        and checks all the other objects to make sure they do not have 
        the same reviewer selection.  If they do, their selection is cleared.
        
        :param obj caller: ProposalReviewerRow object with the checkbox that was clicked
        '''
        code = caller.GetValue()
        for panelist in self.propRevRows:
            if caller != panelist:
                if panelist.GetValue() == code:
                    panelist.SetValue(0)

    def OnSaveButtonPush(self, event):
        '''
        Handle a push of the Save button
        
        :param event: event object
        '''
        liszt = []
        for dct in self.proposal.TellUI():
            key = dct['key']
            dct['entry'] = self.widgets[key].GetValue()
            liszt.append( dct )
        self.proposal.SaveUI(liszt)
        self.ClearDirty()
        ui.log('SaveUI(%s)' % str(self.proposal))
        self.save_button.SetBackgroundColour(DEFAULT_COLOR)
        self.save_button.Disable()
        self.revert_button.Disable()

    def OnRevertButtonPush(self, event):
        '''
        Handle a push of the Revert button
        
        :param event: event object
        '''
        for dct in self.proposal.TellUI():
            key = dct['key']
            value = dct['entry']
            if value == None: value = ""
            self.widgets[key].SetValue( str(value) )
        self.ClearDirty()
        ui.log('RevertEdits(%s)' % str(self.proposal))
        self.save_button.SetBackgroundColour(DEFAULT_COLOR)
        self.save_button.Disable()
        self.revert_button.Disable()

    def OnTopicEdit(self, event):
        '''
        Handle an edit event from a Topic text entry widget.
        This will trigger a re-computation of the reviewer comfort factors and overall score.
        
        :param event: event object
        '''
        self.recomputeTriggered = True
        self.SetDirty()
        event.Skip()
    
    def recomputePoll(self):
        '''
        Start a recomputeComforts() when self.recomputeTriggered is True.
        
        Start recomputePoll polling for self.recomputeTriggered. 
        We need to do this because we want to be smart about
        recomputation and wait for the user to pause.
        
        Set a user-adjustable delay of ~10 s (self.recompute_delay_s).
        This behavior should also be user-selectable (self.auto_recompute).
        It is possible that there may already be a trigger in the queue (self.recomputeNeeded).
        If so, just reset the delay of the queued trigger (self.recompute_target_time).
        '''
        if self.recomputeTriggered:
            self.recomputeTriggered = False
            if self.auto_recompute:
                self.recompute_target_time = time.time() + self.recompute_delay_s
                self.recomputeNeeded = True
        if self.recomputeNeeded and self.auto_recompute and time.time() > self.recompute_target_time:
            self.recomputeNeeded = False
            # --------------------------------------
            # TODO: pull all the widget text fields here
            for k, v in self.topicWidgets.items():
                self.proposal.db['topics'][k] = v.GetValue()    # FIXME: This breaks [Revert]
            # --------------------------------------
            self.recomputeComforts()
        self.recompute_timer = wx.PyTimer(self.recomputePoll)
        self.recompute_timer.Start(self.recompute_poll_interval_ms)
    
    def recomputeComforts(self):
        '''
        Recompute the comfort factors for each reviewer,
        usually in response to an edit event on the topic weightings.
        '''
        for row in self.propRevRows:
            name = row.reviewer
            rev = self.reviewers.db[name]
            comfort = int(100*ui.DotProduct(self.proposal, rev))
            row.SetComfortText(comfort)
            #print row.reviewer
            ui.log("recomputed reviewer strength, %s: %d%%" % (row.reviewer, comfort))
        # TODO: compute the composite score
        # TODO: need algorithm for composite score
        Analysis.RecomputeStrengthGrid(self.main_obj.analysis_grid, self.main_obj)
    
    def SetDirty(self):
        '''note if new edits have not been saved'''
        self.save_button.Enable()
        self.save_button.SetBackgroundColour(wx.RED)
        self.revert_button.Enable()
        self.panel_is_dirty = True
    
    def ClearDirty(self):
        self.panel_is_dirty = False

    def isDirty(self):
        '''report if new edits have not been saved'''
        return self.panel_is_dirty


if __name__ == '__main__':
    pass
