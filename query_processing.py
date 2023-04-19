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


positional_queries = []
and_not_queries = []
and_queries = []

query = '"جواد خیابانی" ! گزارشگر فوتبال'
parse_query()

print(positional_queries)
print(and_not_queries)
print(and_queries)
