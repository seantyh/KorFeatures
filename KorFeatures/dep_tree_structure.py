from typing import List
from .KorTypes import *

class DepTreeStructure:
    def __init__(self, deps: List[DepData], tokens: List[TokenData]) -> None:
        self.tokens = tokens
        self.deps = deps
        self.parse_dep_tree()
    
    def parse_dep_tree(self):
        root_idx = -1
        dep_map:Dict[int, DepData] = {}        
        for dep_x in self.deps:
            if dep_x.relation == "root": 
                root_idx = dep_x.depIndex - 1
                continue
            tok_depIdx = dep_x.depIndex - 1
            tok_govIdx = dep_x.govIndex - 1
            depItems = dep_map.get(tok_govIdx, [])
            depItems.append(tok_depIdx)
            dep_map[tok_govIdx] = depItems
        self.root_index = root_idx
        self.dep_map = dep_map

    def get_depth(self):                
        root_depth = self.get_node_depth(self.root_index, self.dep_map)
        return root_depth
    
    def get_node_depth(self, token_idx, dep_map):
        if token_idx in dep_map:            
            max_depth = 0
            for dep_i in dep_map[token_idx]:                
                depth_x = self.get_node_depth(dep_i, dep_map) + 1
                print("from %s-%d: [depth: %d] %s" %  
                    (self.tokens[token_idx], token_idx, 
                    depth_x, self.tokens[dep_i]))
                if max_depth < depth_x: max_depth = depth_x
            return max_depth
        else:
            return 0


    def n_word_before_mv(self):
        deps = self.deps   
        toks = self.tokens          
        nwMV = []        
        main_verb = self.find_main_verb(deps, toks)
        if main_verb:
            return toks.index(main_verb)
        else:
            return -1

    def find_main_verb(self, seqDep: DepData, tokens) -> TokenData:        
        root_depi = self.root_index
        main_token = tokens[root_depi]
                
        if main_token.pos.startswith("V"):
            return main_token
        else:
            return None
