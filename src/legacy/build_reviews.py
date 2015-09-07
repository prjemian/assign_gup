'''
Build the content of the text file for adding reviews for a reviewer.
'''

import os
from lxml import etree
import config
import Proposals


CYCLE = config.pick_latest_cycle()
#CYCLE = '2015-2'            # picks the subdirectory of ../../data/
VENUE = 'ignored here'
REVIEWER = 'Peter Jemian'   # must match one of the reviewers exactly in analysis.xml


def review_text_template(assignments, template = config.REVIEW_TEXT_TEMPLATE, proposals=None):
    '''build the entire file, based on the template'''
    result = []
    for reviewer_number, role in enumerate(('primary', 'secondary')):
        print '# %s assignments' % role
        print '# ' + ' '.join(assignments[role])
        print '#'
    print ''
    for reviewer_number, role in enumerate(('primary', 'secondary')):
        result.append( '# %s assignments' % role + '\n'*2 )
        for gup_number in sorted(assignments[role]):
            gup = str(gup_number)
            if proposals is not None:
                gup += "\nTitle: " + proposals.db[gup_number].db['proposal_title']
            result.append( template % (gup, reviewer_number+1) )
    return '\n'.join(result)


def get_my_assignments(reviewer=REVIEWER):
    '''find my primary and secondary assignments for this cycle'''
    assignments = {'primary':[], 'secondary':[]}
    xmlfile = config.build_filename('analysis', 'xml')
    if os.path.exists(xmlfile):
        root= etree.parse(xmlfile).getroot()
        if root is not None:
            for reviewer_number, role in enumerate(('primary', 'secondary')):
                xpathStr = "//Reviewers[@reviewer%d='%s']" % (reviewer_number+1, reviewer)
                assignments[role] = [node.getparent().get('id') for node in root.xpath(xpathStr)]
                assignments[role].sort()
    return assignments


def main(reviewer, cycle, venue):
    config.set_review(cycle, venue)
    xmlfile = config.build_filename('proposals', 'xml')
    proposals = Proposals.Proposals(xmlfile, config.ANALYSIS_FILE)
    proposals.readXml()
    assignments = get_my_assignments(reviewer)
    print review_text_template(assignments, proposals=proposals)


if __name__ == '__main__':
    main(REVIEWER, CYCLE, VENUE)
