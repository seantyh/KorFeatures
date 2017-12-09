import unittest
import pickle
from os.path import exists
from KorFeatures.oceanus_data_preproc import OceanusDataPreproc
from KorFeatures.dep_tree_structure import DepTreeStructure
from pyOceanus import Oceanus

class DepTreeStructureTest(unittest.TestCase):
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

    def testTreeDepth(self):                
        od = self.load_test_data()
        odp = OceanusDataPreproc(od)
        deps = odp.deps()
        tokens = odp.tokens()
        dts = DepTreeStructure(deps[0], tokens)
        print(dts.get_depth())
        print(odp.deps())

    def testnWordMV(self):                
        od = self.load_test_data()
        odp = OceanusDataPreproc(od)
        deps = odp.deps()
        tokens = odp.tokens()
        tokens = [x for x in tokens if x.sentenceIndex == 0]
        dts = DepTreeStructure(deps[0], tokens)
        print("nWordBeforeMV:", dts.n_word_before_mv())        

if __name__ == "__main__":
    unittest.main()