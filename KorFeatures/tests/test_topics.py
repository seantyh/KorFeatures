import unittest
from os.path import join
from KorFeatures import TopicModel

class TopicTest(unittest.TestCase):
    def testTopic(self):
        DATA_PATH = "../etc/tm"
        MODEL_PATH = join(DATA_PATH, "asbc5_200_gensim_pass20.model")
        DICT_PATH = join(DATA_PATH, "gensim_asbc.dict")
        topic_model = TopicModel(MODEL_PATH, DICT_PATH)
        W1 = "醫生"
        W2 = "護士"
        W3 = "總統"
        W4 = ["醫院", "醫生"]
        W5 = ["樹木", "醫生"]
        prob1 = topic_model.get_word_assoc(W1, W2)
        prob2 = topic_model.get_word_assoc(W1, W3)
        prob3 = topic_model.get_word_assoc(W2, W4)
        prob4 = topic_model.get_word_assoc(W2, W5)
        
        print("%s -> %s: %.6f" % (W2, W1, prob1))
        print("%s -> %s: %.6f" % (W3, W1, prob2))
        print("%s -> %s: %.6f" % (W4, W2, prob3))
        print("%s -> %s: %.6f" % (W5, W2, prob4))

    def testDocInference(self):
        DATA_PATH = "../etc/tm"
        MODEL_PATH = join(DATA_PATH, "asbc5_200_gensim_pass20.model")
        DICT_PATH = join(DATA_PATH, "gensim_asbc.dict")
        topic_model = TopicModel(MODEL_PATH, DICT_PATH)
        probs = topic_model.get_doc_topic_prob(["政府", "官員", "今日", "出面", "指出"])
        topic_model.print_topic(probs)
        
if __name__ == "__main__":
    unittest.main()

