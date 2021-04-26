import json
import os
import subprocess

from util.multi_processor import multi_process
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from algorithms.vectorize import *
from service.category_classification_service import CategoryClassificationService

from service.linear_regression_with_word_cnt_service import LinearRegressionWithWordCntService
from service.translate_service import TranslateService
from util.category_range_dict import *

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
print("Other modules loaded")


def compile_vue_js_async():
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    os.chdir(cur_dir)
    command = "npm run dev"
    #  pylint: disable=W0603
    global webpack_process
    webpack_process = subprocess.Popen(
        command, shell=True, stderr=subprocess.STDOUT
    )

import tornado.web  # web服务
import tornado.ioloop  # I/O 时间循环
import tornado.httpserver  # 新引入httpserver模块，单线程的http服务


class HSCodeENHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def get(self):
        name = str(self.request.arguments.get("name")[0], encoding='utf-8')
        description = str(self.request.arguments.get("desc")[0], encoding='utf-8')
        print(name, description)
        data = TranslateService.do_translate(name + "\n" + description)
        ans = category_service.do_classify(data)

        results = []
        for k, v in ans.items():
            catg_range = get_category_range(k)
            result = {
                "type": k,
                "range": catg_range[1:],
                "ratio": "%.3f" % v,
                "description": category_description_dict.get(k)
            }

            possible = result.copy()
            inner_ans = hs_service_dict.get(k).do_classify(data)
            for k1, v1 in inner_ans.items():
                possible.update({
                    "hs_code": k1,
                    "category_ratio": "%.3f" % v1,
                    "global_ratio": "%.3f" % (float(possible.get("ratio")) * float("%.3f" % v1))
                })
                results.append(possible.copy())
        results.sort(key=lambda x: x.get("global_ratio"))
        results.reverse()
        self.write(json.dumps(results, ensure_ascii=False))


# 建立路由表
app = tornado.web.Application([
    (r"/index", HSCodeENHandler),
])

compile_vue_js_async()
http_server = tornado.httpserver.HTTPServer(app)
http_server.bind(8000)
http_server.start()
tornado.ioloop.IOLoop.instance().start()  # 开始事件
