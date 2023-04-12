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


toks = Preprocessing.preprocess("وزیر آموزش و پرورش استعفا داد. سخنگوی دولت این موضوع را تایید کرد.")

posi_index = PositionalIndex()
posi_index.add_to_index(toks, 1)

toks = Preprocessing.preprocess("وزیر اقتصاد افزایش قیمت دلار را تایید کرد. همچنین وزیر از این افزایش ابراز نگرانی کرد.")
posi_index.add_to_index(toks, 2)

print(posi_index.pos_index)
