from typing import List

from hazm import *


class Preprocessing:

    @staticmethod
    def preprocess(content: str):
        norm = Preprocessing.normalize(content)
        tokens = Preprocessing.tokenize(norm)
        stemmed = Preprocessing.stem_tokens(tokens)
        without = Preprocessing.remove_stopwords(stemmed)

        return without


    @staticmethod
    def normalize(content: str) -> str:
        # why we use normalization before tokenizing?
        normalizer = Normalizer()

        norm_content = normalizer.normalize(content)

        return norm_content

    @staticmethod
    def tokenize(norm_content: str) -> List[str]:
        sentences = sent_tokenize(norm_content)
        tokens = []

        for sentence in sentences:
            words = word_tokenize(sentence)

            tokens.extend(words)

        return tokens

    @staticmethod
    def stem_tokens(tokens: List[str]) -> List[str]:
        stemmed_tokens = []
        lemmatizer = Lemmatizer()

        for token in tokens:
            lemmatized = lemmatizer.lemmatize(token)
            if '#' in lemmatized:
                lemmatized = lemmatized.split('#')[0]  # because some verbs like ast.
                if lemmatized == "":
                    continue
            stemmed_tokens.append(lemmatized)

        del tokens  # in order to clean used memory
        return stemmed_tokens

    @staticmethod
    def remove_stopwords(tokens: List[str]) -> List[str]:
        stopwords = stopwords_list()

        # when we normalize and tokenize, punctuation marks will be regarded as a single token
        # so we make a punctuation list to remove them
        punctuations = [".", "،", "؛", ":", "؟", "!", "/", "]", "[", "}", "{", "|", "-", "«", "»", "<", ">", "'\'", "(",
                        ")", "*", "%", "#", "@"]

        tokens_without_stopwords = []
        for token in tokens:
            if token in stopwords or token in punctuations:
                continue

            # we do it in this way because deletion in for loop is prohibited.
            tokens_without_stopwords.append(token)

        del tokens  # in order to clean used memory
        return tokens_without_stopwords
