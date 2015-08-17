
'''
List of analyses and assessments 
'''

from PyQt4 import QtCore
from lxml import etree
import os
import traceback
import reviewer
import resources
import xml_utility


XML_SCHEMA_FILE = resources.resource_file('analyses.xsd')
ROOT_TAG = 'analysis'
DEFAULT_TOPIC_VALUE = 0.0


class AGUP_Analyses(QtCore.QObject):
    '''
    the list of all reviewers
    '''
    
    def __init__(self):
        QtCore.QObject.__init__(self)

        self.analyses = {} 
    
    def __len__(self):
        return len(self.analyses)

    def __iter__(self):
        for item in self.analyses.values():
            yield item

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with analyses
        '''
        def keySort(the_dict):
            return ' '.join(sorted(the_dict.keys()))

        if not os.path.exists(filename):
            raise IOError, 'file not found: ' + filename

        try:
            doc = etree.parse(filename)
        except etree.XMLSyntaxError, exc:
            raise xml_utility.XmlSyntaxError, str(exc)

        try:
            self.validateXml(doc)
        except Exception, exc:
            msg = 'In ' + filename + ': ' + traceback.format_exc()
            raise Exception, msg

        topics_keys = None
        db = {}
        root = doc.getroot()
        proposals_node = root.find('Proposals')
        if proposals_node is not None:
            for node in proposals_node.findall('Proposal'):
                prop_id = node.attrib['id'].strip()

                # assessed topic weights
                topics_dict = {}
                t_node = node.find('Topics')
                if t_node is not None:
                    for topic in t_node.attrib.keys():
                        value = t_node.attrib[topic]
                        try:
                            value = float(value)
                        except (TypeError, ValueError):
                            value = 0.0
                        topics_dict[topic] = value

                # check that all proposals have the exact same list of topics
                # TODO: could be a separate function
                if topics_keys is None:
                    # first proposal defines the list of topics
                    topics_keys = keySort(topics_dict)
#                     topics_keys = topics_keys))
                    first_prop_id = prop_id
                else:
                    these_keys = keySort(topics_dict)
                    if these_keys != topics_keys:
                        # look at all the keys for any missing
                        for key in sorted({_:_ for _ in these_keys.split() + topics_keys.split()}.keys()):
                            if key not in topics_dict:
                                topics_dict[key] = DEFAULT_TOPIC_VALUE
                    # still a mismatch?
                    if keySort(topics_dict) != topics_keys:
                        msg = 'In ' + filename
                        msg += ', list topics do not match'
                        msg += ' between proposal ' + first_prop_id
                        msg += ' and proposal ' + prop_id
                        raise KeyError, msg

                # assigned reviewers
                reviewers_dict = {}
                r_node = node.find('Reviewers')
                if r_node is not None:
                    for key in ('reviewer1', 'reviewer2'):
                        reviewers_dict[key] = r_node.get(key, '')

                db[prop_id] = dict(Topics = topics_dict, Reviewers = reviewers_dict)
        self.analyses = db

    def inOrder(self):
        return sorted(self.analyses.values())
    
    def validateXml(self, xmlDoc):
        '''validate XML document for correct root tag & XML Schema'''
        # TODO: plan to import from master XML file (different schema)
        root = xmlDoc.getroot()
        if root.tag != ROOT_TAG:
            msg = 'expected=' + ROOT_TAG
            msg += ', received=' + root.tag
            raise xml_utility.IncorrectXmlRootTag, msg
        try:
            xml_utility.validate(xmlDoc, XML_SCHEMA_FILE)
        except etree.DocumentInvalid, exc:
            raise xml_utility.InvalidWithXmlSchema, str(exc)
        return True


def main():
    findings = AGUP_Analyses()
    findings.importXml(os.path.join('project', '2015-2', 'analysis.xml'))
    if findings is not None:
        print len(findings)


if __name__ == '__main__':
    main()