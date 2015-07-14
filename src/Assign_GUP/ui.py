
'''
various common methods for the user interface
'''

import wx
import datetime
import config


def LabelEntry(panel, sizer, kws):
    '''
    create a label and an entry field in the designated panel and sizer
    
    :param panel: enclosing wx.Panel
    :param sizer: sizer to be used
    :param kws: expected keys are 'label' and 'entry', 'editable' key is optional
    :return: object for entry widget
    '''
    value = kws['entry']
    if value == None: value = ""
    label = wx.StaticText(panel, wx.ID_ANY, label=kws['label'], style=0)
    entry = wx.TextCtrl(panel, wx.ID_ANY, value)
    if 'editable' in kws:
        entry.SetEditable(kws['editable'])
    sizer.Add(label, 0, wx.ALL, 5)
    sizer.Add(entry, 1, wx.ALL | wx.GROW | wx.EXPAND, 5)
    return entry


def LabelEntryMultiline(panel, sizer, kws):
    '''
    create a label and an entry field in the designated panel and sizer
    
    :param panel: enclosing wx.Panel
    :param sizer: sizer to be used
    :param kws: expected keys are 'label' and 'entry', 'editable' key is optional
    :return: object for entry widget
    '''
    value = kws['entry']
    if value == None: value = ""
    label = wx.StaticText(panel, wx.ID_ANY, label=kws['label'], style=0)
    entry = wx.TextCtrl(panel, wx.ID_ANY, str(value), 
        style = wx.TE_AUTO_SCROLL | wx.TE_MULTILINE | wx.TE_LINEWRAP)
    if 'editable' in kws:
        entry.SetEditable(kws['editable'])
    sizer.Add(label, 0, wx.ALL, 5)
    sizer.Add(entry, 1, wx.ALL | wx.GROW | wx.EXPAND, 5)
    row = kws['row']
    sizer.AddGrowableRow(row, 1) 
    return entry


LABEL_ENTRY = 'LabelEntry'
LABEL_ENTRY_MULTILINE = 'LabelEntryMultiline'
function_choice = {}
function_choice[LABEL_ENTRY] = LabelEntry
function_choice[LABEL_ENTRY_MULTILINE] = LabelEntryMultiline


def make(panel, sizer, kws):
    '''
    :param panel: enclosing wx.Panel
    :param sizer: sizer to be used
    :param kws: expected keys are 'label' and 'entry'
    :return: object defined by kws['type']
    '''
    global function_choice
    if kws['type'] in function_choice:
        func = function_choice[kws['type']]
        return func(panel, sizer, kws)
    else:
        msg = 'Unknown ui function requested: %s' % kws['type']
        raise Exception, msg


statusWidget = None
statusLog = []


def log(text, widget = None):
    '''
    log a message, display on the status line of the Main widget
    '''
    global statusWidget, statusLog
    entry = "(%s) %s" % (str(datetime.datetime.now()), text)
    if widget != None:
        statusWidget = widget
    if statusWidget != None:
        statusWidget.SetStatusText(entry)
    statusLog.append( entry )

def ShowLogs():
    '''
    show the status logs
    '''
    global statusLog
    return "\n".join( statusLog )


email_template = None


def EmailMsg(name, email, cycle, primary, secondary, venue):
    '''
    Create the email communicating the assignments to a reviewer.
    
    :param name: name of the reviewer
    :param email: email address
    :param cycle: APS scheduling cycle
    :param primary: list of proposal numbers as primary reviewer
    :param secondary: list of proposal numbers as secondary reviewer
    :param venue: set in config.py, such as: 'in Building 401 on Tuesday, 13 November 2012'
    :return: multiline string containing email message
    '''
    global email_template
    primaries = "\t".join(primary)
    secondaries = "\t".join(secondary)
    if email_template == None:
        fname = config.build_filename('email_template', 'txt')
        f = open(fname, 'r')
        email_template = f.read()
        f.close()
    msg = email_template % (name, email, cycle, 
                            name, cycle, 
			    primaries, secondaries, venue)
    return msg


def DotProduct(proposal, reviewer):
    '''
    compute the dot product of proposal topic weight and reviewer topic strength
    
    :param obj proposal: instance of Proposal
    :param obj reviewer: instance of Reviewer
    :returns float: computed dot product or 0.0 if insufficient information
    '''
    #------------------------------------
    def getAsFloat(topic):
        try:
            value = float(topic)
        except (ValueError, TypeError):
            value = 0.0
        return abs(value)
    #------------------------------------
    proposal_topic_dict = proposal.db['topics']
    reviewer_strength_dict = reviewer.db['topics']
    keyList = sorted(proposal_topic_dict)
    if keyList != sorted(reviewer_strength_dict):
        fmt = "list of topics not the same for proposal %s and reviewer %s"
        msg = fmt % (str(proposal), str(reviewer))
        raise IndexError, msg

    if reviewer.db['full_name'] not in proposal.db['eligible_reviewers']:
        dot_product = 0     # this reviewer cannot review this proposal
    else:
        weights = [getAsFloat(proposal_topic_dict[topic]) for topic in keyList]
        denominator = sum(weights)
        if denominator == 0.0:
            return 0.0            # this proposal has no assigned weights
    
        strengths = [getAsFloat(reviewer_strength_dict[topic]) for topic in keyList]
        numerator = sum([u*v for u, v in zip(weights, strengths)])

        dot_product = numerator / denominator   # sum(proposal_weight * reviewer_strength)
    return dot_product

if __name__ == '__main__':
    pass
