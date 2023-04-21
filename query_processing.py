import json

from preprocessing import Preprocessing
import tkinter as tk


# creating gui of program, code for gui taken from ChatGPT!
def create_gui():
    def search():
        global query
        global and_queries, and_not_queries, phrase_queries

        and_queries.clear()
        and_not_queries.clear()
        phrase_queries.clear()

        # Get the search term from the entry widget
        query = entry.get()

        # Perform your search operation here

        parse_query()
        result = process_query()
        result = prepare(result)

        print(and_queries)

        # Update the results in the text widget
        results_text.delete('1.0', tk.END)
        results_text.insert(tk.END, "Results for '{}'...\n".format(query))

        with open("./data.json", 'r', encoding="utf-8") as source:
            source_data = json.load(source)

        for r in result:
            results_text.insert(tk.END, f"سند شماره {r['doc_id']} : {source_data[r['doc_id']]['title']}\n")

        source.close()

    root = tk.Tk()
    root.title("IR Project")

    # Entry widget for search term
    entry = tk.Entry(root, width=50)
    entry.pack(padx=10, pady=10)

    # Button to initiate search
    button = tk.Button(root, text="Search", command=search)
    button.pack(padx=10, pady=5)

    # Plain text widget for showing results
    results_frame = tk.Frame(root)
    results_frame.pack(padx=10, pady=10)

    results_text = tk.Text(results_frame, height=10, width=50)
    results_text.pack(side=tk.LEFT)

    scrollbar = tk.Scrollbar(results_frame, command=results_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    results_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()


def parse_query():
    tokens = Preprocessing.tokenize(Preprocessing.normalize(query))

    length_of_tokens = len(tokens)

    i = 0
    while i < length_of_tokens:
        if tokens[i] == "«":
            i += 1
            start = i

            while tokens[i] != "»":
                i += 1

            end = i

            phrase_queries.append(Preprocessing.remove_stopwords(Preprocessing.stem_tokens(tokens[start:end])))
            i += 1

        elif tokens[i] == '!':
            i += 1
            and_not_queries.append(Preprocessing.remove_stopwords(Preprocessing.stem_tokens(tokens[i:i+1]))[0])
            i += 1

        else:
            x = Preprocessing.remove_stopwords(Preprocessing.stem_tokens(tokens[i:i+1]))
            if len(x) != 0:
                and_queries.append(x[0])
            i += 1


def process_query():
    and_query_docs = None

    if len(and_queries) > 0:
        and_query_docs = and_intersect(data[and_queries[0]]['postings'], None)
        for i in range(1, len(and_queries)):
            and_query_docs = and_intersect(and_query_docs, data[and_queries[i]]['postings'])

    # check if user entered phrase query
    if len(phrase_queries) > 0:
        for phrase_query in phrase_queries:
            phrase_query_docs = positional_intersect(data[phrase_query[0]]['postings'], data[phrase_query[1]]['postings'])
            and_query_docs = and_intersect(and_query_docs, phrase_query_docs)

    if len(and_not_queries) > 0:
        for and_not_query in and_not_queries:
            and_query_docs = and_not_intersect(and_query_docs, data[and_not_query]['postings'])

    return and_query_docs


def positional_intersect(p1, p2):
    """pi is the postings list of ith word"""

    answer = []

    i = j = 0

    while i != len(p1) and j != len(p2):
        if p1[i]['doc_id'] == p2[j]['doc_id']:

            positions_1 = p1[i]['positions']
            positions_2 = p2[j]['positions']

            pp1 = pp2 = 0
            while pp1 != len(positions_1) and pp2 != len(positions_2):
                if positions_1[pp1] == positions_2[pp2] - 1:
                    answer.append({'doc_id': p1[i]['doc_id'], 'position': positions_1[pp1]})
                    pp1 += 1
                    pp2 += 1
                elif positions_1[pp1] < positions_2[pp2] - 1:
                    pp1 += 1
                else:
                    pp2 += 1
            i += 1
            j += 1
        elif p1[i]['doc_id'] < p2[j]['doc_id']:
            i += 1
        else:
            j += 1
    return answer


def and_intersect(p1, p2):
    answer = []

    if p2 is None:
        for i in range(len(p1)):
            answer.append({'doc_id': p1[i]['doc_id']})
        return answer
    elif p1 is None:
        for i in range(len(p2)):
            answer.append({'doc_id': p2[i]['doc_id']})
        return answer

    i = j = 0

    while i != len(p1) and j != len(p2):
        if p1[i]['doc_id'] == p2[j]['doc_id']:
            answer.append({'doc_id': p1[i]['doc_id']})
            i += 1
            j += 1
        elif p1[i]['doc_id'] < p2[j]['doc_id']:
            i += 1
        else:
            j += 1
    return answer


def and_not_intersect(p1, p2):
    answer = []

    i = j = 0

    while i != len(p1) and j != len(p2):
        if p1[i]['doc_id'] == p2[j]['doc_id']:
            i += 1
            j += 1
        elif p1[i]['doc_id'] < p2[j]['doc_id']:
            answer.append({'doc_id': p1[i]['doc_id']})
            i += 1
        else:
            j += 1
    if j == len(p2):  # add rest of doc ids
        while i != len(p1):
            answer.append({'doc_id': p1[i]['doc_id']})
            i += 1
    return answer


def prepare(result):

    for r in result:
        r['score'] = score(r['doc_id'])

    result = sorted(result, key=lambda x: -x['score'])
    return result


def score(doc_id):
    doc_score = 0

    for and_query in and_queries:
        for p in data[and_query]['postings']:
            if p['doc_id'] == doc_id:
                doc_score += p['in_doc_freq']
                break

    for phrase_query in phrase_queries:
        for term in phrase_query:
            for p in data[term]['postings']:
                if p['doc_id'] == doc_id:
                    doc_score += p['in_doc_freq']
                    break

    return doc_score


phrase_queries = []
and_not_queries = []
and_queries = []

with open('./positional_index.json', 'r', encoding="utf-8") as data_file:
    data = json.load(data_file)

query = None

create_gui()

# query = 'قیمت دلار'
#
# parse_query()
# result = process_query()
# result = prepare(result)
#
# print(result)