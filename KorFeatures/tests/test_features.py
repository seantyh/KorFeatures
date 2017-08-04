import unittest
from unittest import TestCase
from KorFeatures import KorFeatures, OceanusDataPreproc
import pyOceanus

class TestFeatures(TestCase):
    def test_init(self):        
        self.assertRaises(Exception, KorFeatures)

    def test_features(self):
        oc = pyOceanus.Oceanus()
        ocdata = oc.parse("這是一個測試的句子，有的地方沒有句號。句號後有一個新句子，這就是全部的材料。")
        oc_preproc = OceanusDataPreproc(ocdata)
        
        korFeats = KorFeatures("test_sentence",
                    oc_preproc.tokens(), 
                    oc_preproc.trees(), 
                    oc_preproc.deps())
        self.assertTrue(len(korFeats.feats) > 0)
        
if __name__ == "__main__":
    unittest.main()