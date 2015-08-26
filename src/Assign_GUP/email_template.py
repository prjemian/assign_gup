
'''
Create email notices to each Reviewer describing specific assignments
'''

# TODO: needs an associated MVC editor

from lxml import etree
import os

import agup_data
import resources
import xml_utility


DEFAULT_PROJECT_FILE = os.path.abspath('project/agup_project.xml')
DEFAULT_TEMPLATE_FILE = os.path.abspath('resources/email_template.txt')
DEFAULT_TEMPLATE_FIELDS = dict(
    PANEL_CHAIR = 'Pete Jemian',
    REVIEW_CYCLE = '2015-2',
    PRP_DATE = '2015-03-24',
    OTHER_COMMENTS = '''
    This time there are two project proposals:
       GUP-11111 at 5-ID
       GUP-22222 at 12ID
       
       We've discussed the responsibilities for reviewing project proposals.
       If you have any questions, call or write me.
    ''',
    # these to be completed during mail merge step
    # FULL_NAME = 'Ima Reviewer',
    # EMAIL = 'reviewer@institution.net',
    # ASSIGNED_PRIMARY_PROPOSALS = '11111 22222 33333',
    # ASSIGNED_SECONDARY_PROPOSALS = '44444 55555 66666',
)


class EmailTemplate(object):
    '''
    Support the creation of custom emails to each Reviewer from template and fields
    
    It is possible to create and use custom fields.
    Be sure that the custom fields are *uniquely identifiable* to avoid replacing the wrong text.
    '''
    
    def __init__(self):
        filename = resources.resource_file(DEFAULT_TEMPLATE_FILE)
        self.email_template = open(filename).read()
        self.keyword_dict = DEFAULT_TEMPLATE_FIELDS
    
    def mail_merge(self, **kw_dict):
        '''
        create one email with a mail merge of self.keyword_dict and kw_dict into self.email_template
        '''
        kw = self.keyword_dict.copy()   # start with this keyword dictionary
        kw.update(kw_dict)              # add/replace with supplied kw_dict
        email = self.email_template     # grab the current template
        for k, v in kw.items():
            email = email.replace(k, v)
        return email

    def importXml(self, filename):
        '''
        :param str filename: name of XML file with email template and keywords
        '''
        doc = xml_utility.readValidXmlDoc(filename, 
                                          agup_data.AGUP_MASTER_ROOT_TAG, 
                                          agup_data.AGUP_XML_SCHEMA_FILE
                                          )

        root = doc.getroot()
        email_node = root.find('notification_email')
        if email_node is not None:
            text = xml_utility.getXmlText(email_node, 'email_template')
            self.email_template = text or self.email_template
            self.keyword_dict = {}
            for node in email_node.findall('Key'):
                k = node.attrib['name']
                v = node.text.strip()
                self.keyword_dict[k] = v
    
    def writeXmlNode(self, root_node):
        '''
        write email template data to the XML document

        :param obj root_node: XML node to contain this data
        '''
        node = etree.SubElement(root_node, 'notification_email')
        etree.SubElement(node, 'email_template').text = self.email_template
        for k, v in self.keyword_dict.items():
            key_node = etree.SubElement(node, 'Key')
            key_node.attrib['name'] = k
            key_node.text = v.strip()


if __name__ == '__main__':
    kw = dict(
        FULL_NAME = 'Ima Reviewer',
        EMAIL = 'reviewer@institution.net',
        ASSIGNED_PRIMARY_PROPOSALS = '11111 22222 33333',
        ASSIGNED_SECONDARY_PROPOSALS = '44444 55555 66666',
    )
    et = EmailTemplate()
    print et.mail_merge(**kw)
    