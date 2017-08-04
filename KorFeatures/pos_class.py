from os.path import dirname, abspath, join

class PosClass:
    def __init__(self):
        self.basedir = dirname(abspath(__file__))
       
    def get_functional_class(self):
        fpath = join(self.basedir, "etc/func_word_class.txt")
        return open(fpath, "r").read().split()

    def get_content_class(self):
        fpath = join(self.basedir, "etc/content_word_class.txt")
        return open(fpath, "r").read().split()

    def get_connective_class(self):
        fpath = join(self.basedir, "etc/connective_word_class.txt")
        return open(fpath, "r").read().split()