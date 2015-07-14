#!/usr/bin/env python
# -*- coding: iso-8859-1 -*- 

'''runs the Assign_GUP application'''

import os, sys

# locate project sources
__basepath__ = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
if os.path.exists(__basepath__):
    sys.path.insert(0, __basepath__)
from Assign_GUP import Assign_GUP, config


# http://www.aps.anl.gov/Users/Calendars/GUP_Calendar.htm
VENUE = 'in Building 401 on Tuesday, 24 March 2015'
CYCLE = config.pick_latest_cycle()
#CYCLE = '2015-2'

config.set_review(CYCLE, VENUE)
Assign_GUP.main()
