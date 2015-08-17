
'''
Data for all analyses, assignments, & assessments 
'''


from lxml import etree
import os
import traceback
import agup_data
import reviewer
import resources
import topics
import xml_utility


XML_SCHEMA_FILE = resources.resource_file('analyses.xsd')
ROOT_TAG = 'analysis'
DEFAULT_TOPIC_VALUE = 0.0


class AGUP_Analyses(topics.Topic_MixinClass):
    '''
    Data for all analyses, assignments, & assessments
    '''
    
    def __init__(self):
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
        def sortListUnique(the_list):
            # make a dictionary with each list item
            # redundancies will be overwritten
            the_dict = {_:None for _ in the_list}
            return sorted( the_dict.keys() )

        doc = xml_utility.readValidXmlDoc(filename, 
                                          agup_data.AGUP_MASTER_ROOT_TAG, 
                                          agup_data.AGUP_XML_SCHEMA_FILE,
                                          alt_root_tag=ROOT_TAG, 
                                          alt_schema=XML_SCHEMA_FILE,
                                          )
        root = doc.getroot()
        if root.tag == agup_data.AGUP_MASTER_ROOT_TAG:
            proposals_node = root.find('Assignments')
        else:
            proposals_node = root.find('Proposals')    # pre-agup reviewers file

        ref_topics = None
        db = {}
        root = doc.getroot()
        if proposals_node is not None:
            for node in proposals_node.findall('Proposal'):
                prop_id = node.attrib['id'].strip()

                # assessed topic weights
                topics_dict = {}
                t_node = node.find('Topics')
                if t_node is not None:      # FIXME: learn how to read the topics again (format changed today)
                    for topic in t_node.attrib.keys():
                        value = t_node.attrib[topic]
                        try:
                            value = float(value)
                        except (TypeError, ValueError):
                            value = 0.0
                        topics_dict[topic] = value

                # check that all proposals have the exact same list of topics
                if ref_topics is None:             # first proposal defines the list of topics
                    ref_topics = topics.Topics()
                    ref_topics.addItems(topics_dict.keys())
                    first_prop_id = prop_id
                else:
                    if not ref_topics.compareLists(topics_dict.keys()):
                        # look at all the keys for any missing
                        all_topics = topics_dict.keys() + ref_topics.getList()
                        for key in sortListUnique(all_topics):
                            if key not in topics_dict:
                                # define new keys as needed
                                topics_dict[key] = DEFAULT_TOPIC_VALUE
                    # still a mismatch?
                    if not ref_topics.compareLists(topics_dict.keys()):
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
    
    def writeXmlNode(self, specified_node):
        '''
        write Analyses data to a specified node in the XML document

        :param obj specified_node: XML node to contain this data
        '''
        for prop_id, finding in sorted(self.analyses.items()):
            prop_node = etree.SubElement(specified_node, 'Proposal')
            prop_node.attrib['id'] = str(prop_id)
            node = etree.SubElement(prop_node, 'Topics')
            for k, v in sorted(finding['Topics'].items()):
                subnode = etree.SubElement(node, 'Topic')
                subnode.attrib['name'] = k
                subnode.attrib['value'] = str(v)

            node = etree.SubElement(prop_node, 'Reviewers')
            for k, v in sorted(finding['Reviewers'].items()):
                subnode = etree.SubElement(node, 'Reviewer')
                subnode.attrib[k] = str(v)

    def inOrder(self):
        return sorted(self.analyses.values())


def main():
    findings = AGUP_Analyses()
    findings.importXml(os.path.join('project', '2015-2', 'analysis.xml'))
    if findings is not None:
        print len(findings)

if __name__ == '__main__':
    main()
