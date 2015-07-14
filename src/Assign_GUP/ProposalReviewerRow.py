
'''
Panel of widgets of one Reviewer of one Proposal instance
'''

import wx


class ProposalReviewerRow(wx.Panel):
    '''
    Adds a row of widgets to a panel for one Reviewer of one Proposal instance
    '''

    def __init__(self, parent, sizer, crossCheck, reviewer, prop_panel= None):
        '''
        :param obj parent: owner (a treebook)
        :param obj sizer: sizer in which to place these widgets
        :param obj crossCheck: external function to call when a CheckBox is clicked
        :param str reviewer: name of reviewer
        :param ProposalPanel prop_panel: owner of panel to set dirty if a change is made
        '''
        self.parent = parent
        self.sizer = sizer
        self.reviewer = reviewer  # TODO: should be a reviewer object?
        self.crossCheck = crossCheck
        self.comfort = ""
        self.assignment_code = 0
        self.prop_panel = prop_panel
        wx.Panel.__init__(self, parent=self.parent, id=wx.ID_ANY)
        self._init_controls_()

    def _init_controls_(self):
        '''
        Build one row of the GUI panel with the table of the reviewers for this proposal

        =======   =========   =======   =========================
        primary   secondary   comfort   Reviewer Name
        =======   =========   =======   =========================
        [x]       [ ]         100%      Joe User
        [ ]       [x]         80%       Second Reviewer
        [ ]       [ ]         1%        Panel Member
        =======   =========   =======   =========================
        '''
        self.rbPri = wx.CheckBox(self.parent, -1, '')
        self.rbSec = wx.CheckBox(self.parent, -1, '')
        self.stComfort = wx.StaticText(self.parent, wx.ID_ANY, label='-1', style=0)
        # TODO: get reviewer name from self.reviewer object
        self.stName = wx.StaticText(self.parent, wx.ID_ANY, label=self.reviewer, style=0)
        for obj in (self.rbPri, self.rbSec, self.stComfort, self.stName):
            self.sizer.Add(obj, 0, wx.ALL, 5)
        self.rbPri.SetToolTipString("check to select as primary reviewer (#1)")
        self.rbSec.SetToolTipString("check to select as secondary reviewer (#2)")
        self.stComfort.SetToolTipString("computed comfort factor of this reviewer with this proposal")
        self.rbPri.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxClick)
        self.rbSec.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxClick)

    def GetValue(self):
        '''
        return integer telling which type of reviewer this is
        
        ====   =======================
        code   description
        ====   =======================
        0      unassigned
        1      primary reviewer (#1)
        2      secondary reviewer (#2)
        ====   =======================
        
        :return: integer code (0 | 1 | 2)
        :rtype: int
        '''
        code = 0
        if self.rbPri.GetValue():
            code += 1
        if self.rbSec.GetValue():
            code += 2
        self.assignment_code = code
        return self.assignment_code

    def SetValue(self, code):
        '''
        define which type of reviewer this is
        
        ====   =======================
        code   description
        ====   =======================
        0      unassigned
        1      primary reviewer (#1)
        2      secondary reviewer (#2)
        ====   =======================
        
        :param int code: integer code (0 | 1 | 2)
        '''
        if code == "":                  # as called by ProposalPanel.OnRevertButtonPush()
            code = 0
        if type(code) == type(""):      # as called by ProposalPanel.OnRevertButtonPush()
            code = int(code)
        choices = {
                   0: [False, False],   # unassigned
                   1: [True, False],    # primary reviewer
                   2: [False, True],    # secondary reviewer
                   }
        if code in (0, 1, 2):
            if self.GetValue() != code:
                if self.prop_panel is not None:
                    self.prop_panel.SetDirty()
                self.assignment_code = code
                settings = choices[code]
                self.rbPri.SetValue(settings[0])
                self.rbSec.SetValue(settings[1])
        

    def SetComfortText(self, comfort):
        '''
        Set the text of the computed comfort factor for this reviewer with this proposal
        
        :param str comfort: message to display (usually like "25%")
        '''
        if type(comfort) == type(1):
            comfort = "%d%%" % comfort
        self.comfort = comfort
        old_comfort = self.stComfort.GetLabel()
        self.stComfort.SetLabel(self.comfort)
        if self.prop_panel is not None and str(old_comfort).find('%') > -1:
            if old_comfort != comfort:
                self.prop_panel.SetDirty()
        
    def OnCheckBoxClick(self, event):
        '''
        Respond to clicks on the check boxes.
        This code ensures that at most one check box is checked for this reviewer.
        '''
        code = -1
        table = {True : 1, False : 0}
        if event.EventObject == self.rbPri:            # primary checkbox
            code = table[event.EventObject.GetValue()]
        elif event.EventObject == self.rbSec:          # secondary checkbox
            code = 2*table[event.EventObject.GetValue()]
        self.SetValue(code)
        if self.prop_panel is not None:
            self.prop_panel.SetDirty()
        if self.crossCheck:
            self.crossCheck(self)  # callback routine for full table handler

class _example(wx.App):
    '''
    demonstrate how this code works
    '''

    def OnInit(self):
        '''
        create an application frame and run the panel

        ====   ====   =======   =========================
        R1     R2     comfort   Reviewer Name
        ====   ====   =======   =========================
        [x]    [ ]    100%      Joe User
        [ ]    [x]    80%       Second Reviewer
        [ ]    [ ]    1%        Panel Member
        ====   ====   =======   =========================
        '''
        frame = wx.Frame(None, -1, "Hello from wxPython")

        panel = wx.Panel(frame)
        sizer = wx.FlexGridSizer(cols=4)
        panel.SetSizer(sizer)
        sizer.AddGrowableCol(3, 1) 

        for text in ('R1', 'R2', '%', 'Reviewer Name'):
            label = wx.StaticText(panel, wx.ID_ANY, label=text, style=0)
            sizer.Add(label, 0, wx.ALL, 5)
        
        self.reviewers = []
        for name in ("Joe User", "Second Reviewer", "Panel Member"):
            item = ProposalReviewerRow(panel, sizer, self.CrossCheck, name)
            self.reviewers.append( item )
        comforts = (100, 80, 1)
        roles = (1, 2, 0)
        for i in range(len(self.reviewers)):
            self.reviewers[i].SetValue(roles[i])
            self.reviewers[i].SetComfortText("%d%%" % comforts[i])

        frame.Show(True)
        self.SetTopWindow(frame)
        return True

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
        for panelist in self.reviewers:
            if caller != panelist:
                if panelist.GetValue() == code:
                    panelist.SetValue(0)


if __name__ == '__main__':
    app = _example(0)
    app.MainLoop()
