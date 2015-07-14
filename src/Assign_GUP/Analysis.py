#!/usr/bin/env python

'''
Analyze the proposals:
    
*    [ ] automatically assign weights to the various topics
*    [*] evaluate weight of each reviewer on each proposal based on dot product of topics
*    [ ] rank reviewers in order for each proposal
*    [ ] assign reviewers to proposals
'''

import ui
import wx


def DescriptionPanel(*args):
    msg = '''Under Construction'''
    return msg


def ComputeScore(main_obj, proposal_number, reviewer_name):
    '''
    compute the topic dot product of this reviewer on this proposal
    
    :param obj main_obj: instance of Main object
    :param str proposal_number: GUP proposal number
    :param str reviewer_name: reviewer (full) name
    '''
    proposal_object = main_obj.proposals.db[proposal_number]
    reviewer_object = main_obj.team.db[reviewer_name]
    return ui.DotProduct(proposal_object, reviewer_object)


def StrengthGrid(parent, main_obj):
    '''build a wx.Grid object showing the topic dot product of proposals and reviewers
    
    :param obj parent: widget containing this wx.Grid object
    :param obj main_obj: instance of Main object
    '''
    prop_num_list = main_obj.proposals.sorted_proposals_list
    reviewer_list = main_obj.team.sorted_reviewers_list
    rows = len(prop_num_list)
    cols = len(reviewer_list)
    
    grid = wx.grid.Grid(parent, -1)
    grid.CreateGrid(rows, cols)

    for col, label in enumerate(reviewer_list):
        grid.SetColLabelValue(col, label)
    for row, label in enumerate(prop_num_list):
        grid.SetRowLabelValue(row, label)
    for row, gup_num in enumerate(prop_num_list):
        for col, reviewer in enumerate(reviewer_list):
            grid.SetCellValue(row, col, 'uncomputed')
    return grid


def RecomputeStrengthGrid(grid, main_obj):
    '''
    fill the cells in the grid with reviewer strength and color by assignment

    :param obj main_obj: object returned by StrengthGrid()
    :param obj main_obj: instance of Main object
    '''
    prop_num_list = main_obj.proposals.sorted_proposals_list
    reviewer_list = main_obj.team.sorted_reviewers_list
    rows = len(prop_num_list)
    cols = len(reviewer_list)
    bgColors = {None: 'white', '1': '#99ff99', '2': '#ccffcc'}
    
    for row, gup_num in enumerate(prop_num_list):
        for col, reviewer in enumerate(reviewer_list):
            score = ComputeScore(main_obj, gup_num, reviewer)
            grid.SetCellValue(row, col, "%d%%" % int(0.5 + 100*score))
            # color the cell backgrounds based on reviewer assignments
            eligibles = main_obj.proposals.db[gup_num].db['eligible_reviewers']
            try:
                assignment = eligibles[reviewer]
                bgColor = bgColors[assignment]
            except:
                bgColor = bgColors[None]
            grid.SetCellBackgroundColour(row, col, bgColor)


def AnalysisGrid(parent, main_obj):
    '''build a wx.Grid object with a StrengthAnalysis() for all proposals and reviewers
    
    The grid will be added to ``parent`` and filled with data from ``main_obj``
    '''
    #db = StrengthAnalysis(main_obj.proposals.db, main_obj.team.db)
    grid = StrengthGrid(parent, main_obj)
    RecomputeStrengthGrid(grid, main_obj)
    return grid


def AssignProposalTopicValues(*args):
    msg = 'develop code to automatically assign proposal topic values'
    return None


if __name__ == '__main__':
    pass
