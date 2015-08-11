
'''
XML utility methods
'''

from lxml import etree
import os


class IncorrectXmlRootTag(etree.DocumentInvalid):
    '''the root tag of the XML file is incorrect'''
    pass


class InvalidWithXmlSchema(etree.DocumentInvalid):
    '''error while validating against the XML Schema'''
    pass

class XmlSyntaxError(etree.XMLSyntaxError):
    '''Xml Syntax error'''
    pass


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


def validate(xml_tree, xml_schema_file):
    '''
    validate an XML document tree against an XML Schema file

    :param obj xml_tree: instance of etree._ElementTree
    :param str xml_schema_file: name of XML Schema file (local to package directory)
    '''
    path = os.path.abspath(os.path.dirname(__file__))
    xsd_file_name = os.path.join(path, xml_schema_file)
    if not os.path.exists(xsd_file_name):
        raise IOError('Could not find XML Schema file: ' + xml_schema_file)
    
    xsd_doc = etree.parse(xsd_file_name)
    xsd = etree.XMLSchema(xsd_doc)

    return xsd.assertValid(xml_tree)
