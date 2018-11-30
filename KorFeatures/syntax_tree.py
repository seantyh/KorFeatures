import re
import logging
import csv
from typing import Dict
from os.path import dirname, abspath, join

logger = logging.getLogger("KorFeatures.SyntaxTree")
logger.setLevel("INFO")
logging.basicConfig(level="INFO")

def load_terminal_norms(csvpath):
    fin = open(csvpath, "r", encoding="UTF-8")
    csvreader = csv.reader(fin)
    next(csvreader)
    term_data = {}
    for row_x in csvreader:        
        if len(row_x) < 2: continue
        term_tuple = tuple(row_x[0].split(","))
        term_freq = int(row_x[1])
        term_data[term_tuple] = term_freq
    fin.close()
    
    return term_data

def tree_height(tree):
    height = 0
    for ch_tree in tree.children:
        height = max(height, tree_height(ch_tree)+1)
    return height

def get_terminals(tree_node):
    term_nodes = []
    if tree_height(tree_node) <= 1:
        # a effective terminal node (a POS node)
        term_nodes = [tree_node.text]
    else:
        for ch_node in tree_node.children:
            term_nodes += get_terminals(ch_node)
    term_tuple = tuple(term_nodes)
    return term_tuple

def enumerate_terminals(tree_node):
    term_list = []
    if tree_node.text != "ROOT":
        terms = get_terminals(tree_node)
        term_list.append(terms)

    for ch_node in tree_node.children:
        # ignore all POS non-terminal
        if tree_height(ch_node) <= 1: continue
        terminals = enumerate_terminals(ch_node)
        term_list += terminals
    return term_list

basedir = dirname(abspath(__file__))
term_norm = load_terminal_norms(join(basedir, 'etc/term_list_Chinese.csv'))

def get_n_hapaxes(trees):
    n_hapaxes_vec = []

    for tree_x in trees:
        term_list = enumerate_terminals(tree_x)
        term_freq = [term_norm.get(x, 0) for x in term_list]        
        n_hapaxes = sum([x == 1 for x in term_freq])
        n_hapaxes_vec.append(n_hapaxes)

    return n_hapaxes_vec

def get_tree_height(trees):
    height_vec = []

    for tree_x in trees:
        height_x = tree_height(tree_x)
        height_vec.append(height_x)    

    return height_vec
