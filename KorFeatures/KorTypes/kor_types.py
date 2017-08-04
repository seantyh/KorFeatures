from typing import Text, List

class TokenData:
    def __init__(self):
        self.text: Text = ""
        self.pos: Text = ""
        self.ner: Text = ""
        self.chStart: int = -1
        self.chEnd: int = -1
        self.clauseIndex: int = -1
        self.sentenceIndex: int = -1
    
    def __repr__(self):
        repr="<Token {token}/{pos}/{ner} {cs}:{ce} @ {si}:{ci}>".format(
            token=self.text, pos=self.pos, ner=self.ner,
            cs=self.chStart, ce=self.chEnd, 
            si=self.sentenceIndex, ci=self.clauseIndex
        )
        return repr

class DepItem:
    def __init__(self):
        self.relation: Text = ""
        self.governor: Text = ""
        self.dependent: Text = ""
        self.govIndex: int = -1
        self.depIndex: int = -1
    
    def __repr__(self):
        return "({rel}, {gov}, {dep})".format(
            rel=self.relation,
            gov=self.governor,
            dep=self.dependent
        )
        
DepData = List[DepItem]