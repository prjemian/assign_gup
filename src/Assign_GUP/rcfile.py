
'''
Manage the resource configuration (RC) file

EXAMPLE::

    RC_FILE = '.assign_gup.rc'
    SECTION = 'Assign_GUP'
    rc = rcfile.RcFile(RC_FILE, SECTION)
    rc.write(sunday=1,
             monday='2', 
             tuesday='three', 
             wednesday='4.0',
             rcfile = rc.rcfile,
             review_cycle='2020-5',
    )
    # print open(rc.rcfile, 'r').read()
    kw = rc.read()
    import pprint
    pprint.pprint(kw)

RC FILE::

    [metadata]
    timestamp = 2015-07-27 22:25:03.898000
    rcfile = C:\Users\Pete\.assign_gup.rc
    host = amb
    
    [Assign_GUP]
    monday = 2
    rcfile = C:\Users\Pete\.assign_gup.rc
    review_cycle = 2020-5
    sunday = 1
    tuesday = three
    wednesday = 4.0

OUTPUT::

    {'monday': '2',
     'rcfile': 'C:\\Users\\Pete\\.assign_gup.rc',
     'review_cycle': '2020-5',
     'sunday': '1',
     'tuesday': 'three',
     'wednesday': '4.0'}

'''

import datetime
import os, sys
import ConfigParser
import socket


class RcFileNotFound(IOError): 
    '''RC file was not found'''
    pass


class RcFile(object):
    
    def __init__(self, rcfile, section):
        self.rcfile = self.getRcFileName(basename=rcfile)
        self.section = section
    
    def getRcFileName(self, basename = None):
        if basename is None:
            return self.rcfile
        if sys.platform in ('win32', ):
            home = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
        else:
            home = os.environ['HOME']
        return os.path.abspath(os.path.join(home, basename))
    
    def write(self, **kw):
        '''
        write the dictionary of resources to the RC_FILE
        
        :param dict kw: dictionary of resources
        
        Write the *kw* dictionary into the *self.section* section.
        Write metadata into the *metadata* section. (Ignore on read)
        '''
        if len(kw) == 0:
            return
    
        fp = open(self.rcfile, 'w')      # TODO: what if file is not writable?
        
        # https://docs.python.org/2/library/configparser.html
        config = ConfigParser.SafeConfigParser()
    
        section = 'metadata'
        config.add_section(section)
        config.set(section, 'timestamp', str(datetime.datetime.now()))
        config.set(section, 'rcfile', self.rcfile)
        config.set(section, 'host', socket.gethostname())
    
        config.add_section(self.section)
        for key, value in sorted(kw.items()):
            config.set(self.section, key, str(value))
    
        config.write(fp)
        fp.close()

    def read(self):
        '''
        read the *self.section* of RC_FILE and return a dictionary of resources 
        
        :return dict: dictionary of resources
    
        Only read from the *self.section* section
        '''
        if not os.path.exists(self.rcfile):
            raise RcFileNotFound
    
        fp = open(self.rcfile, 'r')
        config = ConfigParser.SafeConfigParser()
        config.readfp(fp)
        keylist = config.options(self.section)
        kw = {}
        for key in keylist:
            kw[key] = config.get(self.section, key)
        fp.close()
        return kw
