"""
Positional_index = {
                    "a word": {
                                total_freq = x,
                                postings = [
                                    {
                                        "doc_id": n,
                                        "in_doc_freq": x,
                                        "positions": [p0, p1, ...]
                                    },
                                    ...
                                ]
                    },
                    ...
}
"""
import json
from preprocessing import Preprocessing


SIMILARITY = "JACCARD"  # or JACCARD


class PositionalIndex:

    def __init__(self):
        self.pos_index = {}

    def add_to_index(self, tokens, doc_id):
        for i, token in enumerate(tokens):
            if token in self.pos_index: # token is available in index
                self.pos_index[token]['total_freq'] += 1

                doc_found = False

                # token is ready, we check if it is belong to the current doc_id which is being processed
                # we need to update the posting ny adding the new position and increase freq
                last_posting = self.pos_index[token]['postings'][-1]
                if doc_id == last_posting['doc_id']:
                    last_posting['in_doc_freq'] += 1
                    last_posting['positions'].append(i)

                # token is ready, but it is not from the last doc_id, so we need to add a new posting
                else:
                    self.pos_index[token]['postings'].append({"doc_id": doc_id,
                                                              "in_doc_freq": 1,
                                                              "positions": [i]})

            # token is totally new, we need to add it and set initial values
            else:
                self.pos_index[token] = {"total_freq": 1, "postings": [{"doc_id": doc_id,
                                                                        "in_doc_freq": 1,
                                                                        "positions": [i]}]}


def construct_index(path, positional_index: PositionalIndex):

    with open(path, 'r', encoding="utf-8") as data_file:
        data = json.load(data_file)

    for news_id, other in data.items():
        tokens = Preprocessing.preprocess((other['content']))

        if SIMILARITY == "COSINE":
            index_for_cosine(tokens, news_id)
        else:
            index_for_jaccard(tokens, news_id)

    if SIMILARITY == "COSINE":
        with open("positional_index.json", "w", encoding="utf-8") as final_index:
            json.dump(positional_index.pos_index, final_index, ensure_ascii=False)
        with open('Doc_length.json', "w") as docs_length_file:
            json.dump(docs_length, docs_length_file)
    else:
        with open('jaccard_set.json', 'w', encoding="utf-8") as jaccard_file:
            json.dump(docs_with_terms, jaccard_file, ensure_ascii=False)


def index_for_cosine(tokens, news_id):
    positional_index.add_to_index(tokens, news_id)

    from collections import Counter
    tokens_in_doc_freq = dict(Counter(tokens))
    docs_length.append(calculate_length(tokens_in_doc_freq))


def index_for_jaccard(tokens, news_id):
    docs_with_terms.append({news_id: list(set(tokens))})


def calculate_length(freqs: dict):
    """
    calculates length of each document by calculating doc's tokens' tf
    :param freqs: frequency of each token in doc
    :return: length of document based on tf
    """
    from math import log10, sqrt
    squared_sum = 0
    for _, freq in freqs.items():
        tf = 1 + log10(freq)
        squared_sum += tf ** 2
    return sqrt(squared_sum)


positional_index = PositionalIndex()
# used for saving documents' length for calculating score later
docs_length = []
docs_with_terms = []
construct_index("./data.json", positional_index)
# print(positional_index.pos_index)
