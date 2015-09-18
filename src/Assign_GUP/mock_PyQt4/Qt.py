
class QMockObject(object):
        def __init__(self, *args, **kwargs):
            super(QMockObject, self).__init__()

        def __call__(self, *args, **kwargs):
            return None

class ApplicationModal(QMockObject): pass

class Key_Down(QMockObject): pass
class Key_Up(QMockObject): pass
