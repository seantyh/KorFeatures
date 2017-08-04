
class PosClass:
    def __init__(self):
        pass
       
    def get_functional_class(self):
        return open("etc/func_word_class.txt", "r").read().split()

    def get_content_class(self):
        return open("etc/content_word_class.txt", "r").read().split()

    def get_connective_class(self):
        return open("etc/connective_word_class.txt", "r").read().split()