
r'''
Support for AGUP program settings

This file is used to preserve settings of the application.
Remove this file to clear any settings.

This module uses QSettings (http://doc.qt.io/qt-4.8/qsettings.html).
'''


import datetime
import os, sys
from PyQt4 import QtCore

import __init__
orgName = __init__.__settings_orgName__
appName = __init__.__package_name__
GLOBAL_GROUP = '___global___'


class ApplicationQSettings(QtCore.QSettings):
    '''
    manage and preserve default settings for this application using QSettings
    
    Use the .ini file format and save under user directory
    '''
    
    def __init__(self):
        QtCore.QSettings.__init__(self, 
                                  QtCore.QSettings.IniFormat, 
                                  QtCore.QSettings.UserScope, 
                                  orgName, 
                                  appName)
        self.init_global_keys()
    
    def init_global_keys(self):
        d = dict(
            this_file = self.fileName(),
            review_cycle = '',           # redundant, treat as non-authoritative
            prp_file = '',
            version = 1.0,
            timestamp = str(datetime.datetime.now())
        )
        for k, v in d.items():
            if self.getKey(GLOBAL_GROUP + '/' + k) in ('', None):
                self.setValue(GLOBAL_GROUP + '/' + k, v)

    def _keySplit_(self, full_key):
        '''
        split full_key into (group, key) tuple
        
        :param str full_key: either `key` or `group/key`, default group (unspecified) is GLOBAL_GROUP
        '''
        if len(full_key) == 0:
            raise KeyError, 'must supply a key'
        parts = full_key.split('/')
        if len(parts) > 2:
            raise KeyError, 'too many "/" separators: ' + full_key
        if len(parts) == 1:
            group, key = GLOBAL_GROUP, str(parts[0])
        elif len(parts) == 2:
            group, key = map(str, parts)
        return group, key
    
    def keyExists(self, key):
        '''does the named key exist?'''
        return key in self.allKeys()

    def getKey(self, key):
        '''
        return the Python value (not a QVariant) of key or None if not found
        
        :raises TypeError: if key is None
        '''
        return self.value(key).toPyObject()
    
    def setKey(self, key, value):
        '''
        set the value of a configuration key, creates the key if it does not exist
        
        :param str key: either `key` or `group/key`
        
        Complement:  self.value(key)  returns value of key
        '''
        #?WHY? if not self.keyExists(key):
        group, k = self._keySplit_(key)
        if group is None:
            group = GLOBAL_GROUP
        self.remove(key)
        self.beginGroup(group)
        self.setValue(k, value)
        self.endGroup()
        if key != 'timestamp':
            self.updateTimeStamp()
 
    def getReviewCycle(self):
        return self.getKey(GLOBAL_GROUP + '/review_cycle') or ''
 
    def setReviewCycle(self, review_cycle):     # redundant, treat as non-authoritative
        key = GLOBAL_GROUP + '/review_cycle'
        self.remove(key)
        self.setKey(key, str(review_cycle))
 
    def getPrpFile(self):
        return self.getKey(GLOBAL_GROUP + '/prp_file') or ''
 
    def setPrpFile(self, prp_file):
        key = GLOBAL_GROUP + '/prp_file'
        self.remove(key)
        self.setKey(key, str(prp_file))

    def resetDefaults(self):
        '''
        Reset all application settings to default values.
        '''
        for key in self.allKeys():
            self.remove(key)
        self.init_global_keys()
    
    def updateTimeStamp(self):
        self.setKey('timestamp', str(datetime.datetime.now()))

    def saveWindowGeometry(self, window):
        '''
        remember where the window was
        
        :param obj window: instance of QWidget
        '''
        group = window.__class__.__name__ + '_geometry'
        geo = window.geometry()
        self.setKey(group + '/x', geo.x())
        self.setKey(group + '/y', geo.y())
        self.setKey(group + '/width', geo.width())
        self.setKey(group + '/height', geo.height())

    def restoreWindowGeometry(self, window):
        '''
        put the window back where it was
        
        :param obj window: instance of QWidget
        
        ..  note:: Multi-monitor support
            
            On multi-monitor systems such as laptops, window may be
            restored to offscreen position.  Here is how it happens:
            
            * geo was saved while window was on 2nd screen while docked
            * now re-opened on laptop display and window is off-screen

        '''
        group = window.__class__.__name__ + '_geometry'
        x = self.getKey(group + '/x')
        y = self.getKey(group + '/y')
        width = self.getKey(group + '/width')
        height = self.getKey(group + '/height')
        if width is None or height is None:
            return
        window.resize(QtCore.QSize(int(width), int(height)))
        if x is None or y is None:
            return
        # TODO: what if (x,y) is off-screen?  Check here is point is off-screen
        point = QtCore.QPoint(int(x), int(y))
        # TODO: only do this if point is on-screen
        # see: http://doc.qt.io/qt-4.8/qdesktopwidget.html#screen-geometry
        # see: http://doc.qt.io/qt-4.8/application-windows.html#window-geometry
        window.move(point)


def qmain():
    ss = ApplicationQSettings()
    print ss
    
    #ss.setValue('morning', 'early')
    #ss.setValue('main_window/x', 40)

    print ss.fileName()
    print ss.applicationName()
    print ss.organizationName()
    print ss.status()
    ss.setKey('billy/goat', 'gruff')
    for key in ss.allKeys():
        print str(key), ss.getKey(key), ss._keySplit_(key)
    ss.resetDefaults()


if __name__ == '__main__':
    qmain()
