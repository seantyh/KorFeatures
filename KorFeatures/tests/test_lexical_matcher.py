import unittest
from KorFeatures.lexical_matcher import LexicalMatcher

class LexicalMatcherTest(unittest.TestCase):
    @unittest.skip("")
    def testLexicalFeature(self):
        lm = LexicalMatcher()
        single_feat = ["雖然"]
        intext = "雖然/你/常/說/雖然/，/但是/我/不/知道/。"
        ret = lm.match_features(intext.split("/"), single_feat)
        print(ret)
        self.assertTrue(ret[("雖然",)] == 2)

    def testLexicalPatterns(self):
        lm = LexicalMatcher()
        single_feat = [["雖然", "但是"], ["與其"]]
        intext = "雖然/你/常/說/與其/這樣/，/但是/我/與其/不/知道/。"
        ret = lm.match_features(intext.split("/"), single_feat)
        print(ret)
        self.assertTrue(ret[("雖然", "但是")] == 1)
        self.assertTrue(ret[("與其", )] == 2)

    def testLexicalPatterns2(self):
        lm = LexicalMatcher()
        single_feat = [["因為", "所以"], ["因為"]]
        intext = "因為/因為/這樣/所以/那樣/所以/。"

        ret = lm.match_features(intext.split("/"), single_feat)
        print(ret)
        self.assertTrue(ret[("因為", "所以")] == 1)
        self.assertTrue(ret[("因為", )] == 2)
if __name__ == "__main__":
    unittest.main()
