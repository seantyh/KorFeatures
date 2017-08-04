import pdb

class PTree:
    def __init__(self, t):
        self.text = t
        self.children = []
    
    def depth(self):
        if len(self.children) == 0:
            return 0
        else:
            return max([x.depth() for x in self.children]) + 1
    
    def size(self):
        if len(self.children) == 0:
            return 1
        else:
            return sum(x.size() for x in self.children) + 1
    
    def intersect(self, to):
        so = self
        text_match = int(so.text == to.text)
        if len(so.children) * len(to.children) == 0:
            return text_match
        else:
            return text_match + sum(sch.intersect(och) for (sch, och)\
                        in zip(so.children, to.children))

    def similarity(self, to):
        so = self
        n_intersect = so.intersect(to)        
        return n_intersect / min(so.size(), to.size())
    
    def __str__(self):
        if len(self.children) > 0:
           return "%s(%s)" % (self.text, ", ".join([str(x) for x in self.children]))
        else:
           return self.text

    def __repr__(self):
        return str(self)

