# coding: utf-8

"""Spiders for CET.

Author:
petalsofcherry (1246000821@qq.com)
exqlnet (github.com/exqlnet)
ZhouYingSASA (a649414476@gmail.com)
"""

# from bs4 import BeautifulSoup
import requests
import random
import re


class NeeaCetQuery(object):
    """另一个四六级查询，这个要验证码，get_zkzh可以获取准考证号"""

    def __init__(self):
        self.url = "http://cache.neea.edu.cn/cet/query"
        self.url_img = "http://cache.neea.edu.cn/Imgs.do"
        self.url_cookie = "http://cet.neea.edu.cn/cet/"

    @staticmethod
    def get_zkzh(ks_xm, ks_sfz):
        url = "http://app.cet.edu.cn:7066/baas/app/setuser.do?method=UserVerify"

        headers = {
            "Referer": "http://app.cet.edu.cn:7066/x5/UI2/v_/CETSETMOBI/index.w",
            "User-Agent": """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36""",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Host": "app.cet.edu.cn:7066",
            "Origin": "http://app.cet.edu.cn:7066"
        }

        jbs = ["1", "2"]
        pre_data = 'action=&params={"ks_xm":"%s","ks_sfz":"%s","jb":"%s"}'
        for jb in jbs:
            data = pre_data % (ks_xm, ks_sfz, jb)
            r = requests.post(url, data=data.encode(), headers=headers)
            result = r.json()
            if result.get('ks_bh'):
                return result.get('ks_bh')

        return None

    def get_image(self, zkzh):
        """
        zkzh: str
        :return (img_url, result_cookies) 验证码图片地址，cookie
        """
        data_image = {
            "c": "CET",
            "ik": zkzh,
            "t": random.random()
        }
        header = {
            "Referer": "http://cet.neea.edu.cn/cet/",
            "Transfer-Encoding": "chunked",
            "User-Agent": """Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36""",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "cache.neea.edu.cn",
            "Origin": "http://cet.neea.edu.cn"
        }
        result = retry_request("GET", self.url_img, params=data_image, timeout=2, retry=5, headers=header)
        if not result:
            return None

        result_cookies = {key: value for key, value in result.cookies.iteritems()}
        img_information = result.content.decode("utf-8")
        re_findall = re.findall(r"http:.*\.png", img_information)
        if re_findall:
            img_url = re_findall[0]
            return img_url, result_cookies
        return None

    def get_result(self, zkzh, key_word, xm, cookies):

        bad_result = {
                         "msg": "error:您查询的结果为空！",
                         "status": 0
                     }, 0
        if len(zkzh) != 15:
            return bad_result
        if zkzh[9] == '1':
            exam_type = 'CET4'
            level = '4'
        elif zkzh[9] == '2':
            exam_type = 'CET6'
            level = '6'
        else:
            return bad_result
        l = "CET{0}_{1}_DANGCI".format(level, zkzh[6:9])
        data_result = {
            "data": l + "," + zkzh + "," + xm,
            "v": key_word
        }
        result_header = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://cet.neea.edu.cn",
            "Referer": "http://cet.neea.edu.cn/cet/",
            "Upgrade-Insecure-Requests": '1',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36"
        }
        requests_session = requests.Session()
        for key, value in cookies.items():
            requests_session.cookies[key] = value

        post_result = retry_request("POST", self.url, data=data_result, headers=result_header,
                                    cookies=requests_session.cookies, retry=5, timeout=2)
        if not post_result:
            return None
        name_list = ["ID", "name", "school", "score", "time", "listening", "reading", "translate", "oralId", "oralLevel"]
        content = post_result.content.decode("utf-8")
        re_findall = re.findall(r"{.*}", content)
        if not re_findall:
            return None
        # 之前的取数据方法(先用这个方法)
        result = re_findall[0][1:-1].split(",")
        result_list = zip(name_list,
                          [self.rm_singal_quotes(atom[4:]) if "ky" in atom else self.rm_singal_quotes(atom[2:]) for atom in
                           result])
        # 新取数据方法
        # result = json.loads(re_findall[0].replace("'", "\""))
        # result_list = zip(name_list, [result.get('z'), result.get('n'), result.get('x'), result.get('s'), '考试时间',
        #                               result.get('l'), result.get('r'), result.get('w'), result.get('kyz'), result.get('kys')])
        #
        result_data = {tu[0]: tu[1] for tu in list(result_list)}
        if 'name' not in result_data.keys():
            return result_data, 0
        result_data['exam_type'] = exam_type
        return result_data, 1

    def rm_singal_quotes(self, string):
        if "'" in string:
            return string.replace("'", "")
        return string

