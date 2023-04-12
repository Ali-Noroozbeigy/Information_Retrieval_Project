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
        positional_index.add_to_index(tokens, news_id)

    with open("positional_index.json", "w", encoding="utf-8") as final_index:
        json.dump(positional_index.pos_index, final_index, indent=4, ensure_ascii=False)


positional_index = PositionalIndex()
construct_index("./data.json", positional_index)
# print(positional_index.pos_index)
