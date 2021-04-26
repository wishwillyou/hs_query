import os
import ujson
import heapq

from service.split_word_service import SplitWordService


class BaseClassificationService(object):

    @classmethod
    def _load_vectorize_model(cls, vectorize_path):
        raise Exception("implement _load_vectorize_model method")

    @classmethod
    def _load_classify_model(cls, classification_path):
        raise Exception("implement _load_classify_model method")

    @classmethod
    def _load_vocabulary(cls, vocabulary_path):
        with open(vocabulary_path) as f:
            return set(f.readline().split(" "))

    @classmethod
    def _load_ydict(cls, ydict_path):
        with open(ydict_path) as f:
            return {int(k): v for k, v in ujson.loads(f.readline()).items()}

    def __init__(self, vocabulary_name, ydict_name, vectorize_name, classify_name):
        cur_dir = os.path.abspath(os.path.dirname(__file__))
        self.vocabulary = self._load_vocabulary(cur_dir + "/../trained_model/vocabulary/" + vocabulary_name)
        self.y_dict = self._load_ydict(cur_dir + "/../trained_model/ydict/" + ydict_name)
        self.vectorize_model = self._load_vectorize_model(cur_dir + "/../trained_model/vectorize/" + vectorize_name)
        self.classify_model = self._load_classify_model(cur_dir + "/../trained_model/classification/" + classify_name)

    def _abstract_keywords(self, data_source):
        return SplitWordService.do_word_split(data_source, self.vocabulary)

    def _word2input(self, words):
        raise Exception("implement _word2input method")

    def _classify_input(self, words):
        raise Exception("implement _word2input method")

    def _find_tops(self, predictions):
        values = [-x for x in predictions.tolist()[:]]
        heapq.heapify(values)
        tops = [-heapq.heappop(values), -heapq.heappop(values), -heapq.heappop(values)]
        return {i: predictions[i] for i in range(len(predictions)) if predictions[i] in tops}

    def do_classify(self, data_source):
        keywords = self._abstract_keywords(data_source)
        classify_input = self._word2input([" ".join(keywords)])
        predictions = self._classify_input(classify_input)[0]
        tops = self._find_tops(predictions)
        return {self.y_dict.get(k): v for k, v in tops.items()}
