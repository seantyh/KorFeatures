import os
import json

BASE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(BASE_PATH)

def get_feature_distr():
    distr_path = os.path.join(BASE_DIR, "etc/grade_feature_dist_20180412.json")
    if not os.path.exists(distr_path): return {}
    fin = open(distr_path, "r", encoding="UTF-8")
    distr_data = json.load(fin)    
    fin.close()

    return distr_data

