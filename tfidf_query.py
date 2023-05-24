import json
from preprocessing import Preprocessing
from math import log10


TOTAL_DOCS = 6
TOP_K = 4
SIMILARITY = "COSINE"  # COSINE or JACCARD
USE_CHMP_LIST = True


def cosine_score():
    if USE_CHMP_LIST:
        with open('./champion_list.json', 'r', encoding="utf-8") as data_file:
            index = json.load(data_file)
    else:
        with open('./positional_index.json', 'r', encoding="utf-8") as data_file:
            index = json.load(data_file)

    scores = {}
    # query_terms = query.split(" ")
    for term in query_terms:
        term_postings = index[term]['postings']
        w_term = log10(TOTAL_DOCS / len(term_postings))  # equivalent to idf of term

        for posting in term_postings:
            w_doc = 1 + log10(posting["in_doc_freq"])  # equivalent to tf of doc
            if posting['doc_id'] in scores:
                scores[posting['doc_id']] += w_doc * w_term
            else:
                scores[posting['doc_id']] = w_doc * w_term

    with open('./Doc_length.json', 'r') as length_file:
        length = json.load(length_file)

    for doc_id in scores.keys():
        scores[doc_id] /= length[int(doc_id)]

    return top_k_docs(scores, TOP_K)


def top_k_docs(scores: dict, k):
    import heapq

    top_k = heapq.nlargest(k, scores.items(), key=lambda x: x[1])
    return top_k


def jaccard_score():

    scores = {}

    query_as_set = set(query_terms)

    with open('jaccard_set.json', 'r', encoding="utf-8") as jaccard_file:
        docs_terms = json.load(jaccard_file)

    for doc in docs_terms:
        doc_id = next(iter(doc))
        term_set = set(doc[doc_id])

        jaccard_weight = len(query_as_set.intersection(term_set)) / len(query_as_set.union(term_set))
        scores[doc_id] = jaccard_weight

    return top_k_docs(scores, TOP_K)


query = "افزایش بودجه"
query_terms = Preprocessing.preprocess(query)
if SIMILARITY == "COSINE":
    print(cosine_score())
else:
    print(jaccard_score())
