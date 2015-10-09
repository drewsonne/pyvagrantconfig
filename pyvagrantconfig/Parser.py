__author__ = 'drews'


class Parser(object):

    @classmethod
    def parses(cls, content):
        return cls(content).parse()

    @classmethod
    def parsep(cls, path):
        with open(path, 'r') as vagrantfile:
            return cls.parses(vagrantfile.read())

    def __init__(self, content):
        self.vagrantfile = content

    def parse(self):
        pass
