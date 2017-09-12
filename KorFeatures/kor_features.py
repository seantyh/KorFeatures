from typing import Text, List, Any, Dict
from itertools import groupby
import numpy as np
from . import feature_template
from .frequency_data import *
from .pos_class import PosClass
from .overlap_algo import *
from .zh_characters import *
from .KorTypes import *
from .PTree import PTree
from .oceanus_data_preproc import OceanusDataPreproc
from . import topics
import pdb

FUNC_POS_LIST = PosClass().get_functional_class()
CONT_POS_LIST = PosClass().get_content_class()
CONN_POS_LIST = PosClass().get_connective_class()

CharFreqData = CharFreq()
WordFreqData = WordFreq()  


def mean(rv):
    if (len(rv) == 0): return 0
    return sum(rv) / len(rv)

class KorFeatures:
    @staticmethod
    def fromOceanusData(ocdata):
        oc_preproc = OceanusDataPreproc(ocdata)
        tokens = oc_preproc.tokens()
        trees = oc_preproc.trees()
        deps = oc_preproc.deps()
        korFeats = KorFeatures("KorFeatures", tokens, trees, deps)
        return korFeats
        
    def __init__(self, dio_name: Text,
        tokens: List[TokenData],
        trees: List[PTree], deps: List[DepData]) -> None:        

        self.name = dio_name        
        self.tokens = tokens
        self.trees = trees
        self.deps = deps

        self.feats = feature_template.make_features()        
        self.computeFeatures()
        
    def features(self) -> Dict[Text, float]:        
        return self.feats

    def topicList(self):
        return topics.TOPIC_LIST
    
    def computeFeatures(self):
        self.computeSurface()
        self.computeStructures()
        self.computeCohesive()
        self.computeTopics()

    def computeSurface(self):
        feats = self.feats
        toks: List[TokenData] = self.tokens
        
        real_tokens = list(filter(lambda x: 
                        not x.pos.startswith("PU"), toks))
        real_tokens = filter(lambda x: isZhChars(x.text), real_tokens)                        
        real_tokens = list(real_tokens)
        chars = "".join([x.text for x in real_tokens])
        nChar = len(chars)        
        nWord = len(real_tokens)
        feats["nChar"] = int(nChar)
        feats["nWord"] = int(nWord)
        
        # Frequency data      
        char_freq_vec = [CharFreqData.get(x) for x in chars]
        word_freq_vec = [WordFreqData.get(x.text) for x in real_tokens]
        self.setQuantileFeatures("CharFreq", char_freq_vec)
        self.setQuantileFeatures("WordFreq", word_freq_vec)
        self.setLowPerctFeatures("CharFreq", char_freq_vec)
        self.setLowPerctFeatures("WordFreq", word_freq_vec)

        # Rank data
        char_rank_vec = [CharFreqData.get_rank(x) for x in chars]
        word_rank_vec = [WordFreqData.get_rank(x.text) for x in real_tokens]
        chnorm = lambda x: x / len(chars)
        feats["CharRank_800"] = chnorm(sum((1 for x in char_rank_vec if x < 800)))
        feats["CharRank_1500"] = chnorm(sum((1 for x in char_rank_vec if x >= 800 and x < 1500)))
        feats["CharRank_3000"] = chnorm(sum((1 for x in char_rank_vec if x >= 1500 and x < 3000)))
        feats["CharRank_6000"] = chnorm(sum((1 for x in char_rank_vec if x >= 3000 and x < 6000)))

        wdnorm = lambda x: x / len(toks)
        feats["WordRank_1000"] = wdnorm(sum((1 for x in word_rank_vec if x < 1000)))
        feats["WordRank_2000"] = wdnorm(sum((1 for x in word_rank_vec if x >= 1000 and x < 2000)))
        feats["WordRank_50K"] = wdnorm(sum((1 for x in word_rank_vec if x >= 2000 and x < 50000)))
        feats["WordRank_100K"] = wdnorm(sum((1 for x in word_rank_vec if x >= 50000 and x < 100000)))

        # Clause/sentence length
        clsLen = {i: len(list(seq)) for i, seq in groupby(real_tokens, lambda x: x.clauseIndex)}
        senLen = {i: len(list(seq)) for i, seq in groupby(real_tokens, lambda x: x.sentenceIndex)}
        
        self.setQuantileFeatures("ClsLen", list(clsLen.values()))
        self.setQuantileFeatures("SenLen", list(senLen.values()))        

    def computeStructures(self):
        # Functional / Content
        toks = self.tokens
        nFunc = len(list(filter(lambda x: x.pos in FUNC_POS_LIST, toks)))
        nCont = len(list(filter(lambda x: x.pos in CONT_POS_LIST, toks)))
        self.feats["rFuncCont"] = nFunc/nCont

        # Tree depths
        trees = self.trees
        props_depth = [tree_x.depth() for tree_x in trees]
        self.setQuantileFeatures("PropDepth", props_depth)

        # Tree similarity of ajacent pairs
        tree_sim = []
        for t1, t2 in zip(trees, trees[1:]):
            tree_sim.append(t1.similarity(t2))
        if (len(tree_sim)) == 0: tree_sim = [0]
        self.feats["SynSim"] = sum(tree_sim)/len(tree_sim)        
        self.feats["nWordBeforeMV"] = 0

        # words before main verb
        deps = self.deps             
        nwMV = []
        for seq_i, seq_dep in enumerate(deps):
            main_verb = self.find_main_verb(seq_i, seq_dep, toks)
            mv_pos = self.find_token_position_in_sentence(main_verb)
            nwMV.append(mv_pos)        
        nwMV = list(filter(lambda x: x>0, nwMV))

        if (len(nwMV)) == 0: nwMV = [0]
        self.feats["nWordBeforeMV"] = sum(nwMV)/len(nwMV)        

    def computeCohesive(self):
        toks = self.tokens

        # number of connective
        nConn = len(list(filter(lambda x: x.pos in CONN_POS_LIST, toks)))
        self.feats["nConn"] = nConn

        # number of Pronoun and Noun
        nNoun = len(list(filter(lambda x: x.pos.startswith("N"), toks)))
        nPronoun = len(list(filter(lambda x: x.pos == "PN", toks)))
        rPronNoun = nPronoun / nNoun
        self.feats["rPronNoun"] = rPronNoun

        # type/token ratio
        uniq_type = set(x.text for x in self.tokens)
        rTypeToken = len(uniq_type) / len(self.tokens)
        self.feats["rTypeToken"] = rTypeToken

        # Overlapping, adjacent(local) and given/new
        seq_list = list(range(max(x.sentenceIndex for x in toks)+1))
        noun_toks = list(filter(lambda x: x.pos.startswith("N"), toks))
        cont_toks = list(filter(lambda x: x.pos in CONT_POS_LIST, toks))
        get_seq_tok = lambda tok_list, seqi: [x for x in tok_list if x.sentenceIndex == seqi]
        get_prev_seq_tok = lambda tok_list, seqi: [x for x in tok_list if x.sentenceIndex < seqi]

        noun_overlap_local_vec = []
        cont_overlap_local_vec = []
        noun_overlap_given_vec = []
        cont_overlap_given_vec = []
        for (seq1, seq2) in zip(seq_list, seq_list[1:]):
            tkOverlap = TokenOverlap()
            noun_overlap_local_vec.append(tkOverlap.text_overlap(
                get_seq_tok(noun_toks, seq1),
                get_seq_tok(noun_toks, seq2),
            ))

            cont_overlap_local_vec.append(tkOverlap.text_overlap(
                get_seq_tok(cont_toks, seq1),
                get_seq_tok(cont_toks, seq2),
            ))

            noun_overlap_given_vec.append(tkOverlap.text_overlap(
                get_seq_tok(noun_toks, seq2),
                get_prev_seq_tok(noun_toks, seq2),
            ))

            cont_overlap_given_vec.append(tkOverlap.text_overlap(
                get_seq_tok(cont_toks, seq2),
                get_prev_seq_tok(cont_toks, seq2),
            ))

        self.feats["NounOverlap_Local"] = mean(noun_overlap_local_vec)
        self.feats["ContentOverlap_Local"] = mean(cont_overlap_local_vec)
        self.feats["NounOverlap_Given"] = mean(noun_overlap_given_vec)
        self.feats["ContentOverlap_Given"] = mean(cont_overlap_given_vec)

        # Embedding overlap
        emb_overlap_local_vec = []
        emb_overlap_given_vec = []
        embOverlap = EmbeddingOverlap()
        for (seq1, seq2) in zip(seq_list, seq_list[1:]):            
            emb_overlap_local_vec.append(embOverlap.embed_overlap(
                get_seq_tok(toks, seq1),
                get_seq_tok(toks, seq2),
            ))

            emb_overlap_given_vec.append(embOverlap.embed_overlap(
                get_seq_tok(toks, seq1),
                get_prev_seq_tok(toks, seq2),
            ))
        
        self.feats["SemanticOverlap_Local"] = mean(emb_overlap_local_vec)
        self.feats["SemanticOverlap_Given"] = mean(emb_overlap_given_vec)
        
    def computeTopics(self):
        # topic_query = TopicQuery()
        if not topics.test_topics_endpoint:
            return
        
        words = [x.text for x in self.tokens]
        topics_data = topics.get_topics(words)
        # topic_ids = topic_query.query_top_topics(self.name)
        # topic_ps = topic_query.query_top_probs(self.name)
        if topics_data is None: return
        topic_ids = topics_data["topic"]
        self.feats["FirstTopic"] = topic_ids[0]
        self.feats["SecondTopic"] = topic_ids[1]
        self.feats["ThirdTopic"] = topic_ids[2]

        topic_probs = topics_data["p"]
        prob5 = np.array(topic_probs[:5])
        self.feats["Top5CumuProp"] = np.sum(prob5)

        prob5x = np.concatenate([prob5, [1-np.sum(prob5)]])
        self.feats["Top5Entropy"] = - np.sum(prob5x * np.log(prob5x))        

    def setQuantileFeatures(self, field, rv):
        try:
            self.feats[field + "_Q25"] = np.percentile(rv, 25)
            self.feats[field + "_Q50"] = np.percentile(rv, 50)
            self.feats[field + "_Q75"] = np.percentile(rv, 75)
        except KeyError as ex:
            logging.getLogger().error("Cannot find %s" % ex)

    def setLowPerctFeatures(self, field, rv):
        try:
            self.feats[field + "_Q05"] = np.percentile(rv, 5)
            self.feats[field + "_Q01"] = np.percentile(rv, 1)
        except KeyError as ex:
            logging.getLogger().error("Cannot find %s" % ex)

    def find_main_verb(self, sentenceIdx: int, seqDep: DepData, tokens) -> TokenData:
        rootDep: DepData = [x for x in seqDep if x.relation == "root"]
        if (len(rootDep) == 0): return None
        
        root_depi = int(rootDep[0].depIndex)
        main_token = [x for i, x in enumerate(tokens) if i == root_depi]
        if len(main_token) == 0:
            return None

        if main_token[0].pos.startswith("V"):
            return main_token[0]
        else:
            return None

    def find_token_position_in_sentence(self, token: TokenData) -> int:
        if token is None:
            return -1

        sent_of_token = [token_x for token_x in self.tokens 
                            if token_x.sentenceIndex == token.sentenceIndex]
        pos_in_sentence = sent_of_token.index(token)
        return pos_in_sentence

