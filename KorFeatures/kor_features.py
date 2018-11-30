from typing import Text, List, Any, Dict
from itertools import groupby
from os.path import abspath, dirname, join
import numpy as np
from . import syntax_tree
from . import feature_template
from .frequency_data import *
from .stroke_data import StrokeData
from .lexical_matcher import LexicalFeatureData
from .sense_data import SenseData
from .pos_class import PosClass
from .dep_tree_structure import DepTreeStructure
from .topics import TopicModel
from .overlap_algo import *
from .zh_characters import *
from .KorTypes import *
from .PTree import PTree
from .oceanus_data_preproc import OceanusDataPreproc
from . import topics
import pdb

CURDIR = abspath(dirname(__file__))

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
        trees: List[PTree], deps: List[DepData], skipTopic=False) -> None:

        self.name = dio_name
        self.tokens = tokens
        self.trees = trees
        self.deps = deps
        self.skipTopic = skipTopic
        self.debugData = {}

        self.feats = feature_template.make_features()
        self.computeFeatures()

    def features(self) -> Dict[Text, float]:
        return self.feats

    def debug_data(self):
        return self.debugData

    def computeFeatures(self):
        # note: self.n_real_tokens is required for various computation
        # it is assigned in computeSurface(), make sure it executes first
        self.computeSurface()
        self.computeStructures()
        self.computeCohesive()

    def computeSurface(self):
        feats = self.feats
        toks: List[TokenData] = self.tokens

        real_tokens = list(filter(lambda x:
                        not x.pos.startswith("PU"), toks))
        real_tokens = filter(lambda x: isZhChars(x.text), real_tokens)
        real_tokens = list(real_tokens)
        self.n_real_tokens = len(real_tokens)
        self.debugData["real_tokens"] = [x.toJSON() for x in real_tokens]

        chars = "".join([x.text for x in real_tokens])
        nChar = len(chars)
        nWord = len(real_tokens)
        wlen_vec = [len(x.text) for x in real_tokens]
        feats["nChar"] = int(nChar)
        feats["nWord"] = int(nWord)
        self.setQuantileFeatures("WordLen", wlen_vec)
        self.debugData["word_len"] = wlen_vec

        # Frequency data
        char_freq_vec = [CharFreqData.get(x) for x in chars]
        word_freq_vec = [WordFreqData.get(x.text) for x in real_tokens]
        self.setQuantileFeatures("CharFreq", char_freq_vec)
        self.setQuantileFeatures("WordFreq", word_freq_vec)
        self.setLowPerctFeatures("CharFreq", char_freq_vec)
        self.setLowPerctFeatures("WordFreq", word_freq_vec)
        self.debugData["char_freq_vec"] = char_freq_vec
        self.debugData["word_freq_vec"] = word_freq_vec

        # Rank data
        char_rank_vec = [CharFreqData.get_rank(x) for x in chars]
        word_rank_vec = [WordFreqData.get_rank(x.text) for x in real_tokens]
        self.debugData["char_rank_vec"] = char_rank_vec
        self.debugData["word_rank_vec"] = word_rank_vec

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

        # Stroke data
        stk_data = StrokeData()
        stk_vec = [stk_data.get(ch) for ch in chars]
        self.setQuantileFeatures("CharStrokes", stk_vec)
        self.debugData["stroke_vec"] = stk_vec

        # Clause/sentence length
        clsLen = {i: len(list(seq)) for i, seq in groupby(real_tokens, lambda x: x.clauseIndex)}
        senLen = {i: len(list(seq)) for i, seq in groupby(real_tokens, lambda x: x.sentenceIndex)}

        # this part is for generating clause length vector nested in sentences
        clsLen_tup_group = groupby(real_tokens, lambda x: (x.sentenceIndex, x.clauseIndex))
        clsLen_tup = {}
        for idx_tup, tok_vec in clsLen_tup_group:
            cls_len_x = len(list(tok_vec))
            cls_sen_idx = idx_tup[0]
            clsLen_sen = clsLen_tup.get(cls_sen_idx, [])
            clsLen_sen.append(cls_len_x)
            clsLen_tup[cls_sen_idx] = clsLen_sen

        self.debugData["clsInSen_len"] = [mean(clsLen_tup[idx]) for idx in sorted(clsLen_tup.keys())]
        self.debugData["sen_len"] = [senLen[idx] for idx in sorted(senLen.keys())]

        # POS data
        pos_freq = {"N": 0, "V": 0, "A": 0, "PN": 0, "BA": 0, "BEI": 0}
        for tok in real_tokens:
            if tok.pos.startswith("N"):
                pos_freq["N"] += 1
            elif tok.pos.startswith("V"):
                pos_freq["V"] += 1
            elif tok.pos in ("JJ", "AD"):
                pos_freq["A"] += 1
            elif tok.pos == "PN":
                pos_freq["PN"] += 1
            elif tok.pos == "BA":
                pos_freq["BA"] += 1
            elif tok.pos in ("LB", "SB"):
                pos_freq["BEI"] += 1

        self.setCountFeatures("Noun", pos_freq["N"], self.n_real_tokens)
        self.setCountFeatures("Verb", pos_freq["V"], self.n_real_tokens)
        self.setCountFeatures("Adjective", pos_freq["A"], self.n_real_tokens)
        self.setCountFeatures("Pronoun", pos_freq["PN"], self.n_real_tokens)
        self.setCountFeatures("BaSentence", pos_freq["BA"], self.n_real_tokens)
        self.setCountFeatures("BeiSentence", pos_freq["BEI"], self.n_real_tokens)
        if pos_freq["N"]:
            self.feats["rPronounNoun"] = pos_freq["PN"] / pos_freq["N"]

        # Intention/Imperative
        DATA_PATH = join(CURDIR, "etc")
        lexFeatData = LexicalFeatureData(join(DATA_PATH, "verb_category.json"))
        word_list = [x.text for x in real_tokens]

        nImpVerb = lexFeatData.count_imperative_verb(word_list)
        nIntVerb = lexFeatData.count_intentional_verb(word_list)
        nBi = lexFeatData.count_BiMarker(word_list)
        nConnAdd = lexFeatData.count_conn(word_list, "並列")
        nConnTemp = lexFeatData.count_conn(word_list, "承接")
        nConnPos = lexFeatData.count_conn(word_list, "遞進")
        nConnSel = lexFeatData.count_conn(word_list, "選擇")
        nConnNeg = lexFeatData.count_conn(word_list, "轉折")
        nConnCausal = lexFeatData.count_conn(word_list, "因果")
        nConnCond = lexFeatData.count_conn(word_list, "條件")
        nConnHypo = lexFeatData.count_conn(word_list, "假設")
        nConnGoal = lexFeatData.count_conn(word_list, "目的")
        nConnExemplar = lexFeatData.count_conn(word_list, "解證")
        nConn = sum([nConnAdd, nConnTemp, nConnPos, nConnSel,
                    nConnNeg, nConnCausal, nConnCond, nConnHypo,
                    nConnGoal, nConnExemplar])
        self.setCountFeatures("ImperativeVerb", nImpVerb, self.n_real_tokens)
        self.setCountFeatures("IntentionVerb", nIntVerb, self.n_real_tokens)
        self.setCountFeatures("BiSentence", nBi, self.n_real_tokens)
        self.setCountFeatures("ConnAdditive", nConnAdd, self.n_real_tokens)
        self.setCountFeatures("ConnTemporal", nConnTemp, self.n_real_tokens)
        self.setCountFeatures("ConnPositive", nConnPos, self.n_real_tokens)
        self.setCountFeatures("ConnSelection", nConnSel, self.n_real_tokens)
        self.setCountFeatures("ConnNegative", nConnNeg, self.n_real_tokens)
        self.setCountFeatures("ConnCausal", nConnCausal, self.n_real_tokens)
        self.setCountFeatures("ConnConditional", nConnCond, self.n_real_tokens)
        self.setCountFeatures("ConnHypothesis", nConnHypo, self.n_real_tokens)
        self.setCountFeatures("ConnGoal", nConnGoal, self.n_real_tokens)
        self.setCountFeatures("ConnExemplar", nConnExemplar, self.n_real_tokens)
        self.setCountFeatures("Conn", nConn, self.n_real_tokens)


        feats["nClause"] = len(clsLen)
        feats["nSentence"] = len(senLen)
        self.setQuantileFeatures("ClsLen", list(clsLen.values()))
        self.setQuantileFeatures("SenLen", list(senLen.values()))


    def computeStructures(self):
        # Functional / Content
        toks = self.tokens
        trees = self.trees

        # max-depth
        tree_heights = syntax_tree.get_tree_height(trees)
        max_depth = max(tree_heights)        

        # nHapaxes
        n_hapaxes = syntax_tree.get_n_hapaxes(trees)
        
        self.feats["max_depth"] = max_depth
        self.setQuantileFeatures("nHapaxes", n_hapaxes)
        self.setQuantileFeatures("treeHeight", tree_heights)

        # Tree similarity of ajacent pairs        
        tree_sim = []
        for t1, t2 in zip(trees, trees[1:]):
            tree_sim.append(t1.similarity(t2))
        if (len(tree_sim)) == 0: tree_sim = [0]
        self.feats["SynSim"] = sum(tree_sim)/len(tree_sim)
        self.debugData["syn_sim_vec"] = [-1] + tree_sim

        # Dep-Tree features
        ## words before main verb
        deps = self.deps
        nwMV_vec = []
        depths_vec = []
        nModNP_vec = []
        for seq_i, seq_dep in enumerate(deps):
            seq_tok = [x for x in toks if x.sentenceIndex == seq_i]
            depStruct = DepTreeStructure(seq_dep, seq_tok)

            # number of words before main verb
            mv_pos = depStruct.n_word_before_mv()
            nwMV_vec.append(mv_pos)

            # maximum number of modifiers per noun
            nModNP = 0
            for toki, tok in enumerate(toks):
                if tok.pos.startswith("N"):
                    nModNP_x = depStruct.get_dependents(toki)
                    if nModNP < nModNP_x: nModNP = nModNP_x
            nModNP_vec.append(nModNP)

            # proposition depth
            depth_x = depStruct.get_depth()
            depths_vec.append(depth_x)

        self.debugData["nModNP_vec"] = nModNP_vec
        self.debugData["nwMV_vec"] = nwMV_vec
        self.debugData["depths_vec"] = depths_vec

        self.feats["nWordBeforeMV"] = sum(nwMV_vec)/len(nwMV_vec)
        self.feats["nModifierNP"] = sum(nModNP_vec)/len(nModNP_vec)
        self.feats["PropDepth"] = sum(depths_vec)/len(depths_vec)

        # count of Noun/Verb/Preposition phrase
        nNP = sum([tree_x.find_node("NP") for tree_x in trees])
        nVP = sum([tree_x.find_node("VP") for tree_x in trees])
        nPP = sum([tree_x.find_node("PP") for tree_x in trees])
        self.setCountFeatures("NP", nNP, self.n_real_tokens)
        self.setCountFeatures("VP", nVP, self.n_real_tokens)
        self.setCountFeatures("PP", nPP, self.n_real_tokens)

    def computeCohesive(self):
        toks = self.tokens

        # type/token ratio
        uniq_type = set(x.text for x in self.tokens)
        rTypeToken = len(uniq_type) / len(self.tokens)
        self.feats["rTypeToken"] = rTypeToken

        # Overlapping, adjacent(local) and given/new
        seq_list = list(range(max(x.sentenceIndex for x in toks)+1))
        real_tokens = list(filter(lambda x: not x.pos.startswith("PU"), toks))
        noun_toks = list(filter(lambda x: x.pos.startswith("N"), toks))
        cont_toks = list(filter(lambda x: x.pos in CONT_POS_LIST, toks))
        func_toks = list(filter(lambda x: x.pos in FUNC_POS_LIST, toks))
        get_seq_tok = lambda tok_list, seqi: [x for x in tok_list if x.sentenceIndex == seqi]
        get_prev_seq_tok = lambda tok_list, seqi: [x for x in tok_list if x.sentenceIndex < seqi]

        self.feats["rContent"] = len(cont_toks) / self.n_real_tokens
        if func_toks:
            self.feats["rContentFunction"] = len(cont_toks) / len(func_toks)

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

        self.debugData["noun_overlap_local_vec"] = [-1] + noun_overlap_local_vec
        self.debugData["noun_overlap_given_vec"] = [-1] + noun_overlap_given_vec
        self.debugData["cont_overlap_local_vec"] = [-1] + cont_overlap_local_vec
        self.debugData["cont_overlap_given_vec"] = [-1] + cont_overlap_given_vec

        # Semantic overlap
        DATA_PATH = join(CURDIR, "etc/tm")
        MODEL_PATH = join(DATA_PATH, "asbc5_200_gensim_pass20.model")
        DICT_PATH = join(DATA_PATH, "gensim_asbc.dict")
        topic_model = TopicModel(MODEL_PATH, DICT_PATH)

        wassoc_local_vec = []
        wassoc_given_vec = []
        for (seq1, seq2) in zip(seq_list, seq_list[1:]):
            tokseq2 = get_seq_tok(toks, seq2)
            tokseq1 = get_seq_tok(toks, seq1)
            tokgiven = get_prev_seq_tok(toks, seq2)

            local_vec = topic_model.get_word_assoc(
                [x.text for x in tokseq2],
                [x.text for x in tokseq1])

            given_vec = topic_model.get_word_assoc(
                [x.text for x in tokseq2],
                [x.text for x in tokgiven])

            if len(local_vec) > 0:
                wassoc_local_vec.append(np.mean(local_vec))
            if len(given_vec) > 0:
                wassoc_given_vec.append(np.mean(given_vec))

        self.feats["SemanticOverlap_Local"] = mean(wassoc_local_vec)
        self.feats["SemanticOverlap_Given"] = mean(wassoc_given_vec)

        self.debugData["wassoc_local_vec"] = [-1] + wassoc_local_vec
        self.debugData["wassoc_given_vec"] = [-1] + wassoc_given_vec
        # sense count
        SENSE_PATH = join(CURDIR, "etc/cwn/cwn_sense_count.txt")
        sense_data = SenseData(SENSE_PATH)
        nsense_vec = [sense_data.get(tok.text) for tok in cont_toks]

        # nsense_vec only include content tokens, but for alignment
        # in debug data, other tokens are filled with -1 in
        # nsense_vec_dbg
        nsense_vec_dbg = []
        for tok in real_tokens:
            is_cont = tok.pos in CONT_POS_LIST
            if is_cont:
                tok_sense = sense_data.get(tok.text)
            else:
                tok_sense = -1
            nsense_vec_dbg.append(tok_sense)
        self.debugData["nsense_vec"] = nsense_vec_dbg

        self.setQuantileFeatures("nSense", nsense_vec)


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

    def setCountFeatures(self, field, val, Z):
        try:
            self.feats["n" + field] = val
            self.feats["r" + field] = val / Z
        except KeyError as ex:
            logging.getLogger().error("Cannot find %s" % ex)




