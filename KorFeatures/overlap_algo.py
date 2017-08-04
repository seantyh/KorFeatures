from .embDist.dist_algo import *
from .embDist.model_params import *
import numpy as np

class TokenOverlap:
    def __init__(self):
        pass
    
    def text_overlap(self, seq_a, seq_b):
        set_a = set([x["text"] for x in seq_a])
        set_b = set([x["text"] for x in seq_b])
        ints = set_a.intersection(set_b)
        return len(ints)

class EmbeddingOverlap:
    def __init__(self):
        # EmbDistQuery will center and normalize the vectors when loading
        param = ModelParams.Get("as4word")
        param["base_dir"] = os.path.dirname(__file__) + "/etc"
        self.emb_query = EmbDistQuery(param)
        self.emb_dim = param["dims"][1]

    def embed_overlap(self, seq_a, seq_b):
        vec_a = self.get_seq_vector(seq_a)
        vec_b = self.get_seq_vector(seq_b)
        norm_vec_a = vec_a / np.sqrt(np.dot(vec_a, vec_a))
        norm_vec_b = vec_b / np.sqrt(np.dot(vec_b, vec_b))
        
        costheta = np.dot(norm_vec_a, norm_vec_b)
        dist = (1-costheta)
        return dist

    def get_seq_vector(self, seq_x):
        emb_query = self.emb_query
        seq_vec = np.zeros(self.emb_dim)
        n_tok = 0
        for tok in seq_x:
            text = tok["text"]
            v1 = emb_query.get_vector(text)
            if v1 is None: continue
            n_tok += 1
            seq_vec += v1
        return seq_vec / n_tok