
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


class AGUP_Analyses(object):
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

    def inOrder(self):
        return sorted(self.analyses.values())

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with analyses
        '''

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
            raise RuntimeError, 'Cannot read old-style analyses.xml files now.'

        ref_prop_id = None
        ref_prop_topics = topics.Topics()
        db = {}
        if proposals_node is not None:
            for node in proposals_node.findall('Proposal'):
                prop_id = node.attrib['id'].strip()
                analysis = ProposalAnalysis()
                analysis.setId(prop_id)

                ts_node = node.find('Topics')
                if ts_node is not None:
                    for t_node in ts_node.findall('Topic'):
                        topic = t_node.attrib['name']
                        try:
                            value = float(t_node.attrib['value'])
                        except (TypeError, ValueError):
                            value = 0.0
                        analysis.addTopic(topic, value)

                topics.synchronizeTopics(analysis.topics, ref_prop_topics)

                # assigned reviewers
                analysis.reviewer1 = xml_utility.getXmlText(node, 'Reviewer1', '')
                analysis.reviewer2 = xml_utility.getXmlText(node, 'Reviewer2', '')

                db[prop_id] = analysis

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
            for k in finding.topics.getTopicList():
                v = finding.topics.get(k)
                subnode = etree.SubElement(node, 'Topic')
                subnode.attrib['name'] = k
                subnode.attrib['value'] = str(v)

            # FIXME: self.analyses does not have the reviewer assignments!
            subnode = etree.SubElement(prop_node, 'Reviewer1')
            subnode.attrib['name'] = str(finding.reviewer1)
            subnode = etree.SubElement(prop_node, 'Reviewer2')
            subnode.attrib['name'] = str(finding.reviewer2)


class ProposalAnalysis(object):
    '''
    analyses, assignments, & assessments of a single proposal
    '''
    
    def __init__(self):
        self.prop_id = None
        self.topics = topics.Topics()
        self.reviewer1 = ''
        self.reviewer2 = ''
    
    def getId(self):
        return self.prop_id
    
    def setId(self, prop_id):
        self.prop_id = prop_id
    
    def getReviewer1(self):
        return self.reviewer1
    
    def setReviewer1(self, reviewer):
        self.reviewer1 = reviewer
    
    def getReviewer2(self):
        return self.reviewer2
    
    def setReviewer2(self, reviewer):
        self.reviewer2 = reviewer
    
    def getTopic(self, topic):
        '''
        return the value of the named topic
        '''
        return self.topics.get(topic)
    
    def getTopicList(self):
        '''
        return a list of all topics
        '''
        return self.topics.getTopicList()
    
    def addTopic(self, topic, value=topics.DEFAULT_TOPIC_VALUE):
        '''
        declare a new topic and give it an initial value
        
        topic must not exist or KeyError exception will be raised
        '''
        self.topics.add(topic, value)
    
    def addTopics(self, topics_list):
        '''
        declare several new topics and give them all default values
        
        each topic must not exist or KeyError exception will be raised
        '''
        self.topics.addTopics(topics_list)
    
    def setTopic(self, topic, value=topics.DEFAULT_TOPIC_VALUE):
        '''
        set value of an existing topic
        
        topic must exist or KeyError exception will be raised
        '''
        self.topics.set(topic, value)

    def removeTopic(self, key):
        '''
        remove the named topic
        '''
        self.topics.remove(key)

    def removeTopics(self, key_list):
        '''
        remove several topics at once
        '''
        self.topics.removeTopics(key)

def main():
    findings = AGUP_Analyses()
    findings.importXml(os.path.join('project', 'agup_project.xml'))
    if findings is not None:
        print len(findings)

if __name__ == '__main__':
    main()
