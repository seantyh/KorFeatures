class ModelParams:
    as4char_params = {
        "base_dir": "../etc",
        "data_path": "as4_char_vec_norm.bytes",
        "label_path": "as4_char_vocab_norm.tsv",
        "dims": (4586, 100)
    }

    as4word_params = {
        "base_dir": "../etc",
        "data_path": "as4_word_vec_norm.bytes",
        "label_path": "as4_word_vocab_norm.tsv",
        "dims": (28272, 200)
    }

    @staticmethod
    def Get(name = None):
        if name.lower() == "as4char":
            return ModelParams.as4char_params
        elif name.lower() == "as4word":
            return ModelParams.as4word_params
        else:
            return """
    Possible values (case-insensitive):
    AS4Char, AS4Word
"""    
