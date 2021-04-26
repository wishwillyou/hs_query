import os
import subprocess

from service.category_classification_service import CategoryClassificationService

from algorithms.vectorize import *
from service.linear_regression_with_word_cnt_service import LinearRegressionWithWordCntService
from service.translate_service import TranslateService
from util.category_range_dict import *
from util.multi_processor import multi_process

category_service = CategoryClassificationService()

print("CategoryClassificationService loaded")

categories = []
params_list = []
for i in range(1, 22):
    categories.append(i)
    params_list.append((
        "glossary_%d.dict" % i,
        "category_%d.dict" % i,
        "ctv_%d.model" % i,
        "clf_multi_%d.model" % i
    ))
services = multi_process(LinearRegressionWithWordCntService, params_list)
hs_service_dict = dict(zip(categories, services))

print("model loaded success...")
