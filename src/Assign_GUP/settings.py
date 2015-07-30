
'''
Support for AGUP program settings
'''

import datetime
import os, sys
import rcfile


class ApplicationSettings(object):
    '''
    '''
    
    def __init__(self, rc_file, rc_section):
        try:
            self.rc = rcfile.RcFile(rc_file, rc_section)
            self.read()
            self.source = 'RC file'
        except rcfile.RcFileNotFound:
            self.config = {
               # these are the supported keys
                'rcfile':         self.rc.rcfile,
                'review_cycle':   '',
                'prp_path':       os.path.abspath(os.getcwd()),
                'reviewers_file': '',
                'proposals_file': '',
                'analyses_file':  '',
                'version':  '1.0',
            }
            self.source = 'defaults'
        self.modified = False

    def read(self):
        self.config = self.rc.read()

    def write(self):
        if self.modified or not os.path.exists(self.config['rcfile']):
            self.rc.write(**self.config)
        self.modified = False
    
    def getKeys(self):
        return self.config.keys()

    def getByKey(self, key):
        '''return configuration file value by index key'''
        if key not in self.config.keys():
            msg = 'Key not found in configuration settings: ' + key
            raise KeyError(msg)
        return self.config[key]

    def setRcFile(self, filename):
        if filename != self.config['rcfile']:
            self.modified = True
        self.config['rcfile'] = filename

    def setReviewCycle(self, review_cycle):
        if review_cycle != self.config['review_cycle']:
            self.modified = True
        self.config['review_cycle'] = review_cycle

    def setPrpPath(self, prp_path):
        if not os.path.exists(prp_path):
            raise RuntimeError('Directory not found: ' + prp_path)
        if prp_path != self.config['prp_path']:
            self.modified = True
        self.config['prp_path'] = prp_path
