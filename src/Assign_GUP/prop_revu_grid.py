
'''
widgets of one Reviewer of one Proposal instance

.. rubric:: :class:`ProposalReviewerRow`

adds one row of widgets for possible Reviewer of Proposal

====================================================  ============================================================
Method                                                Description
====================================================  ============================================================
:meth:`~ProposalReviewerRow.getAssignment`            return which type of reviewer this is (0, 1, 2)
:meth:`~ProposalReviewerRow.setAssignment`            define which type of reviewer this is (0, 1, 2)
:meth:`~ProposalReviewerRow.setValue`                 set dotProduct value as percentage
:meth:`~ProposalReviewerRow.setEnabled`               enable/disable the checkboxes based on Reviewer eligibility
:meth:`~ProposalReviewerRow.dotProduct`               compute and set widget with dot product of reviewer & proposal topics
====================================================  ============================================================

.. rubric:: :class:`ReviewerAssignmentGridLayout`

QGridLayout of possible Reviewers of Proposal

====================================================  ============================================================
Method                                                Description
====================================================  ============================================================
:meth:`~ReviewerAssignmentGridLayout.addReviewer`     add controls for one Reviewer to the grid
:meth:`~ReviewerAssignmentGridLayout.addReviewers`    add list of Reviewers to the grid
:meth:`~ReviewerAssignmentGridLayout.setEnabled`      enable/disable one Reviewer
:meth:`~ReviewerAssignmentGridLayout.setProposal`     specify the Proposal associated with this grid
:meth:`~ReviewerAssignmentGridLayout.setAssignment`   define the type for a named Reviewer 
:meth:`~ReviewerAssignmentGridLayout.onCheck`         ensure only one reviewer is either primary or secondary
:meth:`~ReviewerAssignmentGridLayout.setValue`        set dotProduct value of a named Reviewer as percentage
:meth:`~ReviewerAssignmentGridLayout.clearLayout`     **deprecated**
====================================================  ============================================================

-----
'''

from PyQt4 import QtCore, QtGui

# TODO: refactor to setup widgets rows for all reviewers first
# edit contents for each proposal

class CustomSignals(QtCore.QObject):
    '''custom signals'''
    
    checkBoxGridChanged = QtCore.pyqtSignal()


class ProposalReviewerRow(QtCore.QObject):
    '''
    Adds a row of widgets to an existing grid layout for one Reviewer of one Proposal instance
    '''

    def __init__(self, parent, layout, reviewer, proposal):
        '''
        :param obj parent: owner (a QWidget subclass)
        :param obj layout: layout in which to place these widgets
        :param obj reviewer: instance of reviewer.AGUP_Reviewer_Data
        :param obj proposal: instance of proposal.AGUP_Proposal_Data
        '''
        self.parent = parent
        self.layout = layout
        self.reviewer = reviewer
        self.proposal = proposal
        self.enabled = False

        QtCore.QObject.__init__(self, parent)

        self.comfort = ""
        self.custom_signals = CustomSignals()
        self._init_controls_()
        self.dotProduct()

    def _init_controls_(self):
        '''
        Build one row of the GUI panel with a reviewer for this proposal::

            [ ]       [ ]         1%        I. M. A. Reviewer
        
        '''
        self.primary = QtGui.QCheckBox()
        self.secondary = QtGui.QCheckBox()
        self.percentage = QtGui.QLabel()
        self.full_name = QtGui.QLabel(self.reviewer.getFullName())
        self.setValue(-1)

        w = self.layout.addWidget(self.primary)
# FIXME:         self.layout.setAlignment(w, QtCore.Qt.AlignCenter)
        w = self.layout.addWidget(self.secondary)
# FIXME:         self.layout.setAlignment(w, QtCore.Qt.AlignCenter)
        w = self.layout.addWidget(self.percentage)
# FIXME:         self.layout.setAlignment(w, QtCore.Qt.AlignRight)
        w = self.layout.addWidget(self.full_name)

        self.primary.setEnabled(self.enabled)
        self.secondary.setEnabled(self.enabled)

