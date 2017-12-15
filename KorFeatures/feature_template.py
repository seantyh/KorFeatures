from collections import OrderedDict
import pdb
def make_features():
    fields = [
        # --- surface ---
        ("nChar", 0), 
        ("nWord", 0),  
        ("nClause", 0),
        ("nSentence", 0),
        ("WordLen_Q25", 0),
        ("WordLen_Q50", 0),
        ("WordLen_Q75", 0),
        ("ClsLen_Q25", 0), 
        ("ClsLen_Q50", 0), 
        ("ClsLen_Q75", 0), 
        ("SenLen_Q25", 0), 
        ("SenLen_Q50", 0), 
        ("SenLen_Q75", 0), 
        ("CharStrokes_Q25", 0),
        ("CharStrokes_Q50", 0),
        ("CharStrokes_Q75", 0),

        # --- character/word information ---
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
        ("nNoun", 0), ("rNoun", 0.0), 
        ("nVerb", 0), ("rVerb", 0.0), 
        ("nAdjective", 0), ("rAdjective", 0.0), 
        ("nPronoun", 0), ("rPronoun", 0.0), 
        ("nIntentionVerb", 0), ("rIntentionVerb", 0.0), 
        ("nImperativeVerb", 0), ("rImperativeVerb", 0.0), 
        ("rTypeToken", 0.0),
        ("rContent", 0.0),
        ("rContentFunction", 0.0), 
        ("rPronounNoun", 0.0),
        
        # --- Syntactic ---
        ("PropDepth", 0), 
        ("SynSim", 0.0), 
        ("nWordBeforeMV", 0.0), 
        ("nModifierNP", 0.0),
        ("nNP", 0), ("rNP", 0.0),
        ("nVP", 0), ("rVP", 0.0),
        ("nPP", 0), ("rPP", 0.0),
        ("nBaSentence", 0), ("rBaSentence", 0.0),
        ("nBeiSentence", 0), ("rBeiSentence", 0.0),
        ("nBiSentence", 0), ("rBiSentence", 0.0),
        # --- Connectives ---
        ("nConn", 0), ("rConn", 0.0),
        ("nConnAdditive", 0), ("rConnAdditive", 0.0),
        ("nConnTemporal", 0), ("rConnTemporal", 0.0),
        ("nConnPositive", 0), ("rConnPositive", 0.0),
        ("nConnSelection", 0), ("rConnSelection", 0.0),
        ("nConnNegative", 0), ("rConnNegative", 0.0),
        ("nConnCausal", 0), ("rConnCausal", 0.0),
        ("nConnConditional", 0), ("rConnConditional", 0.0),
        ("nConnHypothesis", 0), ("rConnHypothesis", 0.0),
        ("nConnGoal", 0), ("rConnGoal", 0.0),
        ("nConnExemplar", 0), ("rConnExemplar", 0.0),

        # --- referential coherence ---
        ("NounOverlap_Local", 0), 
        ("NounOverlap_Given", 0),         
        ("ContentOverlap_Local", 0), 
        ("ContentOverlap_Given", 0),   

        # --- semantic ---              
        ("nSense_Q25", 0.0), 
        ("nSense_Q50", 0.0), 
        ("nSense_Q75", 0.0), 
        ("SemanticOverlap_Local", 0), 
        ("SemanticOverlap_Given", 0)                
    ]
    
    return OrderedDict(fields)


