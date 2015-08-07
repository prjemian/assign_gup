'''
document program history events in a log file
'''


import datetime
import logging
import os
import socket
import sys


# from logging.__init__.py
CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
# unique to this code
NO_LOGGING = -1

addMessageToHistory = None


def _now():
    return datetime.datetime.now()


class Logger(object):
    '''
    use Python logging package to record program history
    
    :param str log_file: name of file to store history
    :param enum level: logging interest level (default=logging.INFO, no logs = -1)
    :param obj statusbar: QStatusBar instance in main window
    :param str history_widget: QPlainTextEdit instance in main window
    '''

    def __init__(self, log_file=None, level=logging.INFO, statusbar=None, history_widget=None):
        
        if level == NO_LOGGING:
            self.log_file = None
        else:
            if log_file is None:
                ymd = str(_now()).split()[0]
                pid = os.getpid()
                log_file = 'assign_gup-' +  ymd + '-' + str(pid) + '.log'
            self.log_file = os.path.abspath(log_file)
            logging.basicConfig(filename=log_file, level=level)

        self.level = level
        self.statusbar = statusbar
        self.history_widget = history_widget
        self.history = ''
        self.first_logs()

    def add(self, message):
        '''
        log a message or report from the application

        :param str message: words to be logged
        '''
        if self.statusbar is not None:
            self.statusbar.showMessage(message)
        timestamp = _now()
        name = os.path.basename(sys.argv[0])
        pid = os.getpid()
        text = "(%d,%s,%s) %s" % (pid, name, timestamp, message)
        
        if self.level != NO_LOGGING:
            logging.info(text)
        
        if len(self.history) != 0:
            self.history += '\n'
        self.history += text
        if self.history_widget is not None:
            self.history_widget.appendPlainText(text)

        return text

    def first_logs(self):
        user = os.environ.get('LOGNAME', None) or os.environ.get('USERNAME', None)
        if self.level == NO_LOGGING:
            interest = 'no logging'
        else:
            interest = logging.getLevelName(self.level)
        self.add("startup")
        self.add("log_file         = " + str(self.log_file))
        self.add("interest level   = " + interest)
        self.add("user             = " + user)
        self.add("host             = " + socket.gethostname() )
        self.add("program          = " + sys.argv[0] )
        self.add("PID              = " + str(os.getpid()) )


def addLog(message):
    global addMessageToHistory
    if addMessageToHistory is not None:
        for line in message.splitlines():
            addMessageToHistory(line)
    else:
        print message
