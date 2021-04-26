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

while True:
    data = input("input")
#
# data = """
# micro braided wigs Fashion Synthetic Hand Braided Wig Crochet Braids Front Lace Wigs 22Inch Senegal Twist Braids Lace Wigs havana twist Hair
# Hair Type:100% high quality synthetic Hair Hair Density:150% Average Density Length:12-26inchin stock Cap Style:SwissLace Wig Stretch in Middle brown Cap Size:Average Cap Size(21-23.5inch, you can adjust it by adjustable strap If can babyhair:Yes If can be permed:Yes Hair color ::1b#2#4#6#27#30#613# you can order and left a message what color you like Item Feature:Natural Looking, Soft Feeling, Realistic Refund policy:100% Refund if inferior quality Hair quality:Top quality(No shedding ,No tangling) Cap Size:Medium cap with straps and combs Hair Material:high temperature.wire.fiber.heat hesistant.synthetic hair Feature:glueless.elastic adjustable straps.three combs Delivery Time:We can ship your order in 24 hours after you pay it what'sapp:+008613791150958
#
# """
    data = TranslateService.do_translate(data)

    ans = category_service.do_classify(data)

    for k, v in ans.items():
        catg_range = get_category_range(k)
        print("%d, [%d, %d], %.3f, %s" % (k, catg_range[1], catg_range[2], v, category_description_dict.get(k)))

        inner_ans = hs_service_dict.get(k).do_classify(data)
        for k1, v1 in inner_ans.items():
            print("%s, %.3f" % (k1, v1))
