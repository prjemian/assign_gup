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


def loadUi(ui_file, baseinstance=None, **kw):
    '''
    load a .ui file for use in building a GUI
    
    Wraps `uic.loadUi()` with code that finds our program's
    *resources* directory.
    
    :see: http://nullege.com/codes/search/PyQt4.uic.loadUi
    :see: http://bitesofcode.blogspot.ca/2011/10/comparison-of-loading-techniques.html
    
    inspired by:
    http://stackoverflow.com/questions/14892713/how-do-you-load-ui-files-onto-python-classes-with-pyside?lq=1
    
    Basic Procedure
    1. Use Qt Designer to create a .ui file.
    2. Create a python class of the same type as the widget you created in the .ui file.
    3. When initializing the python class, use uic to dynamically load the .ui file onto the class.

    Here is an example from this code::

        from PyQt4 import QtGui
        import qt_form_support
        
        UI_FILE = 'plainTextEdit.ui'
        
        class TextWindow(QtGui.QDialog, form_class):
        
            def __init__(self, title, text):
                QtGui.QDialog.__init__(self, parent)
                qt_form_support.loadUi(UI_FILE, baseinstance=self)
                self.setWindowTitle(title)
                self.plainTextEdit.setPlainText(text)

        import sys
        app = QtGui.QApplication(sys.argv)
        win = TextWindow('the title', __doc__)
        win.show()
        sys.exit(app.exec_())

    '''
    return uic.loadUi(os.path.join(get_forms_path(), ui_file), baseinstance=baseinstance, **kw)


def get_forms_path():
    '''identify our resources directory'''
    # assume this is less risky than __file__
    ref = inspect.getsourcefile(get_forms_path)
    path = os.path.abspath(os.path.dirname(ref))
    return os.path.join(path, FORMS_SUBDIRECTORY)
