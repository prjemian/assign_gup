#!/usr/bin/env python
# -*- coding: iso-8859-1 -*- 

'''runs the Assign_GUP application'''

import os, sys

# locate project sources
__basepath__ = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
if os.path.exists(__basepath__):
    sys.path.insert(0, __basepath__)
import Assign_GUP

config.set_review(CYCLE, VENUE)
Assign_GUP.main_window.main()
