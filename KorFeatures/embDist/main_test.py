import numpy as np
import pdb
from dist_algo import EmbDistQuery

if __name__ == "__main__":
    # os.chdir(os.path.dirname(os.path.realpath(__file__)))
    model_params = {
        "base_dir": "../etc",
        "data_path": "as4_char_vec_norm.bytes",
        "label_path": "as4_char_vocab_norm.tsv",
        "dims": (4586, 100)
    }

    dist_query = EmbDistQuery(model_params)
    pairs = [("摸", "索"), ("模", "式")]
    for p in pairs:
        print("%s - %s: %.4f" % (p[0], p[1], dist_query.pair_dist_cos(p[0], p[1])))
    print("done")
    
