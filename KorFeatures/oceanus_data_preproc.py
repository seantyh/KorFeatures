from typing import List, Tuple, Text
from itertools import chain
from pyOceanus.oceanus_data import OceanusData
from pyOceanus.tree_parser import Tree as OceanusTree
from .KorTypes import *
from .PTree import PTree
import pdb

CLAUSE_DELIMS = ("，", "；", "：")

class OceanusDataTokenFormatError(Exception):
    pass

class OceanusDataPreproc:
    def __init__(self, oc_data: OceanusData) -> None:
        self.oc_data = oc_data
    
    def tokens(self) -> List[TokenData]:
        oc_tokens = self.oc_data.tokens
        kor_tokens: List[TokenData] = []                
        for sent_idx, sent_token in enumerate(oc_tokens):
            clauseCounter = 0
            for token in sent_token:
                if len(token) < 5:
                    raise OceanusDataTokenFormatError("expect a length-5 tuple")
                kToken = TokenData()
                kToken.text = token[0]
                kToken.pos = token[1]
                kToken.ner = token[2]
                kToken.chStart = int(token[3])
                kToken.chEnd = int(token[4])
                kToken.clauseIndex = clauseCounter
                kToken.sentenceIndex = sent_idx
                kor_tokens.append(kToken)

                if kToken.text in CLAUSE_DELIMS:
                    clauseCounter += 1                
        return kor_tokens

    def trees(self) -> List[PTree]:
        oc_trees = [self.mapTree(x) for x in self.oc_data.trees]
        return oc_trees

    def deps(self) -> List[DepData]:
        oc_deps = self.oc_data.deps
        sent_deps: List[Tuple[Text, Text, int, Text, int]]
        kdepList: List[DepData] = []
        for sent_deps in oc_deps:
            kDepData: DepData = []
            for dep in sent_deps:
                kdep = DepItem()
                kdep.relation = dep[0]
                kdep.governor = dep[1]
                kdep.dependent = dep[3]
                kdep.govIndex = dep[2]
                kdep.depIndex = dep[4]
                kDepData.append(kdep)
            kdepList.append(kDepData)
        return kdepList

    def mapTree(self, x: OceanusTree) -> PTree:
        ptree = PTree(x.node)
        ptree.children = [self.mapTree(x) for x in x.children]
        return ptree
        
            

