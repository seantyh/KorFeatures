from unittest import TestCase
import unittest
from KorFeatures import OceanusDataPreproc
import pyOceanus

class TestOceanusDataPreproc(TestCase):
    def testPreproc(self):
        oc = pyOceanus.Oceanus()
        ocdata = oc.parse("這是一個測試的句子，有的地方沒有句號。句號後有一個新句子，這就是全部的材料。")
        oc_preproc = OceanusDataPreproc(ocdata)
        self.assertGreater(len(oc_preproc.tokens()), 0)
        self.assertGreater(len(oc_preproc.trees()), 0)
        self.assertGreater(len(oc_preproc.deps()), 0)
        # print(oc_preproc.tokens())
        # print(oc_preproc.trees())
        # print(oc_preproc.deps())

if __name__ == "__main__":
    unittest.main()
        