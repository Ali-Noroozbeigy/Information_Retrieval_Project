import json

from preprocessing import Preprocessing


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

            positional_queries.append(Preprocessing.remove_stopwords(Preprocessing.stem_tokens(tokens[start:end])))
            i += 1

        elif tokens[i] == '!':
            i += 1
            and_not_queries.append(Preprocessing.remove_stopwords(Preprocessing.stem_tokens(tokens[i:i+1]))[0])
            i += 1

        else:
            and_queries.append(Preprocessing.remove_stopwords(Preprocessing.stem_tokens(tokens[i:i+1]))[0])
            i += 1


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
    return answer


positional_queries = []
and_not_queries = []
and_queries = []

query = 'وزیر ! اقتصاد'
parse_query()

with open('./positional_index.json', 'r', encoding="utf-8") as data_file:
    data = json.load(data_file)

ans = and_not_intersect(data[and_queries[0]]['postings'], data[and_not_queries[0]]['postings'])
print(ans)
