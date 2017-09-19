import os
import json
import logging
BASEPATH = os.path.dirname(__file__)

class StrokeData():
    def __init__(self):
        fpath = os.path.join(BASEPATH, "etc/stk_data.json")
        self.stkdata = json.load(open(fpath, "r", encoding="UTF-8"))

    def get(self, ch):
        return self.stkdata.get(ch, -1)
        
