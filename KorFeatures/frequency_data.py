import os
import pickle
import logging
import pdb

logger = logging.getLogger(__file__)
BASEPATH = os.path.dirname(__file__)
class CharFreq:
    def __init__(self):
        CHAR_FREQ_FPATH = os.path.join(BASEPATH, "etc/as_chFreq.pickle")
        if not os.path.exists(CHAR_FREQ_FPATH):
            logger.error("Cannot found character frequency pickle: " + CHAR_FREQ_FPATH)
        with open(CHAR_FREQ_FPATH, "rb") as fin:
            self.freq_data = pickle.load(fin)
            sorted_ch = sorted(self.freq_data.keys(), 
                    key = self.freq_data.get, reverse=True)
            self.rank_data = {ch: i for i, ch in enumerate(sorted_ch)}

    def get(self, ch):
        return self.freq_data.get(ch, 0)

    def get_rank(self, ch):
        return self.rank_data.get(ch, len(self.rank_data))

class WordFreq:
    def __init__(self):
        WORD_FREQ_FPATH = os.path.join(BASEPATH, "etc/as_wordFreq.pickle")
        if not os.path.exists(WORD_FREQ_FPATH):
            logger.error("Cannot found word frequency pickle: " + WORD_FREQ_FPATH)
        with open(WORD_FREQ_FPATH, "rb") as fin:
            self.freq_data = pickle.load(fin)
            sorted_wd = sorted(self.freq_data.keys(), 
                    key = self.freq_data.get, reverse=True)
            self.rank_data = {wd: i for i, wd in enumerate(sorted_wd)}

    def get(self, wd):       
        return self.freq_data.get(wd, 0)        
    
    def get_rank(self, wd):
        return self.rank_data.get(wd, len(self.rank_data))
