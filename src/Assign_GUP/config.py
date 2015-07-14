#!/usr/bin/env python

'''
basic configuration details

:param str APS_review_cycle: Defines the set of reviewers, proposals, and analyses
'''


import os
import glob

def pick_latest_cycle():
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    path_list = map(os.path.basename, sorted(glob.glob(os.path.join(data_path, '*-*'))))
    return path_list[-1]


#APS_review_cycle = '2015-1'
APS_review_cycle = pick_latest_cycle()
REVIEW_VENUE = 'in Building 401 on Monday, 17 November 2014'


def set_review(cycle, venue):
    '''set review cycle and venue'''
    global APS_review_cycle, REVIEW_VENUE, PANEL_FILE, PROPOSALS_FILE, ANALYSIS_FILE
    if APS_review_cycle is not None and REVIEW_VENUE is not None:
        APS_review_cycle = cycle
        REVIEW_VENUE = venue
        PANEL_FILE = build_filename('panel', 'xml')
        PROPOSALS_FILE = build_filename('proposals', 'xml')
        ANALYSIS_FILE = build_filename('analysis', 'xml')


def build_filename(name, ext):
    '''
    construct a file name using the APS cycle number
    
    :param str name: name of the type of file
    :param str ext: file extension (no preceding dot)
    '''
    srcpath = os.path.join(os.path.dirname(__file__), '..', '..')
    datapath = os.path.join(os.path.abspath(srcpath), 'data')
    target = os.path.join(datapath, APS_review_cycle, '%s.%s' % (name, ext))
    return target


PANEL_FILE = build_filename('panel', 'xml')
PROPOSALS_FILE = build_filename('proposals', 'xml')
ANALYSIS_FILE = build_filename('analysis', 'xml')
RECOMPUTE_POLL_INTERVAL_MS = 200
RECOMPUTE_DELAY_S = 1
AUTO_RECOMPUTE = True

REVIEW_TEXT_TEMPLATE = """
Proposal: %s
Requested shifts:    //	  (total/this/min)
Score:               
Total shifts:	     
Shifts this cycle:   
Reviewer %s:
Comments: 

"""


def main():
    print __file__
    set_review(APS_review_cycle, REVIEW_VENUE)
    for item in (PANEL_FILE, PROPOSALS_FILE, ANALYSIS_FILE):
        print item


if __name__ == '__main__':
    main()
