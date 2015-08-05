
'''
XML utility methods
'''

from lxml import etree


def getXmlText(parent, tag):
    '''
    Read the text content of an XML node
    
    :param reviewer: lxml node node of the Reviewer
    :return: node text or None
    '''
    node = parent.find(tag)
    if node is None:
        return None
    if node.text is None:
        return None
    text = node.text.strip()
    return text
