import unittest
import pickle
from os.path import exists
from KorFeatures.oceanus_data_preproc import OceanusDataPreproc
from KorFeatures.PTree import PTree
from pyOceanus import Oceanus

class PTreeTest(unittest.TestCase):
    def load_test_data(self):
        DEP_DATA_PATH = "dep_data.pyObj"
        if not exists(DEP_DATA_PATH):
            oc = Oceanus("http://140.112.147.120:8090/nlp/parse")
            od = oc.parse("今天我去看了一部很有趣的電影，它在講童話故事。")            
            with open(DEP_DATA_PATH, "wb") as fout:
                pickle.dump(od, fout)
        else:
            with open(DEP_DATA_PATH, "rb") as fin:
                od = pickle.load(fin)
        return od

    def testFindNode(self):                
        od = self.load_test_data()
        odp = OceanusDataPreproc(od)        
        trees = odp.trees()
        print(trees)
        print("n_NP: ", trees[0].find_node("NP"))
    
    def testTerminalCount(self):                
        od = self.load_test_data()
        odp = OceanusDataPreproc(od)        
        trees = odp.trees()
        print(trees)
        print("n_term: ", trees[0].terminal_count())
        self.assertEqual(trees[0].terminal_count(), 18)

if __name__ == "__main__":
    unittest.main()