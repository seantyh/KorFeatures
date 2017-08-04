import pdb
import numpy as np
import os


class EmbDistQuery:
    def __init__(self, model_params):
        data_path = model_params["data_path"]
        label_path = model_params["label_path"]
        model_dims = model_params["dims"]
        base_dir = model_params["base_dir"]

        mdatapath = os.path.join(base_dir, data_path)
        mlabelpath = os.path.join(base_dir, label_path)
        
        if not os.path.exists(mdatapath):
            raise FileNotFoundError("Cannot find " + mdatapath)
        if not os.path.exists(mlabelpath):
            raise FileNotFoundError("Cannot find " + mlabelpath)

        mat = np.fromfile(mdatapath, dtype=np.float32).reshape(model_dims)        
        self.cnmat = self.center_normalize_mat(mat)
        (self.vocab, self.vocab_list) = self.load_vocab(mlabelpath)

    def pair_dist_cos(self, c1, c2):
        return self.get_distance(c1, c2, True)
    
    def pair_dist_euc(self, c1, c2):
        return self.get_distance(c1, c2, False)
    
    def get_distance_vec(self, vec1, vec2, dist_cos = True):
        norm_vec1 = vec1 / np.sqrt(np.dot(vec1, vec1))
        norm_vec2 = vec2 / np.sqrt(np.dot(vec2, vec2))

        if dist_cos:
            # assume mat contains normalized vector
            costheta = np.dot(norm_vec1, norm_vec2)
            dist = (1-costheta)
        else:
            delta = norm_vec1-norm_vec2
            dist = np.sqrt(np.dot(delta, delta))
        return dist

    def get_distance(self, w1, w2, dist_cos = True):
        mat = self.cnmat
        vocab = self.vocab
        
        if not w1 in vocab or not w2 in vocab:
            return None

        vec1 = mat[vocab[w1],]
        vec2 = mat[vocab[w2],]

        return self.get_distance_vec(vec1, vec2, dist_cos)
    
    def get_vector(self, word):
        if word in self.vocab:
            return self.cnmat[self.vocab[word],]
        else:
            return None

    def get_neighbors(self, w1, dist_cos = True):
        mat = self.cnmat
        vocab = self.vocab

        vec1 = mat[vocab[w1],]
        return self.get_vec_neighbors(vec1, dist_cos)

    def get_vec_neighbors(self, vec, dist_cos = True):
        mat = self.cnmat

        if dist_cos:
            norm_vec = vec / np.sqrt(np.dot(vec, vec))
            dist_vec = (1 - np.dot(mat, norm_vec))
        else:
            delta = mat - vec
            dist_vec = np.sqrt(np.diag(np.dot(delta, np.transpose(delta))))

        max_arg = np.argsort(dist_vec)
        return [(self.vocab_list[x], dist_vec[x]) for x in max_arg[0:10]]

    def center_normalize_mat(self, mat):
        centroid = np.mean(mat, 0) 
        cmat = mat-centroid
        cnmat = np.apply_along_axis(lambda x: x/np.sqrt(np.dot(x, x)), 1, cmat)
        return cnmat

    def load_vocab(self, fpath):
        if not os.path.exists(fpath):
            return {}

        vocab = {}
        vocab_list = []
        with open(fpath, "r", encoding="UTF-8") as fin:
            fin.readline() # read pass the title
            for i_ln, ln in enumerate(fin.readlines()):
                toks = [x.strip() for x in ln.split('\t')]
                vocab[toks[0]] = i_ln
                vocab_list.append(toks[0])
        return vocab, vocab_list

