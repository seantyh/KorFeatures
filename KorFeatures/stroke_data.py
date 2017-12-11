import os
import json
import logging
BASEPATH = os.path.dirname(__file__)

class StrokeData():
    def __init__(self):
        fpath = os.path.join(BASEPATH, "etc/stk_data.json")
        with open(fpath, "r", encoding="UTF-8") as fin:
            self.stkdata = json.load(fin)

    def get(self, ch):
        return self.stkdata.get(ch, -1)
        
