
'''
Support AGUP topics
'''


class Topics(object):
    '''
    manage the list of AGUP topics (known here as ``key``)
    '''
    
    def __init__(self):
        self.clearAll()

    def __iter__(self):
        for key in sorted(self.topics):
            yield key
    
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
    
    def addItems(self, key_list):
        '''add several topics at once'''
        for key in key_list:
            self.add(key)
    
    def clearAll(self):
        '''
        remove all keys from the list of topics
        '''
        self.topics = []
    
    def getList(self):
        return sorted(self.topics)

    def remove(self, key):
        '''remove the named topic'''
        if self.exists(key):
            self.topics.remove(key)
        else:
            raise KeyError, 'Cannot remove (does not exist): ' + key


class Topic_MixinClass(object):
    '''
    provides common methods for topic handling in data classes: proposals & reviewers
    '''

    def importXml(self, reviewer):
        '''
        Fill the class variables with values from the XML node
        
        :param proposal: lxml node of the Reviewer
        '''
        msg = 'each subclass of Topic_MixinClass() must implement importXml() method'
        raise NotImplementedError, msg

    def addTopic(self, key, initial_value=0.0):
        '''
        add a new topic key and initial value
        '''
        initial_value = float(initial_value)
        if initial_value < 0 or initial_value > 1.0:
            raise ValueError, 'initial value must be between 0 and 1: given=' + str(initial_value)
        if key not in self.db['topics']:
            self.db['topics'][key] = initial_value

    def removeTopic(self, key):
        '''
        remove an existing topic key
        '''
        if key in self.db['topics']:
            del self.db['topics'][key]

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
        if topic not in self.db['topics']:
            raise KeyError, 'Topic not found: ' + str(topic)
        self.db['topics'][topic] = value
