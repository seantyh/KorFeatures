
class SenseData:
    def __init__(self, fpath):        
        self.data = {}
        with open(fpath, "r", encoding="UTF-8") as fin:
            for ln in fin.readlines():
                toks = ln.split(",")
                self.data[toks[0]] = int(toks[1])
    
    def get(self, word):
        return self.data.get(word, 1)