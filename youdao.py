import hashlib
import random
import time
import requests
import json

"""
向有道翻译发送data，得到翻译结果
"""

class Youdao:
    def __init__(self, msg):
        self.msg = msg
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.D = "n%A-rKaT5fb[Gy?;N5@Tj"
        self.salt = self.get_salt()
        self.sign = self.get_sign()
        self.ts = self.get_ts()

    def get_md(self, value):
        # md5加密
        m = hashlib.md5()
        # m.update(value)
        m.update(value.encode('utf-8'))
        return m.hexdigest()

    def get_salt(self):
        # 根据当前时间戳获取salt参数
        s = int(time.time() * 1000) + random.randint(0, 10)
        return str(s)

    def get_sign(self):
        # 使用md5函数和其他参数，得到sign参数
        s = "fanyideskweb" + self.msg + self.salt + self.D
        return self.get_md(s)

    def get_ts(self):
        # 根据当前时间戳获取ts参数
        s = int(time.time() * 1000)
        return str(s)

    def get_result(self):
        Form_Data = {
            'i': self.msg,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': self.salt,
            'sign': self.sign,
            'ts': self.ts,
            'bv': 'c6b8c998b2cbaa29bd94afc223bc106c',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }

        headers = {
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-368708839@10.108.160.18; JSESSIONID=aaaL2DMAbpTgg8Qpc2xUw; OUTFOX_SEARCH_USER_ID_NCOO=1451460344.418452; ___rl__test__cookies=1561684330987',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OSX10_14_2) AppleWebKit/537.36(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        response = requests.post(self.url, data=Form_Data, headers=headers).text
        translate_results = json.loads(response)
        # 找到翻译结果
        #print("先看看全部结果",translate_results)
        print()
        if 'translateResult' in translate_results:
            translate_results = translate_results['translateResult'][0][0]['tgt']
            print("翻译的结果是：%s" % translate_results)
        else :
            print(translate_results)


if __name__ == "__main__":
    y = Youdao('王俊谦最帅')

    y.get_result()


#n%A-rKaT5fb[Gy?;N5@Tj