#         self.primary.setTristate(False)
#         self.secondary.setTristate(False)

        self.primary.setToolTip("check to select as primary reviewer (#1)")
        self.secondary.setToolTip("check to select as secondary reviewer (#2)")
        self.percentage.setToolTip("computed comfort factor of this reviewer with this proposal")

        self.primary.clicked.connect(lambda: self.onCheckBoxClick(self.primary))
        self.secondary.clicked.connect(lambda: self.onCheckBoxClick(self.secondary))
    
    def onCheckBoxClick(self, widget):
        '''
        either check box was clicked
        '''
        self.rowCheck(widget)
        self.custom_signals.checkBoxGridChanged.emit()
    
    def rowCheck(self, checkbox):
        '''
        ensure at most one checkbox (primary or secondary) is checked for this reviewer
        
        :param obj checkbox: instance of QCheckBox
        '''
        if checkbox == self.primary:
            if self.isPrimaryChecked():
                self.setSecondaryState(False)
        else:   # MUST be secondary, then
            if self.isSecondaryChecked():
                self.setPrimaryState(False)
    
    def getAssignment(self):
        '''
        report which type of reviewer this is
        
        =======   =======================
        returns   description
        =======   =======================
        0         unassigned
        1         primary reviewer (#1)
        2         secondary reviewer (#2)
        =======   =======================
        '''
        if self.isPrimaryChecked():
            return 1
        elif self.isSecondaryChecked():
            return 2
        return 0

    def setAssignment(self, code):
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
        if code == 0:           # unassigned
            self.setPrimaryState(False)
            self.setSecondaryState(False)
        elif code == 1:
            self.setPrimaryState(True)
        elif code == 2:
            self.setSecondaryState(True)
        self.onCheckBoxClick(self.primary)
        self.onCheckBoxClick(self.secondary)

    def setValue(self, percentage):
        '''
        set the percentage value
        
        :param int percentage: dot product of reviewer and proposal topic strengths
        '''
        self.percentage.setText(str(percentage) + ' %')
    
    def isPrimaryChecked(self):
        return self.primary.checkState() != 0
    
    def setPrimaryState(self, state):
        if self.primary.isChecked() != state:
            self.primary.setChecked(state)
            if state:
                self.secondary.setChecked(False)
    
    def isSecondaryChecked(self):
        return self.secondary.checkState() != 0
    
    def setSecondaryState(self, state):
        if self.secondary.isChecked() != state:
            self.secondary.setChecked(state)
            if state:
                self.primary.setChecked(False)
    
    def setEnabled(self, state=True):
        if state != self.enabled:
            self.primary.setEnabled(state)
            self.secondary.setEnabled(state)
            self.enabled = state

    def dotProduct(self):
        r'''
        dot product of Proposal and Reviewer topic strengths, :math:`\vec{p} \cdot \vec{r}`
        
        Computes :math:`\vec{p} \cdot \vec{r}` where:
        
        * :math:`\vec{p}` is array of topic value strengths for Proposal
        * :math:`\vec{r}` is array of topic value strengths for Reviewer
        
        '''
        if self.proposal and self.reviewer:
            dot = self.proposal.topics.dotProduct(self.reviewer.topics)
        else:
            dot = 0.0
        self.setValue(int(100*dot+0.5))


