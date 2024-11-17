

class Dummy:
    def __init__(self, *args):
        self.m = None
        if len(args) == 1:
            self.m = args[0]
        assert(len(args) < 2)
    def hash(self, p, _progress):
        if self.m is None:
            with open(p, 'r', encoding='utf-8') as f:
                return 'hashof' + f.read()
        #
        if self.m == 'invalid char':
            return '1\2'
        if self.m == 'fail':
            raise Exception()
        return None

