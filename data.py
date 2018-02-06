import os
import torch

class Dictionary:
    def __init__(self):
        self.word2idx = {}
        self.idx2word = []

    def add_word(self, word):
        if word not in self.word2idx:
            self.idx2word.append(word)
            self.word2idx[word] = len(self.idx2word) -1
        return self.word2idx[word]

    def __len__(self):
        return len(self.idx2word)

class Corpus:
    def __init__(self, path):
        self.dictionary = Dictionary()
        self.train = self.tokenize(os.path.join(path, 'train.txt'))
        self.valid = self.tokenize(os.path.join(path, 'valid.txt'))
        self.test = self.tokenize(os.path.join(path, 'test.txt'))

    def tokenize(self, file):
        """Tokenizes the file."""
        assert os.path.exists(file)
        # First add the unique words to dictionary
        with open(file, 'r') as f:
            tokens = 0
            for line in f:
                words = line.split()
                words.append('<eos>')
                tokens += len(words)
                for word in words:
                    self.dictionary.add_word(word)

        # Now tokenize the actual file.
        with open(file, 'r') as f:
            ids = torch.LongTensor(tokens)
            token = 0
            for line in f:
                words = line.split()
                words.append('<eos>')
                for word in words:
                    ids[token] = self.dictionary.word2idx[word]
                    token +=1

        return ids
