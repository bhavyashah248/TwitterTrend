__author__ = 'Nick Hirakawa'

import re


class CorpusParser:
    def __init__(self, filename):
        self.filename = filename
        self.regex = re.compile('^#\s*\d+')
        self.corpus = dict()

    def parse(self):
        with open(self.filename) as f:
            s = ''.join(f.readlines())
            s = s.lower()
        blobs = s.split('$$$')[3:]
        for x in blobs:
            text = x.split()
            docid = text.pop(0)
            self.corpus[docid] = text
        # print text

    def get_text(self, docid):
        text = ' '.join(self.corpus[docid])
        return text

    def get_corpus(self):
        return self.corpus


class QueryParser:
    def __init__(self, filename):
        self.filename = filename
        self.queries = []

    #		print os.listdir('.')

    def parse(self):
        with open(self.filename) as f:
            lines = ''.join(f.readlines())
            lines = lines.lower()
        self.queries = [x.rstrip().split() for x in lines.split('\n')[:-1]]

    def get_queries(self):
        return self.queries


if __name__ == '__main__':
    qp = QueryParser('text/query.txt')
# print qp.get_queries()
