import jieba


class SplitWordService(object):

    jieba.enable_parallel()

    @classmethod
    def do_word_split(cls, sentences, vocabulary):
        words = jieba.lcut(sentences)
        words = [w for w in words if w in vocabulary]
        return words
