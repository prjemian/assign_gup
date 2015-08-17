
'''
Support for AGUP program settings

Maintains a resource configuration file such as the following:

.. code-block:: generic
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
        if self.modified or not os.path.exists(self.config['rcfile']):
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
        if key not in self.config.keys():
            msg = 'Key not found in configuration settings: ' + key
            raise KeyError(msg)
        return self.config[key]

    # set methods are used to control the modified flag

    def setRcFile(self, filename):
        if filename != self.config['rcfile']:
            self.modified = True
        self.config['rcfile'] = filename

    def setReviewCycle(self, review_cycle):     # redundant, treat as non-authoritative
        if review_cycle != self.config['review_cycle']:
            self.modified = True
        self.config['review_cycle'] = review_cycle

    def setPrpFile(self, prp_file):
#         if not os.path.exists(prp_file):
#             raise IOError('File not found: ' + prp_file)
        if prp_file != self.config['prp_file']:
            self.modified = True
        self.config['prp_file'] = prp_file
