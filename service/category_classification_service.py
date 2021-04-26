import joblib
from service.base_classification_service import BaseClassificationService


class CategoryClassificationService(BaseClassificationService):

    def __init__(self):
        super(CategoryClassificationService, self).__init__(
            "glossary", "dummy_path", "tfidf.model", "category_classification.model")

    @classmethod
    def _load_vectorize_model(cls, vectorize_path):
        return joblib.load(vectorize_path)

    @classmethod
    def _load_classify_model(cls, classification_path):
        return joblib.load(classification_path)

    @classmethod
    def _load_ydict(cls, ydict_path):
        return {i: i+1 for i in range(22)}

    def _word2input(self, words):
        return self.vectorize_model.transform(words)

    def _classify_input(self, words):
        return self.classify_model.predict_proba(words)

