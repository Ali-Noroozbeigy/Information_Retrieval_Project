import json
from preprocessing import Preprocessing
from math import log10
import tkinter as tk


SOURCE_NEWS_PATH = './IR_data_news_12k.json'
CHMP_LIST_PATH = './IR_champion_list.json'
POSITIONAL_INDEX_PATH = './IR_positional_index.json'
DOC_LENGTH_PATH = './IR_Doc_length.json'
JACCARD_SET_PATH = './IR_jaccard_set.json'
TOTAL_DOCS = 12360
TOP_K = 10
SIMILARITY = None  # COSINE or JACCARD
USE_CHMP_LIST = None


def create_gui():
    def search():
        global query_terms
        global SIMILARITY, USE_CHMP_LIST
        query_terms.clear()

        query = entry.get()
        query_terms = Preprocessing.preprocess(query)

        if cosine_var.get():  # use COSINE similarity
            SIMILARITY = "COSINE"
            USE_CHMP_LIST = champion_var.get()
            result = cosine_score()
        else:
            SIMILARITY = "JACCARD"
            result = jaccard_score()

        results_text.delete('1.0', tk.END)
        results_text.insert(tk.END, "Results for '{}'...\n".format(query))

        with open(SOURCE_NEWS_PATH, 'r', encoding="utf-8") as source:
            source_data = json.load(source)

        for r in result:
            results_text.insert(tk.END, f"سند شماره {r[0]}: {source_data[r[0]]['title']}\n")
            print(r[1])

    root = tk.Tk()
    root.title("IR Project")

    # Entry widget for search term
    entry = tk.Entry(root, width=50)
    entry.pack(padx=10, pady=10)

    # Button to initiate search
    button = tk.Button(root, text="Search", command=search)
    button.pack(padx=10, pady=5)

    cosine_var = tk.BooleanVar()
    cosine_check = tk.Checkbutton(root, text="Use Cosine Similarity", variable=cosine_var)
    cosine_check.pack(padx=10, pady=10)

    champion_var = tk.BooleanVar()
    champion_check = tk.Checkbutton(root, text="Use Champion List", variable=champion_var)
    champion_check.pack(padx=10, pady=10)

    # Plain text widget for showing results
    results_frame = tk.Frame(root)
    results_frame.pack(padx=10, pady=10)

    results_text = tk.Text(results_frame, height=15, width=100)
    results_text.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(results_frame, command=results_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    results_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()


def cosine_score():
    if USE_CHMP_LIST:
        with open(CHMP_LIST_PATH, 'r', encoding="utf-8") as data_file:
            index = json.load(data_file)
    else:
        with open(POSITIONAL_INDEX_PATH, 'r', encoding="utf-8") as data_file:
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

    with open(DOC_LENGTH_PATH, 'r') as length_file:
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

    with open(JACCARD_SET_PATH, 'r', encoding="utf-8") as jaccard_file:
        docs_terms = json.load(jaccard_file)

    for doc in docs_terms:
        doc_id = next(iter(doc))
        term_set = set(doc[doc_id])

        jaccard_weight = len(query_as_set.intersection(term_set)) / len(query_as_set.union(term_set))
        scores[doc_id] = jaccard_weight

    return top_k_docs(scores, TOP_K)


query_terms = []
create_gui()
# query = "بودجه"
# if SIMILARITY == "COSINE":
#     print(cosine_score())
# else:
#     print(jaccard_score())
