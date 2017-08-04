class DepRelation:
    def __init__(self, rel, g, d):
        self.relation = rel
        self.gov = g
        self.dep = d
    
    def __repr__(self):
        return "%s(%s, %s)" % (self.relation, self.gov, self.dep)