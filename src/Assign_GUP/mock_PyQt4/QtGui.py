
class QMockObject(object):
        def __init__(self, *args, **kwargs):
            super(QMockObject, self).__init__()

        def __call__(self, *args, **kwargs):
            return None

class QDesktopServices(QMockObject): pass
class QDialog(QMockObject): pass

