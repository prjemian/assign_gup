
'''
Support AGUP topics
'''


class Topics(object):
    '''
    manage the list of AGUP topics
    '''
    
    def __init__(self):
        self.clear()

    def __iter__(self):
        for key in sorted(self.topics):
            yield key
    
    def exists(self, key):
        return key in self.topics
    
    def add(self, value):
        if not self.exists(key):
            self.topics.append(key)
    
    def clear(self):
        self.topics = []
