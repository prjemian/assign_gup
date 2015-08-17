
'''
Support AGUP topics
'''

DEFAULT_TOPIC_VALUE = 0.0

# FIXME: there is confused use of these two classes


class Topics(object):
    '''
    manage the list of AGUP topics (known here as ``key``)
    '''
    
    def __init__(self):
        self.clearAll()

    def __iter__(self):
        for key in sorted(self.topics):
            yield key
    
    def __len__(self):
        return len(self.topics)
    
    def exists(self, key):
        '''
        Is ``key`` already known?
        '''
        return key in self.topics
    
    def add(self, key):
        '''
        define a new topic (known here as ``key``)
        
        ``key`` should be a single word or mnemonic, with no white space
        '''
        if self.exists(key):
            raise KeyError, 'This topic is already defined: ' + key
        if len(key.strip()) == 0:
            raise KeyError, 'Must give a value for the topic'
        if len(key.strip().split()) != 1:
            raise KeyError, 'topic cannot have embedded white space: ' + key
        self.topics.append(key.strip())
        self.topics_string = ' '.join(self.getList())
    
    def addItems(self, key_list):
        '''add several topics at once'''
        for key in key_list:
            self.add(key)
    
    def clearAll(self):
        '''
        remove all keys from the list of topics
        '''
        self.topics = []
        self.topics_string = ''
    
    def getList(self):
        return sorted(self.topics)

    def remove(self, key):
        '''
        remove the named topic
        '''
        if self.exists(key):
            self.topics.remove(key)
        else:
            raise KeyError, 'Cannot remove (does not exist): ' + key

    def compareLists(self, other_topics_list):
        '''
        compare topics in self.topics with the other_topics_list, return True if identical
        
        convert each list to a sorted string and compare them
        '''
        return ' '.join(sorted(other_topics_list)) == self.topics_string


class Topic_MixinClass(object):
    '''
    provides common methods for topic handling in data classes: proposals & reviewers
    '''

    def importXml(self, reviewer):
        '''
        Fill the class variables with values from the XML node
        
        :param proposal: lxml node of the Reviewer
        
        The first step usually is to call::
        
          self.readValidXmlDoc(filename, expected_root_tag, XSD_Schema_file)
        
        '''
        msg = 'each subclass of Topic_MixinClass() must implement importXml() method'
        raise NotImplementedError, msg
    
    def addTopic(self, key, initial_value=DEFAULT_TOPIC_VALUE):
        '''
        add a new topic key and initial value
        '''
        if not 0 <= float(initial_value) <= 1.0:
            msg = 'initial value must be between 0 and 1: given=' + str(initial_value)
            raise ValueError, msg
        if not self.topicExists(key):
            self.db['topics'][key] = float(initial_value)

    def removeTopic(self, key):
        '''
        remove an existing topic key
        '''
        if self.topicExists(key):
            del self.db['topics'][key]

    def topicExists(self, key):
        return key in self.db['topics']

    def getTopics(self):
        '''
        return a dictionary of topics: values
        '''
        return self.db['topics']

    def setTopics(self, topic_dict):
        '''
        set topic values from a dictionary, each topic name must already exist
        '''
        for topic, value in topic_dict.items():
            self.setTopic(topic, value)

    def setTopic(self, topic, value):
        '''
        set the value of an existing topic
        '''
        if value < 0 or value > 1.0:
            raise ValueError, 'value must be between 0 and 1: given=' + str(value)
        if not self.topicExists(topic):
            raise KeyError, 'Topic not found: ' + str(topic)
        self.db['topics'][topic] = value
