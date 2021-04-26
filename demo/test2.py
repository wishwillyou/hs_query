from service.category_classification_service import CategoryClassificationService

from algorithms.vectorize import *
from service.linear_regression_with_word_cnt_service import LinearRegressionWithWordCntService
from service.translate_service import TranslateService
from util.category_range_dict import *
from util.multi_processor import multi_process

# category_service = CategoryClassificationService()
#
# print("CategoryClassificationService loaded")
#
# categories = []
# params_list = []
# for i in range(1, 22):
#     if i == 16:
#         continue
#     categories.append(i)
#     params_list.append((
#         "glossary_%d.dict" % i,
#         "category_%d.dict" % i,
#         "ctv_%d.model" % i,
#         "clf_multi_%d.model" % i
#     ))
# services = multi_process(LinearRegressionWithWordCntService, params_list)
# hs_service_dict = dict(zip(categories, services))

i = 11
service = LinearRegressionWithWordCntService((
        "glossary_%d.dict" % i,
        "category_%d.dict" % i,
        "ctv_%d.model" % i,
        "clf_multi_%d.model" % i
))

print("model loaded success...")


data = """
NEW ARRIVALS MODERN GENTLEMAN England Fashion Wave Point Men's Slim Fit Long Sleeved Tide Rugby Polo Shirt
A VINTAGE-INSPIRED RUGBY SHIRT WITH ENGLAND FASHION WAVE POINT, CONTRAST COLLAR, MUSCLE FIT, IMPORTED 1.Material：Cotton Blended 2.Color：White／Black／Navy 3.Size：M／L／XL／XXL／XXXL SIZE CHART：(1cm =0.39inch) M： Shoulder：42cm／Chest： 96cm／Length：66cm／Sleeve:62cm L： Shoulder：43cm／Chest：100cm／Length：68cm／Sleeve:63cm XL： Shoulder：44cm／Chest：104cm／Length：70cm／Sleeve:64cm XXL： Shoulder：45cm／Chest：108cm／Length：72cm／Sleeve:65cm XXXL： Shoulder：46cm／Chest：112cm／Length：74cm／Sleeve:66cm NOTE： All size is Asian size，Please chose 1～2 bigger size than usual，Thank you !
"""
data = TranslateService.do_translate(data)

ans = service.do_classify(data)

for k, v in ans.items():
    print("%s, %.3f" % (k, v))
