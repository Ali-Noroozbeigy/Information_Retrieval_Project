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


class PositionalIndex:

    def __init__(self):
        self.pos_index = {}

    def add_to_index(self, tokens, doc_id):
        for i, token in enumerate(tokens):
            if token in self.pos_index:
                self.pos_index[token]['total_freq'] += 1

                doc_found = False

                for posting in self.pos_index[token]['postings']:
                    if doc_id == posting['doc_id']:
                        posting['in_doc_freq'] += 1
                        posting['positions'].append(i)
                        doc_found = True
                        break

                if not doc_found:
                    self.pos_index[token]['postings'].append({"doc_id": doc_id,
                                                              "in_doc_freq": 1,
                                                              "positions": [i]})

            else:
                self.pos_index[token] = {"total_freq": 1, "postings": [{"doc_id": doc_id,
                                                                        "in_doc_freq": 1,
                                                                        "positions": [i]}]}


def construct_index(path, positional_index: PositionalIndex):
    with open(path, 'r', encoding="utf-8") as data_file:
        data = json.load(data_file)

    for news_id, other in data.items():
        tokens = Preprocessing.preprocess((other['content']))
        positional_index.add_to_index(tokens, news_id)

    with open("positional_index.json", "w", encoding="utf-8") as final_index:
        json.dump(positional_index.pos_index, final_index, indent=4, ensure_ascii=False)


positional_index = PositionalIndex()
construct_index("./data.json", positional_index)
# print(positional_index.pos_index)
