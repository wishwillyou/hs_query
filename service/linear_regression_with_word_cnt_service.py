import joblib

from service.base_classification_service import BaseClassificationService


class LinearRegressionWithWordCntService(BaseClassificationService):

    def __init__(self, x):
        glossary_file, y_dict_file, vectorize_file, classification_model = x
        super(LinearRegressionWithWordCntService, self).__init__(
            glossary_file, y_dict_file, vectorize_file, classification_model
        )
        print(x, "-->loaded")

    @classmethod
    def _load_vocabulary(cls, vocabulary_path):
        with open(vocabulary_path) as f:
            return set(f.readline().split(","))

    @classmethod
    def _load_vectorize_model(cls, vectorize_path):
        return joblib.load(vectorize_path)

    @classmethod
    def _load_classify_model(cls, classification_path):
        return joblib.load(classification_path)

    def _word2input(self, words):
        return self.vectorize_model.transform(words)

    def _classify_input(self, words):
        return self.classify_model.predict_proba(words)
