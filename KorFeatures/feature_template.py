from collections import OrderedDict

def make_features():
    fields = [
        ("CharFreq_Q01", 0), 
        ("CharFreq_Q05", 0), 
        ("CharFreq_Q25", 0), 
        ("CharFreq_Q50", 0), 
        ("CharFreq_Q75", 0),                 
        ("CharRank_800", 0),
        ("CharRank_1500", 0),
        ("CharRank_3000", 0),
        ("CharRank_6000", 0),
        ("WordFreq_Q01", 0), 
        ("WordFreq_Q05", 0), 
        ("WordFreq_Q25", 0), 
        ("WordFreq_Q50", 0), 
        ("WordFreq_Q75", 0),                 
        ("WordRank_1000", 0),
        ("WordRank_2000", 0),
        ("WordRank_50K", 0),
        ("WordRank_100K", 0),
        ("nChar", 0), 
        ("CharStrokes_Q25", 0),
        ("CharStrokes_Q50", 0),
        ("CharStrokes_Q75", 0),
        ("nWord", 0),         
        ("WordLen_Q25", 0),
        ("WordLen_Q25", 0),
        ("WordLen_Q50", 0),
        ("ClsLen_Q25", 0), 
        ("ClsLen_Q50", 0), 
        ("ClsLen_Q75", 0), 
        ("SenLen_Q25", 0), 
        ("SenLen_Q50", 0), 
        ("SenLen_Q75", 0), 
        # ---
        ("PropDepth_Q25", 0), 
        ("PropDepth_Q50", 0), 
        ("PropDepth_Q75", 0), 
        ("rFuncCont", 0.0), 
        ("SynSim", 0), 
        ("nWordBeforeMV", 0), 
        # ---
        ("nConn", 0), 
        ("rPronNoun", 0.0), 
        ("rTypeToken", 0.0), 
        ("NounOverlap_Local", 0), 
        ("NounOverlap_Given", 0),         
        ("ContentOverlap_Local", 0), 
        ("ContentOverlap_Given", 0),                 
        ("SemanticOverlap_Local", 0), 
        ("SemanticOverlap_Given", 0),         
        # ---
        ("FirstTopic", -1), 
        ("SecondTopic", -1), 
        ("ThirdTopic", -1), 
        ("Top5CumuProp", 0.0), 
        ("Top5Entropy", 0.0)
    ]
    return OrderedDict(fields)


