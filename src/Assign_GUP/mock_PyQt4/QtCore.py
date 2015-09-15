
class QMockObject(object):
        def __init__(self, *args, **kwargs):
            super(QMockObject, self).__init__()

        def __call__(self, *args, **kwargs):
            return None

class QObject(QMockObject): pass
class QUrl(QMockObject): pass
