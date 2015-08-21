
r'''
Support for AGUP program settings

Maintains a resource configuration file such as the following:

.. code-block:: ini
    :linenos:
 
    [metadata]
    timestamp = 2015-08-05 11:39:43.128000
    rcfile = C:\Users\Developer\.assign_gup.rc
    host = laptop
     
    [Assign_GUP]
    prp_file = C:\Users\Developer\Documents\PRP\reviews\2015-2.xml
    rcfile = C:\Users\Developer\.assign_gup.rc
    review_cycle = 2015-2
    version = 1.0

This file is used to preserve settings of the application.
Remove this file to clear any settings.
'''

# TODO: consider using QSettings instead
# :see: http://doc.qt.io/qt-4.8/qsettings.html
# :see: http://youku.io/questions/4849068/python-pyqt4-functions-to-save-and-restore-ui-widget-values
'''
example::

    from PyQt4 import QtCore
    
    # Windows: %APPDATA%\orgName\appName.ini
    # UNIX:    $HOME/.config/orgName/appName.ini
    
    settings = QtCore.QSettings(QtCore.QSettings.IniFormat, 
                                QtCore.QSettings.UserScope, 
                                'orgName', 
                                'appName')
    
    settings.beginGroup("mainwindow")
    settings.setValue("this", 'that')
    settings.setValue("fullScreen", True)
    settings.endGroup()
    
    settings.beginGroup("outputpanel")
    settings.setValue("visible", dict(a=1, b='2', c=3.0))
    settings.endGroup()
    
    
    settings.beginGroup("mainwindow")
    settings.setValue("another", 2)
    settings.setValue("fullScreen", False)
    settings.endGroup()
    
    settings.beginGroup("outputpanel")
    settings.setValue("invisible", 'never')
    settings.endGroup()

    print settings.fileName()
    print settings.applicationName()
    print settings.organizationName()
    print settings.status()
    for key in settings.allKeys():
        print str(key)

output::

    C:/Users/WINDOWS_USER/AppData/Roaming/orgName/appName.ini
    appName
    orgName
    0
    mainwindow/another
    mainwindow/fullScreen
    mainwindow/this
    outputpanel/invisible
    outputpanel/visible

'''

import datetime
import os, sys
import rcfile


class ApplicationSettings(object):
    '''
    manage and preserve default settings for this application
    '''
    
    def __init__(self, rc_file, rc_section):
        try:
            self.rc = rcfile.RcFile(rc_file, rc_section)
            self.read()
            self.source = 'RC file'
        except rcfile.RcFileNotFound:
            self.resetDefaults()
        self.modified = False

    def resetDefaults(self):
        '''
        Reset all application settings to default values.
        '''
        self.config = {
            # these are the supported keys
            'rcfile':         self.rc.rcfile,
            'review_cycle':   '',           # redundant, treat as non-authoritative
            'prp_file':       '',
            'version':        '1.0',
        }
        self.source = 'defaults'
        self.modified = True

    def read(self):
        '''read settings from the designated RC file'''
        self.config = self.rc.read()

    def write(self):
        '''write settings to the designated RC file'''
        if self.modified or not os.path.exists(self.getByKey('rcfile')):
            self.rc.write(**self.config)
        self.modified = False
    
    def getKeys(self):
        '''get a list of all the configuration keys'''
        return self.config.keys()

    def getByKey(self, key):
        '''
        return configuration file value by index key
        
        Use this method rather than defining get methods
        for each configuration value.
        '''
        if not self.keyExists(key):
            msg = 'Key not found in configuration settings: ' + key
            raise KeyError(msg)
        return self.config[key]
    
    def keyExists(self, key):
        '''does the named key exist?'''
        return key in self.config.keys()
    
    def setKey(self, key, value):
        '''set the value of a configuration key, creates the key if it does not exist'''
        if not self.keyExists(key) or key != self.config[key]:
            self.config[key] = value
            self.modified = True

    # set methods are used to control the modified flag

    def setRcFile(self, filename):
        self.setKey('rcfile', str(filename))

    def setReviewCycle(self, review_cycle):     # redundant, treat as non-authoritative
        self.setKey('review_cycle', str(review_cycle))

    def getPrpFile(self):
        return self.getByKey('prp_file')

    def setPrpFile(self, prp_file):
        self.setKey('prp_file', str(prp_file))
