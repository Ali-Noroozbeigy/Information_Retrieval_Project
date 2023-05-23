import json
from preprocessing import Preprocessing
from math import log10


def cosine_score():
    with open('./positional_index.json', 'r', encoding="utf-8") as data_file:
        index = json.load(data_file)

    scores = {}
    # query_terms = query.split(" ")
    for term in query_terms:
        term_postings = index[term]['postings']
        w_term = log10(6 / len(term_postings))  # equivalent to idf of term

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

    return top_k_docs(scores, 4)


def top_k_docs(scores: dict, k):
    import heapq

    top_k = heapq.nlargest(k, scores.items(), key=lambda x: x[1])
    return top_k


query = "افزایش بودجه"
query_terms = Preprocessing.preprocess(query)
print(cosine_score())
