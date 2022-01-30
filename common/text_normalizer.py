#  Copyright 2022. Nguyen Thanh Tuan, To Duc Anh, Tran Minh Khoa, Duong Thu Phuong, Nguyen Anh Tu, Kieu Son Tung, Nguyen Son Tung
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import unicodedata


def normalized(text, blacklist_patterns=None, stopwords=None, folding=None,
               max_words=None, delimiter=' '):
    """
    Simple normalization of the text by folding, convert to lower, remove
    pattern remove stopwords
    """
    def tokenized(text, stopwords=None, folding=None, max_words=None):
        def fold(text):
            s = ''
            for c in unicodedata.normalize('NFD', text):
                if c == 'đ' or c == 'ð':
                    s = s + 'd'
                elif unicodedata.category(c) != 'Mn':
                    s = s + c
            return s

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

    if blacklist_patterns:
        generic_pattern = '(%s)' % '|'.join(blacklist_patterns)
        pattern = re.compile(generic_pattern)
        text = pattern.sub(' ', text)
    tokens = tokenized(text, stopwords=stopwords, folding=folding, max_words=max_words)
    return delimiter.join(tokens).lower()