class ReviewerAssignmentGridLayout(QtGui.QGridLayout):
    '''
    display and manage the assignment checkboxes and reported percentages for each reviewer on this proposal
    '''
    
    def __init__(self, parent, proposal):
        self.parent = parent
        self.proposal = None

        QtGui.QGridLayout.__init__(self, parent)

        self._init_basics()
    
    def _init_basics(self):
        self.setColumnStretch(0, 1)
        self.setColumnStretch(1, 1)
        self.setColumnStretch(2, 1)
        self.setColumnStretch(3, 3)
        self.addWidget(QtGui.QLabel('R1', styleSheet='background: #888; color: white'))
        self.addWidget(QtGui.QLabel('R2', styleSheet='background: #888; color: white'))
        self.addWidget(QtGui.QLabel('%', styleSheet='background: #888; color: white'))
        self.addWidget(QtGui.QLabel('Reviewer Name', styleSheet='background: #888; color: white'))
        self.rvrw_widgets = {}
    
    def addReviewer(self, rvwr):
        '''
        add this reviewer object for display
        '''
        row_widget = ProposalReviewerRow(self.parent, self, rvwr, self.proposal)
        self.rvrw_widgets[rvwr.getSortName()] = row_widget
        row_widget.custom_signals.checkBoxGridChanged.connect(lambda: self.onCheck(row_widget))

    def addReviewers(self, reviewers):
        '''
        add a list of reviewers
        '''
        if self.proposal is not None:
            for rvwr in reviewers:
                if rvwr is not None:
                    self.addReviewer(rvwr)
                    dot = self.proposal.topics.dotProduct(rvwr.topics)
            for full_name, assignment in self.proposal.eligible_reviewers.items():
                rvwr = reviewers.getByFullName(full_name)
                sort_name = rvwr.getSortName()
                self.rvrw_widgets[sort_name].setEnabled(True)   # eligible means True
                self.rvrw_widgets[sort_name].setAssignment(assignment or 0)

    def clearLayout(self):
        '''
        remove all the reviewer rows in the layout
        '''
        # thanks: http://www.gulon.co.uk/2013/05/01/clearing-a-qlayout/
        # TODO: causes unnecessary widget blinking, refactor to reuse widgets instead
        # enable/disable eligible reviewers per each proposal
        for i in reversed(xrange(self.count())):
            self.itemAt(i).widget().setParent(None)
        self._init_basics()
    
    def setProposal(self, proposal):
        '''
        declare which proposal is associated with this grid
        '''
        self.proposal = proposal
    
    def setAssignment(self, sort_name, code):
        '''
        define which type of reviewer this is
        
        :param str sort_name: reviewer's identifying key
        :param int code: integer code (0 | 1 | 2)
        '''
        self.rvrw_widgets[sort_name].setAssignment(code)
    
    def setValue(self, sort_name, percentage):
        '''
        set the percentage value
        '''
        widget = self.rvrw_widgets[sort_name]
        widget.setValue(percentage)

    def onCheck(self, row_widget):
        '''
        ensure only one reviewer is either primary or secondary
        '''
        assignment = row_widget.getAssignment()
        if assignment > 0:
            for row in self.rvrw_widgets.values():
                if row != row_widget:
                    {1: row.setPrimaryState, 2: row.setSecondaryState}[assignment](False)
    
    def setEnabled(self, sort_name, state=True):
        '''
        enable (True) or disable (False) a Reviewer identified by sort_name
        
        All eligible Reviewers are enabled.
        Reviewers become ineligible when they are named as part of the Proposal team.
        '''
        self.rvrw_widgets[sort_name].setEnabled(state)


def project_main():
    '''
        create QGroupBox + QGridLayout and run the panel

        ====   ====   =======   =========================
        R1     R2     %         Reviewer Name
        ====   ====   =======   =========================
        [x]    [ ]    100%      Joe User
        [ ]    [x]    80%       Second Reviewer
        [ ]    [ ]    22%       Some Panel Member
        [ ]    [ ]    1%        Another Panel Member
        ====   ====   =======   =========================
    '''
    import sys
    import os
    import agup_data
    global layout

    testfile = os.path.abspath('project/agup_project.xml')
    test_gup_id = str(941*9*5)

    agup = agup_data.AGUP_Data()    
    agup.openPrpFile(testfile)
    proposal = agup.proposals.proposals[test_gup_id]

    app = QtGui.QApplication(sys.argv)
    grid = QtGui.QGroupBox('prop_revu_grid demo')

    layout = ReviewerAssignmentGridLayout(grid, proposal)
    layout.setProposal(proposal)
    layout.addReviewers(agup.reviewers)
#     layout.clearLayout()
#     layout.addReviewers(agup.reviewers)
    layout.setEnabled('0-Myers', False)
    timer = QtCore.QTimer()
    timer.singleShot(2000, onDelay)

    grid.show()
    sys.exit(app.exec_())


def onDelay():
    global layout
    layout.setEnabled('0-Myers', True)
    layout.setEnabled('Jemian', False)


if __name__ == '__main__':
    # AGUP_main()
    project_main()
