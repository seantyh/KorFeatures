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
        feats = korFeats.feats
        print("KorFeatures: ")
        print(korFeats.feats)
        self.assertTrue(len(korFeats.feats) > 0)
        self.assertTrue(feats['CharFreq_Q25'] > 0)
        self.assertTrue(feats['WordFreq_Q25'] > 0)
        self.assertTrue(feats['CharRank_1500'] > 0)
        self.assertTrue(feats['WordRank_1000'] > 0)
        self.assertTrue(feats['nChar'] > 0)
        self.assertTrue(feats['nWord'] > 0)
        self.assertTrue(feats['ClsLen_Q25'] > 0)
        self.assertTrue(feats['SenLen_Q25'] > 0)
        self.assertTrue(feats['PropDepth_Q25'] > 0)
        self.assertTrue(feats['SynSim'] > 0)
        self.assertTrue(feats['nWordBeforeMV'] > 0)
        self.assertTrue(feats['nConn'] > 0)
        self.assertTrue(feats['rPronNoun'] > 0)
        self.assertTrue(feats['NounOverlap_Local'] > 0)
        self.assertTrue(feats['SemanticOverlap_Local'] > 0)                
        
if __name__ == "__main__":
    unittest.main()