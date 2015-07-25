#!/usr/bin/env python

'''
(internal) support for forms defined in .ui files
'''

# Copyright (c) 2009 - 2015, UChicago Argonne, LLC.
# See LICENSE file for details.


import os
import inspect
from PyQt4 import QtGui, uic, QtCore


FORMS_SUBDIRECTORY = 'resources'
FORM_CACHE = None


def get_forms_path():
    '''identify our resources directory'''
    # assume this is less risky than __file__
    ref = inspect.getsourcefile(get_forms_path)
    path = os.path.abspath(os.path.dirname(ref))
    return os.path.join(path, FORMS_SUBDIRECTORY)


def load_form(form_name, parent = None):
    '''
    loads a .ui file from our FORMS_SUBDIRECTORY (or cache if found previously)
    
    :param str form_name: name of .ui file (not including path)
    :param obj parent: parent window object
    :returns obj: instance of QFile with content defined in .ui file
    :raises: RuntimeError if uifile cannot be found
    '''
    uifile = os.path.join(get_forms_path(), form_name)
    return loadUiWidget(uifile, parent)


def loadUiWidget(uifilename, parent=None):
    '''
    loads a .ui file created by Qt Creator or Designer
    
    :param str uifilename: name of .ui file (including path)
    :param obj parent: parent window object
    :returns obj: instance of QFile with content defined in .ui file
    :raises: RuntimeError if uifile cannot be found
    '''
    global FORM_CACHE
    if FORM_CACHE is None:
        FORM_CACHE = {}
    if uifilename not in FORM_CACHE:
        FORM_CACHE[uifilename] = uic.loadUi(uifilename)
    return FORM_CACHE[uifilename]
