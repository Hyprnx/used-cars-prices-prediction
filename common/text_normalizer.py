import re
import unicodedata


def fold(text):
    """
    Strip accent from the text, e.g: ü => u, é=>e
    """
    s = ''
    for c in unicodedata.normalize('NFD', text):
        if c == 'đ' or c == 'ð':
            s = s + 'd'
        elif unicodedata.category(c) != 'Mn':
            s = s + c
    return s


def tokenized(text, stopwords=None, folding=None, max_words=None):
    """
    Split a text to a list of tokens
    """
    if text is None:
        return None
    pattern = re.compile(r"\W+", re.UNICODE)
    tokens = []
    if folding:
        text = fold(text)
    for token in pattern.split(text.lower()):
        if token and (not stopwords or token not in stopwords):
            tokens.append(token)
            if max_words and len(tokens) >= max_words:
                break
    return tokens


def normalized(text, blacklist_patterns=None, stopwords=None, folding=None,
               max_words=None, delimiter=' '):
    """
    Simple normalization of the text by folding, convert to lower, remove
    pattern remove stopwords
    """
    if blacklist_patterns:
        generic_pattern = '(%s)' % '|'.join(blacklist_patterns)
        pattern = re.compile(generic_pattern)
        text = pattern.sub(' ', text)
    tokens = tokenized(text, stopwords=stopwords, folding=folding, max_words=max_words)
    return delimiter.join(tokens).lower()