import requests
import ujson


TRANSLATOR_URL = 'http://translate.google.cn/translate_a/single?client=gtx&dt=t&dj=1&ie=UTF-8&sl=auto&tl=zh_CN&q='


class TranslateService(object):

    @classmethod
    def do_translate(cls, content):
        response = requests.post(TRANSLATOR_URL + content)
        resp_body = ujson.loads(response.content)
        results = [x.get('trans') for x in resp_body.get('sentences')]
        return "".join(results)
