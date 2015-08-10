
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
